"""
Resolve (or build) the EDA YANG schema-profile zip a NodeProfile.spec.yang points
at, so the user never has to upload it. Stdlib only.

Resolution order (the caller handles an explicit user upload, which always wins):
  1. FETCH the published profile from github nokia-eda/schema-profiles (BOTH srl
     and sros) — resolved via the GitHub releases API because the tags/asset names
     are inconsistent (sros-<ver>.zip under tag nokia-sros[-v]<ver>;
     srlinux-<ver>-<build>.zip under nokia-srl-<ver>).
  2. SROS ONLY — BUILD it from github nokia/7x50_YangModels tag sros_<ver>.

The published SROS profile is reproducible from the 7x50 repo tag (verified
byte-identical against sros-25.10.r1 and sros-26.3.r1): it is the tag's
LICENSE.md + README.md + a generated schema_profile.yml + the YANG/ tree with the
nokia-submodule/ and openconfig/ subdirs dropped (keeping ietf/, nokia-combined/
and the top-level nokia-*.yang). The schema_profile.yml is static except
versionMatch, a deterministic transform of the version.

SR Linux is NOT built from raw YANG: its schema_profile.yml carries per-release
features/modules lists that track the models, so only fetch/upload apply.
"""

import io
import json
import logging
import os
import re
import tarfile
import time
import urllib.error
import urllib.request
import zipfile

logger = logging.getLogger("schemaprofile")

_TIMEOUT = 60          # per-attempt; retries bound the total
_ATTEMPTS = 3          # ride out a transient GitHub hiccup
_BACKOFF = 2           # seconds; grows 2s, 4s between attempts
_UA = "eda-imagemanager"
_RELEASES_API = "https://api.github.com/repos/nokia-eda/schema-profiles/releases?per_page=100"
_X50_TARBALL = "https://codeload.github.com/nokia/7x50_YangModels/tar.gz/refs/tags/sros_{ver}"

# YANG/ subdirs the EDA SROS profile excludes from the 7x50 payload.
_SROS_DROP_DIRS = ("YANG/nokia-submodule/", "YANG/openconfig/")

# The SROS schema_profile.yml is static across versions except versionMatch
# (verified: 25.10.r1 vs 26.3.r1 differ by that one line only). __VERSION_MATCH__
# is substituted per upload.
_SROS_SCHEMA_PROFILE = """platforms:
  - platform: default
    secretTypeDefs:
    - nokia-types-sros:hashed-leaf
    - nokia-types-sros:encrypted-leaf
    modules:
      - nokia-conf
      - nokia-state
    gnmiSupport:
      depth: True
      commitConfirmed: True
      configSubscripton: True
      removeEmptyNonPresenceChoiceCases: True
    versionMatch: "__VERSION_MATCH__"
    versionPath: .state.system.version.version-number
    platformPath: .state.system.platform
    pathPolling:
      defaultInterval: 60s
      jspathList:
      - jspath: .state.card.hardware-data
        interval: 10s
      - jspath: .state.chassis.fan.hardware-data
        interval: 10s
      - jspath: .state.chassis.hardware-data
        interval: 10s
      - jspath: .state.chassis.power-supply.hardware-data
        interval: 10s
      - jspath: .state.cpm.hardware-data
        interval: 10s
      - jspath: .state.port
        interval: 10s
      - jspath: .state.port.transceiver
        interval: 10s
      - jspath: .state.router.bgp.neighbor.statistics
        interval: 10s
      - jspath: .state.router.interface
        interval: 10s
      - jspath: .state.service.vpls
        interval: 10s
      - jspath: .state.service.vprn
        interval: 10s
      - jspath: .state.service.vprn.interface
        interval: 10s
      - jspath: .state.chassis.power-shelf.power-module.hardware-data
        interval: 10s
      - jspath: .state.chassis.power-shelf.hardware-data
        interval: 10s
      - jspath: .state.bfd.pt-to-pt-session.state
        interval: 10s
      - jspath: .state.sfm.hardware-data
        interval: 10s
"""


def schema_profile_filename(nos, version):
    """The asvr filePath we host the profile as (matches EDA's convention)."""
    return ("sros-%s.zip" if nos == "sros" else "srlinux-%s.zip") % version


def sros_version_match(version):
    """Compute the SROS schema_profile.yml versionMatch value from a version.
    The value is written into a double-quoted YAML string, so the backslash is
    doubled to survive YAML escaping (matching the published profile byte-for-byte):
    26.3.r1 -> [A-Z]-26\\\\.3.R1 in the file. None if unparsable."""
    m = re.match(r"(\d+)\.(\d+)\.r(\d+)$", (version or "").strip().lower())
    if not m:
        return None
    maj, mn, rev = m.groups()
    return r"[A-Z]-%s\\.%s.R%s" % (maj, mn, rev)


