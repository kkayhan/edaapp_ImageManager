# EDA Image Manager

A Nokia EDA application that lets you **upload network OS images through a web page** and turns each upload into proper EDA **Artifact(s)** automatically, ready for Zero‑Touch Provisioning (ZTP) and software upgrades. It supports:

- **SR Linux** — the raw `.bin` (optionally with an MD5 hash) or the **vendor `.zip`** (the `.bin` and its `.md5` are extracted for you) → one Artifact in the `images` repo.
- **SR OS — Nokia 7750 (TiMOS)** — the vendor **`.zip`**. The app extracts the boot‑image set (`both.tim`, `cpm.tim`, `iom.tim`, `kernel.tim`, `support.tim`, `boot.ldr`) and creates **one Artifact per file** in the `srosimages` repo, plus the matching **YANG schema profile** (auto‑fetched from `nokia-eda/schema-profiles`, or uploaded by you) in the `schemaprofiles` repo.

---

## What it's for

EDA's built‑in **artifact server** (`eda-asvr`) hosts the files network elements download during bootstrap and upgrade (NOS images, boot scripts, configs), and it works by a **pull model**: an `Artifact` resource tells `eda-asvr` *where the file already lives*, and it fetches and re‑hosts it. That design is deliberately **flexible** — it plugs straight into the image registry, artifact store, or central data lake an organization already operates, keeping EDA decoupled from where and how images are kept. For production, that's exactly the right fit.

In a **lab or proof‑of‑concept**, though, you usually don't have that central store on hand — and standing one up just to try a NOS version (an external file server, plus a hand‑written `Artifact` resource per image) is friction you'd rather skip.

**Image Manager is the lab‑friendly alternative.** It runs as a pod inside EDA and gives you a simple web page that stores the upload in‑cluster and creates the `Artifact` for you — no external file server, no YAML to author:

```
You (browser)                Image Manager pod              eda-asvr (built-in)
─────────────                ─────────────────              ───────────────────
 pick srl.bin or .zip (+ md5)
 ────────────────────────▶   store on PVC
                             create an Artifact CR  ───────▶ download over HTTPS,
                                                             verify MD5 (if given),
                             ◀───────────────────────────── re‑host the file
 status table → "Available"
 + NodeProfile snippet to copy
```

So in a lab you upload a file in the browser and, a few seconds later, it's a first‑class EDA artifact that nodes can pull — using the **same `eda-asvr` pull model EDA uses everywhere**, just with the staging and `Artifact` creation handled for you.

---

## Installing it in EDA (via the GUI)

Everything below is done in the **EDA web UI** — no command line needed.

### Step 1 — Register the app catalog (one‑time per cluster)

EDA discovers installable apps through **Catalog** resources that point at a Git repository. This app lives in its own repository, so your cluster needs a Catalog pointing at it. (Each app/repository has its own Catalog — if you also run other community apps, this is a separate, additional entry.)

In the EDA UI, open the **App Store → Catalogs** view (or the generic resource editor) and **create a new Catalog** with the following content:

```yaml
apiVersion: appstore.eda.nokia.com/v1
kind: Catalog
metadata:
  name: imagemanager-catalog
  namespace: eda-system
spec:
  enabled: true
  refreshInterval: 180
  remoteType: git
  remoteURL: https://github.com/kkayhan/edaapp_ImageManager.git
  skipTLSVerify: false
  title: Image Manager
```

Within a few minutes the Catalog shows **Operational = true** and **EDA Image Manager** appears in the App Store.

### Step 2 — Install from the App Store

1. In the EDA UI, go to the **App Store** and open **EDA Image Manager**.
2. Click **Install**.
3. (Optional) Adjust the install‑time settings on the form:
   - **Controller CPU / memory limit** — pod resource limits.
   - **Upload storage size** — size of the volume that holds images before `eda-asvr` re‑hosts them (default `20Gi`; set it large enough for the images you upload at once).
