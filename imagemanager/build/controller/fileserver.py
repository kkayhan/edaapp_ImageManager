"""
Embedded HTTPS server (port 8443). Runs as a daemon thread.

Serves three audiences on one port:
  * the browser, via the EDA HttpProxy (path prefixed /core/httpproxy/v1/imagemanager)
      GET  /                 the upload web UI
      GET  /healthz          liveness/readiness (also used by kubelet probes)
      GET  /api/config       defaults for the UI form
      GET  /api/namespaces   namespace names for the UI (best-effort)
      GET  /api/artifacts    tracked uploads + live Artifact download status
      POST /api/upload       raw-body file upload -> store on PVC -> create Artifact
  * eda-asvr, connecting directly to the Service to PULL an uploaded file:
      GET/HEAD /files/<uploadId>/<filename>[.md5]
TLS: serving cert from the cert-manager CSI mount (issuer eda-internal-issuer),
which eda-asvr trusts via the internal CA.
"""

import html
import json
import logging
import os
import re
import shutil
import ssl
import tempfile
import threading
import time
import urllib.error
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, quote, unquote, urlencode, urlsplit

import artifact
import auth
import schemaprofile
import uploads
import webui

logger = logging.getLogger("fileserver")

UPLOAD_DIR = "/data/uploads"
HEALTHZ_FILE = os.path.join(UPLOAD_DIR, ".healthz.json")
PROXY_PREFIX = "/core/httpproxy/v1/imagemanager"
TLS_DIR = "/var/run/eda/tls/serving"
_SERVE_CHUNK = 256 * 1024

# Shared, set by main each reconcile cycle (dict assignment is atomic in CPython).
CONFIG = {
    "defaultArtifactNamespace": "eda",
    "defaultRepo": "images",
    "maxUploadMiB": 4096,
    "filePullBaseUrl": "",
}
POD_NAMESPACE = os.environ.get("POD_NAMESPACE", "eda-system")
SERVICE_NAME = "eda-imagemanager"

# OCI distribution (registry v2) path patterns. `name` may contain '/'.
_V2_MANIFEST_RE = re.compile(r"^/v2/(.+)/manifests/(.+)$")
_V2_BLOB_RE = re.compile(r"^/v2/(.+)/blobs/(sha256:[0-9a-f]{64})$")
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")


def sim_registry_host():
    """The registry host that the node's containerd reaches this app at (the
    Service FQDN, which is also the serving cert's SAN). A one-time Talos
    machine.registries mirror maps this host to the in-cluster Service. Used as
    the host in a SR-SIM NodeProfile's containerImage."""
    return f"{SERVICE_NAME}.{POD_NAMESPACE}.svc"

# Material-styled standalone message page (sign-out / access-denied). Mirrors the
# EDA palette + the saved Light/Dark preference used by the main UI.
_MSG_PAGE = """<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width, initial-scale=1"><title>{title}</title>
<script>try{{document.documentElement.setAttribute("data-theme",localStorage.getItem("imagemanager-theme")||"light");}}catch(e){{}}</script>
<style>
 :root{{--bg:#f7f9fd;--panel:#fff;--fg:#2b2b2b;--muted:#687282;--accent:#005aff;--accent2:#0a44ad;--line:#d9dee7;--elev:0 11px 18px rgba(20,30,50,.18),0 22px 44px rgba(20,30,50,.22);}}
 html[data-theme=dark]{{--bg:#101824;--panel:#1a222e;--fg:#e6edf3;--muted:#8b98a6;--accent:#4d8dff;--accent2:#6aa4ff;--line:#2c3644;--elev:0 22px 48px rgba(0,0,0,.7);}}
 *{{box-sizing:border-box}}
 body{{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:var(--bg);color:var(--fg);font:14px/1.55 "Nokia Pure Text","Inter","Segoe UI",Roboto,Helvetica,Arial,sans-serif;padding:24px}}
 .card{{background:var(--panel);border-radius:16px;box-shadow:var(--elev);padding:30px 32px;max-width:460px;width:100%}}
 .mark{{width:18px;height:18px;border-radius:5px;background:var(--accent);box-shadow:0 0 0 4px color-mix(in srgb,var(--accent) 20%,transparent);display:inline-block;vertical-align:-2px;margin-right:9px}}
 h2{{margin:0 0 12px;font-size:19px;font-weight:600}}
 p{{margin:8px 0;color:var(--fg)}} p.muted{{color:var(--muted);font-size:13px}}
 .imbtn{{display:inline-block;margin-top:16px;background:var(--accent);color:#fff;text-decoration:none;border-radius:8px;padding:10px 20px;font-weight:600;font-size:13.5px}}
 .imbtn:hover{{background:var(--accent2)}}
 .imbtn.ghost{{background:transparent;color:var(--accent);border:1px solid var(--line)}}
 .imbtn.ghost:hover{{background:color-mix(in srgb,var(--accent) 8%,transparent)}}
</style></head><body><div class="card"><h2><span class="mark"></span>{heading}</h2>{body}{action}</div></body></html>"""


