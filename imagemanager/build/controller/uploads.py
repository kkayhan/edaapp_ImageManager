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

import hashlib
import json
import logging
import lzma
import os
import re
import shutil
import tarfile
import zipfile
from datetime import datetime, timezone

logger = logging.getLogger("uploads")

DATA_DIR = "/data/uploads"
_CHUNK = 1024 * 1024  # 1 MiB
# A fast upload (e.g. 20 MB/s) to slower backing storage (CephFS) piles up dirty
# pages in the kernel page cache, which cgroup v2 charges to the container's
# memory limit -> OOMKill mid-upload (502 at the proxy). Periodically force the
# written bytes to disk and drop them from the page cache so the container's
# memory stays flat regardless of upload speed or how many uploads run at once.
_FADV_EVERY = 32 * 1024 * 1024  # 32 MiB


def _trim_write_cache(fileobj):
    """Best-effort: flush + fsync `fileobj`, then evict its pages from the page
    cache (POSIX_FADV_DONTNEED). Keeps cgroup-charged page cache from growing
    while writing a large file. No-op where fadvise is unavailable."""
    try:
        fileobj.flush()
        os.fsync(fileobj.fileno())
        if hasattr(os, "posix_fadvise") and hasattr(os, "POSIX_FADV_DONTNEED"):
            os.posix_fadvise(fileobj.fileno(), 0, 0, os.POSIX_FADV_DONTNEED)
    except OSError:
        pass


def _copy_streaming(src, dst, hasher=None):
    """Copy src -> dst in _CHUNK blocks, trimming the write cache every
    _FADV_EVERY bytes (and once at the end) so a large copy stays memory-flat.
    If `hasher` is given (e.g. hashlib.sha256()), it is updated with every byte
    written, so the caller can verify content integrity without a second read."""
    since = 0
    total = 0
    while True:
        buf = src.read(_CHUNK)
        if not buf:
            break
        dst.write(buf)
        if hasher is not None:
            hasher.update(buf)
        total += len(buf)
        since += len(buf)
        if since >= _FADV_EVERY:
            _trim_write_cache(dst)
            since = 0
    _trim_write_cache(dst)
    return total


# Recognize Nokia SR Linux image filenames (e.g.
# "Nokia-7220_IXR_SR_Linux-<hw>-26.3.2.zip") and a semantic version in them.
_SRLINUX_RE = re.compile(r"sr[ _-]?linux", re.I)
_SRSIM_NAME_RE = re.compile(r"sr[ _-]?sim", re.I)  # e.g. "Nokia-SR-SIM-26.3.R3.zip"
_VERSION_RE = re.compile(r"(\d+\.\d+\.\d+(?:-\d+)?)")
_SROS_VER_RE = re.compile(r"(\d+\.\d+\.[Rr]\d+)")  # SR OS style, e.g. 26.3.R3

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

# ----------------------------- SR-SIM (SR OS simulator) -----------------------------
# A Nokia SR-SIM vendor zip (Nokia-SR-SIM-<ver>.zip) unpacks to
# vm/SR-Simulator/srsim.tar.xz -- an OCI/docker-save CONTAINER image archive
# (RepoTags localhost/nokia/srsim:<ver>), NOT a node-bootable file. EDA's Digital
# Twin (eda-cx) runs this image as the simulator pod, pulling it BY TAG from a
# registry the node can reach. So we do NOT hand it to eda-asvr; instead we unpack
# the OCI layout onto the PVC and serve it from our own read-only OCI /v2 endpoint
# (see fileserver._serve_registry_v2), and emit a NodeProfile with containerImage.
_SRSIM_MEMBER = "srsim.tar.xz"
# tag in the archive, e.g. localhost/nokia/srsim:26.3.R3 -> 26.3.R3
_SRSIM_TAG_RE = re.compile(r":([A-Za-z0-9._-]+)$")


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
    """Suggest a clean image name from an upload filename. Always lowercase, so
    the Artifact name, served filePath and NodeProfile name are uniformly small
    letters. Nokia SR Linux images -> 'srlinux-<version>' (e.g. srlinux-26.3.2);
    otherwise the filename with its extension stripped (lowercased)."""
    base = os.path.basename((filename or "").replace("\\", "/").strip())
    stem = re.sub(r"\.[A-Za-z0-9]+$", "", base)
    if _SRSIM_NAME_RE.search(base):   # SR-SIM (container image) -> distinct from HW SR OS
        m = _SROS_VER_RE.search(base) or _VERSION_RE.search(base)
        if m:
            return ("srsim-" + m.group(1)).lower()
    if _SRLINUX_RE.search(base):
        m = _VERSION_RE.search(base)
        if m:
            return "srlinux-" + m.group(1)
    return (stem or "image").lower()


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


