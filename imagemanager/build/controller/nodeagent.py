#!/usr/bin/env python3
"""Node registry-trust agent (runs as a DaemonSet, one pod per node).

The problem
-----------
The SR-SIM NodeProfile that Image Manager generates points `containerImage` at
this app's in-cluster OCI registry by its Service FQDN
(`eda-imagemanager.<ns>.svc`). EDA's Digital Twin (eda-cx) runs the simulator
container on a *node*, and the node's containerd performs that image pull. Node
containerd does NOT use in-cluster DNS and does NOT trust the app's serving cert
(internal-CA, SAN = the Service FQDN), so the pull fails two ways: the `.svc`
name doesn't resolve, and the cert wouldn't match the node-reachable ClusterIP.

What this agent does
--------------------
On every node it writes the documented containerd *registry hosts* file
(`<config_path>/<registry-host>/hosts.toml`) that redirects the registry FQDN to
the live Service ClusterIP over HTTPS on the serving port, skipping TLS server
verification. skip_verify is safe here: the node->ClusterIP path is inside the
cluster overlay, and containerd still verifies every manifest/layer by sha256
digest regardless of transport, so image integrity is unaffected. It re-resolves
the ClusterIP each cycle so the redirect self-heals if the Service is recreated.

This is the same `config_path` mechanism EDA's own `edabuilder deploy` uses to
let nodes pull from the in-cluster dev registry (its `--skip-containerd-patch`
flag), and containerd honours it with no restart. Nodes whose runtime does not
expose this mechanism (notably Talos, whose immutable /etc is rebuilt from
machine config) are detected and reported -- there the redirect must be set at
the cluster level (Talos: `machine.registries`).

Needs no Kubernetes API access: the live ClusterIP is learned from in-cluster
DNS (pods *can* resolve `.svc`; only node containerd cannot).
"""
import glob
import logging
import os
import re
import socket
import sys
import tempfile
import time

SERVICE_NAME = "eda-imagemanager"
REGISTRY_PORT = int(os.environ.get("REGISTRY_PORT", "8443"))
POD_NAMESPACE = os.environ.get("POD_NAMESPACE", "eda-system")
# The DaemonSet mounts the node's containerd config dir here (read-write).
HOST_ROOT = os.environ.get("HOST_ROOT", "/host")
CONTAINERD_DIR = os.environ.get("CONTAINERD_DIR", "/etc/containerd")
RESYNC_SECONDS = int(os.environ.get("RESYNC_SECONDS", "120"))
HEARTBEAT_FILE = os.environ.get("HEARTBEAT_FILE", "/tmp/.heartbeat")
ENABLED = os.environ.get("NODE_AGENT_ENABLED", "true").lower() not in ("0", "false", "no")

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("nodeagent")

# `config_path = "..."` as declared anywhere in containerd's config (the key is
# spelled the same across the containerd 1.x and 2.x registry config layouts).
_CONFIG_PATH_RE = re.compile(r'^\s*config_path\s*=\s*"([^"]*)"', re.M)


def registry_host(ns=None):
    """The host containerd sees in the sim image ref (the Service FQDN)."""
    return f"{SERVICE_NAME}.{ns or POD_NAMESPACE}.svc"


def _endpoint(ip, port=REGISTRY_PORT):
    if ":" in ip and not ip.startswith("["):   # bracket IPv6 literals
        return f"https://[{ip}]:{port}"
    return f"https://{ip}:{port}"


def render_hosts_toml(host, cluster_ip, port=REGISTRY_PORT):
    """containerd registry-hosts file: redirect `host` -> https://ip:port,
    skipping TLS server-cert verification (the serving cert's SAN is the FQDN,
    not the ClusterIP; layer integrity is still enforced by digest)."""
    return (
        "# Managed by eda-imagemanager node-agent. Redirects the in-cluster\n"
        "# Image Manager registry FQDN to its live ClusterIP so node containerd\n"
        "# can pull SR-SIM images. Regenerated automatically; do not edit.\n"
        f'server = "https://{host}"\n\n'
        f'[host."{_endpoint(cluster_ip, port)}"]\n'
        '  capabilities = ["pull", "resolve"]\n'
        '  skip_verify = true\n'
    )


def parse_config_path(config_text):
    """Return containerd's registry `config_path` if declared, else None."""
    m = _CONFIG_PATH_RE.search(config_text or "")
    if not m:
        return None
    return m.group(1).strip() or None


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError as e:
        log.warning("could not read %s: %s", path, e)
        return ""