def set_config(cfg):
    global CONFIG
    CONFIG = cfg


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # quiet; we log meaningful events ourselves

    # --------------------------- helpers ---------------------------

    def _route(self):
        """Return (path, query_dict) with query stripped and proxy prefix removed."""
        parts = urlsplit(self.path)
        path = parts.path
        if path.startswith(PROXY_PREFIX):
            path = path[len(PROXY_PREFIX):] or "/"
        if len(path) > 1:
            path = path.rstrip("/")
        return path or "/", parse_qs(parts.query)

    def _send_json(self, obj, code=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, text, code=200, ctype="text/plain; charset=utf-8"):
        body = text.encode("utf-8") if isinstance(text, str) else text
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # --------------------------- auth (EDA SSO) ---------------------------

    def _cookie(self, name):
        raw = self.headers.get("Cookie")
        if not raw:
            return ""
        c = SimpleCookie()
        try:
            c.load(raw)
        except Exception:
            return ""
        m = c.get(name)
        return m.value if m else ""

    def _authed_user(self):
        """Username if the request carries a valid session, else None.
        With auth disabled (local dev), returns a placeholder user."""
        if not auth.enabled():
            return "local"
        return auth.verify_session(self._cookie(auth.SESSION_COOKIE))

    def _set_cookie(self, name, value, max_age):
        parts = [f"{name}={value}", f"Path={auth.APP_PROXY_PREFIX}",
                 "HttpOnly", "Secure", "SameSite=Lax"]
        if max_age is not None:
            parts.append(f"Max-Age={max_age}")
        self.send_header("Set-Cookie", "; ".join(parts))

    def _redirect(self, location, cookies=None):
        self.send_response(302)
        for (n, v, a) in (cookies or []):
            self._set_cookie(n, v, a)
        self.send_header("Location", location)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _redirect_to_login(self):
        state = auth.new_state()
        try:
            url = auth.authorize_url(self.headers, state)
        except Exception as e:
            logger.error("Cannot build authorize URL: %s", e)
            self._send_text("Sign-in is unavailable: cannot reach EDA Keycloak.", 503)
            return
        self._redirect(url, cookies=[(auth.STATE_COOKIE, state, 600)])

    def _handle_oauth_callback(self, q):
        code = (q.get("code") or [None])[0]
        state = (q.get("state") or [None])[0]
        expected = self._cookie(auth.STATE_COOKIE)
        if not code or not state or not expected or state != expected:
            self._send_text("Sign-in failed (invalid state). Please retry.", 400)
            return
        try:
            tok = auth.exchange_code(code, self.headers)
        except Exception as e:
            logger.error("OIDC code exchange failed: %s", e)
            self._send_text("Sign-in failed: could not complete authentication.", 502)
            return
        user, roles = auth.token_identity(tok)
        if not user:
            self._send_text("Sign-in failed: invalid token.", 502)
            return
        if not auth.is_allowed(roles):
            logger.info("Access denied: %s lacks an allowed role (have=%s need-any-of=%s)",
                        user, sorted(roles), auth.allowed_roles())
            self._deny_page(user)
            return
        logger.info("Sign-in OK: %s", user)
        self._redirect(auth.APP_PROXY_PREFIX + "/", cookies=[
            (auth.SESSION_COOKIE, auth.make_session(user), auth.SESSION_TTL),
            (auth.STATE_COOKIE, "", 0),
        ])

    def _handle_logout(self):
        # Local logout: clear our session only; the EDA Keycloak session stays.
        link = auth.APP_PROXY_PREFIX + "/oauth/login"
        body = _MSG_PAGE.format(
            title="Signed out",
            heading="Signed out of Image Manager",
            body="<p>You're still logged into EDA.</p>",
            action=f"<a class='imbtn' href='{link}'>Sign in again</a>",
        ).encode("utf-8")
        self.send_response(200)
        self._set_cookie(auth.SESSION_COOKIE, "", 0)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _deny_page(self, user):
        roles = ", ".join(auth.allowed_roles())
        link = auth.APP_PROXY_PREFIX + "/oauth/logout"
        self._send_text(
            _MSG_PAGE.format(
                title="Access denied",
                heading="Access denied",
                body=(f"<p>You're signed in to EDA as <b>{html.escape(user)}</b>, but Image "
                      f"Manager is restricted to users with the role: "
                      f"<b>{html.escape(roles)}</b>.</p>"
                      f"<p class='muted'>Ask an administrator for the role.</p>"),
                action=f"<a class='imbtn ghost' href='{link}'>Sign out</a>",
            ),
            403, ctype="text/html; charset=utf-8")

    # --------------------------- GET / HEAD ---------------------------

    def do_GET(self):
        path, q = self._route()
        try:
            # Machine endpoints — never gated (kubelet probes; eda-asvr file pulls).
            if path == "/healthz":
                self._serve_healthz()
                return
            if path.startswith("/files/"):
                self._serve_file(path[len("/files/"):], head_only=False)
                return
            # OCI registry (read-only) — the node's containerd pulls SR-SIM sim
            # images from here. Machine traffic (no OIDC); auth is by network reach
            # to the in-cluster Service, like /files/.
            if path == "/v2" or path.startswith("/v2/"):
                self._serve_registry_v2(path, head_only=False)
                return
            # OIDC endpoints.
            if path == "/oauth/callback":
                self._handle_oauth_callback(q)
                return
            if path == "/oauth/logout":
                self._handle_logout()
                return
            if path == "/oauth/login":
                self._redirect_to_login()
                return
            # Everything else requires a valid EDA session.
            if auth.enabled() and not self._authed_user():
                if path.startswith("/api/"):
                    self._send_json({"ok": False, "error": "not authenticated"}, 401)
                else:
                    self._redirect_to_login()
                return
            if path == "/":
                self._send_text(webui.INDEX_HTML, ctype="text/html; charset=utf-8")
            elif path == "/api/config":
                self._serve_config()
            elif path == "/api/namespaces":
                self._serve_namespaces()
            elif path == "/api/artifacts":
                self._serve_artifacts()
            else:
                self.send_error(404, "Not Found")
        except BrokenPipeError:
            pass
        except Exception as e:
            logger.error("GET %s failed: %s", self.path, e)
            try:
                self.send_error(500, "Internal Server Error")
            except Exception:
                pass

    def do_HEAD(self):
        path, _ = self._route()
        try:
            if path.startswith("/files/"):
                self._serve_file(path[len("/files/"):], head_only=True)
            elif path == "/v2" or path.startswith("/v2/"):
                self._serve_registry_v2(path, head_only=True)
            elif path in ("/", "/healthz"):
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
            else:
                self.send_error(404, "Not Found")
        except Exception:
            pass

    def _serve_healthz(self):
        try:
            with open(HEALTHZ_FILE) as f:
                self._send_text(f.read(), ctype="application/json")
        except FileNotFoundError:
            self._send_text('{"status":"starting","last_reconcile":null}',
                            ctype="application/json")

    def _serve_config(self):
        c = CONFIG
        self._send_json({
            "defaultArtifactNamespace": c.get("defaultArtifactNamespace", "eda"),
            "defaultRepo": c.get("defaultRepo", "images"),
            "maxUploadMiB": c.get("maxUploadMiB", 4096),
            "user": self._authed_user() or "",
        })

    def _serve_namespaces(self):
        import k8s
        names = []
        try:
            # Suggest only EDA *user* namespaces (labelled eda.nokia.com/source,
            # e.g. eda/demo) — not infrastructure namespaces (eda-system, kube-*,
            # cert-manager, rook-ceph, vcluster-*, ...). The field is still free
            # text, so a user can type any namespace manually.
            q = urlencode({"labelSelector": "eda.nokia.com/source"})
            obj = k8s._request("GET", "/api/v1/namespaces?" + q)  # noqa: SLF001
            names = sorted(
                ns["metadata"]["name"] for ns in (obj or {}).get("items", [])
            )
        except Exception as e:
            logger.info("namespace list unavailable (RBAC?): %s", e)
        self._send_json({"namespaces": names})

    def _serve_artifacts(self):
        self._send_json({"artifacts": build_tracked_list(),
                         "storage": uploads.disk_usage()})

    def _serve_file(self, rest, head_only):
        # rest = "<uploadId>/<filename>" (filename may end with .md5)
        rest = unquote(rest)
        comps = rest.split("/")
        if len(comps) != 2 or any(c in ("", ".", "..") for c in comps):
            self.send_error(400, "Bad path")
            return
        upload_id, filename = comps
        if "/" in filename or "\\" in filename:
            self.send_error(400, "Bad path")
            return
        base = os.path.realpath(os.path.join(UPLOAD_DIR, upload_id))
        full = os.path.realpath(os.path.join(base, filename))
        if not full.startswith(os.path.realpath(UPLOAD_DIR) + os.sep):
            self.send_error(403, "Forbidden")
            return
        if not os.path.isfile(full):
            self.send_error(404, "Not Found")
            return
        size = os.path.getsize(full)
        ctype = "text/plain; charset=utf-8" if filename.endswith(".md5") \
            else "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(size))
        self.send_header("Accept-Ranges", "none")
        self.end_headers()
        if head_only:
            return
        with open(full, "rb") as f:
            shutil.copyfileobj(f, self.wfile, _SERVE_CHUNK)

    # --------------------------- OCI registry (read-only v2) ---------------------------

    def _v2_404(self, msg="not found"):
        body = json.dumps({"errors": [{"code": "NOT_FOUND", "message": msg}]}).encode()
        self.send_response(404)
        self.send_header("Docker-Distribution-Api-Version", "registry/2.0")
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_registry_v2(self, path, head_only):
        """Minimal pull-only OCI distribution endpoint backed by the OCI layouts
        unpacked under /data/uploads/<name>/. Implements GET/HEAD /v2/ (version
        check), /v2/<name>/manifests/<ref> and /v2/<name>/blobs/<digest>."""
        if path in ("/v2", "/v2/"):
            body = b"{}"
            self.send_response(200)
            self.send_header("Docker-Distribution-Api-Version", "registry/2.0")
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if not head_only:
                self.wfile.write(body)
            return
        m = _V2_MANIFEST_RE.match(path)
        if m:
            self._serve_oci_manifest(unquote(m.group(1)), unquote(m.group(2)), head_only)
            return
        b = _V2_BLOB_RE.match(path)
        if b:
            self._serve_oci_blob(unquote(b.group(1)), b.group(2), head_only)
            return
        self._v2_404("unsupported registry path")

    def _serve_oci_manifest(self, name, ref, head_only):
        meta, blobs_dir = uploads.srsim_meta(name)
        if not meta:
            self._v2_404("repository %s not found" % name)
            return
        manifest_digest = meta.get("manifestDigest") or ""
        media = meta.get("manifestMediaType") or "application/vnd.oci.image.manifest.v1+json"
        if ref == (meta.get("imageTag") or ""):
            digest = manifest_digest
        elif ref.startswith("sha256:"):
            digest = ref
        else:
            self._v2_404("manifest %s unknown" % ref)
            return
        h = digest.split(":", 1)[1] if ":" in digest else ""
        if not _SHA256_HEX.match(h):
            self._v2_404("bad manifest digest")
            return
        full = os.path.join(blobs_dir, h)
        if not os.path.isfile(full):
            self._v2_404("manifest blob missing")
            return
        size = os.path.getsize(full)
        self.send_response(200)
        self.send_header("Docker-Distribution-Api-Version", "registry/2.0")
        self.send_header("Content-Type",
                         media if digest == manifest_digest else "application/octet-stream")
        self.send_header("Docker-Content-Digest", digest)
        self.send_header("Content-Length", str(size))
        self.end_headers()
        if head_only:
            return
        with open(full, "rb") as f:
            shutil.copyfileobj(f, self.wfile, _SERVE_CHUNK)

    def _serve_oci_blob(self, name, digest, head_only):
        meta, blobs_dir = uploads.srsim_meta(name)
        if not meta:
            self._v2_404("repository %s not found" % name)
            return
        h = digest.split(":", 1)[1]
        if not _SHA256_HEX.match(h):
            self._v2_404("bad blob digest")
            return
        full = os.path.join(blobs_dir, h)
        if not os.path.isfile(full):
            self._v2_404("blob unknown")
            return
        size = os.path.getsize(full)
        # Optional single-range request (containerd may resume large layer pulls).
        start, end, partial = 0, size - 1, False
        rng = self.headers.get("Range")
        if rng:
            mm = re.match(r"bytes=(\d+)-(\d*)$", rng.strip())
            if mm:
                start = int(mm.group(1))
                end = int(mm.group(2)) if mm.group(2) else size - 1
                if start <= end < size:
                    partial = True
                else:
                    self.send_response(416)
                    self.send_header("Docker-Distribution-Api-Version", "registry/2.0")
                    self.send_header("Content-Range", "bytes */%d" % size)
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
        length = (end - start + 1) if partial else size
        self.send_response(206 if partial else 200)
        self.send_header("Docker-Distribution-Api-Version", "registry/2.0")
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Docker-Content-Digest", digest)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(length))
        if partial:
            self.send_header("Content-Range", "bytes %d-%d/%d" % (start, end, size))
        self.end_headers()
        if head_only:
            return
        with open(full, "rb") as f:
            if start:
                f.seek(start)
            remaining = length
            while remaining > 0:
                buf = f.read(min(_SERVE_CHUNK, remaining))
                if not buf:
                    break
                self.wfile.write(buf)
                remaining -= len(buf)

    # --------------------------- POST ---------------------------

    def do_POST(self):
        path, q = self._route()
        try:
            # All POSTs are user actions — require a valid EDA session.
            if auth.enabled() and not self._authed_user():
                self._send_json({"ok": False, "error": "not authenticated"}, 401)
                return
            if path == "/api/upload":
                self._handle_upload(q)
            elif path == "/api/delete":
                self._handle_delete(q)
            else:
                self.send_error(405, "Method Not Allowed")
        except BrokenPipeError:
            pass
        except Exception as e:
            logger.error("POST %s failed: %s", self.path, e)
            try:
                self._send_json({"ok": False, "error": str(e)}, code=500)
            except Exception:
                pass

    def _handle_delete(self, q):
        def one(name):
            v = q.get(name, [None])
            return v[0] if v else None

        upload_id = one("uploadId")
        namespace = one("namespace")
        name = one("name")
        meta = uploads.read_meta(upload_id) if upload_id else None
        namespace = namespace or (meta or {}).get("namespace")
        # Collect every Artifact this upload created: a group (SR OS) lists them in
        # meta.artifacts (+ yang); a single image is name + its optional md5 sidecar.
        names = []
        if meta and meta.get("artifacts"):
            for a in meta["artifacts"]:
                if a.get("artifactName"):
                    names.append(a["artifactName"])
                if a.get("md5ArtifactName"):     # per-file md5 sidecar Artifact (SR OS)
                    names.append(a["md5ArtifactName"])
            yang = meta.get("yang") or {}
            if yang.get("artifactName"):
                names.append(yang["artifactName"])
        else:
            md5_name = (meta or {}).get("md5ArtifactName") or ""
            yang = (meta or {}).get("yang") or {}
            names = [n for n in (name, md5_name, yang.get("artifactName")) if n]
        artifact_deleted = False
        if namespace:
            for art_name in names:
                try:
                    artifact.delete_artifact(namespace, art_name)
                    artifact_deleted = True
                except urllib.error.HTTPError as e:
                    if e.code != 404:
                        self._send_json({"ok": False,
                                         "error": f"Artifact delete failed (HTTP {e.code})"}, 502)
                        return
                    artifact_deleted = True  # already gone
        local_removed = uploads.delete_upload(upload_id) if upload_id else False
        logger.info("Delete %s/%s (%d artifact(s)) (artifactDeleted=%s localRemoved=%s)",
                    namespace, upload_id, len(names), artifact_deleted, local_removed)
        self._send_json({"ok": True, "artifactDeleted": artifact_deleted,
                         "localRemoved": local_removed})

    def _handle_upload(self, q):
        """Single entry point for image uploads. Only vendor .zip files are
        accepted; the NOS (SR Linux vs SR OS) is auto-detected from the zip
        contents. The md5 and the YANG schema profile are taken/derived
        automatically -- the user supplies neither."""
        def one(name, default=None):
            v = q.get(name, [default])
            return v[0] if v else default

        filename = uploads.sanitize_filename(one("filename", ""))
        namespace = (one("namespace") or "").strip()
        name_override = (one("name") or "").strip()
        if not filename:
            self._send_json({"ok": False, "error": "filename query param required"}, 400)
            return
        if not namespace:
            self._send_json({"ok": False, "error": "namespace query param required"}, 400)
            return
        if not filename.lower().endswith(".zip"):
            self._send_json({"ok": False,
                             "error": "Only vendor .zip images are supported "
                                      "(SR Linux or SR OS 7750 TiMOS)."}, 400)
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0
        if content_length <= 0:
            self._send_json({"ok": False, "error": "Content-Length required"}, 411)
            return
        max_bytes = int(CONFIG.get("maxUploadMiB", 4096)) * 1024 * 1024

        # Stream the zip to a per-request temp area, auto-detect the NOS from its
        # contents, then dispatch. The temp area is always removed.
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        tmp_dir = tempfile.mkdtemp(dir=UPLOAD_DIR, prefix=".incoming-")
        try:
            tmp_zip = os.path.join(tmp_dir, "upload.zip")
            try:
                uploads.stream_upload(self.rfile, content_length, tmp_zip, max_bytes)
            except uploads.UploadTooLarge as e:
                self._send_json({"ok": False, "error": f"upload too large: {e}"}, 413)
                return
            if not uploads.looks_like_zip(tmp_zip):
                self._send_json({"ok": False,
                                 "error": "the uploaded file is not a valid .zip archive"}, 400)
                return
            nos = uploads.detect_nos_from_zip(tmp_zip)
            if nos == "srsim":
                self._finish_srsim_upload(tmp_zip, filename, namespace, name_override)
            elif nos == "sros":
                self._finish_sros_upload(tmp_dir, tmp_zip, namespace, name_override)
            elif nos == "srl":
                self._finish_srl_upload(tmp_zip, filename, namespace, name_override)
            else:
                self._send_json({"ok": False,
                                 "error": "could not detect an SR Linux (.bin), SR OS 7750 "
                                          "TiMOS, or SR-SIM (srsim.tar.xz) image inside the "
                                          "zip"}, 400)
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def _finish_srl_upload(self, tmp_zip, filename, namespace, name_override):
        """SR Linux: extract the .bin (+ its packaged md5) from the temp zip into
        the image dir, create the image (+md5) Artifact, then resolve the YANG."""
        repo = (CONFIG.get("defaultRepo") or "images").strip()
        # Lowercase everywhere: this name becomes the Artifact name and the
        # NodeProfile name, so capitals must never get through.
        display_name = (name_override or uploads.derive_name(filename)).strip().lower()
        artifact_name = uploads.to_k8s_name(display_name)
        if not artifact_name:
            self._send_json({"ok": False, "error": "could not derive a valid image name"}, 400)
            return
        upload_dir = os.path.join(UPLOAD_DIR, artifact_name)
        if os.path.isfile(os.path.join(upload_dir, "meta.json")):
            self._send_json({"ok": False,
                             "error": f"An image named '{display_name}' already exists. "
                                      f"Delete it first to replace it."}, 409)
            return
        shutil.rmtree(upload_dir, ignore_errors=True)
        os.makedirs(upload_dir, exist_ok=True)
        try:
            bin_filename, md5 = uploads.extract_image_from_zip(tmp_zip, upload_dir)
        except uploads.BadZip as e:
            shutil.rmtree(upload_dir, ignore_errors=True)
            self._send_json({"ok": False, "error": f"could not read the zip: {e}"}, 400)
            return
        written = os.path.getsize(os.path.join(upload_dir, bin_filename))
        md5_artifact_name = (artifact_name + "-md5") if md5 else ""
        # Re-host each artifact under its real shipped filename: eda-asvr serves it at
        # <ns>/<repo>/<artifactName>/<filePath>, so filePath carries the extension SR
        # Linux ZTP expects -- the image as <name>.bin and its checksum as <name>.bin.md5.
        # The same value is recorded in meta.json so the UI matches what is served.
        image_file_path = bin_filename
        md5_file_path = bin_filename + ".md5"
        uploads.finalize_upload(artifact_name, bin_filename, md5, repo, image_file_path,
                                namespace, written, artifact_name, display_name, md5_artifact_name)
        base_url = CONFIG.get("filePullBaseUrl") or artifact.default_base_url(POD_NAMESPACE)
        file_url, md5_url = artifact.file_urls(base_url, artifact_name, bin_filename)
        try:
            artifact.create_artifact(namespace, artifact_name, repo, image_file_path,
                                     file_url, md5_url if md5 else None)
        except urllib.error.HTTPError as e:
            shutil.rmtree(upload_dir, ignore_errors=True)
            if e.code == 409:
                self._send_json({"ok": False,
                                 "error": f"An Artifact named '{artifact_name}' already exists "
                                          f"in {namespace}. Delete it first."}, 409)
                return
            detail = ""
            try:
                detail = e.read().decode("utf-8", errors="replace")[:300]
            except Exception:  # noqa: BLE001
                pass
            self._send_json({"ok": False,
                             "error": f"Artifact create failed (HTTP {e.code}): {detail}"}, 502)
            return
        except Exception as e:  # noqa: BLE001 - URLError/timeout: don't orphan
            shutil.rmtree(upload_dir, ignore_errors=True)
            self._send_json({"ok": False, "error": f"Artifact create failed: {e}"}, 502)
            return
        if md5:
            try:
                artifact.create_artifact(namespace, md5_artifact_name, repo,
                                         md5_file_path, md5_url, None)
            except Exception as e:  # noqa: BLE001 - md5 sidecar Artifact is best-effort
                logger.warning("md5 Artifact %s/%s create failed: %s",
                               namespace, md5_artifact_name, e)
        # YANG (best-effort, never aborts the image): auto-resolve from the version.
        yang_created = False
        try:
            vm = _VER_RE.search(display_name)
            srl_ver = vm.group(1).split("-")[0] if vm else ""
            if srl_ver:
                yfn, _src = schemaprofile.resolve_yang("srl", srl_ver, upload_dir)
                if yfn:
                    ok, yrec = self._create_yang_artifact(namespace, artifact_name,
                                                          artifact_name + "-yang", yfn, base_url)
                    if ok:
                        m = uploads.read_meta(artifact_name) or {}
                        m["yang"] = yrec
                        m["nos"] = "srl"
                        m["version"] = srl_ver
                        uploads.rewrite_meta(artifact_name, m)
                        yang_created = True
        except Exception as e:  # noqa: BLE001 - YANG is best-effort
            logger.warning("SRL YANG handling failed for %s: %s", artifact_name, e)
        logger.info("Upload complete: %s (%d bytes, md5=%s, yang=%s) -> Artifact %s/%s",
                    bin_filename, written, bool(md5), yang_created, namespace, artifact_name)
        self._send_json({"ok": True, "uploadId": artifact_name, "artifactName": artifact_name,
                         "displayName": display_name, "namespace": namespace, "repo": repo,
                         "nos": "srl", "filePath": image_file_path, "md5": md5 or "",
                         "sizeBytes": written, "fromZip": True, "filename": bin_filename,
                         "yangCreated": yang_created})

    # ---------------------- SR OS (7750 TiMOS) upload ----------------------

    def _create_yang_artifact(self, namespace, upload_id, yname, yang_filename, base_url):
        """Create the schema-profile (yang) Artifact. The file is hosted by us at
        /files/<upload_id>/<yang_filename>; the Artifact is named `yname` (SR OS:
        the group id sros-<ver> -> reference path; SR Linux: <img>-yang to avoid
        clashing with the image Artifact). Returns (ok, record); never raises (a
        YANG failure must not abort the image upload)."""
        file_url, _ = artifact.file_urls(base_url, upload_id, yang_filename)
        for attempt in range(4):
            try:
                artifact.create_artifact(namespace, yname, artifact.SCHEMAPROFILE_REPO,
                                         yang_filename, file_url, None)
                return True, {"artifactName": yname, "filename": yang_filename,
                              "filePath": yang_filename, "repo": artifact.SCHEMAPROFILE_REPO}
            except urllib.error.HTTPError as e:
                # On a re-upload we delete the same-named Artifact first; it may still
                # be Terminating (finalizer) -> 409. Back off and retry a few times.
                if e.code == 409 and attempt < 3:
                    time.sleep(1.0)
                    continue
                logger.warning("YANG Artifact %s/%s create failed (HTTP %s)",
                               namespace, yname, e.code)
                return False, None
            except Exception as e:  # noqa: BLE001 - YANG is best-effort
                logger.warning("YANG Artifact %s/%s create error: %s", namespace, yname, e)
                return False, None

    def _finish_sros_upload(self, tmp_dir, tmp_zip, namespace, name_override):
        """SR OS (7750 TiMOS): extract the boot-image set from the temp zip, create
        one Artifact per file plus a per-file md5 Artifact (md5 from the zip's
        md5sums.txt), then resolve the YANG (fetch nokia-eda, else build from 7x50).
        The display name is editable; the version (for yang) comes from the zip."""
        try:
            version_disp, extracted = uploads.extract_sros_images(tmp_zip, tmp_dir)
        except uploads.BadZip as e:
            self._send_json({"ok": False, "error": f"not a 7750 SR OS image: {e}"}, 400)
            return
        version = version_disp.lower()
        # Lowercase everywhere (Artifact names, served filePaths, NodeProfile name).
        display_name = (name_override or ("sros-" + version)).strip().lower()
        group_id = uploads.to_k8s_name(display_name)
        if not group_id:
            self._send_json({"ok": False, "error": "could not derive a valid image name"}, 400)
            return
        group_dir = os.path.join(UPLOAD_DIR, group_id)
        if os.path.isfile(os.path.join(group_dir, "meta.json")):
            self._send_json({"ok": False,
                             "error": f"An image named '{display_name}' already exists. "
                                      f"Delete it first to replace it."}, 409)
            return
        shutil.rmtree(group_dir, ignore_errors=True)
        os.makedirs(group_dir, exist_ok=True)
        total = 0
        for it in extracted:
            os.replace(os.path.join(tmp_dir, it["filename"]),
                       os.path.join(group_dir, it["filename"]))
            total += int(it.get("size") or 0)

        base_url = CONFIG.get("filePullBaseUrl") or artifact.default_base_url(POD_NAMESPACE)
        created = []
        art_records = []

        def rollback():
            for ns_, nm_ in created:
                try:
                    artifact.delete_artifact(ns_, nm_)
                except Exception:  # noqa: BLE001
                    pass
            shutil.rmtree(group_dir, ignore_errors=True)

        for it in extracted:
            fn = it["filename"]
            md5 = it.get("md5")
            art_name = uploads.to_k8s_name(group_id + "-" + fn)
            file_url, md5_url = artifact.file_urls(base_url, group_id, fn)
            if md5:
                with open(os.path.join(group_dir, fn + ".md5"), "w") as f:
                    f.write(md5 + "\n")
            try:
                artifact.create_artifact(namespace, art_name, artifact.SROS_REPO,
                                         fn, file_url, md5_url if md5 else None)
            except urllib.error.HTTPError as e:
                rollback()
                detail = ""
                try:
                    detail = e.read().decode("utf-8", "replace")[:200]
                except Exception:  # noqa: BLE001
                    pass
                code = 409 if e.code == 409 else 502
                self._send_json({"ok": False,
                                 "error": f"Artifact {art_name} create failed "
                                          f"(HTTP {e.code}): {detail}"}, code)
                return
            except Exception as e:  # noqa: BLE001 - roll back, never orphan
                rollback()
                self._send_json({"ok": False,
                                 "error": f"Artifact {art_name} create failed: {e}"}, 502)
                return
            created.append((namespace, art_name))
            rec = {"artifactName": art_name, "filename": fn, "filePath": fn}
            if md5:
                md5_art = uploads.to_k8s_name(art_name + "-md5")
                try:
                    artifact.create_artifact(namespace, md5_art, artifact.SROS_REPO,
                                             fn + ".md5", md5_url, None)
                    created.append((namespace, md5_art))
                    rec["md5ArtifactName"] = md5_art
                except Exception as e:  # noqa: BLE001 - md5 sidecar Artifact is best-effort
                    logger.warning("md5 Artifact %s/%s create failed: %s", namespace, md5_art, e)
            art_records.append(rec)

        # YANG schema profile (best-effort): fetch published, else build from 7x50.
        yang_meta = None
        try:
            yfn, src = schemaprofile.resolve_yang("sros", version, group_dir)
            if yfn:
                ok, yang_meta = self._create_yang_artifact(namespace, group_id, group_id,
                                                           yfn, base_url)
                if ok:
                    total += os.path.getsize(os.path.join(group_dir, yfn))
                    note = ("YANG schema profile auto-fetched from nokia-eda/schema-profiles."
                            if src == "published" else
                            "YANG schema profile built from nokia/7x50_YangModels.")
                else:
                    note = "Image artifacts created, but the YANG schema-profile Artifact failed."
            else:
                note = (f"Image artifacts created. Could not obtain a YANG schema profile for "
                        f"{version} (not published upstream and no 7x50 tag).")
        except Exception as e:  # noqa: BLE001 - YANG is best-effort; keep the image artifacts
            logger.warning("YANG handling failed for %s: %s", group_id, e)
            yang_meta = None
            note = "Image artifacts created; the YANG step failed."

        uploads.finalize_group(group_id, display_name, "sros", namespace, artifact.SROS_REPO,
                               art_records, yang_meta, total, version)
        logger.info("SR OS upload complete: %s (%d files, %d bytes) -> %d Artifact(s) in %s/%s (yang=%s)",
                    display_name, len(extracted), total, len(created), namespace,
                    artifact.SROS_REPO, bool(yang_meta))
        self._send_json({"ok": True, "uploadId": group_id, "artifactName": group_id,
                         "displayName": display_name, "namespace": namespace,
                         "repo": artifact.SROS_REPO, "nos": "sros", "version": version,
                         "fileCount": len(extracted), "sizeBytes": total,
                         "yangCreated": bool(yang_meta), "note": note})

    # ---------------------- SR-SIM (SR OS simulator container image) ----------------------

    def _finish_srsim_upload(self, tmp_zip, filename, namespace, name_override):
        """SR-SIM: unpack srsim.tar.xz into an OCI layout on the PVC (served from
        our /v2 endpoint -- eda-cx pulls it by tag, no eda-asvr Artifact), then
        best-effort resolve the SR OS YANG schema profile so the emitted sim
        NodeProfile carries a working yang: URL. Name drives the served repo path
        and the NodeProfile name; kept lowercase."""
        display_name = (name_override or uploads.derive_name(filename)).strip().lower()
        artifact_name = uploads.to_k8s_name(display_name)
        if not artifact_name:
            self._send_json({"ok": False, "error": "could not derive a valid image name"}, 400)
            return
        image_dir = os.path.join(UPLOAD_DIR, artifact_name)
        if os.path.isfile(os.path.join(image_dir, "meta.json")):
            self._send_json({"ok": False,
                             "error": f"An image named '{display_name}' already exists. "
                                      f"Delete it first to replace it."}, 409)
            return
        shutil.rmtree(image_dir, ignore_errors=True)
        os.makedirs(image_dir, exist_ok=True)
        try:
            oci = uploads.extract_srsim_image(tmp_zip, image_dir)
        except uploads.BadZip as e:
            shutil.rmtree(image_dir, ignore_errors=True)
            self._send_json({"ok": False, "error": f"could not read the SR-SIM image: {e}"}, 400)
            return
        except Exception as e:  # noqa: BLE001 - never leave a partial OCI layout on the PVC
            shutil.rmtree(image_dir, ignore_errors=True)
            logger.warning("SR-SIM extract failed for %s: %s", artifact_name, e)
            self._send_json({"ok": False, "error": f"failed to unpack the SR-SIM image: {e}"}, 500)
            return
        # YANG schema profile (best-effort, via eda-asvr) so the NodeProfile's
        # required yang: field has a working URL. Same resolver as SR OS HW.
        version = oci.get("version") or ""
        yang_meta = None
        base_url = CONFIG.get("filePullBaseUrl") or artifact.default_base_url(POD_NAMESPACE)
        try:
            if version:
                yfn, _src = schemaprofile.resolve_yang("sros", version, image_dir)
                if yfn:
                    ok, yang_meta = self._create_yang_artifact(namespace, artifact_name,
                                                               artifact_name + "-yang", yfn, base_url)
                    if not ok:
                        yang_meta = None
        except Exception as e:  # noqa: BLE001 - YANG is best-effort, never abort the image
            logger.warning("SR-SIM YANG handling failed for %s: %s", artifact_name, e)
            yang_meta = None
        uploads.finalize_srsim(artifact_name, display_name, namespace, oci, yang_meta)
        container_image = f"{sim_registry_host()}/{artifact_name}:{oci.get('tag')}"
        logger.info("SR-SIM upload complete: %s (%d bytes, tag %s, yang=%s) -> /v2/%s",
                    display_name, oci.get("sizeBytes") or 0, oci.get("tag"),
                    bool(yang_meta), artifact_name)
        self._send_json({"ok": True, "uploadId": artifact_name, "artifactName": artifact_name,
                         "displayName": display_name, "namespace": namespace, "nos": "srsim",
                         "version": version, "imageTag": oci.get("tag"),
                         "containerImage": container_image,
                         "sizeBytes": oci.get("sizeBytes"), "yangCreated": bool(yang_meta)})