_MD5SUMS_LINE = re.compile(r"^([0-9a-fA-F]{32})\s+\*?(.+?)\s*$")


def _norm_md5_path(p):
    """Normalize a md5sums path so it aligns with zip member paths: drop a leading
    './' and a leading 'cflash/' (md5sums.txt lists paths relative to cflash/,
    while zip members carry the cflash/ prefix)."""
    p = (p or "").strip().lstrip("/")
    if p.startswith("./"):
        p = p[2:]
    if p.startswith("cflash/"):
        p = p[len("cflash/"):]
    return p


def parse_md5sums(text):
    """Parse a coreutils md5sums file ('<md5>  <path>' per line) into
    ({normalized_path: md5}, {basename: md5}). The path map is preferred so the
    versioned TiMOS-SR-<ver>/<file> md5 wins over the cflash-root duplicate;
    basename is a fallback for zips that list bare names."""
    by_path, by_base = {}, {}
    for line in (text or "").splitlines():
        m = _MD5SUMS_LINE.match(line.strip())
        if not m:
            continue
        md5 = m.group(1).lower()
        path = _norm_md5_path(m.group(2))
        by_path[path] = md5
        by_base.setdefault(os.path.basename(path), md5)
    return by_path, by_base


def _srsim_member(names):
    """Return the srsim container-image archive member name in a zip, or None.
    Matches basename 'srsim.tar.xz' (the SR-SIM vendor layout puts it under
    vm/SR-Simulator/)."""
    for n in names:
        if os.path.basename(n).lower() == _SRSIM_MEMBER:
            return n
    return None


def detect_nos_from_zip(zip_path):
    """Classify a vendor zip by its contents: 'srsim' (an SR OS *simulator*
    container image, vm/SR-Simulator/srsim.tar.xz), 'sros' (a 7750 TiMOS boot set
    under cflash/TiMOS-<x>-<ver>/), 'srl' (an SR Linux .bin), or None.
    SR-SIM is checked first: it is a container image, not an asvr file artifact.
    The TiMOS rules require a cflash/ ancestor so a stray .bin zip can't misfire."""
    try:
        zf = zipfile.ZipFile(zip_path)
    except (zipfile.BadZipFile, OSError):
        return None
    with zf:
        names = [m.filename for m in zf.infolist() if not m.is_dir()]
    if _srsim_member(names):
        return "srsim"
    if any("cflash/" in n and _SROS_DIR_RE.search(n) and os.path.basename(n) == "both.tim"
           for n in names):
        return "sros"
    if any(os.path.basename(n).lower().endswith(".bin") for n in names):
        return "srl"
    if any("cflash/" in n and _SROS_DIR_RE.search(n) for n in names):  # TiMOS dir, no both.tim
        return "sros"
    return None


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
            _copy_streaming(src, out)
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
        # per-file md5 from the packaged md5sums.txt, if present. Look up by the
        # member's versioned path (not basename) so the served versioned boot.ldr
        # gets ITS md5, never the cflash-root duplicate's.
        md5_by_path, md5_by_base = {}, {}
        for m in members:
            if os.path.basename(m.filename).lower() == "md5sums.txt":
                try:
                    md5_by_path, md5_by_base = parse_md5sums(zf.read(m).decode("utf-8", "replace"))
                except Exception:  # noqa: BLE001
                    md5_by_path, md5_by_base = {}, {}
                break
        for base in SROS_TIM_FILES:
            m = by_base.get(base)
            if not m:
                continue
            safe = sanitize_filename(base)
            out_path = os.path.join(dest_dir, safe)
            with zf.open(m, "r") as src, open(out_path, "wb") as out:
                _copy_streaming(src, out)
            md5 = md5_by_path.get(_norm_md5_path(m.filename)) or md5_by_base.get(base)
            extracted.append({"filename": safe, "size": m.file_size, "md5": md5})
    try:
        os.remove(zip_path)
    except OSError:
        pass
    n_md5 = sum(1 for e in extracted if e.get("md5"))
    logger.info("Extracted %d SR OS image file(s) for version %s (%d with md5)",
                len(extracted), version, n_md5)
    return version, extracted