4. Confirm. EDA creates the controller, its Service, the HTTP‑proxy route, RBAC, and the config resource. Wait until the app shows as installed / its pod is **Ready**.

> **Air‑gapped cluster?** A self‑contained offline bundle (images + catalog + step‑by‑step install guide) is attached to the GitHub Release for each version, under the tag `apps/imagemanager.eda.edacommunity.com/<version>`.

---

## Opening the app's web UI

Image Manager is served **through the EDA API’s HTTP proxy**, so you reach it at a path under your EDA address while logged into the EDA UI:

```
https://<your-eda-address>/core/httpproxy/v1/imagemanager/
```

Open that URL in the same browser where you're logged into the EDA UI (the EDA login protects the page).

**Using it:**

Click **Upload Image From File** (top right) to open the upload dialog, then:

1. **Pick the image type** — *SR Linux* (`.bin` / vendor `.zip`) or *SR OS — 7750 (TiMOS `.zip`)*.
2. **Pick the image file.**
   - **SR Linux:** the raw `.bin`, or the **vendor `.zip`** (e.g. `Nokia-7220_IXR_SR_Linux-<hw>-26.3.2.zip`). For a zip, the app extracts the `.bin` and reads the packaged `.md5` automatically. The **Image name** auto‑fills as `SRLinux-<version>` — editable.
   - **SR OS:** the 7750 **TiMOS `.zip`** (e.g. `Nokia-7750_SR-TiMOS-26.3.R3.zip`). The app extracts the boot‑image set and creates one Artifact per file. The name is fixed to `SROS-<version>` (read from the image). *Optionally* attach a **YANG schema profile `.zip`** — if you don't, it's auto‑fetched from `nokia-eda/schema-profiles` for that version (provide it for versions not yet published upstream).
