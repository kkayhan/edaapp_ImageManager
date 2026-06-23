# Imagemanager Application

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                         |
| -------------------- |-----------------------------------------|
| **Group/Version**    | -{{ app_group }}-/-{{ app_api_version }}-   |
| **Supported OS**     | -{{ supported_os_versions() }}-  |
| **Catalog**          | [edacommunity/catalog/imagemanager ][manifest] |
| **Source Code**      | [kkayhan/edaapp_ImageManager][src]      |

[manifest]: https://github.com/kkayhan/edaapp_ImageManager/tree/main/apps/imagemanager.eda.edacommunity.com
[src]: https://github.com/kkayhan/edaapp_ImageManager

Upload network OS images (`.bin`) and their `.md5` checksums through a web page. Each upload
is stored in‑cluster and an EDA **Artifact** is created automatically, so the built‑in artifact
server (`eda-asvr`) downloads the file, validates it against the md5, and re‑hosts it for
Zero‑Touch Provisioning and software upgrades. This removes the need to run an external file
server and to hand‑write `Artifact` resources.

After install, open the app UI (while signed into the EDA UI) at
`https://<your-eda-address>/core/httpproxy/v1/imagemanager/`, pick a `.bin` (and optionally its
`.md5`), set the repo / namespace / file path, and upload. A status table shows each artifact
move from `InProgress` to `Available` along with its reusable URL.

The application provides the following components:

/// tab | Resources

<div class="grid" markdown>
<div markdown>

* **ImageManagerConfig** — cluster‑scoped settings (default namespace/repo, max upload size, retention) and live status.

</div>
</div>
///