# ----------------------------- SR-SIM (container image) -----------------------------
# An extracted OCI layout has these top-level files plus blobs/sha256/<digest>.
_OCI_ALLOWED_TOP = {"index.json", "manifest.json", "oci-layout", "repositories"}
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")


def extract_srsim_image(zip_path, dest_dir):
    """Unpack the SR-SIM container image (vm/SR-Simulator/srsim.tar.xz) from a
    vendor zip into an OCI layout under dest_dir, so our /v2 endpoint can serve it.

    srsim.tar.xz is an OCI/docker-save archive (blobs/sha256/*, index.json,
    manifest.json, oci-layout, repositories). We stream-decompress it (lzma) and
    stream-extract each member (the layer blob is ~2 GB) with the same
    fsync+fadvise discipline used elsewhere, so the pod stays memory-flat. Each
    blob is hashed as it is written and checked against its sha256 filename, for
    end-to-end integrity. Member paths are constrained to blobs/sha256/<hex> and a
    small allow-list of top-level files (no path traversal).

    Returns the _parse_oci_layout dict augmented with sizeBytes + blobCount.
    Raises BadZip on any structural / integrity problem.
    """
    try:
        zf = zipfile.ZipFile(zip_path)
    except (zipfile.BadZipFile, OSError) as e:
        raise BadZip("not a readable zip archive (%s)" % e)
    blobs_dir = os.path.join(dest_dir, "blobs", "sha256")
    os.makedirs(blobs_dir, exist_ok=True)
    total = 0
    blob_count = 0
    with zf:
        names = [m.filename for m in zf.infolist() if not m.is_dir()]
        member = _srsim_member(names)
        if not member:
            raise BadZip("no srsim.tar.xz container image found in the zip")
        info = zf.getinfo(member)
        # Decompress + read errors (a corrupt or truncated .tar.xz -- e.g. a cut
        # connection mid-upload of the ~2 GB layer) surface as LZMAError/EOFError/
        # OSError/TarError; convert them all to BadZip so the caller cleans up and
        # returns a 400, never a partial OCI layout + cryptic 500.
        try:
            with zf.open(info, "r") as zsrc, lzma.open(zsrc, "rb") as xz:
                with tarfile.open(fileobj=xz, mode="r|") as tar:
                    for m in tar:
                        if not m.isfile():
                            continue
                        rel = m.name.lstrip("./")
                        base = os.path.basename(rel)
                        parent = os.path.dirname(rel).replace("\\", "/")
                        src = tar.extractfile(m)
                        if src is None:
                            continue
                        if parent == "blobs/sha256":
                            if not _SHA256_HEX.match(base):
                                continue  # ignore stray non-digest blobs
                            out_path = os.path.join(blobs_dir, base)
                            h = hashlib.sha256()
                            with src, open(out_path, "wb") as out:
                                total += _copy_streaming(src, out, hasher=h)
                            if h.hexdigest() != base:
                                raise BadZip("blob %s… failed sha256 integrity check" % base[:16])
                            blob_count += 1
                        elif rel in _OCI_ALLOWED_TOP:
                            with src, open(os.path.join(dest_dir, base), "wb") as out:
                                total += _copy_streaming(src, out)
                        else:
                            src.close()  # ignore anything else (no path traversal)
        except BadZip:
            raise
        except (lzma.LZMAError, EOFError, OSError, tarfile.TarError) as e:
            raise BadZip("could not decompress/read srsim.tar.xz (%s)" % e)
    try:
        os.remove(zip_path)
    except OSError:
        pass
    if blob_count == 0:
        raise BadZip("the srsim image archive contained no blobs")
    info_d = _parse_oci_layout(dest_dir)
    # Fail closed on a structurally incomplete image (would 404 later at the node
    # pull): the manifest blob the index points at must be present, and the
    # manifest must list a config + at least one layer.
    mh = (info_d.get("manifestDigest") or "").split(":")[-1]
    if not (mh and os.path.isfile(os.path.join(blobs_dir, mh))):
        raise BadZip("the image manifest blob is missing from the archive")
    if not info_d.get("configDigest") or not info_d.get("layerDigests"):
        raise BadZip("the image manifest lists no config/layers (incomplete image)")
    info_d["sizeBytes"] = total
    info_d["blobCount"] = blob_count
    logger.info("Extracted SR-SIM image %s (%d blobs, %d bytes, tag %s)",
                (info_d.get("manifestDigest") or "?")[:19], blob_count, total, info_d.get("tag"))
    return info_d