_VER_RE = re.compile(r"(\d+\.\d+\.[A-Za-z]?\d+(?:-\d+)?)")


def _nodeprofile_yaml(nos, version, namespace, prof_name, image_entries, yang_url):
    """A complete, copy-ready NodeProfile example for an Available image. The
    image path(s)+imageMd5, version, operatingSystem and yang are filled from the
    real artifact(s); environment-specific fields are left as <placeholders>.
    image_entries = [(image_path, md5_path_or_empty), ...]."""
    L = [
        "apiVersion: core.eda.nokia.com/v1",
        "kind: NodeProfile",
        "metadata:",
        f"  name: {prof_name}",
        f"  namespace: {namespace}",
        "  labels:",
        '    eda.nokia.com/bootstrap: "true"',
        "spec:",
        "  annotate: false",
        f"  operatingSystem: {nos}",
        f"  version: {version}",
        "  port: 57400",
        "  # image(s) registered by EDA Image Manager:",
        "  images:",
    ]
    for path, md5_path in image_entries:
        L.append(f"  - image: {path}")
        if md5_path:
            L.append(f"    imageMd5: {md5_path}")
    if yang_url:
        L.append(f"  yang: {yang_url}")
    else:
        L.append(f"  # yang: https://eda-asvr.eda-system.svc/{namespace}/schemaprofiles/"
                 "<profile>/<profile>.zip   # add the matching schema profile")
    L += [
        "  # llmDb: https://eda-asvr.eda-system.svc/<ns>/llm-dbs/<db>/<db>.tar.gz"
        "   # optional, EDA-provided per version",
        "  nodeUser: admin",
        "  onboardingUsername: admin",
        "  onboardingPassword: NokiaSrl1!",
        "  dhcp:",
        "    managementPoolv4: <your-ipv4-mgmt-pool>",
        "    dhcp4Options:",
        "    - option: 6-DomainNameServer",
        "      value:",
        "      - <dns-server-ip>",
        "    - option: 42-NTPServers",
        "      value:",
        "      - <ntp-server-ip>",
    ]
    return "\n".join(L)


