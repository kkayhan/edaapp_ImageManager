"""
Upload handling (stdlib only).

The browser streams the file as the RAW request body (not multipart), so
arbitrarily large NOS images (1.5 GB+) are written straight to the PVC in
fixed-size chunks without ever being buffered whole in memory. Per-upload
metadata travels as query parameters.

Two upload shapes are accepted:
  * a raw NOS image (.bin) -- the user may optionally type the vendor's md5;
  * a vendor zip (e.g. Nokia-7220_IXR_SR_Linux-<hw>-26.3.2.zip) that contains
    the .bin AND its .md5. For a zip we extract the .bin (that is what eda-asvr
    re-hosts) and read the md5 from inside the zip; any user-typed md5 is
    ignored, because the md5 packaged with the image is the trusted one.

The app never computes/verifies md5 itself: the md5 (typed or from the zip) is
written to a sidecar file that eda-asvr downloads and validates the image against.

On-disk layout (the PVC is the source of truth for uploaded bytes):
    /data/uploads/<uploadId>/<filename>        the binary (.bin)
    /data/uploads/<uploadId>/<filename>.md5    text file: md5 (only if known)
    /data/uploads/<uploadId>/meta.json         {uploadId, filename, md5, repo,
                                                 filePath, namespace,
                                                 artifactName, sizeBytes,
                                                 storedAt}
"""

import json
import logging
import os
import re
import shutil
import zipfile
from datetime import datetime, timezone

logger = logging.getLogger("uploads")

DATA_DIR = "/data/uploads"
_CHUNK = 1024 * 1024  # 1 MiB
# Recognize Nokia SR Linux image filenames (e.g.
# "Nokia-7220_IXR_SR_Linux-<hw>-26.3.2.zip") and a semantic version in them.
_SRLINUX_RE = re.compile(r"sr[ _-]?linux", re.I)
_VERSION_RE = re.compile(r"(\d+\.\d+\.\d+(?:-\d+)?)")

# ----------------------------- SR OS (7750 TiMOS) -----------------------------
# A 7750 SR OS vendor zip unpacks to cflash/TiMOS-SR-<ver>/{both.tim,cpm.tim,...}.
# EDA's NodeProfile.spec.images[] references each of these boot files as its OWN
# Artifact (repo srosimages), so one upload -> several Artifacts. We extract the
# canonical boot set; the combined both.tim plus the role images (cpm/iom) cover
# both integrated and distributed 7750 chassis. SR OS images carry no per-file
# md5 in the zip (only signatures.txt), and the reference NodeProfiles omit
# imageMd5, so we host the files without an md5 sidecar.
SROS_TIM_FILES = ["boot.ldr", "both.tim", "cpm.tim", "iom.tim", "kernel.tim", "support.tim"]
# e.g. "cflash/TiMOS-SR-26.3.R3/both.tim" -> 26.3.R3
_SROS_DIR_RE = re.compile(r"TiMOS-[A-Za-z]+-(\d+\.\d+\.[Rr]\d+)")


class UploadTooLarge(Exception):
    pass


def sanitize_filename(name):
    """Reduce to a safe basename: strip any path, keep a conservative charset."""
    base = os.path.basename((name or "").strip().replace("\\", "/"))
    base = base.split("/")[-1]
    base = re.sub(r"[^A-Za-z0-9._-]", "_", base)
    base = base.strip("._-") or "upload.bin"
    return base[:200]


def derive_name(filename):
    """Suggest a clean image name from an upload filename.
    Nokia SR Linux images -> 'SRLinux-<version>' (e.g. SRLinux-26.3.2);
    otherwise the filename with its extension stripped."""
    base = os.path.basename((filename or "").replace("\\", "/").strip())
    stem = re.sub(r"\.[A-Za-z0-9]+$", "", base)
    if _SRLINUX_RE.search(base):
        m = _VERSION_RE.search(base)
        if m:
            return "SRLinux-" + m.group(1)
    return stem or "image"


def to_k8s_name(name):
    """Reduce a display name to a DNS-1123-subdomain Artifact name (lowercase)."""
    s = re.sub(r"[^a-z0-9.-]", "-", (name or "").strip().lower())
    s = re.sub(r"-{2,}", "-", s).strip("-.")
    return s[:253].strip("-.")


class BadZip(Exception):
    pass


_ZIP_MAGIC = b"PK\x03\x04"
_MD5_IN_TEXT = re.compile(r"\b([0-9a-fA-F]{32})\b")


def looks_like_zip(path):
    """True if the stored file begins with the local-file-header zip magic."""
    try:
        with open(path, "rb") as f:
            return f.read(4) == _ZIP_MAGIC
    except OSError:
        return False


