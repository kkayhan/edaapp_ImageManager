"""
EDA Image Manager controller - entry point.

Long-running controller that:
  * serves an upload web UI + an in-cluster file-serve endpoint (fileserver.py),
  * on upload, stores the file on the PVC and creates an Artifact CR pointing
    eda-asvr back at this app to pull + re-host the file,
  * reconciles every RECONCILE_INTERVAL: mirrors each Artifact's download status
    into ImageManagerConfig.status for the UI, computes storage stats, and
    (optionally) purges local copies once eda-asvr reports Available.

K8s-API only (pod ServiceAccount token). No Keycloak / EDA REST API.
"""

import logging
import os
import shutil
import signal
import threading
import time
from datetime import datetime, timezone

import fileserver
import k8s
import uploads

VERSION = "v26.4.2-3"
UPLOAD_DIR = "/data/uploads"
TLS_CRT = "/var/run/eda/tls/serving/tls.crt"
PORT = 8443
RECONCILE_INTERVAL = 30

CRD_GROUP = "imagemanager.eda.edacommunity.com"
CRD_VERSION = "v1alpha1"
CRD_PLURAL = "imagemanagerconfigs"
CRD_KIND = "ImageManagerConfig"
CRD_NAME = "default"

DEFAULTS = {
    "defaultArtifactNamespace": "eda",
    "defaultRepo": "images",
    "maxUploadMiB": 4096,
    "filePullBaseUrl": "",
    "retentionDays": 0,
}

logger = logging.getLogger("main")
shutdown_event = threading.Event()


def _setup_logging():
    fmt = logging.Formatter(
        fmt="%(asctime)s %(levelname)-5s [%(name)s] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
    fmt.converter = time.gmtime
    handler = logging.StreamHandler()
    handler.setFormatter(fmt)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()
    root.addHandler(handler)


def _signal_handler(signum, frame):
    logger.info("Received signal %d, initiating shutdown", signum)
    shutdown_event.set()


def _wait_for_cert(timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if os.path.isfile(TLS_CRT):
            return True
        if shutdown_event.wait(1):
            return False
    return False


def _read_config():
    """Read ImageManagerConfig/default spec, merged over DEFAULTS."""
    cfg = dict(DEFAULTS)
    try:
        cr = k8s.read_cr(CRD_GROUP, CRD_VERSION, CRD_PLURAL, CRD_NAME)
        if cr:
            spec = cr.get("spec", {}) or {}
            for key in DEFAULTS:
                if spec.get(key) not in (None, ""):
                    cfg[key] = spec[key]
    except Exception as e:
        logger.warning("Failed to read %s/%s: %s", CRD_KIND, CRD_NAME, e)
    # clamp
    cfg["maxUploadMiB"] = max(1, min(65536, int(cfg["maxUploadMiB"])))
    cfg["retentionDays"] = max(0, int(cfg["retentionDays"]))
    return cfg


def _ensure_default_cr():
    try:
        if k8s.read_cr(CRD_GROUP, CRD_VERSION, CRD_PLURAL, CRD_NAME):
            return
        body = {
            "apiVersion": f"{CRD_GROUP}/{CRD_VERSION}",
            "kind": CRD_KIND,
            "metadata": {"name": CRD_NAME},
            "spec": {},
        }
        k8s.create_cr(CRD_GROUP, CRD_VERSION, CRD_PLURAL, body)
        logger.info("Created default %s CR", CRD_KIND)
    except Exception as e:
        logger.warning("Failed to ensure default %s: %s", CRD_KIND, e)


def _retention_sweep(tracked, retention_days):
    """Delete the local PVC copy of uploads whose Artifact is Available and old."""
    if retention_days <= 0:
        return 0
    now = datetime.now(timezone.utc)
    deleted = 0
    for t in tracked:
        if t.get("downloadStatus") != "Available":
            continue
        stored = t.get("storedAt")
        uid = t.get("uploadId")
        if not stored or not uid:
            continue
        try:
            dt = datetime.fromisoformat(stored)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            age_days = (now - dt).total_seconds() / 86400.0
        except ValueError:
            continue
        if age_days > retention_days:
            d = os.path.join(UPLOAD_DIR, uid)
            shutil.rmtree(d, ignore_errors=True)
            deleted += 1
            logger.info("Retention: purged local copy of %s (age %.1fd, asvr hosts it)",
                        uid, age_days)
    return deleted


def _update_status(health, message, tracked):
    try:
        cr = k8s.read_cr(CRD_GROUP, CRD_VERSION, CRD_PLURAL, CRD_NAME)
        if not cr:
            return
        count, total_bytes = uploads.storage_stats()
        cr["status"] = {
            "health": health,
            "message": message,
            "lastReconcileTime": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "uploadsStored": count,
            "bytesStored": total_bytes,
            "artifacts": [
                {
                    "name": t.get("name", ""),
                    "namespace": t.get("namespace", ""),
                    "repo": t.get("repo", ""),
                    "filePath": t.get("filePath", ""),
                    "downloadStatus": t.get("downloadStatus", ""),
                    "statusReason": t.get("statusReason", ""),
                    "externalUrl": t.get("externalUrl", ""),
                }
                for t in tracked[:500]
            ],
            "version": VERSION,
        }
        k8s.update_cr_status(CRD_GROUP, CRD_VERSION, CRD_PLURAL, CRD_NAME, cr)
    except Exception as e:
        logger.warning("Failed to update CRD status: %s", e)


def main():
    _setup_logging()
    logger.info("Image Manager controller started (version %s)", VERSION)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)

    if not _wait_for_cert(timeout=30):
        logger.error("Serving cert %s not present after 30s; server will fall back "
                     "to HTTP (probes/pulls will fail until cert mounts)", TLS_CRT)
    fileserver.set_config(_read_config())
    fileserver.start_file_server(PORT)
    fileserver.write_healthz("starting", None)

    _ensure_default_cr()

    while not shutdown_event.is_set():
        cycle_start = time.time()
        cfg = _read_config()
        fileserver.set_config(cfg)

        health, message = "ok", "All systems operational"
        tracked = []
        try:
            tracked = fileserver.build_tracked_list()
            bad = [t for t in tracked if t.get("downloadStatus") in ("Error", "Failed")]
            if bad:
                health = "degraded"
                message = f"{len(bad)} artifact(s) reported Error/Failed by eda-asvr"
        except Exception as e:
            health, message = "degraded", f"reconcile error: {e}"
            logger.warning("Reconcile listing failed: %s", e)

        _retention_sweep(tracked, cfg["retentionDays"])

        now_str = datetime.now(timezone.utc).isoformat(timespec="seconds")
        fileserver.write_healthz(health, now_str)
        _update_status(health, message, tracked)

        logger.info("Reconcile done: %d tracked upload(s), health=%s (%dms)",
                    len(tracked), health, int((time.time() - cycle_start) * 1000))
        shutdown_event.wait(timeout=RECONCILE_INTERVAL)

    logger.info("Controller shutting down")


if __name__ == "__main__":
    main()