def detect_certs_dir():
    """Resolve this node's registry-hosts directory as an absolute path under
    HOST_ROOT, or None (with an actionable log) if the node's containerd does
    not use the hosts.toml mechanism (e.g. Talos immutable nodes)."""
    mount_prefix = os.path.normpath(
        os.path.join(HOST_ROOT, CONTAINERD_DIR.lstrip("/")))
    # config_path may live in the main config or a drop-in fragment.
    candidates = [os.path.join(mount_prefix, "config.toml")]
    candidates += sorted(glob.glob(os.path.join(mount_prefix, "conf.d", "*.toml")))
    config_path = None
    for cfg in candidates:
        if os.path.isfile(cfg):
            config_path = parse_config_path(_read(cfg))
            if config_path:
                break
    if not config_path:
        log.warning(
            "no containerd registry config_path on this node (hosts.toml "
            "mechanism unavailable -- e.g. Talos immutable nodes). Configure "
            "the registry mirror at the cluster level so %s images can be "
            "pulled (Talos: machine.registries).", registry_host())
        return None
    target = os.path.normpath(os.path.join(HOST_ROOT, config_path.lstrip("/")))
    if os.path.commonpath([target, mount_prefix]) != mount_prefix:
        log.warning(
            "containerd config_path %s is outside the mounted %s; this agent "
            "only manages %s. Adjust the DaemonSet hostPath to cover it.",
            config_path, CONTAINERD_DIR, CONTAINERD_DIR)
        return None
    return target


def resolve_cluster_ip():
    """Current ClusterIP of the Service via in-cluster DNS (self-heals if the
    Service is recreated), falling back to the kubelet-injected env var."""
    for name in (f"{SERVICE_NAME}.{POD_NAMESPACE}.svc.cluster.local",
                 f"{SERVICE_NAME}.{POD_NAMESPACE}.svc"):
        try:
            infos = socket.getaddrinfo(name, REGISTRY_PORT,
                                       proto=socket.IPPROTO_TCP)
            if infos:
                return infos[0][4][0]
        except socket.gaierror:
            continue
    return os.environ.get(
        SERVICE_NAME.upper().replace("-", "_") + "_SERVICE_HOST") or None


def write_if_changed(path, content):
    """Atomically write `content` to `path` iff it differs. Returns True if
    the file was (re)written."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            if f.read() == content:
                return False
    except OSError:
        pass
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.chmod(tmp, 0o644)
        os.replace(tmp, path)
        tmp = None
    finally:
        if tmp and os.path.exists(tmp):
            os.unlink(tmp)
    return True


def reconcile():
    """One pass: ensure the node's hosts.toml points at the live ClusterIP."""
    certs_dir = detect_certs_dir()
    if not certs_dir:
        return None
    ip = resolve_cluster_ip()
    if not ip:
        log.warning("could not resolve ClusterIP for %s yet; will retry",
                    registry_host())
        return None
    host = registry_host()
    path = os.path.join(certs_dir, host, "hosts.toml")
    if write_if_changed(path, render_hosts_toml(host, ip)):
        log.info("redirect set: %s -> %s (skip_verify)",
                 host, _endpoint(ip))
    return path


def cleanup():
    """Remove the registry redirect written by this agent (SIGTERM cleanup).

    Keeps reinstall clean: a stale hosts.toml redirect left on a node can block
    a later SR-SIM pull after the app is reinstalled.
    """
    certs_dir = detect_certs_dir()
    if not certs_dir:
        return
    path = os.path.join(certs_dir, registry_host(), "hosts.toml")
    try:
        os.remove(path)
        log.info("removed registry redirect %s", path)
    except FileNotFoundError:
        pass
    except OSError as e:
        log.warning("could not remove %s: %s", path, e)


def main():
    import signal

    def _handle_signal(signum, frame):
        log.info("received signal %s, cleaning up", signum)
        cleanup()
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT, _handle_signal)
    log.info("node registry-trust agent starting (host=%s ns=%s port=%s "
             "resync=%ss enabled=%s)", registry_host(), POD_NAMESPACE,
             REGISTRY_PORT, RESYNC_SECONDS, ENABLED)
    if not ENABLED:
        log.info("NODE_AGENT_ENABLED=false; idle heartbeat only (no hosts.toml writes)")
    while True:
        if ENABLED:
            try:
                reconcile()
            except Exception as e:   # never let the reconcile loop die
                log.error("reconcile error: %s", e)
        try:
            with open(HEARTBEAT_FILE, "w") as f:
                f.write(str(int(time.time())))
        except OSError:
            pass
        time.sleep(RESYNC_SECONDS)


if __name__ == "__main__":
    sys.exit(main())