def _parse_oci_layout(dest_dir):
    """Read index.json (with manifest.json as a fallback) from an extracted OCI
    layout to find the image manifest digest, its mediaType and the tag. Returns
    {tag, version, manifestDigest, manifestMediaType, configDigest, layerDigests,
    repoTag}. Raises BadZip if the layout is unusable."""
    idx_path = os.path.join(dest_dir, "index.json")
    try:
        with open(idx_path) as f:
            idx = json.load(f)
    except (OSError, ValueError) as e:
        raise BadZip("missing/invalid index.json in the image (%s)" % e)
    manifests = idx.get("manifests") or []
    if not manifests:
        raise BadZip("the image index lists no manifests")
    md = manifests[0]
    manifest_digest = md.get("digest") or ""
    manifest_mt = md.get("mediaType") or "application/vnd.oci.image.manifest.v1+json"
    tag = (md.get("annotations") or {}).get("org.opencontainers.image.ref.name") or ""
    repo_tag = ""
    try:
        with open(os.path.join(dest_dir, "manifest.json")) as f:
            mj = json.load(f)
        if isinstance(mj, list) and mj:
            rts = mj[0].get("RepoTags") or []
            if rts:
                repo_tag = rts[0]
                if not tag:
                    mt = _SRSIM_TAG_RE.search(repo_tag)
                    tag = mt.group(1) if mt else ""
    except (OSError, ValueError):
        pass
    if not manifest_digest or not tag:
        raise BadZip("could not determine the image manifest digest / tag")
    config_digest, layer_digests = "", []
    try:
        h = manifest_digest.split(":", 1)[1]
        with open(os.path.join(dest_dir, "blobs", "sha256", h)) as f:
            man = json.load(f)
        config_digest = (man.get("config") or {}).get("digest", "")
        layer_digests = [ly.get("digest", "") for ly in (man.get("layers") or [])]
    except (OSError, ValueError, IndexError):
        pass
    return {"tag": tag, "version": tag.lower(), "manifestDigest": manifest_digest,
            "manifestMediaType": manifest_mt, "configDigest": config_digest,
            "layerDigests": layer_digests, "repoTag": repo_tag}