def parse_md5_text(text):
    """Pull a 32-hex md5 out of a checksum file's contents (handles
    'md5sum  filename' and bare-hash forms). Returns lowercase hash or None."""
    m = _MD5_IN_TEXT.search(text or "")
    return m.group(1).lower() if m else None


def extract_image_from_zip(zip_path, dest_dir):
    """Extract the NOS image (.bin) and its md5 from a vendor zip.

    Streams the .bin out member-by-member (never buffers it whole), reads the
    md5 from the packaged checksum file, then removes the zip. Member names are
    reduced to a safe basename (no zip-slip). Returns (bin_filename, md5_or_None).
    Raises BadZip if the archive is unreadable or has no .bin image.
    """
    try:
        zf = zipfile.ZipFile(zip_path)
    except (zipfile.BadZipFile, OSError) as e:
        raise BadZip("not a readable zip archive (%s)" % e)
    with zf:
        members = [m for m in zf.infolist() if not m.is_dir()]
        bins = [m for m in members
                if os.path.basename(m.filename).lower().endswith(".bin")]
        if not bins:
            raise BadZip("the zip does not contain a .bin image")
        bin_m = max(bins, key=lambda m: m.file_size)  # the NOS image is the big one
        bin_filename = sanitize_filename(os.path.basename(bin_m.filename))
        out_path = os.path.join(dest_dir, bin_filename)
        with zf.open(bin_m, "r") as src, open(out_path, "wb") as out:
            shutil.copyfileobj(src, out, _CHUNK)
        md5 = None
        md5_members = [m for m in members
                       if os.path.basename(m.filename).lower().endswith((".md5", ".md5sum"))]
        for m in md5_members:
            try:
                md5 = parse_md5_text(zf.read(m).decode("utf-8", "replace"))
            except Exception:
                md5 = None
            if md5:
                break
    try:
        os.remove(zip_path)
    except OSError:
        pass
    logger.info("Extracted %s from zip (md5 %s)", bin_filename, "present" if md5 else "absent")
    return bin_filename, md5


def detect_sros_version(member_names):
    """Return the SR OS version string (e.g. '26.3.R3') discovered in a TiMOS
    zip's member paths (the cflash/TiMOS-SR-<ver>/ directory), or None."""
    for n in member_names:
        m = _SROS_DIR_RE.search(n or "")
        if m:
            return m.group(1)
    return None


def extract_sros_images(zip_path, dest_dir):
    """Extract the SR OS boot image set from a 7750 TiMOS vendor zip.

    Streams each target file (both.tim, cpm.tim, iom.tim, kernel.tim,
    support.tim, boot.ldr) out of the cflash/TiMOS-SR-<ver>/ directory, then
    removes the zip. Returns (version_display, [{'filename':.., 'size':..}, ..]).
    Raises BadZip if the archive is unreadable or is not a 7750 TiMOS image.
    """
    try:
        zf = zipfile.ZipFile(zip_path)
    except (zipfile.BadZipFile, OSError) as e:
        raise BadZip("not a readable zip archive (%s)" % e)
    extracted = []
    with zf:
        members = [m for m in zf.infolist() if not m.is_dir()]
        version = detect_sros_version([m.filename for m in members])
        if not version:
            raise BadZip("not an SR OS TiMOS image (no TiMOS-SR-<version>/ directory)")
        # Pin to the canonical image directory so we don't pick up the duplicate
        # boot.ldr that also sits at the cflash/ root.
        verdir = None
        for m in members:
            mm = _SROS_DIR_RE.search(m.filename)
            if mm and mm.group(1) == version:
                end = m.filename.find(mm.group(0)) + len(mm.group(0))
                verdir = m.filename[:end] + "/"
                break
        wanted = set(SROS_TIM_FILES)
        by_base = {}
        for m in members:
            if verdir and not m.filename.startswith(verdir):
                continue
            base = os.path.basename(m.filename)
            if base in wanted and (base not in by_base or m.file_size > by_base[base].file_size):
                by_base[base] = m
        if "both.tim" not in by_base:
            raise BadZip("not a 7750 SR OS image (both.tim not found)")
        for base in SROS_TIM_FILES:
            m = by_base.get(base)
            if not m:
                continue
            safe = sanitize_filename(base)
            out_path = os.path.join(dest_dir, safe)
            with zf.open(m, "r") as src, open(out_path, "wb") as out:
                shutil.copyfileobj(src, out, _CHUNK)
            extracted.append({"filename": safe, "size": m.file_size})
    try:
        os.remove(zip_path)
    except OSError:
        pass
    logger.info("Extracted %d SR OS image file(s) for version %s", len(extracted), version)
    return version, extracted