def _single_row(m, status_by_key):
    """Tracked-list row for a one-file image (SR Linux .bin / raw upload)."""
    ns = m.get("namespace")
    st = status_by_key.get((ns, m.get("artifactName")), {})
    md5_name = m.get("md5ArtifactName")
    md5_st = status_by_key.get((ns, md5_name), {}) if md5_name else {}
    # NodeProfile paths are only valid once eda-asvr reports the file Available.
    image_path = (artifact.asvr_path(st.get("internalUrl", ""))
                  if st.get("downloadStatus") == "Available" else "")
    md5_path = (artifact.asvr_path(md5_st.get("internalUrl", ""))
                if md5_st.get("downloadStatus") == "Available" else "")
    display = m.get("displayName") or m.get("artifactName") or ""
    nos = m.get("nos") or "srl"
    # optional YANG schema-profile artifact (auto-fetched or uploaded)
    yang = m.get("yang") or {}
    yst = status_by_key.get((ns, yang.get("artifactName")), {}) if yang.get("artifactName") else {}
    yang_url = yst.get("internalUrl", "") if yst.get("downloadStatus") == "Available" else ""
    snippet = ""
    example = ""
    if image_path:
        snippet = "images:\n  - image: " + image_path
        if md5_path:
            snippet += "\n    imageMd5: " + md5_path
        if yang_url:
            snippet += "\nyang: " + yang_url
        vm = _VER_RE.search(display)
        example = _nodeprofile_yaml(nos, vm.group(1) if vm else "<version>", ns,
                                    uploads.to_k8s_name(display) or "my-nodeprofile",
                                    [(image_path, md5_path)], yang_url)
    return {
        "uploadId": m.get("uploadId"),
        "name": m.get("artifactName"),
        "displayName": display,
        "namespace": ns,
        "repo": m.get("repo"),
        "filePath": m.get("filePath"),
        "filename": m.get("filename"),
        "sizeBytes": m.get("sizeBytes"),
        "md5": m.get("md5"),
        "storedAt": m.get("storedAt"),
        "downloadStatus": st.get("downloadStatus", "NoArtifact" if not st else ""),
        "statusReason": st.get("statusReason", ""),
        "imagePath": image_path,
        "md5Path": md5_path,
        "snippet": snippet,
        "nodeProfileExample": example,
        "nos": nos,
        "yangStatus": (yst.get("downloadStatus") if yang.get("artifactName") else None),
    }


