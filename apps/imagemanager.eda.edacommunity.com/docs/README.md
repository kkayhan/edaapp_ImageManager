# EDA Image Manager

Upload network OS images through a web page — either the raw `.bin` (optionally with an
`.md5`), or the vendor `.zip` that contains both. Each upload automatically becomes an EDA
**Artifact** that the built‑in artifact server (`eda-asvr`) downloads, validates, and
re‑hosts for ZTP and software upgrades.

EDA's artifact server uses a pull model that integrates with an organization's central
image store or data lake — the right fit for production. This app is the lab‑friendly
alternative: it stages the upload in‑cluster and writes the `Artifact` for you, so you
don't need an external file server or hand‑written resources just to try a NOS image.

## How to use

1. Install from the EDA App Store.
2. Open the app UI (logged into the EDA UI):
   `https://<your-eda-address>/core/httpproxy/v1/imagemanager/`
3. Pick a `.bin` (and optionally paste an MD5 hash), or pick the vendor `.zip` — the app
   extracts the `.bin` and its packaged `.md5` for you (any typed MD5 is ignored for zips).
   The image name is auto‑filled (SR Linux images become `SRLinux-<version>`); set the
   namespace and upload. The progress bar shows size, percentage, and speed.
4. Watch the status table: the artifact moves `InProgress → Available`, then the row
   shows a copy‑paste **NodeProfile** snippet (`image:` / `imageMd5:` paths) and a
   **delete** action.

## Configuration

Edit the cluster‑scoped `ImageManagerConfig` named `default` (GUI: **Image Manager → Config**):
default artifact namespace (`eda`), default repo (`images`), and max upload size (`4096` MiB).
The app keeps each uploaded file as the durable origin `eda-asvr` pulls from (it re‑pulls on
restart), so files are never auto‑purged — they are removed only when you delete the Artifact.

See the repository README for full details.
