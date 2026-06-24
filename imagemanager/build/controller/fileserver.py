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
        meta = uploads.read_meta(upload_id) if upload_id else None
        namespace = namespace or (meta or {}).get("namespace")
        # Collect every Artifact this upload created: a group (SR OS) lists them in
        # meta.artifacts (+ yang); a single image is name + its optional md5 sidecar.
        names = []
        if meta and meta.get("artifacts"):
            names = [a.get("artifactName") for a in meta["artifacts"] if a.get("artifactName")]
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
        def one(name, default=None):
            v = q.get(name, [default])
            return v[0] if v else default

        # SR OS flows: a multi-file 7750 TiMOS zip (nostype=sros) creates several
        # Artifacts; an optional follow-up (part=yang) attaches the schema profile.
        part = (one("part") or "").strip().lower()
        if part == "yang":
            self._handle_yang_upload(q)
            return
        if (one("nostype") or "srl").strip().lower() == "sros":
            self._handle_sros_upload(q)
            return

        filename = uploads.sanitize_filename(one("filename", ""))
        # repo is a single fixed grouping (Artifact requires one); not user-facing.
        repo = (CONFIG.get("defaultRepo") or "images").strip()
        # No default namespace: the UI forces an explicit pick, so require one here too.
        namespace = (one("namespace") or "").strip()
        # The user-facing image name (e.g. "SRLinux-26.3.2"). Defaults to a name
        # derived from the filename; becomes the Artifact identity + served path.
        display_name = (one("name") or "").strip() or uploads.derive_name(filename)
        artifact_name = uploads.to_k8s_name(display_name)
        provided_md5 = (one("md5") or "").strip().lower() or None
        # If the user attached a YANG schema profile, a part=yang follow-up will
        # supply it; skip the auto-fetch so the uploaded one wins.
        yang_provided = (one("yangProvided") or "").lower() in ("1", "true", "yes")
        # A vendor .zip carries the trusted md5 inside it; ignore any typed md5.
        is_zip_name = filename.lower().endswith(".zip")
        if is_zip_name:
            provided_md5 = None

        if not filename:
            self._send_json({"ok": False, "error": "filename query param required"}, 400)
            return
        if not namespace:
            self._send_json({"ok": False, "error": "namespace query param required"}, 400)
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

        # YANG schema profile (best-effort, never aborts the image): a follow-up
        # upload (yang_provided) wins; otherwise auto-fetch from nokia-eda/schema-profiles.
        yang_created = False
        if not yang_provided:
            try:
                vm = _VER_RE.search(display_name)
                # the schema profile is per-release (X.Y.Z); drop any -<build> suffix
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

        logger.info("Upload complete: %s (%d bytes, md5supplied=%s, yang=%s) -> Artifact %s/%s (name=%s)",
                    filename, written, bool(provided_md5), yang_created, namespace, artifact_name, display_name)
        self._send_json({"ok": True, "uploadId": artifact_name, "artifactName": artifact_name,
                         "displayName": display_name, "namespace": namespace, "repo": repo,
                         "filePath": display_name, "md5": provided_md5 or "", "sizeBytes": written,
                         "fromZip": from_zip, "filename": filename,
                         "yangProvided": yang_provided, "yangCreated": yang_created})

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

    def _handle_sros_upload(self, q):
        def one(name, default=None):
            v = q.get(name, [default])
            return v[0] if v else default

        namespace = (one("namespace") or "").strip()
        yang_provided = (one("yangProvided") or "").lower() in ("1", "true", "yes")
        if not namespace:
            self._send_json({"ok": False, "error": "namespace query param required"}, 400)
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0
        if content_length <= 0:
            self._send_json({"ok": False, "error": "Content-Length required"}, 411)
            return
        max_bytes = int(CONFIG.get("maxUploadMiB", 4096)) * 1024 * 1024

        # The group name comes from the version INSIDE the zip, so stream to a
        # PER-REQUEST temp dir (concurrent SR OS uploads must not share one),
        # extract, then move into the version-named group dir. The temp dir is
        # always removed via finally.
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        tmp_dir = tempfile.mkdtemp(dir=UPLOAD_DIR, prefix=".sros-incoming-")
        try:
            tmp_zip = os.path.join(tmp_dir, "timos.zip")
            try:
                uploads.stream_upload(self.rfile, content_length, tmp_zip, max_bytes)
            except uploads.UploadTooLarge as e:
                self._send_json({"ok": False, "error": f"upload too large: {e}"}, 413)
                return
            if not uploads.looks_like_zip(tmp_zip):
                self._send_json({"ok": False,
                                 "error": "the SR OS upload must be the 7750 TiMOS .zip"}, 400)
                return
            try:
                version_disp, extracted = uploads.extract_sros_images(tmp_zip, tmp_dir)
            except uploads.BadZip as e:
                self._send_json({"ok": False, "error": f"not a 7750 SR OS image: {e}"}, 400)
                return

            version = version_disp.lower()                      # 26.3.r3
            group_id = uploads.to_k8s_name("sros-" + version)   # sros-26.3.r3
            display_name = "SROS-" + version_disp               # SROS-26.3.R3
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
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

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
            art_name = uploads.to_k8s_name(group_id + "-" + fn)
            file_url, _ = artifact.file_urls(base_url, group_id, fn)
            try:
                artifact.create_artifact(namespace, art_name, artifact.SROS_REPO,
                                         fn, file_url, None)
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
            except Exception as e:  # noqa: BLE001 - URLError/timeout/etc: roll back, never orphan
                rollback()
                self._send_json({"ok": False,
                                 "error": f"Artifact {art_name} create failed: {e}"}, 502)
                return
            created.append((namespace, art_name))
            art_records.append({"artifactName": art_name, "filename": fn, "filePath": fn})

        # YANG schema profile is BEST-EFFORT and must never abort the (already
        # created) image artifacts: a follow-up upload (yang_provided) takes
        # priority; otherwise auto-fetch from nokia-eda/schema-profiles.
        yang_meta = None
        try:
            if yang_provided:
                note = "Awaiting YANG schema profile upload."
            else:
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
                            f"{version} (not published and no 7x50 tag); upload one to complete onboarding.")
        except Exception as e:  # noqa: BLE001 - YANG is best-effort; keep the image artifacts
            logger.warning("YANG handling failed for %s: %s", group_id, e)
            yang_meta = None
            note = "Image artifacts created; the YANG step failed and can be retried by uploading it."

        uploads.finalize_group(group_id, display_name, "sros", namespace, artifact.SROS_REPO,
                               art_records, yang_meta, total, version)
        logger.info("SR OS upload complete: %s (%d files, %d bytes) -> %d Artifact(s) in %s/%s "
                    "(yang=%s, provided=%s)", display_name, len(extracted), total, len(created),
                    namespace, artifact.SROS_REPO, bool(yang_meta), yang_provided)
        self._send_json({"ok": True, "uploadId": group_id, "artifactName": group_id,
                         "displayName": display_name, "namespace": namespace,
                         "repo": artifact.SROS_REPO, "nos": "sros", "version": version,
                         "fileCount": len(extracted), "sizeBytes": total,
                         "yangProvided": yang_provided, "yangCreated": bool(yang_meta),
                         "note": note})

    def _handle_yang_upload(self, q):
        """Attach a user-uploaded YANG schema profile to an existing image (SR OS
        group OR SR Linux). The Artifact is named per NOS so it never clashes with
        the image Artifact."""
        def one(name, default=None):
            v = q.get(name, [default])
            return v[0] if v else default

        namespace = (one("namespace") or "").strip()
        upload_id = uploads.to_k8s_name(one("name") or "")
        meta = uploads.read_meta(upload_id) if upload_id else None
        if not meta:
            self._send_json({"ok": False, "error": "unknown image for YANG upload"}, 404)
            return
        nos = meta.get("nos") or "srl"
        namespace = namespace or meta.get("namespace")
        version = meta.get("version") or ""
        if not version:
            mm = _VER_RE.search(meta.get("displayName") or upload_id)
            version = mm.group(1) if mm else ""
        if not version:
            self._send_json({"ok": False, "error": "could not determine the image version"}, 400)
            return
        up_dir = os.path.join(UPLOAD_DIR, upload_id)
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0
        if content_length <= 0:
            self._send_json({"ok": False, "error": "Content-Length required"}, 411)
            return
        max_bytes = int(CONFIG.get("maxUploadMiB", 4096)) * 1024 * 1024
        yfn = schemaprofile.schema_profile_filename(nos, version)   # sros-/srlinux-<ver>.zip
        dest = os.path.join(up_dir, yfn)
        try:
            uploads.stream_upload(self.rfile, content_length, dest, max_bytes)
        except uploads.UploadTooLarge as e:
            try:
                os.remove(dest)
            except OSError:
                pass
            self._send_json({"ok": False, "error": f"upload too large: {e}"}, 413)
            return
        if not uploads.looks_like_zip(dest):
            try:
                os.remove(dest)
            except OSError:
                pass
            self._send_json({"ok": False,
                             "error": "the YANG schema profile must be a .zip archive"}, 400)
            return

        base_url = CONFIG.get("filePullBaseUrl") or artifact.default_base_url(POD_NAMESPACE)
        yname = upload_id if nos == "sros" else (upload_id + "-yang")
        old = meta.get("yang") or {}
        if old.get("artifactName"):
            try:
                artifact.delete_artifact(namespace, old["artifactName"])
            except Exception:  # noqa: BLE001
                pass
        ok, yang_meta = self._create_yang_artifact(namespace, upload_id, yname, yfn, base_url)
        if not ok:
            self._send_json({"ok": False, "error": "YANG schema-profile Artifact create failed"}, 502)
            return
        meta["yang"] = yang_meta
        meta["sizeBytes"] = uploads.upload_dir_size(upload_id)
        uploads.rewrite_meta(upload_id, meta)
        logger.info("YANG schema profile attached to %s/%s (nos=%s)", namespace, upload_id, nos)
        self._send_json({"ok": True, "uploadId": upload_id, "yangCreated": True,
                         "displayName": meta.get("displayName") or upload_id})