def finalize_srsim(artifact_name, display_name, namespace, oci, yang=None):
    """Write meta.json for an SR-SIM container-image upload (nos='srsim'). The
    image is served from our own /v2 endpoint (no eda-asvr Artifact); `oci` is the
    dict from extract_srsim_image; `yang` optionally records a schema-profile
    Artifact when one was resolved."""
    meta = {
        "uploadId": artifact_name,
        "artifactName": artifact_name,
        "displayName": display_name,
        "nos": "srsim",
        "namespace": namespace,
        "version": oci.get("version"),
        "imageTag": oci.get("tag"),
        "manifestDigest": oci.get("manifestDigest"),
        "manifestMediaType": oci.get("manifestMediaType"),
        "sizeBytes": oci.get("sizeBytes"),
        "yang": yang or None,
        "storedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    return rewrite_meta(artifact_name, meta)


def srsim_meta(artifact_name):
    """Return (meta, blobs_dir) for an extracted SR-SIM image if `artifact_name`
    names one on the PVC, else (None, None). Used by the /v2 registry endpoint."""
    if not artifact_name or "/" in artifact_name or "\\" in artifact_name or ".." in artifact_name:
        return None, None
    m = read_meta(artifact_name)
    if not m or m.get("nos") != "srsim":
        return None, None
    return m, os.path.join(DATA_DIR, artifact_name, "blobs", "sha256")


# ----------------------------- License (key) handling -----------------------------
# A NOS license is a small text key file (one or more lines of
# "<node-uuid> <base64-key>", '#' comments allowed). EDA models it as a ConfigMap
# with a single key "license.key" that NodeProfile/SimNode/TopoNode reference; the
# Digital Twin (eda-cx) feeds that value to the simulator. (A sim boots on an
# empty license; a real key unlocks licensed scale/features.) The license ConfigMap
# lives in eda-system -- where all of EDA's own license ConfigMaps live and where
# eda-cx resolves it -- regardless of the image's artifact namespace.
LICENSE_KEY = "license.key"
_LICENSE_MAX = 256 * 1024  # a key file is < 2 KiB; cap well above any real one
# The vendor labels each key with an inline "# ..." comment naming the product /
# version family: SR Linux -> "# SRL_26_3_*", SR OS -> "# NOKIA BELL NV(*)".
_LIC_SRL_RE = re.compile(r"\bSRL[ _-]?\d", re.I)
_LIC_SROS_RE = re.compile(r"NOKIA\s+BELL|\bTiMOS\b", re.I)
# A license entry = a node-id UUID then whitespace then the base64 key. This is
# the anchor used to pull the real key out of pasted text that may carry a label
# prefix ("license: ..."), surrounding quotes, or stray leading/trailing lines.
_LIC_ENTRY_RE = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
    r"\s+[A-Za-z0-9+/=]{16,}")


def license_cm_name(artifact_name):
    """The license ConfigMap name for an image: '<image>-license'."""
    return to_k8s_name((artifact_name or "") + "-license")


def normalize_license(raw):
    """Robustly extract the license key(s) from pasted/typed/uploaded text and
    return the string stored in the ConfigMap's license.key.

    Tolerant by design: the user may paste with a leading label ('license: ...'),
    surrounding quotes, or extra blank/junk lines and whitespace. We anchor on each
    '<node-uuid> <base64-key>' entry, drop everything before the UUID and trim
    surrounding quotes/whitespace, and keep the rest of the line VERBATIM (incl. the
    vendor's inline '# ...' label, which eda-cx writes byte-for-byte to the sim's
    TiMOS license file). Multiple entries (one per line) are preserved. Returns ""
    when no valid license entry is present."""
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", "replace")
    entries = []
    for line in (raw or "").splitlines():
        s = line.strip()
        m = _LIC_ENTRY_RE.search(s)
        if not m:
            continue                       # skip blank / comment-only / junk lines
        entry = s[m.start():].strip()      # from the UUID to end-of-line (key kept verbatim)
        # Strip a trailing wrap quote/backtick ONLY when the text before the key ends
        # with the SAME quote — i.e. the whole entry was wrapped, possibly behind a
        # label like 'license: "<uuid> <key>"'. A genuine trailing quote on a vendor
        # label (no matching opening quote) is kept verbatim. The key itself can never
        # end in a quote (base64 alphabet excludes them).
        prefix = s[:m.start()].rstrip()
        if prefix and prefix[-1] in "\"'`" and entry and entry[-1] == prefix[-1]:
            entry = entry[:-1].rstrip()
        if entry:
            entries.append(entry)
    return "\n".join(entries)