3. **Choose the Namespace** — pick the target EDA namespace from the dropdown. There's no default; you must select one before uploading.
4. *(SR Linux raw `.bin` only)* **Paste the vendor's MD5 hash** so EDA can verify the download. (Vendor zips use the packaged checksum; SR OS images carry no per‑file MD5, matching the reference NodeProfiles.)
5. **Click Upload.** The dialog closes and the image appears in the table right away as **Uploading**, then **Un‑zipping**.
6. The row turns **`InProgress`** and finally **`Available`** once `eda-asvr` has fetched every part. Each row shows a ready‑to‑paste **NodeProfile** snippet (for SR OS it lists all image paths plus the `yang:` URL) — click **copy** to grab it, or **delete** to remove the image and all its Artifacts (also dropping `eda-asvr`'s hosted copies).

Image names are unique — to replace an image, delete the old one first.

**What the Status column means:**

| Status | Meaning |
|---|---|
| `InProgress` | `eda-asvr` is downloading the image (and validating the MD5, if you supplied one). |
| `Available` | Downloaded, validated, and re‑hosted — the row's NodeProfile snippet is ready to copy. |
| `Failed` | `eda-asvr` rejected the image (for example, the MD5 doesn't match). The reason is shown in the row. |
| `Error` | `eda-asvr` hit a problem fetching or processing the image. The reason is shown in the row. |
| `NoArtifact` | The file is stored in the app but has no matching Artifact (for example, it was deleted). |

**Using an image in a NodeProfile**

Once a row is `Available`, copy its snippet straight into a `NodeProfile`'s `spec.images`. The paths are where `eda-asvr` serves the file(s).

SR Linux (`imageMd5` appears only if you supplied an MD5):

```yaml
images:
  - image: eda/images/srlinux-26.3.9/SRLinux-26.3.9
    imageMd5: eda/images/srlinux-26.3.9-md5/SRLinux-26.3.9-md5
```

SR OS — every boot file is its own image entry, and the schema profile is the `yang:`:

```yaml
images:
  - image: eda/srosimages/sros-26.3.r3-boot.ldr/boot.ldr
  - image: eda/srosimages/sros-26.3.r3-both.tim/both.tim
  - image: eda/srosimages/sros-26.3.r3-cpm.tim/cpm.tim
  - image: eda/srosimages/sros-26.3.r3-iom.tim/iom.tim
  - image: eda/srosimages/sros-26.3.r3-kernel.tim/kernel.tim
  - image: eda/srosimages/sros-26.3.r3-support.tim/support.tim
yang: https://eda-asvr.eda-system.svc/eda/schemaprofiles/sros-26.3.r3/sros-26.3.r3.zip
```

---

## Configuration

App behavior is controlled by a single cluster‑scoped resource, **`ImageManagerConfig`** named `default` (created automatically on first start). Edit it in the EDA GUI under **Image Manager → Config**:

| Setting | Default | Meaning |
|---|---|---|
| `defaultArtifactNamespace` | `eda` | _Deprecated / no longer applied._ The upload form now requires you to pick a namespace from a dropdown each time, so nothing is pre‑filled or defaulted. |
| `defaultRepo` | `images` | The single artifact repo that all uploads are placed in (not shown in the upload form; `Artifact` requires a repo, so the app uses one fixed value). |
| `maxUploadMiB` | `4096` | Reject uploads larger than this (MiB). |
| `retentionDays` | `0` | After this many days, delete the app's local copy of an image once `eda-asvr` reports it `Available` (`0` = keep forever). |
| `filePullBaseUrl` | _(auto)_ | Advanced: override the in‑cluster URL `eda-asvr` uses to pull from this app. |

Its **status** also reports overall health and a list of every artifact the app created, mirroring each one's live download status.

---

## Uninstalling

Uninstall from the EDA Store (or remove the `AppInstaller`). This removes the controller, its Service/proxy/RBAC, and **its PersistentVolumeClaim** — i.e. the app's local copies of uploaded files are deleted. Artifacts that `eda-asvr` already re‑hosted keep working, because `eda-asvr` stores its own copy. Treat the app's volume as a staging area, not permanent storage.

---

## How it works under the hood

- The controller is a small, dependency‑free Python 3 process. It talks only to the Kubernetes API using its pod ServiceAccount token (no Keycloak needed) to create `Artifact` CRs and report status.
- It serves its file‑pull endpoint over **HTTPS** using a certificate issued by EDA's internal CA (via the cert‑manager CSI driver). Because `eda-asvr`'s download client does **not** trust that CA by default, the controller also creates a small trust‑bundle ConfigMap in each target namespace and sets `spec.trustBundle` on every Artifact — so `eda-asvr` can pull from it securely with no manual setup.
- The PersistentVolumeClaim is the source of truth for uploaded bytes; the `Artifact` resources are the source of truth for status.

---

## For maintainers

This repository is both the **source** and the **app catalog**.

- App project (edabuilder layout): repository root — `PROJECT`, `imagemanager/` (API types, controller, manifests), `common/`, `utils/`.
- Controller source: [`imagemanager/build/controller/`](imagemanager/build/controller/).
- Kubernetes manifests: [`imagemanager/manifests/`](imagemanager/manifests/).
- Catalog entries (published by `edabuilder publish`): `apps/imagemanager.eda.edacommunity.com/`.

Build & publish flow (high level): `docker build/push` the controller image → `edabuilder build-push` the app bundle to GHCR → `edabuilder publish app` the catalog entry + version tag → attach the offline bundle to the GitHub Release.

**Versioning:** the app version tracks the EDA release it targets, as `v<eda-release>-<build>` — e.g. `v26.4.2-1`, `v26.4.2-2`, … against EDA `26.4.2` (the leading `v` matches EDA's own version string and is required by `edabuilder`). EDA cuts major releases on the 4th/8th/12th month each year (`26.4.x`, `26.8.x`, `26.12.x`, then `27.4.x`, …); the `-<build>` increments per app change within a given EDA release. The controller image and app bundle share this tag.

**License:** MIT.