_VER_RE = re.compile(r"(\d+\.\d+\.[A-Za-z]?\d+(?:-\d+)?)")


def _nodeprofile_yaml(nos, version, namespace, prof_name, image_paths, md5_path, yang_url):
    """A complete, copy-ready NodeProfile example for an Available image. The
    image path(s), version, operatingSystem and yang are filled from the real
    artifact(s); environment-specific fields are left as <placeholders>. Mirrors
    the reference NodeProfile shape (SR Linux single image+imageMd5; SR OS the
    full boot-file set + yang)."""
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
    for i, p in enumerate(image_paths):
        L.append(f"  - image: {p}")
        if md5_path and i == 0:
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
                                    [image_path], md5_path, yang_url)
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
    statuses, image_lines, image_paths, reasons = [], [], [], []
    all_images_available = bool(arts)
    for a in arts:
        st = status_by_key.get((ns, a.get("artifactName")), {})
        ds = st.get("downloadStatus", "NoArtifact" if not st else "")
        statuses.append(ds)
        if ds == "Available":
            p = artifact.asvr_path(st.get("internalUrl", ""))
            if p:
                image_lines.append("  - image: " + p)
                image_paths.append(p)
            else:
                all_images_available = False
        else:
            all_images_available = False
        if st.get("statusReason"):
            reasons.append((a.get("filename") or "") + ": " + st["statusReason"])

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
                                    image_paths, None, yang_url)
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
        if m.get("artifacts"):
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
