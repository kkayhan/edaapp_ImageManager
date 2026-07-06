"""
Raw Kubernetes API client using urllib (stdlib only).
Reads the in-cluster service account token; uses the K8s CA for TLS.
All requests have a 30-second timeout.

The image-manager controller talks ONLY to the K8s API (via the pod's
ServiceAccount token):
  - cluster-scoped CRUD on its own ImageManagerConfig (one "default" instance)
  - namespaced create + read of Artifact CRs (artifacts.eda.nokia.com/v1)
  - cluster-wide list of Artifacts (to mirror download status into the UI)
No Keycloak / EDA REST API is used.
"""

import json
import logging
import ssl
import time
import urllib.error
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

logger = logging.getLogger("k8s")

_K8S_BASE = "https://kubernetes.default.svc"
_SA_TOKEN_PATH = "/var/run/secrets/kubernetes.io/serviceaccount/token"
_SA_CA_PATH = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
_TIMEOUT = 30
_RETRYABLE_HTTP = frozenset({429, 500, 502, 503, 504})
_MAX_RETRIES = 4


def _ssl_ctx():
    return ssl.create_default_context(cafile=_SA_CA_PATH)


def _token():
    with open(_SA_TOKEN_PATH) as f:
        return f.read().strip()


def _retry_delay(attempt, err):
    """Backoff for transient API errors (429 storage init, 503 overload)."""
    delay = 1
    try:
        payload = json.loads(err.read().decode("utf-8", errors="replace"))
        delay = int((payload.get("details") or {}).get("retryAfterSeconds", delay))
    except Exception:
        pass
    return min(max(delay, 1), 8) * (attempt + 1)


def _request(method, path, body=None):
    url = _K8S_BASE + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    last_err = None
    for attempt in range(_MAX_RETRIES):
        req = Request(url=url, data=data, method=method)
        req.add_header("Authorization", f"Bearer {_token()}")
        req.add_header("Accept", "application/json")
        if data:
            req.add_header("Content-Type", "application/json")
        try:
            with urlopen(req, context=_ssl_ctx(), timeout=_TIMEOUT) as resp:
                raw = resp.read()
                return json.loads(raw.decode("utf-8")) if raw else None
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in _RETRYABLE_HTTP and attempt < _MAX_RETRIES - 1:
                wait = _retry_delay(attempt, e)
                logger.info("K8s API %s %s -> HTTP %d; retry in %ss (%d/%d)",
                            method, path, e.code, wait, attempt + 1, _MAX_RETRIES)
                time.sleep(wait)
                continue
            body_text = ""
            try:
                body_text = e.read().decode("utf-8", errors="replace")[:500]
            except Exception:
                pass
            logger.warning("K8s API %s %s -> HTTP %d: %s", method, path, e.code, body_text)
            raise
    if last_err is not None:
        raise last_err


# ----------------------------- cluster-scoped CR (ImageManagerConfig) --------------

def read_cr(group, version, plural, name):
    path = f"/apis/{group}/{version}/{plural}/{quote(name, safe='')}"
    try:
        return _request("GET", path)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def create_cr(group, version, plural, body):
    path = f"/apis/{group}/{version}/{plural}"
    return _request("POST", path, body)


def update_cr_status(group, version, plural, name, full_obj):
    path = f"/apis/{group}/{version}/{plural}/{quote(name, safe='')}/status"
    return _request("PUT", path, full_obj)


# ----------------------------- namespaced CR (Artifact) ----------------------------

def create_namespaced_cr(group, version, namespace, plural, body):
    path = f"/apis/{group}/{version}/namespaces/{quote(namespace, safe='')}/{plural}"
    return _request("POST", path, body)


def read_namespaced_cr(group, version, namespace, plural, name):
    path = (
        f"/apis/{group}/{version}/namespaces/{quote(namespace, safe='')}"
        f"/{plural}/{quote(name, safe='')}"
    )
    try:
        return _request("GET", path)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def list_cr_all_namespaces(group, version, plural, label_selector=None):
    """Cluster-wide list of a namespaced resource. Returns the list .items."""
    path = f"/apis/{group}/{version}/{plural}"
    if label_selector:
        path += "?" + urlencode({"labelSelector": label_selector})
    obj = _request("GET", path)
    return (obj or {}).get("items", [])


def delete_namespaced_cr(group, version, namespace, plural, name):
    path = (
        f"/apis/{group}/{version}/namespaces/{quote(namespace, safe='')}"
        f"/{plural}/{quote(name, safe='')}"
    )
    try:
        return _request("DELETE", path)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def read_configmap(name, namespace):
    path = f"/api/v1/namespaces/{quote(namespace, safe='')}/configmaps/{quote(name, safe='')}"
    try:
        return _request("GET", path)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def create_configmap(name, namespace, data, labels=None):
    path = f"/api/v1/namespaces/{quote(namespace, safe='')}/configmaps"
    meta = {"name": name, "namespace": namespace}
    if labels:
        meta["labels"] = labels
    body = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": meta,
        "data": data,
    }
    return _request("POST", path, body)


def replace_configmap(name, namespace, data, labels=None):
    """PUT (replace) a ConfigMap's data. Used to update a license ConfigMap when a
    license is re-attached to an existing image (create returned 409)."""
    path = f"/api/v1/namespaces/{quote(namespace, safe='')}/configmaps/{quote(name, safe='')}"
    meta = {"name": name, "namespace": namespace}
    if labels:
        meta["labels"] = labels
    body = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": meta,
        "data": data,
    }
    return _request("PUT", path, body)


def delete_configmap(name, namespace):
    """Delete a ConfigMap (e.g. an image's license ConfigMap on image delete).
    404 -> None."""
    path = f"/api/v1/namespaces/{quote(namespace, safe='')}/configmaps/{quote(name, safe='')}"
    try:
        return _request("DELETE", path)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def namespace_exists(name):
    try:
        _request("GET", f"/api/v1/namespaces/{quote(name, safe='')}")
        return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        raise


def read_secret(name, namespace):
    """Read a Secret's .data (base64 values). Returns dict or None (404)."""
    path = f"/api/v1/namespaces/{quote(namespace, safe='')}/secrets/{quote(name, safe='')}"
    try:
        return _request("GET", path)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
