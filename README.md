# EDA Image Manager

A Nokia EDA application that lets you **upload network OS images through a web page** and turns each upload into proper EDA **Artifact(s)** automatically, ready for Zero‑Touch Provisioning (ZTP) and software upgrades. It supports:

- **SR Linux** — a vendor **`.zip`** (e.g. `Nokia-7220_IXR_SR_Linux-…-26.3.2.zip`). The app extracts the `.bin` and its packaged `.md5` and creates, in the `images` repo, an **image** Artifact **plus a separate `md5` Artifact** that the image references as its `imageMd5`.
- **SR OS — Nokia 7750 (TiMOS)** — a vendor **`.zip`**. The app extracts the boot‑image set (`boot.ldr`, `both.tim`, `cpm.tim`, `iom.tim`, `kernel.tim`, `support.tim`) and creates, in the `srosimages` repo, **one image Artifact per file plus a matching `md5` Artifact for each** (the md5s come from the zip's `md5sums.txt`).

On top of those, the matching **YANG schema profile** (the NodeProfile `yang:`) is obtained automatically and hosted in the `schemaprofiles` repo — you don't upload it. It's fetched from `nokia-eda/schema-profiles` when published; for SR OS versions not yet published there, it's **built on the fly from `nokia/7x50_YangModels`** (byte‑identical to the official profile).

So a single upload becomes **several** Artifacts — the image(s), their md5(s), and the YANG profile — all created, tracked, and deleted together.

---

## What it's for

EDA's built‑in **artifact server** (`eda-asvr`) hosts the files network elements download during bootstrap and upgrade (NOS images, boot scripts, configs), and it works by a **pull model**: an `Artifact` resource tells `eda-asvr` *where the file already lives*, and it fetches and re‑hosts it. That design is deliberately **flexible** — it plugs straight into the image registry, artifact store, or central data lake an organization already operates, keeping EDA decoupled from where and how images are kept. For production, that's exactly the right fit.

In a **lab or proof‑of‑concept**, though, you usually don't have that central store on hand — and standing one up just to try a NOS version (an external file server, plus a hand‑written `Artifact` resource per image) is friction you'd rather skip.

**Image Manager is the lab‑friendly alternative.** It runs as a pod inside EDA and gives you a simple web page that stores the upload in‑cluster and creates the `Artifact`(s) for you — no external file server, no YAML to author:

```
You (browser)                Image Manager pod              eda-asvr (built-in)
─────────────                ─────────────────              ───────────────────
 pick a vendor .zip (SRL/SROS)
 ────────────────────────▶   unzip + store on PVC
                             create the Artifact CRs ──────▶ download over HTTPS,
                                                             verify each MD5,
                             ◀───────────────────────────── re‑host the file(s)
 status table → "Available"
 + NodeProfile snippet to copy
```

So in a lab you upload a file in the browser and, a few seconds later, it's a first‑class EDA artifact that nodes can pull — using the **same `eda-asvr` pull model EDA uses everywhere**, just with the in‑cluster hosting and `Artifact` creation handled for you.

> **The app keeps the file — on purpose.** `eda-asvr` does not store images permanently; it re‑hosts them by pulling from wherever the `Artifact` says they live, and in this app that source is the Image Manager pod itself. Its volume is therefore the **durable source of truth**, not a throwaway staging copy: `eda-asvr`'s own copy lives on ephemeral pod storage and it **re‑pulls from this app whenever its pod restarts** (during EDA upgrades, node drains, reschedules). That's why the app keeps your upload even after the artifact reports `Available` — and why deleting an image, or uninstalling the app, makes `eda-asvr` lose it. The two copies you see are *origin* (this app, durable) + *cache* (`eda-asvr`, disposable), not pointless duplication.

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

1. **Pick the vendor `.zip`** — either an SR Linux zip (e.g. `Nokia-7220_IXR_SR_Linux-<hw>-26.3.2.zip`) or a 7750 SR OS TiMOS zip (e.g. `Nokia-7750_SR-TiMOS-26.3.R3.zip`). Only `.zip` is accepted; the type is **detected automatically** from the contents. Everything else is handled for you: the **md5** comes from inside the zip, and the **YANG schema profile** is obtained automatically (fetched from `nokia-eda/schema-profiles`, or for unpublished SR OS versions built from `nokia/7x50_YangModels`).
2. **Choose the Namespace** — pick the target EDA namespace from the dropdown. There's no default; you must select one before uploading.
3. *(Optional)* edit the **auto‑generated name** (`srlinux-<version>` / `sros-<version>`). Names are always lowercase (the field lowercases as you type), so the Artifact name, the served path and the NodeProfile name are uniformly small letters.
4. **Click Upload.** The dialog closes and the image appears in the table as **Uploading**, then **Un‑zipping**.
5. The row turns **`InProgress`** and finally **`Available`** once `eda-asvr` has fetched every part. The list stays compact — **Name, Namespace, Size, Status** and actions. Click **node profile** on a row to open a popup with both the copy‑paste `spec.images` **snippet** (`image` + `imageMd5` per file, plus the `yang:` URL) and a **complete NodeProfile example**, or **delete** to remove the image and all its Artifacts. **Delete asks you to confirm first** — a dialog spells out the consequences (the Artifacts are removed, `eda-asvr` stops hosting the image, and anything pointing at it — NodeProfiles, ZTP, upgrades — will fail until you re‑add a valid image, and the app's only copy is deleted) and only proceeds once you tick an acknowledgement.

Image names are unique — to replace an image, delete the old one first.

**What the Status column means:**

| Status | Meaning |
|---|---|
| `InProgress` | `eda-asvr` is downloading the file(s) and validating each MD5. |
| `Available` | Downloaded, validated, and re‑hosted — the row's NodeProfile snippet is ready to copy. |
| `Failed` | `eda-asvr` rejected the image (for example, the MD5 doesn't match). The reason is shown in the row. |
| `Error` | `eda-asvr` hit a problem fetching or processing the image. The reason is shown in the row. |
| `NoArtifact` | The file is stored in the app but has no matching Artifact (for example, it was deleted). |

**Using an image in a NodeProfile**

Once a row is `Available`, click **node profile** to open the popup. The **snippet** drops straight into an existing `NodeProfile`'s `spec.images`; the **complete example** is a ready‑to‑edit NodeProfile (the image paths/version/OS/`yang:` are filled in; `<…>` values like the management pool and DNS are yours to set). The paths are where `eda-asvr` serves the file(s).

SR Linux (the `imageMd5` line comes from the `.md5` packaged in the zip):

```yaml
images:
  - image: eda/images/srlinux-26.3.9/srlinux-26.3.9
    imageMd5: eda/images/srlinux-26.3.9-md5/srlinux-26.3.9-md5
```

SR OS — every boot file is its own image entry (each with its `imageMd5`), and the schema profile is the `yang:`:

```yaml
images:
  - image: eda/srosimages/sros-26.3.r3-boot.ldr/boot.ldr
    imageMd5: eda/srosimages/sros-26.3.r3-boot.ldr-md5/boot.ldr.md5
  - image: eda/srosimages/sros-26.3.r3-both.tim/both.tim
    imageMd5: eda/srosimages/sros-26.3.r3-both.tim-md5/both.tim.md5
  - image: eda/srosimages/sros-26.3.r3-cpm.tim/cpm.tim
    imageMd5: eda/srosimages/sros-26.3.r3-cpm.tim-md5/cpm.tim.md5
  - image: eda/srosimages/sros-26.3.r3-iom.tim/iom.tim
    imageMd5: eda/srosimages/sros-26.3.r3-iom.tim-md5/iom.tim.md5
  - image: eda/srosimages/sros-26.3.r3-kernel.tim/kernel.tim
    imageMd5: eda/srosimages/sros-26.3.r3-kernel.tim-md5/kernel.tim.md5
  - image: eda/srosimages/sros-26.3.r3-support.tim/support.tim
    imageMd5: eda/srosimages/sros-26.3.r3-support.tim-md5/support.tim.md5
yang: https://eda-asvr.eda-system.svc/eda/schemaprofiles/sros-26.3.r3/sros-26.3.r3.zip
```

---

## Configuration

App behavior is controlled by a single cluster‑scoped resource, **`ImageManagerConfig`** named `default` (created automatically on first start). Edit it in the EDA GUI under **Image Manager → Config**:

| Setting | Default | Meaning |
|---|---|---|
| `defaultArtifactNamespace` | `eda` | _Deprecated / no longer applied._ The upload form now requires you to pick a namespace from a dropdown each time, so nothing is pre‑filled or defaulted. |
| `defaultRepo` | `images` | The repo for **SR Linux** image and md5 Artifacts. (SR OS boot images always go to `srosimages` and YANG schema profiles to `schemaprofiles` — those are fixed; not shown in the upload form.) |
| `maxUploadMiB` | `4096` | Reject uploads larger than this (MiB). |
| `filePullBaseUrl` | _(auto)_ | Advanced: override the in‑cluster URL `eda-asvr` uses to pull from this app. |

Its **status** also reports overall health and a list of every artifact the app created, mirroring each one's live download status.

---

## Uninstalling

Uninstall from the EDA Store (or remove the `AppInstaller`). This removes the controller, its Service/proxy/RBAC, and **its PersistentVolumeClaim** — i.e. the app's stored images are deleted. Because this app is the **durable origin** `eda-asvr` pulls from (see _What it's for_ above), uninstalling breaks every Artifact it created: `eda-asvr` keeps no permanent copy of its own and will fail to re‑pull the files the next time its pod restarts. Before uninstalling, move any images you still need into a permanent store and re‑point their Artifacts there.

---

## How it works under the hood

- The controller is a small, dependency‑free Python 3 process (standard library only). It creates `Artifact` CRs and reports status through the **Kubernetes API**, authenticating with its pod ServiceAccount token. The **web UI** is protected by **EDA single sign‑on** — an OIDC Authorization‑Code flow against EDA's Keycloak (reached in‑cluster via `eda-api`) — and is restricted to users holding an allowed EDA role (default `system-administrator`).
- It serves its file‑pull endpoint over **HTTPS** using a certificate issued by EDA's internal CA (via the cert‑manager CSI driver). Because `eda-asvr`'s download client does **not** trust that CA by default, the controller also creates a small trust‑bundle ConfigMap in each target namespace and sets `spec.trustBundle` on every Artifact — so `eda-asvr` can pull from it securely with no manual setup.
- The PersistentVolumeClaim is the **durable** source of truth for uploaded bytes — `eda-asvr` keeps no permanent store of its own and re‑pulls from this app on restart, so the files are retained for the life of their Artifacts (never auto‑purged); they are removed only when you delete the Artifact. The `Artifact` resources are the source of truth for status.

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