def _group_row(m, status_by_key):
    """Tracked-list row for a multi-file image group (SR OS): one upload, several
    Artifacts. Status is aggregated; the NodeProfile snippet lists every image
    path (plus the yang: URL) once all parts report Available."""
    ns = m.get("namespace")
    arts = m.get("artifacts") or []
    yang = m.get("yang") or None
    statuses, image_lines, image_entries, reasons = [], [], [], []
    all_images_available = bool(arts)
    for a in arts:
        st = status_by_key.get((ns, a.get("artifactName")), {})
        ds = st.get("downloadStatus", "NoArtifact" if not st else "")
        statuses.append(ds)
        ipath = ""
        if ds == "Available":
            ipath = artifact.asvr_path(st.get("internalUrl", ""))
            if not ipath:
                all_images_available = False
        else:
            all_images_available = False
        if st.get("statusReason"):
            reasons.append((a.get("filename") or "") + ": " + st["statusReason"])
        # per-file md5 artifact (SR OS imageMd5, from the zip's md5sums.txt)
        mpath = ""
        md5_name = a.get("md5ArtifactName")
        if md5_name:
            mst = status_by_key.get((ns, md5_name), {})
            statuses.append(mst.get("downloadStatus", "NoArtifact" if not mst else ""))
            if mst.get("downloadStatus") == "Available":
                mpath = artifact.asvr_path(mst.get("internalUrl", ""))
            if mst.get("statusReason"):
                reasons.append((a.get("filename") or "") + ".md5: " + mst["statusReason"])
        if ipath:
            image_lines.append("  - image: " + ipath
                               + ("\n    imageMd5: " + mpath if mpath else ""))
            image_entries.append((ipath, mpath))

    yang_status, yang_url = None, ""
    if yang:
        yst = status_by_key.get((ns, yang.get("artifactName")), {})
        yang_status = yst.get("downloadStatus", "NoArtifact" if not yst else "")
        statuses.append(yang_status)
        if yang_status == "Available":
            yang_url = yst.get("internalUrl", "")    # yang: takes a full asvr URL
        if yst.get("statusReason"):
            reasons.append("yang: " + yst["statusReason"])

    if statuses and all(s == "Available" for s in statuses):
        agg = "Available"
    elif any(s in ("Error", "Failed") for s in statuses):
        agg = "Error"
    elif statuses:
        agg = "InProgress"
    else:
        agg = "NoArtifact"

    snippet = ""
    example = ""
    if all_images_available and image_lines:
        snippet = "images:\n" + "\n".join(image_lines)
        if yang_url:
            snippet += "\nyang: " + yang_url
        example = _nodeprofile_yaml("sros", m.get("version") or "<version>", ns,
                                    m.get("uploadId") or "my-nodeprofile",
                                    image_entries, yang_url)
    return {
        "uploadId": m.get("uploadId"),
        "name": m.get("uploadId"),
        "displayName": m.get("displayName") or m.get("uploadId"),
        "namespace": ns,
        "repo": m.get("repo"),
        "filePath": "",
        "sizeBytes": m.get("sizeBytes"),
        "storedAt": m.get("storedAt"),
        "downloadStatus": agg,
        "statusReason": "; ".join(reasons[:4]),
        "snippet": snippet,
        "nodeProfileExample": example,
        "nos": "sros",
        "fileCount": len(arts),
        "yangStatus": yang_status,
    }