def stream_upload(rfile, content_length, dest_path, max_bytes):
    """
    Stream `content_length` bytes from rfile into dest_path in fixed-size chunks
    (no hashing). Raises UploadTooLarge if the declared or actual size exceeds
    max_bytes. Returns bytes_written.
    """
    if max_bytes and content_length and content_length > max_bytes:
        raise UploadTooLarge(f"declared size {content_length} exceeds limit {max_bytes}")

    written = 0
    remaining = content_length
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "wb") as out:
        while remaining > 0:
            chunk = rfile.read(min(_CHUNK, remaining))
            if not chunk:
                break
            out.write(chunk)
            written += len(chunk)
            remaining -= len(chunk)
            if max_bytes and written > max_bytes:
                raise UploadTooLarge(f"upload exceeded limit {max_bytes}")
    return written


def finalize_upload(upload_id, filename, md5, repo, file_path, namespace,
                    size_bytes, artifact_name, display_name, md5_artifact_name=""):
    """Write meta.json (and a .md5 sidecar only if the user supplied a checksum)."""
    d = os.path.join(DATA_DIR, upload_id)
    if md5:
        with open(os.path.join(d, filename + ".md5"), "w") as f:
            f.write(md5 + "\n")
    meta = {
        "uploadId": upload_id,
        "filename": filename,
        "displayName": display_name,
        "md5": md5 or "",
        "md5ArtifactName": md5_artifact_name,
        "repo": repo,
        "filePath": file_path,
        "namespace": namespace,
        "artifactName": artifact_name,
        "sizeBytes": size_bytes,
        "storedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    tmp = os.path.join(d, "meta.json.tmp")
    with open(tmp, "w") as f:
        json.dump(meta, f)
    os.replace(tmp, os.path.join(d, "meta.json"))
    return meta


def rewrite_meta(group_id, meta):
    """Atomically (re)write meta.json for an upload from a full dict."""
    d = os.path.join(DATA_DIR, group_id)
    tmp = os.path.join(d, "meta.json.tmp")
    with open(tmp, "w") as f:
        json.dump(meta, f)
    os.replace(tmp, os.path.join(d, "meta.json"))
    return meta


def finalize_group(group_id, display_name, nos, namespace, repo,
                   artifacts, yang, size_bytes, version):
    """Write meta.json for a multi-file image group (one upload -> many Artifacts,
    e.g. SR OS). `artifacts` = [{artifactName, filename, filePath}, ...]; `yang`
    = {artifactName, filename, filePath, repo} or None."""
    meta = {
        "uploadId": group_id,
        "displayName": display_name,
        "nos": nos,
        "namespace": namespace,
        "repo": repo,
        "version": version,
        "artifacts": artifacts,
        "yang": yang or None,
        "sizeBytes": size_bytes,
        "storedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    return rewrite_meta(group_id, meta)


def delete_upload(upload_id):
    """Remove an upload's directory from the PVC. Returns True if it existed."""
    if not upload_id or "/" in upload_id or "\\" in upload_id or ".." in upload_id:
        return False
    d = os.path.join(DATA_DIR, upload_id)
    if os.path.isdir(d):
        shutil.rmtree(d, ignore_errors=True)
        return True
    return False


def read_meta(upload_id):
    try:
        with open(os.path.join(DATA_DIR, upload_id, "meta.json")) as f:
            return json.load(f)
    except (FileNotFoundError, ValueError):
        return None


def list_meta():
    """Return meta.json dicts for every stored upload (skips half-written ones)."""
    out = []
    try:
        for uid in sorted(os.listdir(DATA_DIR)):
            if not os.path.isdir(os.path.join(DATA_DIR, uid)):
                continue
            m = read_meta(uid)
            if m:
                out.append(m)
    except FileNotFoundError:
        pass
    return out


def upload_dir_size(upload_id):
    total = 0
    d = os.path.join(DATA_DIR, upload_id)
    try:
        for name in os.listdir(d):
            fp = os.path.join(d, name)
            if os.path.isfile(fp):
                total += os.path.getsize(fp)
    except FileNotFoundError:
        pass
    return total


def storage_stats():
    """(count_of_uploads, total_bytes) across the upload tree."""
    metas = list_meta()
    total = 0
    try:
        for uid in os.listdir(DATA_DIR):
            if os.path.isdir(os.path.join(DATA_DIR, uid)):
                total += upload_dir_size(uid)
    except FileNotFoundError:
        pass
    return len(metas), total
