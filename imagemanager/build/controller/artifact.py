"""
Build and create EDA Artifact CRs (artifacts.eda.nokia.com/v1).

The Artifact's remoteFileUrl points back at THIS app's in-cluster HTTPS
file-serve endpoint. The built-in artifact server (eda-asvr) then pulls the
file from us, validates it against the md5, and re-hosts it. eda-asvr's pull
client does NOT trust eda-internal-ca by default, so each Artifact also sets
spec.trustBundle to a per-namespace ConfigMap holding our serving CA (see
ensure_trust_bundle); without it the pull fails x509 unknown-authority.
"""

import logging
from urllib.parse import quote, urlsplit

import k8s

logger = logging.getLogger("artifact")

ARTIFACT_GROUP = "artifacts.eda.nokia.com"
ARTIFACT_VERSION = "v1"
ARTIFACT_PLURAL = "artifacts"

MANAGED_LABEL = "imagemanager.eda.edacommunity.com/managed"
SERVICE_NAME = "eda-imagemanager"
SERVICE_PORT = 8443

# eda-asvr's pull client does NOT trust eda-internal-ca by default, so each
# Artifact must point spec.trustBundle at a ConfigMap holding the CA that signs
# our serving cert. The CSI driver writes that CA here; we replicate it into a
# ConfigMap (key trust-bundle.pem, the EDA convention) in the artifact's
# namespace, since eda-internal-trust-bundle is only present in eda-system.
TRUST_BUNDLE_CM = "imagemanager-trust-bundle"
TRUST_BUNDLE_KEY = "trust-bundle.pem"
SERVING_CA_PATH = "/var/run/eda/tls/serving/ca.crt"
_ca_cache = [None]


def _serving_ca():
    if _ca_cache[0] is None:
        try:
            with open(SERVING_CA_PATH) as f:
                _ca_cache[0] = f.read()
        except OSError:
            _ca_cache[0] = ""
    return _ca_cache[0]


def ensure_trust_bundle(namespace):
    """Ensure a trust-bundle ConfigMap with our serving CA exists in `namespace`.
    Returns the ConfigMap name, or None if we have no CA (plain-HTTP mode)."""
    ca = _serving_ca()
    if not ca.strip():
        return None
    if k8s.read_configmap(TRUST_BUNDLE_CM, namespace) is None:
        try:
            k8s.create_configmap(TRUST_BUNDLE_CM, namespace, {TRUST_BUNDLE_KEY: ca})
            logger.info("Created trust bundle ConfigMap %s/%s", namespace, TRUST_BUNDLE_CM)
        except Exception as e:
            logger.warning("Failed to create trust bundle CM in %s: %s", namespace, e)
            return None
    return TRUST_BUNDLE_CM


def default_base_url(pod_namespace):
    """In-cluster HTTPS base eda-asvr uses to pull from us (cert SAN host)."""
    return f"https://{SERVICE_NAME}.{pod_namespace}.svc:{SERVICE_PORT}/"


def file_urls(base_url, upload_id, filename):
    """(fileUrl, md5Url) for an upload, rooted at base_url."""
    root = (base_url or "").rstrip("/")
    f = f"{root}/files/{quote(upload_id, safe='')}/{quote(filename, safe='')}"
    return f, f + ".md5"


def build_artifact(namespace, name, repo, file_path, file_url, md5_url=None, trust_bundle=None):
    remote = {"fileUrl": file_url}
    if md5_url:
        remote["md5Url"] = md5_url
    spec = {
        "repo": repo,
        "filePath": file_path,
        "remoteFileUrl": remote,
    }
    if trust_bundle:
        spec["trustBundle"] = trust_bundle
    return {
        "apiVersion": f"{ARTIFACT_GROUP}/{ARTIFACT_VERSION}",
        "kind": "Artifact",
        "metadata": {
            "name": name,
            "namespace": namespace,
            "labels": {MANAGED_LABEL: "true"},
        },
        "spec": spec,
    }


def create_artifact(namespace, name, repo, file_path, file_url, md5_url=None):
    # eda-asvr pulls over HTTPS and must trust our internal-CA serving cert.
    trust_bundle = ensure_trust_bundle(namespace)
    body = build_artifact(namespace, name, repo, file_path, file_url, md5_url, trust_bundle)
    logger.info("Creating Artifact %s/%s (repo=%s filePath=%s md5=%s trustBundle=%s) fileUrl=%s",
                namespace, name, repo, file_path, bool(md5_url), trust_bundle, file_url)
    return k8s.create_namespaced_cr(
        ARTIFACT_GROUP, ARTIFACT_VERSION, namespace, ARTIFACT_PLURAL, body
    )


def delete_artifact(namespace, name):
    """Delete an Artifact CR (eda-asvr drops its re-hosted copy too). 404 -> None."""
    logger.info("Deleting Artifact %s/%s", namespace, name)
    return k8s.delete_namespaced_cr(
        ARTIFACT_GROUP, ARTIFACT_VERSION, namespace, ARTIFACT_PLURAL, name
    )


def list_managed_artifacts():
    """All Artifacts this app created, across namespaces (label-selected)."""
    return k8s.list_cr_all_namespaces(
        ARTIFACT_GROUP, ARTIFACT_VERSION, ARTIFACT_PLURAL,
        label_selector=f"{MANAGED_LABEL}=true",
    )


def artifact_status(namespace, name):
    """Live status dict for one Artifact, or {} if missing."""
    cr = k8s.read_namespaced_cr(
        ARTIFACT_GROUP, ARTIFACT_VERSION, namespace, ARTIFACT_PLURAL, name
    )
    return (cr or {}).get("status", {}) or {}


def asvr_path(internal_url):
    """Convert an Artifact status.internalUrl into the artifact-server path used
    in a NodeProfile's spec.images[].image (host stripped). e.g.
    https://eda-asvr.eda-system.svc/eda/images/srlinux-26.3.2/SRLinux-26.3.2
    -> eda/images/srlinux-26.3.2/SRLinux-26.3.2 . Returns "" if not available."""
    if not internal_url:
        return ""
    try:
        return urlsplit(internal_url).path.lstrip("/")
    except Exception:
        return ""