def _sim_nodeprofile_yaml(version, namespace, prof_name, container_image, yang_url):
    """A complete, copy-ready SR OS *simulator* NodeProfile: containerImage points
    at this app's /v2 endpoint, plus a dummy license ConfigMap. <…> values are for
    the operator to set."""
    license_cm = "sros-sim-license"
    L = [
        "apiVersion: core.eda.nokia.com/v1",
        "kind: NodeProfile",
        "metadata:",
        f"  name: {prof_name}",
        f"  namespace: {namespace}",
        "  labels:",
        '    eda.nokia.com/bootstrap: "true"',
        "spec:",
        "  operatingSystem: sros",
        f"  version: {version}",
        f"  containerImage: {container_image}",
        "  imagePullSecret: core      # a Secret in eda-system (where sims run); 'core' exists "
        "and works — this registry is anonymous, so its contents are unused",
        f"  license: {license_cm}      # ConfigMap below (an SR-SIM sim boots on an empty license)",
    ]
    if yang_url:
        L.append(f"  yang: {yang_url}")
    else:
        L.append("  # yang: https://eda-asvr.eda-system.svc/<ns>/schemaprofiles/<p>/<p>.zip"
                 "   # add the matching SR OS schema profile")
    L += [
        "  nodeUser: admin",
        "  onboardingUsername: admin",
        "  onboardingPassword: NokiaSrl1!",
        "  dhcp:",
        "    managementPoolv4: <your-ipv4-mgmt-pool>",
        "---",
        "# License ConfigMap referenced above. The Digital Twin SR-SIM accepts an",
        "# empty dummy license; supply a real key only if your image requires one.",
        "apiVersion: v1",
        "kind: ConfigMap",
        "metadata:",
        f"  name: {license_cm}",
        "  namespace: eda-system",
        "data:",
        '  license.key: ""',
    ]
    return "\n".join(L)


