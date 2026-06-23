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
import shutil
import ssl
import threading
import urllib.error
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, quote, unquote, urlencode, urlsplit

import artifact
import auth
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
        body = (
            "<!doctype html><meta charset=utf-8><title>Signed out</title>"
            "<body style='font:14px -apple-system,Segoe UI,sans-serif;padding:48px;color:#2b2b2b'>"
            "<h2>Signed out of Image Manager</h2>"
            "<p>You're still logged into EDA.</p>"
            f"<p><a href='{link}'>Sign in again</a></p></body>"
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
            "<!doctype html><meta charset=utf-8><title>Access denied</title>"
            "<body style='font:14px -apple-system,Segoe UI,sans-serif;padding:48px;color:#2b2b2b'>"
            "<h2>Access denied</h2>"
            f"<p>You're signed in to EDA as <b>{html.escape(user)}</b>, but Image Manager is "
            f"restricted to users with the role: <b>{html.escape(roles)}</b>.</p>"
            f"<p>Ask an administrator for the role, or <a href='{link}'>sign out</a>.</p></body>",
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
        self._send_json({"artifacts": build_tracked_list()})

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
        # also remove the companion md5 Artifact, if one was created for this upload
        md5_name = ""
        if upload_id:
            md5_name = (uploads.read_meta(upload_id) or {}).get("md5ArtifactName") or ""
        artifact_deleted = False
        for art_name in [n for n in (name, md5_name) if n]:
            if not namespace:
                break
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
        logger.info("Delete %s/%s (+md5 %s) (artifactDeleted=%s localRemoved=%s)",
                    namespace, name, md5_name or "-", artifact_deleted, local_removed)
        self._send_json({"ok": True, "artifactDeleted": artifact_deleted,
                         "localRemoved": local_removed})

    def _handle_upload(self, q):
        def one(name, default=None):
            v = q.get(name, [default])
            return v[0] if v else default

        filename = uploads.sanitize_filename(one("filename", ""))
        # repo is a single fixed grouping (Artifact requires one); not user-facing.
        repo = (CONFIG.get("defaultRepo") or "images").strip()
        namespace = (one("namespace") or CONFIG.get("defaultArtifactNamespace", "eda")).strip()
        # The user-facing image name (e.g. "SRLinux-26.3.2"). Defaults to a name
        # derived from the filename; becomes the Artifact identity + served path.
        display_name = (one("name") or "").strip() or uploads.derive_name(filename)
        artifact_name = uploads.to_k8s_name(display_name)
        provided_md5 = (one("md5") or "").strip().lower() or None
        # A vendor .zip carries the trusted md5 inside it; ignore any typed md5.
        is_zip_name = filename.lower().endswith(".zip")
        if is_zip_name:
            provided_md5 = None

        if not filename:
            self._send_json({"ok": False, "error": "filename query param required"}, 400)
            return
        if not artifact_name:
            self._send_json({"ok": False, "error": "could not derive a valid image name"}, 400)
            return
        if provided_md5 and (len(provided_md5) != 32
                             or any(c not in "0123456789abcdef" for c in provided_md5)):
            self._send_json({"ok": False,
                             "error": "MD5 checksum must be a 32-character hex string"}, 400)
            return
        # Duplicate guard: the image name is the identity. Replace = delete first.
        if os.path.isdir(os.path.join(UPLOAD_DIR, artifact_name)):
            self._send_json({"ok": False,
                             "error": f"An image named '{display_name}' already exists. "
                                      f"Delete it first to replace it."}, 409)
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0
        if content_length <= 0:
            self._send_json({"ok": False, "error": "Content-Length required"}, 411)
            return

        max_bytes = int(CONFIG.get("maxUploadMiB", 4096)) * 1024 * 1024
        upload_dir = os.path.join(UPLOAD_DIR, artifact_name)
        dest = os.path.join(upload_dir, filename)

        try:
            written = uploads.stream_upload(
                self.rfile, content_length, dest, max_bytes)
        except uploads.UploadTooLarge as e:
            shutil.rmtree(upload_dir, ignore_errors=True)
            self._send_json({"ok": False, "error": f"upload too large: {e}"}, 413)
            return

        # Vendor zip: extract the .bin (that is what eda-asvr re-hosts) and read the
        # packaged md5; we host the bin, not the zip. The typed md5 was already cleared.
        from_zip = False
        if uploads.looks_like_zip(dest):
            from_zip = True
            try:
                bin_filename, provided_md5 = uploads.extract_image_from_zip(dest, upload_dir)
            except uploads.BadZip as e:
                shutil.rmtree(upload_dir, ignore_errors=True)
                self._send_json({"ok": False, "error": f"could not read the zip: {e}"}, 400)
                return
            filename = bin_filename
            dest = os.path.join(upload_dir, filename)
            written = os.path.getsize(dest)
        elif is_zip_name:
            shutil.rmtree(upload_dir, ignore_errors=True)
            self._send_json({"ok": False,
                             "error": "the file has a .zip name but is not a valid zip archive"}, 400)
            return

        md5_artifact_name = (artifact_name + "-md5") if provided_md5 else ""

        # No app-side md5 verification; eda-asvr validates against the supplied md5.
        # filePath = the clean image name (what eda-asvr hosts it as).
        uploads.finalize_upload(artifact_name, filename, provided_md5, repo, display_name,
                                namespace, written, artifact_name, display_name, md5_artifact_name)

        base_url = CONFIG.get("filePullBaseUrl") or artifact.default_base_url(POD_NAMESPACE)
        file_url, md5_url = artifact.file_urls(base_url, artifact_name, filename)

        try:
            artifact.create_artifact(namespace, artifact_name, repo, display_name,
                                     file_url, md5_url if provided_md5 else None)
        except urllib.error.HTTPError as e:
            if e.code == 409:
                shutil.rmtree(os.path.join(UPLOAD_DIR, artifact_name), ignore_errors=True)
                self._send_json({"ok": False,
                                 "error": f"An Artifact named '{artifact_name}' already "
                                          f"exists in {namespace}. Delete it first."}, 409)
                return
            detail = ""
            try:
                detail = e.read().decode("utf-8", errors="replace")[:300]
            except Exception:
                pass
            self._send_json({"ok": False, "uploadId": artifact_name,
                             "error": f"file stored but Artifact create failed "
                                      f"(HTTP {e.code}): {detail}"}, 502)
            return

        # When an md5 was supplied, also host it as its OWN Artifact so a NodeProfile
        # can reference it via imageMd5 (eda-asvr re-hosts the md5 file at its own path).
        if provided_md5:
            try:
                artifact.create_artifact(namespace, md5_artifact_name, repo,
                                         display_name + "-md5", md5_url, None)
            except urllib.error.HTTPError as e:
                logger.warning("md5 Artifact %s/%s create failed (HTTP %s); imageMd5 path "
                               "unavailable", namespace, md5_artifact_name, e.code)

        logger.info("Upload complete: %s (%d bytes, md5supplied=%s) -> Artifact %s/%s (name=%s)",
                    filename, written, bool(provided_md5), namespace, artifact_name, display_name)
        self._send_json({"ok": True, "uploadId": artifact_name, "artifactName": artifact_name,
                         "displayName": display_name, "namespace": namespace, "repo": repo,
                         "filePath": display_name, "md5": provided_md5 or "", "sizeBytes": written,
                         "fromZip": from_zip, "filename": filename})


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
        ns = m.get("namespace")
        st = status_by_key.get((ns, m.get("artifactName")), {})
        md5_name = m.get("md5ArtifactName")
        md5_st = status_by_key.get((ns, md5_name), {}) if md5_name else {}
        # NodeProfile paths are only valid once eda-asvr reports the file Available.
        image_path = (artifact.asvr_path(st.get("internalUrl", ""))
                      if st.get("downloadStatus") == "Available" else "")
        md5_path = (artifact.asvr_path(md5_st.get("internalUrl", ""))
                    if md5_st.get("downloadStatus") == "Available" else "")
        out.append({
            "uploadId": m.get("uploadId"),
            "name": m.get("artifactName"),
            "displayName": m.get("displayName") or m.get("artifactName"),
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
        })
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