def _http_get(url, accept="application/octet-stream"):
    """GET with up to _ATTEMPTS tries to ride out a transient GitHub hiccup.
    Retries network errors / timeouts / HTTP 5xx / 429; fails fast on other 4xx
    (e.g. 404 = unpublished version or missing 7x50 tag — retrying won't help).
    Raises the last error after exhausting attempts (callers treat that as None)."""
    last = None
    for i in range(_ATTEMPTS):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": _UA, "Accept": accept})
            with urllib.request.urlopen(req, timeout=_TIMEOUT) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            last = e
            if e.code != 429 and e.code < 500:
                raise  # permanent 4xx (404/403/...): don't retry
        except Exception as e:  # noqa: BLE001 - URLError/timeout/socket/TLS: transient
            last = e
        if i < _ATTEMPTS - 1:
            logger.info("GitHub GET %s failed (%s); retry %d/%d", url, last, i + 1, _ATTEMPTS - 1)
            time.sleep(_BACKOFF * (i + 1))
    raise last


def fetch_published_profile(nos, version, dest_dir):
    """Download the matching nokia-eda/schema-profiles release asset into dest_dir.
    Returns the stored filename, or None (no matching release / network error).
    Never raises."""
    if nos == "sros":
        want = re.compile(r"^sros-%s\.zip$" % re.escape(version))
    else:
        # SRL asset = srlinux-<X.Y.Z>-<build>[...].zip. The build segment is OPTIONAL
        # (the caller may pass a version with or without it) and anchored so a 3-part
        # version cannot bleed into a longer one (ver 26.3.1 must NOT match
        # srlinux-26.3.10-100.zip), while still matching srlinux-26.3.1-410.zip and
        # srlinux-24.10.4-244-v2.zip.
        want = re.compile(r"^srlinux-%s(?:-\d+)?(?:[._-].*)?\.zip$" % re.escape(version))
    try:
        releases = json.loads(_http_get(_RELEASES_API, "application/vnd.github+json").decode("utf-8"))
    except Exception as e:  # noqa: BLE001 - best-effort
        logger.warning("schema-profiles releases API failed: %s", e)
        return None
    for rel in releases:
        for asset in rel.get("assets", []) or []:
            name = asset.get("name", "")
            if want.match(name):
                url = asset.get("browser_download_url")
                out = schema_profile_filename(nos, version)
                out_path = os.path.join(dest_dir, out)
                try:
                    data = _http_get(url)
                    with open(out_path, "wb") as f:
                        f.write(data)
                except Exception as e:  # noqa: BLE001 - best-effort; honor "never raises"
                    logger.warning("schema profile asset %s store failed: %s", name, e)
                    try:
                        if os.path.exists(out_path):
                            os.remove(out_path)
                    except OSError:
                        pass
                    return None
                logger.info("Fetched published %s schema profile %s (asset %s)", nos, out, name)
                return out
    return None


def build_sros_profile(version, dest_dir):
    """Build the SROS schema profile from github nokia/7x50_YangModels tag
    sros_<ver>: LICENSE.md + README.md + generated schema_profile.yml + YANG/
    (minus nokia-submodule/ and openconfig/). Returns the filename or None. Never
    raises."""
    vm = sros_version_match(version)
    if not vm:
        logger.warning("cannot derive versionMatch for SROS version %r", version)
        return None
    url = _X50_TARBALL.format(ver=version)
    try:
        blob = _http_get(url)
    except Exception as e:  # noqa: BLE001 - tag may not exist upstream yet
        logger.warning("7x50 tarball fetch %s failed: %s", url, e)
        return None
    out = schema_profile_filename("sros", version)
    out_path = os.path.join(dest_dir, out)
    try:
        with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tf:
            members = tf.getmembers()
            if not members:
                return None
            root = members[0].name.split("/", 1)[0] + "/"
            kept = 0
            with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
                z.writestr("schema_profile.yml",
                           _SROS_SCHEMA_PROFILE.replace("__VERSION_MATCH__", vm))
                for m in members:
                    if not m.isfile():
                        continue
                    rel = m.name[len(root):] if m.name.startswith(root) else m.name
                    keep = rel in ("LICENSE.md", "README.md")
                    if rel.startswith("YANG/") and not any(rel.startswith(d) for d in _SROS_DROP_DIRS):
                        keep = True
                    if not keep:
                        continue
                    f = tf.extractfile(m)
                    if f is None:
                        continue
                    z.writestr(rel, f.read())
                    kept += 1
    except Exception as e:  # noqa: BLE001
        logger.warning("building SROS profile for %s failed: %s", version, e)
        try:
            if os.path.exists(out_path):
                os.remove(out_path)
        except OSError:
            pass
        return None
    if kept < 10:   # sanity: a real profile has ~99 files
        logger.warning("built SROS profile for %s has only %d files; discarding", version, kept)
        try:
            os.remove(out_path)
        except OSError:
            pass
        return None
    logger.info("Built SROS schema profile %s from 7x50 tag sros_%s (%d files)", out, version, kept)
    return out


def resolve_yang(nos, version, dest_dir):
    """Resolve the schema profile for (nos, version) into dest_dir.
    Returns (filename, source) where source is 'published' | 'built' | None.
    Order: published nokia-eda profile, then (sros only) build from 7x50."""
    fn = fetch_published_profile(nos, version, dest_dir)
    if fn:
        return fn, "published"
    if nos == "sros":
        fn = build_sros_profile(version, dest_dir)
        if fn:
            return fn, "built"
    return None, None
