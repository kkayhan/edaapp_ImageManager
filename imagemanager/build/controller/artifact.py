"""
Build and create EDA Artifact CRs (artifacts.eda.nokia.com/v1).

The Artifact's remoteFileUrl points back at THIS app's in-cluster HTTPS
file-serve endpoint. The built-in artifact server (eda-asvr) then pulls the
file from us, validates it against the md5, and re-hosts it. eda-asvr's pull
client does NOT trust eda-internal-ca by default, so each Artifact also sets
spec.trustBundle to a per-namespace ConfigMap holding our serving CA (see
ensure_trust_bundle); without it the pull fails x509 unknown-authority.
reconcile_trust keeps those ConfigMaps current when EDA re-keys its CAs.
"""

import logging
import re
from urllib.parse import quote, urlsplit

import k8s

logger = logging.getLogger("artifact")

ARTIFACT_GROUP = "artifacts.eda.nokia.com"
ARTIFACT_VERSION = "v1"
ARTIFACT_PLURAL = "artifacts"

# EDA repo conventions consumed by NodeProfiles. SR Linux uploads use the
# config-driven defaultRepo ("images"); SR OS boot images and their YANG schema
# profile go to the repos the reference SR OS NodeProfiles expect.
SROS_REPO = "srosimages"
SCHEMAPROFILE_REPO = "schemaprofiles"

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
# EDA's own internal trust set: the current CA plus any rollover CA that
# trust-manager carries while EDA re-keys it. Adding it lets the ConfigMap
# cover both the leaf we serve now and the one the CSI driver issues next.
CLUSTER_TRUST_CM = "eda-internal-trust-bundle"
CLUSTER_TRUST_NS = "eda-system"

_PEM_CERT_RE = re.compile(r"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----", re.S)


def _pem_certs(text):
    """The certificates in a PEM text, normalised so equal certs compare equal."""
    out = []
    for m in _PEM_CERT_RE.finditer(text or ""):
        lines = [ln.strip() for ln in m.group(0).splitlines() if ln.strip()]
        out.append("\n".join(lines) + "\n")
    return out


def trusted_cas():
    """CA certificates eda-asvr needs to pull from us, read fresh on every call:
    EDA re-keys its CAs (every 30 days on 26.4; the 26.8 internal root every
    ~9 months), so a copy taken at startup goes stale. [] = no serving CA, i.e.
    plain-HTTP mode, where no trust bundle is needed."""
    try:
        with open(SERVING_CA_PATH) as f:
            certs = _pem_certs(f.read())
    except OSError:
        certs = []
    if not certs:
        return []
    try:
        cm = k8s.read_configmap(CLUSTER_TRUST_CM, CLUSTER_TRUST_NS) or {}
        certs += _pem_certs((cm.get("data") or {}).get(TRUST_BUNDLE_KEY, ""))
    except Exception as e:  # noqa: BLE001 - the serving CA alone still works
        logger.info("Cluster trust bundle %s/%s unreadable: %s",
                    CLUSTER_TRUST_NS, CLUSTER_TRUST_CM, e)
    return list(dict.fromkeys(certs))


def ensure_trust_bundle(namespace):
    """Ensure `namespace` has a trust-bundle ConfigMap that holds every CA in
    trusted_cas(). Returns the ConfigMap name, or None if we have no CA
    (plain-HTTP mode) or could not create it.

    An existing ConfigMap is rewritten only when a CA we need is missing from
    it: EDA re-keyed the CA, or the ConfigMap is left over from an earlier
    install (it is created at runtime, so an app uninstall keeps it). eda-asvr
    watches the ConfigMap, so Failed pulls that use it recover at once, but
    every write also makes eda-asvr re-download each Artifact that uses it --
    hence no write while the content already covers what we serve."""
    cas = trusted_cas()
    if not cas:
        return None
    data = {TRUST_BUNDLE_KEY: "".join(cas)}
    labels = {MANAGED_LABEL: "true"}
    cm = k8s.read_configmap(TRUST_BUNDLE_CM, namespace)
    if cm is None:
        try:
            k8s.create_configmap(TRUST_BUNDLE_CM, namespace, data, labels=labels)
            logger.info("Created trust bundle ConfigMap %s/%s", namespace, TRUST_BUNDLE_CM)
        except Exception as e:
            if getattr(e, "code", None) == 409:  # an upload and the reconcile raced
                return TRUST_BUNDLE_CM
            logger.warning("Failed to create trust bundle CM in %s: %s", namespace, e)
            return None
        return TRUST_BUNDLE_CM
    have = set(_pem_certs((cm.get("data") or {}).get(TRUST_BUNDLE_KEY, "")))
    missing = [c for c in cas if c not in have]
    if missing:
        try:
            k8s.replace_configmap(TRUST_BUNDLE_CM, namespace, data, labels=labels)
            logger.warning("Refreshed trust bundle ConfigMap %s/%s: it lacked %d of the "
                           "%d CA(s) EDA now uses (CA re-keyed, or left over from an "
                           "earlier install); eda-asvr re-pulls the Artifacts that use it",
                           namespace, TRUST_BUNDLE_CM, len(missing), len(cas))
        except Exception as e:
            logger.warning("Failed to refresh trust bundle CM in %s: %s", namespace, e)
    return TRUST_BUNDLE_CM


def reconcile_trust():
    """Keep each namespace's trust bundle current, and attach it to managed
    HTTPS Artifacts that were created without one, so pulls that fail
    'x509: certificate signed by unknown authority' heal without a re-upload."""
    by_ns = {}
    for art in list_managed_artifacts():
        ns = (art.get("metadata") or {}).get("namespace")
        if ns:
            by_ns.setdefault(ns, []).append(art)
    for ns, arts in sorted(by_ns.items()):
        try:
            tb = ensure_trust_bundle(ns)
        except Exception as e:  # noqa: BLE001 - one namespace must not stop the rest
            logger.warning("Trust bundle check failed in %s: %s", ns, e)
            continue
        if not tb:
            continue
        for art in arts:
            spec = art.get("spec") or {}
            url = (spec.get("remoteFileUrl") or {}).get("fileUrl", "")
            status = (art.get("status") or {}).get("downloadStatus", "")
            if spec.get("trustBundle") or not url.startswith("https://") \
                    or status == "Available":
                continue
            name = art["metadata"]["name"]
            try:
                k8s.patch_namespaced_cr(ARTIFACT_GROUP, ARTIFACT_VERSION, ns,
                                        ARTIFACT_PLURAL, name, {"spec": {"trustBundle": tb}})
                logger.warning("Artifact %s/%s had no trustBundle (status %s); set it to %s",
                               ns, name, status or "pending", tb)
            except Exception as e:  # noqa: BLE001
                logger.warning("Failed to set trustBundle on Artifact %s/%s: %s", ns, name, e)


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
    https://eda-asvr.eda-system.svc/eda/images/srlinux-26.3.2/srlinux-26.3.2
    -> eda/images/srlinux-26.3.2/srlinux-26.3.2 . Returns "" if not available."""
    if not internal_url:
        return ""
    try:
        return urlsplit(internal_url).path.lstrip("/")
    except Exception:
        return ""