def _sim_setup_note(container_image, namespace, prof_name):
    """One-time, per-cluster instructions: teach the node's containerd to pull
    from this app's registry, plus a topology to launch the sim."""
    host = sim_registry_host()
    return "\n".join([
        "ONE-TIME SETUP (per cluster) — let the node pull this image",
        "EDA's Digital Twin (eda-cx) starts the sim with the node's container",
        f"runtime, which must be told how to reach Image Manager's registry. Add a",
        f"Talos registry mirror for host '{host}' that points at the eda-imagemanager",
        "Service (ClusterIP:8443):",
        "",
        "  machine:",
        "    registries:",
        "      mirrors:",
        f"        {host}:",
        "          endpoints:",
        "            - https://<eda-imagemanager-ClusterIP>:8443",
        "      config:",
        f"        {host}:",
        "          tls:",
        "            insecureSkipVerify: true   # in-cluster internal-CA serving cert",
        "",
        "  # ClusterIP: kubectl -n eda-system get svc eda-imagemanager -o jsonpath='{.spec.clusterIP}'",
        "  # apply with no reboot: talosctl -n <node> patch mc -p @mirror.json --mode=no-reboot",
        "",
        "LAUNCH A SIM NODE — apply the NodeProfile above, then a topology:",
        "",
        "apiVersion: topologies.eda.nokia.com/v1",
        "kind: NetworkTopology",
        "metadata:",
        "  name: srsim-demo",
        f"  namespace: {namespace}",
        "spec:",
        "  operation: Create",
        "  nodeTemplates:",
        "    - name: srsim",
        f"      nodeProfile: {prof_name}",
        '      platform: "7750 SR-1"',
        "  nodes:",
        "    - name: srsim1",
        "      template: srsim",
        "",
        "NOTES",
        f"- A NodeUser named 'admin' must exist in namespace '{namespace}' (referenced by the profile).",
        "- imagePullSecret must name a Secret that exists in eda-system (where the sim pod runs);",
        "  eda-cx requires the field, but this anonymous registry never uses its contents. The",
        "  built-in 'core' secret works.",
    ])