def is_valid_license(raw):
    """True if at least one parseable license entry is present (used for a lenient
    structure check). Surrounding junk/whitespace does not make it invalid."""
    return bool(normalize_license(raw))


def detect_license_nos(content, filename=""):
    """Best-effort classify a license key as 'srl' or 'sros' from its inline label
    (and the filename as a hint), or None if unclear. Used only to warn when a
    license is attached to an image of a different NOS -- never to block."""
    fn = (filename or "").lower()
    t = content or ""
    if "srlinux" in fn or "srl_" in fn or _LIC_SRL_RE.search(t):
        return "srl"
    if "sros" in fn or "timos" in fn or "srsim" in fn or _LIC_SROS_RE.search(t):
        return "sros"
    return None


def set_license_meta(upload_id, license_rec):
    """Record an attached license on an image's meta.json. Returns the new meta,
    or None if the image is unknown."""
    m = read_meta(upload_id)
    if m is None:
        return None
    m["license"] = license_rec
    return rewrite_meta(upload_id, m)


def store_license_file(upload_id, content):
    """Keep a copy of the raw license text on the PVC next to the image, so the
    upload dir is self-describing and the ConfigMap can be reconstructed. Returns
    the path written, or None on failure (best-effort; the ConfigMap is the
    source of truth)."""
    d = os.path.join(DATA_DIR, upload_id)
    try:
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, "license.key")
        with open(p, "w") as f:
            f.write(content)
        return p
    except OSError:
        return None


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
    last_trim = 0
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
            # keep the kernel page cache (cgroup-charged) from piling up dirty
            # pages when the upload outruns CephFS writeback
            if written - last_trim >= _FADV_EVERY:
                _trim_write_cache(out)
                last_trim = written
        _trim_write_cache(out)
    return written


def stream_download(rfile, dest_path, max_bytes, content_length=None):
    """Stream an HTTP(S) response body into dest_path until EOF, using the same
    OOM-safe page-cache trimming as stream_upload (fsync + POSIX_FADV_DONTNEED
    every _FADV_EVERY bytes). Unlike stream_upload this reads to EOF, so it also
    works when the server sends no Content-Length. Enforces max_bytes. Returns
    bytes written."""
    if max_bytes and content_length and content_length > max_bytes:
        raise UploadTooLarge(f"declared size {content_length} exceeds limit {max_bytes}")
    written = 0
    last_trim = 0
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "wb") as out:
        while True:
            chunk = rfile.read(_CHUNK)
            if not chunk:
                break
            out.write(chunk)
            written += len(chunk)
            if max_bytes and written > max_bytes:
                raise UploadTooLarge(f"download exceeded limit {max_bytes}")
            if written - last_trim >= _FADV_EVERY:
                _trim_write_cache(out)
                last_trim = written
        _trim_write_cache(out)
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
    # Recurse: SR-SIM images keep their bytes under blobs/sha256/ (a subdir).
    try:
        for root, _dirs, files in os.walk(d):
            for name in files:
                fp = os.path.join(root, name)
                try:
                    if os.path.isfile(fp):
                        total += os.path.getsize(fp)
                except OSError:
                    pass
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


def disk_usage(path=DATA_DIR):
    """df-style capacity stats for the PVC backing the uploads dir:
    {totalBytes, usedBytes, freeBytes, usedPercent}. freeBytes/usedPercent use the
    space available to the (unprivileged) pod user. Zeros if the path is missing."""
    try:
        s = os.statvfs(path)
    except OSError:
        return {"totalBytes": 0, "usedBytes": 0, "freeBytes": 0, "usedPercent": 0.0}
    total = s.f_frsize * s.f_blocks
    free = s.f_frsize * s.f_bavail
    used = total - free if total > free else 0
    pct = round(used / total * 100, 1) if total else 0.0
    return {"totalBytes": total, "usedBytes": used, "freeBytes": free, "usedPercent": pct}