def _srsim_row(m, status_by_key):
    """Tracked-list row for an SR-SIM container image. Served from our own /v2
    endpoint (no eda-asvr Artifact), so it is Ready as soon as it is unpacked. The
    Details popup yields a sim NodeProfile (containerImage) + the one-time node
    registry-mirror setup."""
    ns = m.get("namespace")
    artifact_name = m.get("artifactName")
    tag = m.get("imageTag") or m.get("version") or "latest"
    version = m.get("version") or "<version>"
    container_image = f"{sim_registry_host()}/{artifact_name}:{tag}"
    yang = m.get("yang") or {}
    yst = status_by_key.get((ns, yang.get("artifactName")), {}) if yang.get("artifactName") else {}
    yang_url = yst.get("internalUrl", "") if yst.get("downloadStatus") == "Available" else ""
    snippet = ("operatingSystem: sros\nversion: " + version
               + "\ncontainerImage: " + container_image
               + "\nimagePullSecret: core")
    example = _sim_nodeprofile_yaml(version, ns, artifact_name or "my-sim-nodeprofile",
                                    container_image, yang_url)
    setup = _sim_setup_note(container_image, ns, artifact_name or "my-sim-nodeprofile")
    return {
        "uploadId": m.get("uploadId"),
        "name": artifact_name,
        "displayName": m.get("displayName") or artifact_name,
        "namespace": ns,
        "repo": "served by Image Manager (/v2)",
        "filePath": "",
        "sizeBytes": m.get("sizeBytes"),
        "storedAt": m.get("storedAt"),
        "downloadStatus": "Ready",
        "statusReason": "",
        "snippet": snippet,
        "nodeProfileExample": example,
        "setupNote": setup,
        "nos": "srsim",
        "containerImage": container_image,
        "imageTag": tag,
        "yangStatus": (yst.get("downloadStatus") if yang.get("artifactName") else None),
    }


def build_tracked_list():
    """Merge PVC upload metadata with live Artifact download status for the UI."""
    # one cluster-wide list call, indexed by (namespace, name)
    status_by_key = {}
    try:
        for art in artifact.list_managed_artifacts():
            md = art.get("metadata", {})
            st = art.get("status", {}) or {}
            status_by_key[(md.get("namespace"), md.get("name"))] = st
    except Exception as e:
        logger.info("artifact list unavailable: %s", e)

    out = []
    for m in uploads.list_meta():
        if m.get("nos") == "srsim":
            out.append(_srsim_row(m, status_by_key))
        elif m.get("artifacts"):
            out.append(_group_row(m, status_by_key))
        else:
            out.append(_single_row(m, status_by_key))
    out.sort(key=lambda r: r.get("storedAt") or "", reverse=True)
    return out


def write_healthz(status="ok", last_reconcile=None):
    """Atomic write of .healthz.json via rename."""
    data = json.dumps({"status": status, "last_reconcile": last_reconcile})
    tmp = HEALTHZ_FILE + ".tmp"
    with open(tmp, "w") as f:
        f.write(data)
    os.replace(tmp, HEALTHZ_FILE)


def _build_ssl_context():
    crt = os.path.join(TLS_DIR, "tls.crt")
    key = os.path.join(TLS_DIR, "tls.key")
    if not (os.path.isfile(crt) and os.path.isfile(key)):
        return None
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(crt, key)
    return ctx


def start_file_server(port=8443):
    """Start the HTTPS file server as a daemon thread. Falls back to HTTP if no cert."""
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    ctx = None
    try:
        ctx = _build_ssl_context()
    except Exception as e:
        logger.error("Failed to load serving cert from %s: %s", TLS_DIR, e)
    if ctx is not None:
        server.socket = ctx.wrap_socket(server.socket, server_side=True)
        scheme = "https"
    else:
        logger.error("No serving cert at %s -- starting PLAIN HTTP (kubelet HTTPS "
                     "probes and eda-asvr HTTPS pulls will fail until cert present)",
                     TLS_DIR)
        scheme = "http"
    t = threading.Thread(target=server.serve_forever, daemon=True, name="fileserver")
    t.start()
    logger.info("File server started on %s://0.0.0.0:%d", scheme, port)
    return server
