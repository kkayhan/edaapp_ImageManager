"""Self-contained upload web UI (no external assets), served at GET /.

Material Design layout (vanilla HTML/CSS/JS, no React/build step) dressed in the
Nokia EDA palette: a top AppBar with a Material switch for Light/Dark, the
artifacts list rendered as a sortable Material data table, the upload form moved
into a modal Dialog, and result notifications shown as Material snackbar toasts.

Material is expressed in pure CSS/JS: elevation (dp shadow scale), state-layer
hovers, click ripples, the type scale, rounded surfaces, and dialog/snackbar
motion. Colors come from EDA's own appearance themes (light surfaces
#F7F9FD/#FFFFFF + Nokia-blue #005AFF; dark surfaces #101824/#1A222E + #4D8DFF),
so it still reads as native inside the EDA GUI."""

INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>EDA Image Manager</title>
<style>
  :root {
    --bg:#f7f9fd; --appbar:#ffffff; --panel:#ffffff; --panel2:#f2f4f8; --input-bg:#ffffff;
    --line:#d9dee7; --fg:#2b2b2b; --muted:#687282; --accent:#005aff; --accent2:#0a44ad;
    --accent-soft:#ecf3ff; --state:rgba(0,90,255,.06); --state-strong:rgba(0,90,255,.12);
    --row-hover:rgba(0,90,255,.045);
    --ok-fg:#00822b; --ok-bg:#e3fcec; --ok-bd:#24d45e;
    --info-fg:#0a44ad; --info-bg:#ecf3ff; --info-bd:#0a44ad;
    --err-fg:#911a1a; --err-bg:#ffeded; --err-bd:#d32f2f;
    --danger:#d32f2f; --danger-strong:#a31515; --on-danger:#ffffff;
    --neutral-fg:#687282; --neutral-bg:#eef0f3; --neutral-bd:#cfcfcf;
    --snack-bg:#2b303a; --snack-fg:#f3f5f8; --snack-action:#9cc0ff;
    --scrim:rgba(16,24,36,.46);
    --elev1:0 1px 2px rgba(20,30,50,.10),0 1px 3px rgba(20,30,50,.08);
    --elev2:0 1px 5px rgba(20,30,50,.10),0 2px 8px rgba(20,30,50,.07);
    --elev4:0 2px 6px rgba(20,30,50,.12),0 4px 14px rgba(20,30,50,.10);
    --elev8:0 6px 16px rgba(20,30,50,.16),0 9px 28px rgba(20,30,50,.12);
    --elev24:0 11px 18px rgba(20,30,50,.18),0 22px 44px rgba(20,30,50,.22);
  }
  html[data-theme="dark"] {
    --bg:#101824; --appbar:#162030; --panel:#1a222e; --panel2:#222c37; --input-bg:#222c37;
    --line:#2c3644; --fg:#e6edf3; --muted:#8b98a6; --accent:#4d8dff; --accent2:#6aa4ff;
    --accent-soft:#1b2740; --state:rgba(120,160,255,.10); --state-strong:rgba(120,160,255,.18);
    --row-hover:rgba(255,255,255,.04);
    --ok-fg:#5ee58b; --ok-bg:rgba(36,212,94,.14); --ok-bd:#24d45e;
    --info-fg:#90b7ff; --info-bg:rgba(144,183,255,.13); --info-bd:#4d8dff;
    --err-fg:#ff9b9b; --err-bg:rgba(211,47,47,.18); --err-bd:#d32f2f;
    --danger:#e5484d; --danger-strong:#ff5c61; --on-danger:#ffffff;
    --neutral-fg:#abb4c2; --neutral-bg:rgba(171,180,194,.12); --neutral-bd:#3a4452;
    --snack-bg:#e8edf4; --snack-fg:#1a222e; --snack-action:#0a44ad;
    --scrim:rgba(0,0,0,.6);
    --elev1:0 1px 2px rgba(0,0,0,.5);
    --elev2:0 2px 6px rgba(0,0,0,.5);
    --elev4:0 4px 14px rgba(0,0,0,.55);
    --elev8:0 8px 26px rgba(0,0,0,.6);
    --elev24:0 22px 48px rgba(0,0,0,.7);
  }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--fg);
    font:14px/1.5 "Nokia Pure Text","Inter","Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    -webkit-font-smoothing:antialiased; }

  /* ---------- ripple (Material touch feedback) ---------- */
  .ripple { position:relative; overflow:hidden; }
  .ripple-ink { position:absolute; border-radius:50%; background:currentColor; opacity:.26;
    transform:scale(0); pointer-events:none; animation:ink .55s cubic-bezier(.4,0,.2,1); }
  @keyframes ink { to { transform:scale(1); opacity:0; } }

  /* ---------- AppBar ---------- */
  .appbar { position:sticky; top:0; z-index:30; height:60px; padding:0 22px;
    background:var(--appbar); box-shadow:var(--elev4);
    display:flex; align-items:center; gap:14px; }
  .brand-mark { width:18px; height:18px; border-radius:5px; background:var(--accent);
    box-shadow:0 0 0 4px color-mix(in srgb,var(--accent) 20%,transparent); flex:none; }
  .brand-name { font-size:18px; font-weight:600; letter-spacing:.01em; }
  .appbar .sub { color:var(--muted); font-size:12.5px; }
  @media (max-width:880px){ .appbar .sub { display:none; } }
  .appbar-actions { margin-left:auto; display:flex; align-items:center; gap:6px; }
  .user-chip { display:inline-flex; align-items:center; gap:7px; padding:5px 12px 5px 9px;
    border-radius:18px; background:var(--panel2); color:var(--fg); font-size:12.5px; font-weight:500; }
  .user-chip .avatar { width:22px; height:22px; border-radius:50%; background:var(--accent);
    color:#fff; font-size:11px; font-weight:700; display:flex; align-items:center;
    justify-content:center; text-transform:uppercase; }
  @media (max-width:560px){ .user-chip .uname { display:none; } }

  /* ---------- Material switch (theme toggle) ---------- */
  .switch { display:inline-flex; align-items:center; gap:9px; cursor:pointer;
    padding:6px 8px; border-radius:8px; user-select:none; }
  .switch:hover { background:var(--state); }
  .switch input { position:absolute; opacity:0; width:0; height:0; }
  .switch .track { position:relative; width:36px; height:14px; border-radius:7px;
    background:var(--neutral-bd); transition:background .2s; flex:none; }
  .switch .thumb { position:absolute; top:-3px; left:-1px; width:20px; height:20px;
    border-radius:50%; background:#fafafa; box-shadow:var(--elev1);
    transition:transform .2s, background .2s; }
  .switch input:checked + .track { background:color-mix(in srgb,var(--accent) 55%,transparent); }
  .switch input:checked + .track .thumb { transform:translateX(18px); background:var(--accent); }
  .switch input:focus-visible + .track .thumb { box-shadow:0 0 0 8px var(--state-strong); }
  .switch .swlabel { font-size:12.5px; color:var(--muted); min-width:34px; }

  /* ---------- buttons ---------- */
  .btn { border:0; border-radius:8px; padding:9px 18px; font:500 13.5px/1 inherit;
    letter-spacing:.012em; cursor:pointer; display:inline-flex; align-items:center; gap:8px;
    text-decoration:none; transition:box-shadow .18s, background .15s; }
  .btn:focus-visible { outline:2px solid var(--accent); outline-offset:2px; }
  .btn .ic { width:18px; height:18px; flex:none; }
  .btn.contained { background:var(--accent); color:#fff; box-shadow:var(--elev1); }
  .btn.contained:hover { background:var(--accent2); box-shadow:var(--elev4); }
  .btn.contained:disabled { background:var(--neutral-bd); color:#fff; box-shadow:none;
    cursor:not-allowed; }
  .btn.text { background:transparent; color:var(--accent); padding:9px 14px; }
  .btn.text:hover { background:var(--state); }
  .btn.text.subtle { color:var(--muted); }
  .btn.text.subtle:hover { color:var(--fg); }
  .btn.text.danger { color:var(--err-fg); }
  .btn.text.danger:hover { background:var(--err-bg); }

  /* ---------- layout ---------- */
  main { max-width:1200px; margin:0 auto; padding:26px 20px 64px; }
  .page-head { display:flex; align-items:flex-end; gap:16px; margin:4px 2px 20px; }
  .page-title { margin:0; font-size:23px; font-weight:600; letter-spacing:.005em;
    display:flex; align-items:center; gap:11px; }
  .count { font-size:12.5px; font-weight:600; color:var(--accent); background:var(--accent-soft);
    border-radius:12px; padding:2px 10px; }
  .page-sub { margin:5px 0 0; color:var(--muted); font-size:13px; }
  .page-head .grow { flex:1; }

  /* ---------- app-storage bar ---------- */
  .storage-card { padding:14px 18px 15px; margin-bottom:20px; }
  .storage-row { display:flex; align-items:baseline; justify-content:space-between; gap:12px; margin-bottom:9px; }
  .storage-label { font-size:11px; font-weight:600; color:var(--muted); text-transform:uppercase; letter-spacing:.06em; }
  .storage-stat { font-size:13px; color:var(--muted); }
  .storage-stat .mono { color:var(--fg); font-weight:600; }
  .storage-track { height:10px; border-radius:6px; background:var(--panel2); overflow:hidden; }
  .storage-fill { height:100%; width:0; border-radius:6px; background:var(--accent);
    transition:width .45s ease, background .3s; }
  .storage-fill.warn { background:#e0a800; }
  .storage-fill.crit { background:var(--danger); }

  .card { background:var(--panel); border-radius:14px; box-shadow:var(--elev2);
    margin-bottom:20px; overflow:hidden; }

  /* ---------- data table ---------- */
  .table-wrap { overflow-x:auto; }
  table.mtable { width:100%; border-collapse:collapse; font-size:13px; }
  .mtable th, .mtable td { text-align:left; padding:13px 16px;
    border-bottom:1px solid var(--line); vertical-align:top; }
  .mtable thead th { color:var(--muted); font-weight:600; font-size:11px; text-transform:uppercase;
    letter-spacing:.06em; white-space:nowrap; }
  .mtable th.sortable { cursor:pointer; user-select:none; }
  .mtable th.sortable:hover { color:var(--fg); }
  .mtable th.sortable .arr { opacity:0; margin-left:5px; font-size:10px; transition:opacity .15s; }
  .mtable th.sortable:hover .arr { opacity:.45; }
  .mtable th.sorted .arr { opacity:1; color:var(--accent); }
  .mtable th.num { text-align:right; }
  .mtable td.num { text-align:right; }
  .mtable tbody tr { transition:background .12s; }
  .mtable tbody tr:hover { background:var(--row-hover); }
  .mtable tbody tr:last-child td { border-bottom:0; }
  td.mono, .mono { font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:12px; }
  .namecell { font-weight:600; }

  .chip { display:inline-flex; align-items:center; gap:6px; padding:3px 11px; border-radius:13px;
    font-size:11.5px; font-weight:600; border:1px solid transparent; white-space:nowrap; }
  .chip::before { content:""; width:7px; height:7px; border-radius:50%; background:currentColor; }
  .c-Available, .c-Ready { background:var(--ok-bg); color:var(--ok-fg); border-color:var(--ok-bd); }
  .c-InProgress { background:var(--info-bg); color:var(--info-fg); border-color:var(--info-bd); }
  .c-Error, .c-Failed { background:var(--err-bg); color:var(--err-fg); border-color:var(--err-bd); }
  .c-NoArtifact, .c-empty { background:var(--neutral-bg); color:var(--neutral-fg); border-color:var(--neutral-bd); }
  .c-Uploading, .c-Unzipping, .c-Processing { background:var(--info-bg); color:var(--info-fg); border-color:var(--info-bd); }
  .c-Uploading::before, .c-Unzipping::before, .c-Processing::before { animation:pulse 1.1s ease-in-out infinite; }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.25} }
  .upinfo { margin-top:6px; font:11px ui-monospace,SFMono-Regular,Menlo,monospace; color:var(--muted); }
  .uprog { margin-top:6px; height:5px; width:170px; max-width:100%; background:var(--state);
    border-radius:3px; overflow:hidden; }
  .uprog > div { height:100%; background:var(--accent); border-radius:3px; transition:width .15s; }
  .uprog.indet > div { width:40%; animation:indet 1.15s ease-in-out infinite; }
  @keyframes indet { 0%{margin-left:-42%} 100%{margin-left:102%} }
  .reason { color:var(--err-fg); font-size:12px; margin-top:5px; }
  .empty { color:var(--muted); padding:34px 16px; text-align:center; }

  pre.snippet { margin:0; padding:9px 11px; background:var(--panel2); border:1px solid var(--line);
    border-radius:6px; font:12px ui-monospace,SFMono-Regular,Menlo,monospace; white-space:pre;
    overflow-x:auto; color:var(--fg); }
  .pending { color:var(--muted); }
  .iconbtn { background:var(--panel2); border:1px solid var(--line); color:var(--fg);
    border-radius:7px; padding:5px 12px; font-size:11.5px; font-weight:500; cursor:pointer;
    transition:background .12s,border-color .12s,color .12s,box-shadow .12s,transform .04s; }
  .iconbtn:hover { border-color:var(--accent); color:var(--accent); }
  /* row action buttons: prominent, filled (Details = accent, Delete = red) */
  .iconbtn.primary { background:var(--accent); border-color:var(--accent); color:#fff;
    font-weight:600; padding:6px 15px; box-shadow:var(--elev1); }
  .iconbtn.primary:hover { background:var(--accent2); border-color:var(--accent2); color:#fff;
    box-shadow:var(--elev4); }
  .iconbtn.del { background:var(--danger); border-color:var(--danger); color:var(--on-danger);
    font-weight:600; padding:6px 15px; box-shadow:var(--elev1); }
  .iconbtn.del:hover { background:var(--danger-strong); border-color:var(--danger-strong);
    color:var(--on-danger); box-shadow:var(--elev4); }
  .iconbtn.primary:active, .iconbtn.del:active { transform:translateY(1px); box-shadow:var(--elev1); }
  .iconbtn + .iconbtn { margin-left:10px; }   /* space between Details and Delete */
  /* dialog "copy" buttons: tinted + accent border so they stand out */
  .copybtn { background:var(--accent-soft); border-color:var(--accent); color:var(--accent); font-weight:600; }
  .copybtn:hover { background:var(--accent); border-color:var(--accent); color:#fff; }

  /* ---------- scrim + dialog ---------- */
  .scrim { position:fixed; inset:0; background:var(--scrim); opacity:0; visibility:hidden;
    transition:opacity .2s; z-index:40; }
  .scrim.show { opacity:1; visibility:visible; }
  .dialog { position:fixed; z-index:50; left:50%; top:50%;
    transform:translate(-50%,-48%) scale(.96); opacity:0; visibility:hidden;
    width:min(560px,calc(100vw - 32px)); max-height:calc(100vh - 48px); overflow:auto;
    background:var(--panel); border-radius:16px; box-shadow:var(--elev24);
    transition:opacity .2s, transform .2s; }
  .dialog.open { transform:translate(-50%,-50%) scale(1); opacity:1; visibility:visible; }
  .dialog.confirm { width:min(420px,calc(100vw - 32px)); }
  .dialog.wide { width:min(780px,calc(100vw - 32px)); }
  .np-sec { margin-top:14px; }
  .np-head { display:flex; align-items:center; justify-content:space-between; margin-bottom:6px; }
  .np-label { font-size:12px; font-weight:600; color:var(--muted); }
  .dialog .snippet { max-height:46vh; overflow:auto; }
  .dialog-title { margin:0; padding:22px 24px 6px; font-size:18px; font-weight:600; }
  .dialog-body { padding:8px 24px 4px; }
  .dialog-body p { margin:6px 0 4px; color:var(--muted); font-size:13.5px; }
  .dialog-actions { display:flex; justify-content:flex-end; gap:8px; padding:14px 18px 18px; }
  .dialog-title.danger-title { color:var(--err-fg); }
  .warn-list { margin:10px 0 4px; padding-left:18px; color:var(--muted); font-size:13px; line-height:1.5; }
  .warn-list li { margin:3px 0; }
  .warn-list li b, .warn-list li .mono { color:var(--fg); }
  label.ack { display:flex; align-items:flex-start; gap:9px; margin:14px 0 2px; padding:10px 12px;
    background:var(--err-bg); border:1px solid var(--err-bd); border-radius:9px;
    font-size:12.5px; color:var(--fg); cursor:pointer; }
  label.ack input { margin-top:1px; accent-color:var(--err-fg); flex:none; }
  .btn.text.danger:disabled { color:var(--muted); background:transparent; cursor:not-allowed; opacity:.55; }

  /* ---------- text fields (outlined, floating label) ---------- */
  .tf { position:relative; margin-top:18px; }
  .tf input { width:100%; padding:14px 13px; border:1px solid var(--line); border-radius:8px;
    background:var(--input-bg); color:var(--fg); font:14px inherit; transition:border-color .15s,box-shadow .15s; }
  .tf input:focus { outline:none; border-color:var(--accent); box-shadow:inset 0 0 0 1px var(--accent); }
  .tf input:disabled { opacity:.55; cursor:not-allowed; }
  .tf label { position:absolute; left:9px; top:14px; padding:0 5px; background:var(--panel);
    color:var(--muted); font-size:14px; pointer-events:none; transition:.14s ease; }
  .tf input:focus ~ label,
  .tf input:not(:placeholder-shown) ~ label { top:-8px; font-size:11.5px; }
  .tf input:focus ~ label { color:var(--accent); }
  .tf input:disabled ~ label { opacity:.55; }
  /* multiline (license paste) — same outlined/floating-label treatment, monospace */
  .tf textarea { width:100%; padding:14px 13px; border:1px solid var(--line); border-radius:8px;
    background:var(--input-bg); color:var(--fg);
    font:12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
    resize:vertical; min-height:80px; transition:border-color .15s,box-shadow .15s; }
  .tf textarea:focus { outline:none; border-color:var(--accent); box-shadow:inset 0 0 0 1px var(--accent); }
  .tf textarea ~ label { background:var(--panel); }
  .tf textarea:focus ~ label,
  .tf textarea:not(:placeholder-shown) ~ label { top:-8px; font-size:11.5px; }
  .tf textarea:focus ~ label { color:var(--accent); }
  /* outlined select (namespace) — label stays floated; native arrow replaced by a chevron */
  .tf.select select { width:100%; padding:14px 38px 14px 13px; border:1px solid var(--line);
    border-radius:8px; background:var(--input-bg); color:var(--fg); font:14px inherit;
    appearance:none; -webkit-appearance:none; cursor:pointer;
    transition:border-color .15s, box-shadow .15s; }
  .tf.select select:focus { outline:none; border-color:var(--accent); box-shadow:inset 0 0 0 1px var(--accent); }
  .tf.select select:required:invalid { color:var(--muted); }
  .tf.select select option { color:var(--fg); }
  .tf.select label { top:-8px; font-size:11.5px; }
  .tf.select select:focus ~ label { color:var(--accent); }
  .tf.select::after { content:""; position:absolute; right:15px; top:21px; width:8px; height:8px;
    border-right:2px solid var(--muted); border-bottom:2px solid var(--muted);
    transform:rotate(45deg); pointer-events:none; }
  .helper { margin:6px 4px 0; font-size:11.5px; color:var(--muted); line-height:1.45; }

  .filefield { margin-top:6px; }
  .filefield > .lbl { font-size:12px; color:var(--muted); font-weight:500; }
  .filebox { margin-top:7px; display:flex; align-items:center; gap:12px; flex-wrap:wrap;
    border:1px dashed var(--line); border-radius:10px; padding:13px 14px; background:var(--panel2); }
  .filebox input[type=file] { color:var(--muted); font-size:12.5px; max-width:100%; }
  .filebox input[type=file]::file-selector-button { background:var(--accent); color:#fff; border:0;
    border-radius:8px; padding:8px 16px; margin-right:12px; cursor:pointer; font-weight:600;
    font-size:12.5px; transition:background .15s; }
  .filebox input[type=file]::file-selector-button:hover { background:var(--accent2); }

  /* ---------- snackbar ---------- */
  .snackbar { position:fixed; left:50%; bottom:26px; transform:translate(-50%,140%);
    z-index:60; min-width:300px; max-width:min(560px,calc(100vw - 32px));
    background:var(--snack-bg); color:var(--snack-fg); border-radius:9px; box-shadow:var(--elev8);
    padding:13px 12px 13px 18px; display:flex; align-items:center; gap:14px;
    opacity:0; visibility:hidden; transition:transform .26s cubic-bezier(.2,.7,.3,1), opacity .26s; }
  .snackbar.show { transform:translate(-50%,0); opacity:1; visibility:visible; }
  .snackbar .stext { flex:1; font-size:13px; line-height:1.45; word-break:break-word; }
  .snackbar .sdot { width:9px; height:9px; border-radius:50%; flex:none; }
  .snackbar.ok .sdot { background:#24d45e; }
  .snackbar.err .sdot { background:#ff6b6b; }
  .snackbar .saction { background:transparent; border:0; color:var(--snack-action);
    font:600 12.5px inherit; letter-spacing:.04em; text-transform:uppercase; cursor:pointer;
    padding:6px 10px; border-radius:6px; }
  .snackbar .saction:hover { background:rgba(127,127,127,.18); }
</style>
<script>try{var _t=localStorage.getItem("imagemanager-theme")||"light";document.documentElement.setAttribute("data-theme",_t);}catch(e){}</script>
</head>
<body>
<header class="appbar">
  <span class="brand-mark"></span>
  <span class="brand-name">EDA Image Manager</span>
  <span class="sub">Upload a NOS image (SR Linux / SR OS / SR-SIM) &rarr; hosted in-cluster &rarr; ready for EDA bootstrap or the Digital Twin</span>
  <div class="appbar-actions">
    <span id="userInfo" class="user-chip" style="display:none"><span class="avatar" id="avatar"></span><span class="uname" id="uname"></span></span>
    <label class="switch" title="Toggle light / dark appearance">
      <input type="checkbox" id="themeToggle">
      <span class="track"><span class="thumb"></span></span>
      <span class="swlabel" id="themeLabel">Dark</span>
    </label>
    <a id="signoutLink" class="btn text subtle ripple" title="Sign out of Image Manager">Sign out</a>
  </div>
</header>

<main>
  <div class="page-head">
    <div>
      <h1 class="page-title">Images <span class="count" id="refreshNote" style="display:none"></span></h1>
      <p class="page-sub">Once <span class="mono">eda-asvr</span> reports an image <span class="mono">Available</span>, open its <b>node profile</b> for a ready-to-use NodeProfile.</p>
    </div>
    <div class="grow"></div>
    <button class="btn contained ripple" id="openUpload">
      <svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>
      Upload Image From File
    </button>
  </div>

  <div class="card storage-card">
    <div class="storage-row">
      <span class="storage-label">App storage</span>
      <span class="storage-stat" id="storageStat">&mdash;</span>
    </div>
    <div class="storage-track"><div class="storage-fill" id="storageFill"></div></div>
  </div>

  <div class="card">
    <div class="table-wrap">
      <table class="mtable">
        <thead><tr>
          <th class="sortable" data-sort="displayName">Name <span class="arr"></span></th>
          <th class="sortable" data-sort="namespace">Namespace <span class="arr"></span></th>
          <th class="sortable num" data-sort="sizeBytes">Size <span class="arr"></span></th>
          <th class="sortable" data-sort="downloadStatus">Status <span class="arr"></span></th>
          <th></th>
        </tr></thead>
        <tbody id="rows"><tr><td colspan="5" class="empty">Loading&hellip;</td></tr></tbody>
      </table>
    </div>
  </div>
</main>

<!-- scrim shared by all dialogs -->
<div class="scrim" id="scrim"></div>

<!-- upload dialog -->
<div class="dialog" id="uploadDialog" role="dialog" aria-modal="true" aria-labelledby="dlgTitle">
  <h2 class="dialog-title" id="dlgTitle">Upload image</h2>
  <div class="dialog-body">
    <div class="filefield">
      <span class="lbl">Vendor image &mdash; <span class="mono">.zip</span> (file or URL below)</span>
      <div class="filebox">
        <input type="file" id="binFile" accept=".zip">
      </div>
      <div class="helper" id="binHint"></div>
    </div>

    <div class="tf" style="margin-top:2px">
      <input type="text" id="importUrl" placeholder=" " autocomplete="off" spellcheck="false">
      <label for="importUrl">&hellip; or paste an image URL (optional)</label>
      <div class="helper">Leave the file box empty and paste a direct <span class="mono">https://</span> link to a vendor <span class="mono">.zip</span>; the controller downloads it server-side and creates the Artifacts. Use a file <b>or</b> a URL, not both.</div>
    </div>

    <div class="tf select">
      <select id="namespace" required>
        <option value="" disabled selected>Select a namespace&hellip;</option>
      </select>
      <label for="namespace">Namespace</label>
      <div class="helper">Choose the EDA namespace where the Artifact(s) will be created.</div>
    </div>

    <div class="tf">
      <input type="text" id="imageName" placeholder=" " autocomplete="off">
      <label for="imageName">Image name (auto-generated &mdash; edit if you like)</label>
      <div class="helper" id="nameHint">SR Linux, SR OS (7750 TiMOS) or SR-SIM (SR OS simulator) is detected automatically from the zip; the md5 and YANG schema profile are handled for you.</div>
    </div>

    <div class="tf" style="margin-top:18px">
      <textarea id="licText" placeholder=" " rows="3" spellcheck="false" autocapitalize="off" autocomplete="off"></textarea>
      <label for="licText">License key (optional) &mdash; paste it here</label>
      <div class="helper" id="licHint">Paste the SR OS / SR Linux <b>simulator license key</b> if this image needs one. Extra spaces, quotes or a leading label are fine &mdash; Image Manager parses out the key, stores it as a <span class="mono">license.key</span> ConfigMap in <span class="mono">eda-system</span>, and wires <span class="mono">spec.license</span> into the generated NodeProfile. The free SR Linux sim and SR-SIM boot without one.</div>
    </div>
  </div>
  <div class="dialog-actions">
    <button class="btn text subtle ripple" id="cancelUpload">Cancel</button>
    <button class="btn contained ripple" id="uploadBtn">Upload &amp; create Artifact</button>
  </div>
</div>

<!-- nodeprofile dialog -->
<div class="dialog wide" id="npDialog" role="dialog" aria-modal="true" aria-labelledby="npTitle">
  <h2 class="dialog-title" id="npTitle">NodeProfile</h2>
  <div class="dialog-body">
    <p id="npIntro">Paste the <b>snippet</b> into an existing <span class="mono">NodeProfile</span>'s <span class="mono">spec.images</span>, or copy the <b>complete example</b> as a starting point. The image path(s), version, OS and <span class="mono">yang</span> are filled from this image; <span class="mono">&lt;…&gt;</span> values are for you to set.</p>
    <div class="np-sec">
      <div class="np-head"><span class="np-label" id="npSnipLabel">Snippet &mdash; <span class="mono">spec.images</span></span><button class="iconbtn copybtn ripple" id="npCopySnip">Copy</button></div>
      <pre class="snippet" id="npSnippet"></pre>
    </div>
    <div class="np-sec">
      <div class="np-head"><span class="np-label">Complete NodeProfile example</span><button class="iconbtn copybtn ripple" id="npCopyFull">Copy</button></div>
      <pre class="snippet" id="npFull"></pre>
    </div>
  </div>
  <div class="dialog-actions">
    <button class="btn text subtle ripple" id="npClose">Close</button>
  </div>
</div>

<!-- delete-artifact confirm dialog (warning + explicit acknowledgement) -->
<div class="dialog confirm" id="confirmDialog" role="dialog" aria-modal="true" aria-labelledby="confirmTitle">
  <h2 class="dialog-title danger-title" id="confirmTitle">Delete artifact</h2>
  <div class="dialog-body">
    <p id="confirmLead"></p>
    <ul class="warn-list" id="confirmList"></ul>
    <label class="ack"><input type="checkbox" id="confirmAck"> I understand this permanently removes the artifact and can't be undone.</label>
  </div>
  <div class="dialog-actions">
    <button class="btn text subtle ripple" id="confirmCancel">Cancel</button>
    <button class="btn text danger ripple" id="confirmOk" disabled>Delete artifact</button>
  </div>
</div>

<!-- snackbar -->
<div class="snackbar" id="snackbar">
  <span class="sdot"></span>
  <span class="stext" id="snackText"></span>
  <button class="saction" id="snackClose">Dismiss</button>
</div>

<script>
(function(){
  var apiBase = location.pathname.replace(/\/+$/, "");
  function api(p){ return apiBase + p; }
  var maxBytes = 4096*1024*1024;

  var el = function(id){ return document.getElementById(id); };
  var binFile=el("binFile"), ns=el("namespace"), imageName=el("imageName"),
      btn=el("uploadBtn"), binHint=el("binHint"), rows=el("rows"), licText=el("licText"),
      importUrl=el("importUrl");

  // Lenient structure check: does ANY single line contain a "<node-id> <key>"
  // entry? Surrounding labels / quotes / blank lines don't matter. Tested per-line
  // to mirror the server parser exactly (which iterates lines), so the GUI never
  // accepts a paste the server would then reject.
  function looksLikeLicense(t){
    var RE=/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\s+[A-Za-z0-9+/=]{16,}/;
    return (t||"").split(/\r?\n/).some(function(l){ return RE.test(l); });
  }
  var signout=el("signoutLink"); if(signout) signout.href=apiBase+"/oauth/logout";

  // ---------- ripple ----------
  document.body.addEventListener("pointerdown", function(e){
    var t = e.target.closest(".ripple"); if(!t) return;
    if(t.disabled) return;
    var r = t.getBoundingClientRect(), s = Math.max(r.width, r.height);
    var ink = document.createElement("span");
    ink.className = "ripple-ink";
    ink.style.width = ink.style.height = s + "px";
    ink.style.left = (e.clientX - r.left - s/2) + "px";
    ink.style.top = (e.clientY - r.top - s/2) + "px";
    t.appendChild(ink);
    setTimeout(function(){ ink.remove(); }, 560);
  });

  // ---------- helpers ----------
  function fmtBytes(n){
    if(n==null) return "";
    var u=["B","KiB","MiB","GiB","TiB"], i=0; n=Number(n);
    while(n>=1024 && i<u.length-1){ n/=1024; i++; }
    return n.toFixed(i?1:0)+" "+u[i];
  }
  function isZip(name){ return /\.zip$/i.test(name||""); }
  function esc(s){ return String(s==null?"":s).replace(/[&<>"]/g,function(m){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[m]; }); }
  // Suggest a name from the filename; the NOS is detected server-side from the
  // zip contents, so this is just a friendly default the user may edit.
  // Names are always lowercase (Artifact + served path + NodeProfile name), so
  // capitals can never sneak into an EDA object name.
  function deriveName(fn){
    var base=(fn||"").split(/[\\/]/).pop();
    var stem=base.replace(/\.[A-Za-z0-9]+$/,"");
    if(/sr[ _-]?sim/i.test(base)){   // SR-SIM (container image) — distinct from HW SR OS
      var xm=base.match(/(\d+\.\d+\.[Rr]\d+)/)||base.match(/(\d+\.\d+\.\d+(?:-\d+)?)/);
      if(xm) return ("srsim-"+xm[1]).toLowerCase();
    }
    if(/sr[ _-]?linux/i.test(base)){
      var m=base.match(/(\d+\.\d+\.\d+(?:-\d+)?)/);
      if(m) return ("srlinux-"+m[1]).toLowerCase();
    }
    var s=base.match(/(\d+\.\d+\.[Rr]\d+)/);   // SR OS style, e.g. 26.3.R3
    if(s) return ("sros-"+s[1]).toLowerCase();
    return (stem||"image").toLowerCase();
  }

  // ---------- snackbar ----------
  var snackbar=el("snackbar"), snackText=el("snackText"), snackTimer=null;
  function snack(kind, text, sticky){
    snackbar.className = "snackbar show " + (kind==="ok"?"ok":"err");
    snackText.textContent = text;
    if(snackTimer){ clearTimeout(snackTimer); snackTimer=null; }
    if(!sticky){ snackTimer=setTimeout(hideSnack, kind==="ok"?6000:9000); }
  }
  function hideSnack(){ snackbar.classList.remove("show"); }
  el("snackClose").addEventListener("click", hideSnack);

  // ---------- modal infrastructure ----------
  var scrim=el("scrim"), openDlg=null;
  function openModal(d){
    openDlg=d; scrim.classList.add("show"); d.classList.add("open");
    document.body.style.overflow="hidden";
    var f=d.querySelector("input:not([type=file]),button,select,textarea");
    if(f){ try{ f.focus(); }catch(e){} }
  }
  function closeModal(){
    if(openDlg){ openDlg.classList.remove("open"); }
    scrim.classList.remove("show"); document.body.style.overflow=""; openDlg=null;
  }
  scrim.addEventListener("click", closeModal);
  document.addEventListener("keydown", function(e){ if(e.key==="Escape" && openDlg) closeModal(); });

  el("openUpload").addEventListener("click", function(){ openModal(el("uploadDialog")); });
  el("cancelUpload").addEventListener("click", closeModal);

  // ---------- delete-artifact confirm dialog ----------
  // The destructive Delete button stays disabled until the user ticks the
  // acknowledgement, so deletion is always an informed, explicit action.
  var confirmLead=el("confirmLead"), confirmList=el("confirmList"),
      confirmAck=el("confirmAck"), confirmOk=el("confirmOk"), pendingConfirm=null;
  confirmAck.addEventListener("change", function(){ confirmOk.disabled = !confirmAck.checked; });
  el("confirmCancel").addEventListener("click", closeModal);
  confirmOk.addEventListener("click", function(){
    if(!confirmAck.checked) return;
    var fn=pendingConfirm; pendingConfirm=null; closeModal(); if(fn) fn();
  });
  function askDelete(lead, items, onYes){
    confirmLead.innerHTML = lead;
    confirmList.innerHTML = items.map(function(s){ return "<li>"+s+"</li>"; }).join("");
    confirmAck.checked=false; confirmOk.disabled=true; pendingConfirm=onYes;
    openModal(el("confirmDialog"));
  }

  // ---------- config + namespaces ----------
  fetch(api("/api/config")).then(function(r){return r.json();}).then(function(c){
    // No default namespace: the user must pick one from the dropdown.
    if(c.maxUploadMiB) maxBytes=c.maxUploadMiB*1024*1024;
    binHint.textContent="Maximum upload size: "+c.maxUploadMiB+" MiB.";
    if(c.user){
      var ui=el("userInfo"); ui.style.display="inline-flex";
      el("uname").textContent=c.user;
      el("avatar").textContent=(c.user||"?").slice(0,1);
    }
  }).catch(function(){});

  fetch(api("/api/namespaces")).then(function(r){return r.json();}).then(function(d){
    (d.namespaces||[]).forEach(function(n){
      var o=document.createElement("option"); o.value=n; o.textContent=n; ns.appendChild(o);
    });
  }).catch(function(){});

  // ---------- file selection ----------
  binFile.addEventListener("change", function(){
    var f=binFile.files[0];
    if(!f) return;
    imageName.value = deriveName(f.name);
    binHint.textContent=f.name+"  ·  "+fmtBytes(f.size);
  });
  // Names are lowercased everywhere; keep the field lowercase as the user edits.
  imageName.addEventListener("input", function(ev){
    if(ev && ev.isComposing) return;   // don't disturb a mid-IME composition
    var s=imageName.selectionStart, e=imageName.selectionEnd, lo=imageName.value.toLowerCase();
    if(lo!==imageName.value){ imageName.value=lo; try{ imageName.setSelectionRange(s,e); }catch(_){} }
  });

  // ---------- upload (closes dialog; progress shown as a live table row) ----------
  function resetUploadForm(){
    binFile.value=""; imageName.value=""; ns.selectedIndex=0; licText.value=""; if(importUrl) importUrl.value="";
    binHint.textContent="Maximum upload size: "+Math.round(maxBytes/1048576)+" MiB.";
  }

  // Attach a license to a freshly-uploaded image: POST the raw key file to
  // /api/license. Additive — a failure here never undoes the image upload. baseMsg
  // is the image-upload snack text, folded in so the user sees one coherent result
  // (no green flash that's instantly overwritten).
  function attachLicense(uploadId, what, licStr, baseMsg){
    var pre=baseMsg?(baseMsg+" "):"";
    if(!uploadId || !licStr) { if(baseMsg) snack("ok", baseMsg); refresh(); return; }
    var qs=new URLSearchParams({uploadId:uploadId});
    var xhr=new XMLHttpRequest();
    xhr.open("POST", api("/api/license")+"?"+qs.toString());
    xhr.setRequestHeader("Content-Type","text/plain; charset=utf-8");
    xhr.onload=function(){ var r={}; try{ r=JSON.parse(xhr.responseText); }catch(e){}
      if(xhr.status>=200 && xhr.status<300 && r.ok){
        var warn=r.mismatch?(" Note: that key looks like a "+(r.licenseNos||"different")+
                 " license but the image is "+(r.imageNos||"")+"; using it anyway."):"";
        snack("ok", pre+"License attached."+warn, !!r.mismatch);
      } else {
        snack("err", pre+"But the license could not be attached: "+
              ((r&&r.error)||("HTTP "+xhr.status)), true);
      }
      refresh();
    };
    xhr.onerror=function(){ snack("err", pre+"But attaching the license failed (network).", true); refresh(); };
    xhr.send(licStr);
  }
  function paintPendingCell(p){
    var c=document.getElementById("upstat-"+p.key);
    if(c) c.innerHTML=pendStatusHtml(p); else render();
  }

  // Shared XHR uploader: streams `file` to `url`, driving the live pending row `p`.
  function sendUpload(url, file, p, handlers){
    var xhr=new XMLHttpRequest();
    xhr.open("POST", url);
    var startT=Date.now();
    xhr.upload.onprogress=function(e){
      if(!e.lengthComputable) return;
      p.loaded=e.loaded; p.total=e.total||p.total;
      p.pct=p.total ? (e.loaded/p.total*100) : 0;
      p.elapsed=(Date.now()-startT)/1000;
      p.speed=p.elapsed>0 ? (e.loaded/1048576/p.elapsed) : 0;
      paintPendingCell(p);
    };
    xhr.upload.onload=function(){ if(handlers.onBodySent) handlers.onBodySent(); };
    xhr.onload=function(){ var r={}; try{ r=JSON.parse(xhr.responseText);}catch(e){}
      handlers.onDone(xhr.status, r); };
    xhr.onerror=function(){ handlers.onError(); };
    xhr.send(file);
    return xhr;
  }

  // Single upload path. The NOS is auto-detected server-side from the zip; md5
  // and the YANG schema profile are handled automatically.
  function doUpload(f, namespace, lic){
    // Lowercase unconditionally here (the authoritative client-side point), so the
    // query param and the live pending row match the server's lowercased name
    // regardless of how text reached the field — the input listener is then cosmetic.
    var name=(imageName.value||deriveName(f.name)).trim().toLowerCase();
    var qs=new URLSearchParams({ filename:f.name, namespace:namespace, name:name });
    var key="u"+(++uploadSeq);
    var p={ key:key, displayName:name, namespace:namespace, total:f.size, isZip:true,
            phase:"Uploading", loaded:0, pct:0, speed:0, elapsed:0 };
    pendingUploads[key]=p; closeModal(); resetUploadForm(); render();
    sendUpload(api("/api/upload")+"?"+qs.toString(), f, p, {
      onBodySent:function(){ p.phase="Unzipping"; paintPendingCell(p); },
      onDone:function(status, r){
        if(status>=200 && status<300 && r.ok){
          // The authoritative row now exists server-side; clear the pending row.
          delete pendingUploads[key];
          var what=(r.displayName||name), msg;
          if(r.nos==="srsim") msg="Uploaded "+what+" — SR-SIM image ready. Open Details for the sim NodeProfile and one-time setup."+(r.yangCreated?" YANG profile attached.":"");
          else if(r.nos==="sros") msg="Uploaded "+what+" — "+(r.fileCount||0)+" image files. "+(r.note||"");
          else msg="Uploaded "+what+"."+(r.md5?(" md5 "+r.md5+"."):"")+(r.yangCreated?" YANG profile attached.":"");
          if(lic){ attachLicense(r.artifactName||r.uploadId||name, what, lic, msg); }
          else { snack("ok", msg); refresh(); }
        } else { delete pendingUploads[key]; render();
          snack("err",(r.error||("HTTP "+status)), true); if(r.uploadId) refresh(); }
      },
      onError:function(){ delete pendingUploads[key]; render();
        snack("err","Network error during upload.", true); }
    });
  }

  // URL import: the controller downloads the zip server-side (no browser upload
  // progress bar), then runs the SAME detect + finish path as a file upload.
  function doImportUrl(url, namespace, lic){
    var guessFn=(url.split(/[?#]/)[0].split(/[\\/]/).pop())||"import.zip";
    var name=(imageName.value||deriveName(guessFn)).trim().toLowerCase();
    var qs=new URLSearchParams({ url:url, namespace:namespace, name:name });
    var key="u"+(++uploadSeq);
    var p={ key:key, displayName:name, namespace:namespace, total:null, isZip:true,
            phase:"Downloading", loaded:0, pct:0, speed:0, elapsed:0 };
    pendingUploads[key]=p; closeModal(); resetUploadForm(); render();
    var xhr=new XMLHttpRequest();
    xhr.open("POST", api("/api/import-url")+"?"+qs.toString());
    xhr.onload=function(){ var r={}; try{ r=JSON.parse(xhr.responseText);}catch(e){}
      if(xhr.status>=200 && xhr.status<300 && r.ok){
        delete pendingUploads[key];
        var what=(r.displayName||name), msg;
        if(r.nos==="srsim") msg="Imported "+what+" — SR-SIM image ready. Open Details for the sim NodeProfile.";
        else if(r.nos==="sros") msg="Imported "+what+" — "+(r.fileCount||0)+" image files. "+(r.note||"");
        else msg="Imported "+what+"."+(r.md5?(" md5 "+r.md5+"."):"")+(r.yangCreated?" YANG profile attached.":"");
        if(lic){ attachLicense(r.artifactName||r.uploadId||name, what, lic, msg); }
        else { snack("ok", msg); refresh(); }
      } else { delete pendingUploads[key]; render();
        snack("err",(r.error||("HTTP "+xhr.status)), true); if(r.uploadId) refresh(); }
    };
    xhr.onerror=function(){ delete pendingUploads[key]; render();
      snack("err","Network error starting the URL import.", true); };
    xhr.send();
  }

  btn.addEventListener("click", function(){
    var f=binFile.files[0];
    var url=(importUrl.value||"").trim();
    // Either a local file OR a URL — validate whichever was provided.
    if(!f && !url){ snack("err","Select a vendor .zip file, or paste an image URL."); return; }
    if(f && url){ snack("err","Provide a file OR a URL, not both."); return; }
    if(f && !isZip(f.name)){ snack("err","Only vendor .zip images are supported (SR Linux or SR OS)."); return; }
    if(f && f.size>maxBytes){ snack("err","File is "+fmtBytes(f.size)+", over the "+fmtBytes(maxBytes)+" limit."); return; }
    if(url && !/^https?:\/\//i.test(url)){ snack("err","The URL must start with http:// or https://."); return; }
    var namespace=(ns.value||"").trim();
    if(!namespace){ snack("err","Choose a namespace first."); return; }
    var lic=(licText.value||"").trim();   // optional pasted license key
    if(lic && lic.length>262144){ snack("err","License text is too large (expected a small key)."); return; }
    if(lic && !looksLikeLicense(lic)){ snack("err","That doesn't look like a license key — paste the full “<node-id> <key>” line (extra spaces, quotes or a label are fine)."); return; }
    if(url){ doImportUrl(url, namespace, lic); } else { doUpload(f, namespace, lic); }
  });

  // ---------- artifacts table ----------
  var pendingUploads={}, uploadSeq=0;   // in-flight browser->controller uploads (client-side)
  function chip(s){ var c=s||"NoArtifact"; return '<span class="chip c-'+c+'">'+esc(c)+'</span>'; }
  function fmtElapsed(sec){ sec=Math.max(0,Math.floor(sec)); var m=Math.floor(sec/60), s=sec%60;
    return m+":"+(s<10?"0":"")+s; }

  function pendStatusHtml(p){
    if(p.phase==="Uploading"){
      var line=p.pct.toFixed(0)+"%  ·  "+fmtBytes(p.loaded)+" / "+fmtBytes(p.total)+
               "  ·  "+p.speed.toFixed(1)+" MB/s  ·  "+fmtElapsed(p.elapsed);
      return '<span class="chip c-Uploading">Uploading</span>'+
             '<div class="uprog"><div style="width:'+p.pct.toFixed(1)+'%"></div></div>'+
             '<div class="upinfo">'+esc(line)+'</div>';
    }
    var label = p.phase==="Unzipping" ? "Un-zipping" : (p.phase==="Downloading" ? "Downloading" : "Finalizing");
    var sub   = p.phase==="Unzipping" ? "extracting image + reading md5" : (p.phase==="Downloading" ? "fetching + processing on the server" : "creating Artifact");
    var cls   = p.phase==="Downloading" ? "Uploading" : p.phase;
    return '<span class="chip c-'+cls+'">'+label+'</span>'+
           '<div class="uprog indet"><div></div></div>'+
           '<div class="upinfo">'+esc(sub)+'</div>';
  }
  function pendingRowHtml(p){
    return '<tr><td class="mono namecell">'+esc(p.displayName)+'</td><td>'+esc(p.namespace)+
      '</td><td class="num">'+fmtBytes(p.total)+'</td><td id="upstat-'+p.key+'">'+pendStatusHtml(p)+
      '</td><td></td></tr>';
  }
  function serverRowHtml(t){
    var reason=t.statusReason?('<div class="reason">'+esc(t.statusReason)+'</div>'):'';
    var fcount=(t.nos==="sros" && t.fileCount)?('<div class="upinfo">'+t.fileCount+' image files'+(t.yangStatus?' + yang':'')+'</div>'):'';
    var lic=t.license?('<div class="upinfo">+ license &middot; '+esc(t.licenseNos||'key')+'</div>'):'';
    var view=t.snippet
      ?('<button class="iconbtn primary ripple" data-act="view" data-uid="'+esc(t.uploadId||"")+'">Details</button> ')
      :'';
    var del='<button class="iconbtn del ripple" data-act="del" data-uid="'+esc(t.uploadId||"")+'" data-ns="'+esc(t.namespace||"")+'" data-name="'+esc(t.name||"")+'">Delete</button>';
    return '<tr><td class="mono namecell">'+esc(t.displayName||t.name)+fcount+lic+'</td><td>'+esc(t.namespace)+
      '</td><td class="num">'+fmtBytes(t.sizeBytes)+'</td><td>'+chip(t.downloadStatus)+reason+
      '</td><td style="white-space:nowrap">'+view+del+'</td></tr>';
  }

  function imDelete(uid, nsv, name){
    var t=null;
    for(var i=0;i<currentData.length;i++){ if(currentData[i].uploadId===uid){ t=currentData[i]; break; } }
    var label=name||uid||"this image";
    var hasYang=!!(t && t.yangStatus);
    var isSrsim=(t && t.nos==="srsim");
    var removes=isSrsim
      ? ("Removes the SR-SIM container image from this app's registry"
         +(hasYang?", and its YANG schema-profile Artifact":"")+".")
      : (t && t.nos==="sros")
      ? ('Removes all '+(t.fileCount||'the')+' boot-image Artifacts, their md5 Artifacts'
         +(hasYang?', and the YANG schema-profile Artifact':'')+' from EDA.')
      : ('Removes the image Artifact, its md5 Artifact'
         +(hasYang?', and the YANG schema-profile Artifact':'')+' from EDA.');
    var hostBullet=isSrsim
      ? "EDA's Digital Twin (eda-cx) can no longer pull this image — creating or restarting a sim that uses it will fail."
      : '<span class="mono">eda-asvr</span> stops hosting it — the served image URLs will return 404.';
    var lead='Permanently delete <b class="mono">'+esc(label)+'</b>'
             +(nsv?(' in <span class="mono">'+esc(nsv)+'</span>'):'')+'?';
    var bullets=[
      removes,
      hostBullet,
      'Any NodeProfile, node bootstrap (ZTP) or image upgrade that points at this image will fail until you re-add a valid image.',
      'This app holds the only durable copy, so its local file is deleted too — to restore it you must re-upload the vendor .zip.',
      'This cannot be undone.'
    ];
    if(t && t.license){ bullets.splice(1, 0, 'Also deletes the license ConfigMap <span class="mono">'+esc(t.license)+'</span> from <span class="mono">eda-system</span>.'); }
    askDelete(lead, bullets, function(){
      var qs=new URLSearchParams({uploadId:uid||"", namespace:nsv||"", name:name||""});
      fetch(api("/api/delete")+"?"+qs.toString(), {method:"POST"})
        .then(function(r){return r.json();})
        .then(function(d){ if(d && d.ok){ snack("ok","Deleted "+label+"."); refresh(); }
                           else { snack("err","Delete failed: "+((d&&d.error)||"unknown"), true); } })
        .catch(function(){ snack("err","Delete failed (network).", true); });
    });
  }

  // ---------- NodeProfile dialog (snippet + complete example) ----------
  var npSnippet=el("npSnippet"), npFull=el("npFull");
  function copyBtn(btn, text){
    if(navigator.clipboard) navigator.clipboard.writeText(text||"");
    var t0=btn.textContent; btn.textContent="Copied"; setTimeout(function(){ btn.textContent=t0; }, 1200);
  }
  function openNodeProfile(uid){
    var t=null;
    for(var i=0;i<currentData.length;i++){ if(currentData[i].uploadId===uid){ t=currentData[i]; break; } }
    if(!t) return;
    el("npTitle").textContent = "NodeProfile — " + (t.displayName||t.name||"");
    // SR-SIM emits a containerImage-based sim NodeProfile, not a spec.images
    // fragment; relabel the snippet section + intro accordingly.
    var isSim=(t.nos==="srsim");
    el("npIntro").innerHTML = isSim
      ? 'Copy the <b>complete sim NodeProfile</b> below, or paste the <b>snippet</b> fields into an existing <span class="mono">NodeProfile</span>. The <span class="mono">containerImage</span>, version and <span class="mono">yang</span> are filled from this image; <span class="mono">&lt;…&gt;</span> values are for you to set.'
      : 'Paste the <b>snippet</b> into an existing <span class="mono">NodeProfile</span>\'s <span class="mono">spec.images</span>, or copy the <b>complete example</b> as a starting point. The image path(s), version, OS and <span class="mono">yang</span> are filled from this image; <span class="mono">&lt;…&gt;</span> values are for you to set.';
    if(t.license){
      el("npIntro").innerHTML += ' <b>License:</b> Image Manager created the ConfigMap '+
        '<span class="mono">'+esc(t.license)+'</span> in <span class="mono">eda-system</span> '+
        'from your uploaded key and referenced it in <span class="mono">spec.license</span> below.';
    }
    el("npSnipLabel").innerHTML = isSim
      ? 'Snippet &mdash; sim NodeProfile <span class="mono">spec</span>'
      : 'Snippet &mdash; <span class="mono">spec.images</span>';
    npSnippet.textContent = t.snippet || "(not ready yet)";
    npFull.textContent = t.nodeProfileExample || "(ready once the image is Available)";
    openModal(el("npDialog"));
  }
  el("npClose").addEventListener("click", closeModal);
  el("npCopySnip").addEventListener("click", function(){ copyBtn(this, npSnippet.textContent); });
  el("npCopyFull").addEventListener("click", function(){ copyBtn(this, npFull.textContent); });

  rows.addEventListener("click", function(e){
    var b = e.target.closest("button[data-act]");
    if(!b) return;
    if(b.getAttribute("data-act")==="view"){
      openNodeProfile(b.getAttribute("data-uid"));
    } else if(b.getAttribute("data-act")==="del"){
      imDelete(b.getAttribute("data-uid"), b.getAttribute("data-ns"), b.getAttribute("data-name"));
    }
  });

  // sorting
  var STATUS_RANK={Available:0,Ready:0,InProgress:1,Error:2,Failed:3,NoArtifact:4};
  var currentData=[], sortState=null;  // null = server order (newest first)
  function sortData(arr){
    if(!sortState) return arr;
    var col=sortState.col, dir=sortState.dir, c=arr.slice();
    c.sort(function(a,b){
      var x,y;
      if(col==="sizeBytes"){ x=Number(a.sizeBytes||0); y=Number(b.sizeBytes||0); }
      else if(col==="downloadStatus"){ var rs=function(v){ return v in STATUS_RANK?STATUS_RANK[v]:9; };
        x=rs(a.downloadStatus); y=rs(b.downloadStatus); }
      else if(col==="displayName"){ x=(a.displayName||a.name||"").toLowerCase(); y=(b.displayName||b.name||"").toLowerCase(); }
      else { x=String(a[col]==null?"":a[col]).toLowerCase(); y=String(b[col]==null?"":b[col]).toLowerCase(); }
      if(x<y) return dir==="asc"?-1:1;
      if(x>y) return dir==="asc"?1:-1;
      return 0;
    });
    return c;
  }
  function paintHeaders(){
    var ths=document.querySelectorAll(".mtable th.sortable");
    ths.forEach(function(th){
      var col=th.getAttribute("data-sort");
      var arr=th.querySelector(".arr");
      if(sortState && sortState.col===col){
        th.classList.add("sorted"); arr.textContent = sortState.dir==="asc"?"▲":"▼";
      } else { th.classList.remove("sorted"); arr.textContent="↕"; }
    });
  }
  document.querySelectorAll(".mtable th.sortable").forEach(function(th){
    th.addEventListener("click", function(){
      var col=th.getAttribute("data-sort");
      if(sortState && sortState.col===col){ sortState.dir = sortState.dir==="asc"?"desc":"asc"; }
      else { sortState={col:col, dir:"asc"}; }
      paintHeaders(); render();
    });
  });
  paintHeaders();

  function render(){
    var serverRows=sortData(currentData);
    var seen={};
    currentData.forEach(function(t){ seen[(t.displayName||t.name)+"|"+t.namespace]=true; });
    var pend=[];
    Object.keys(pendingUploads).forEach(function(k){
      var p=pendingUploads[k];
      if(!seen[p.displayName+"|"+p.namespace]) pend.push(p);  // hide once the real artifact appears
    });
    if(!(pend.length+serverRows.length)){
      rows.innerHTML='<tr><td colspan="5" class="empty">No images yet. Click <b>Upload Image From File</b> to add one.</td></tr>';
      el("refreshNote").style.display="none"; return;
    }
    rows.innerHTML = pend.map(pendingRowHtml).join("") + serverRows.map(serverRowHtml).join("");
    el("refreshNote").style.display="inline-block";
    el("refreshNote").textContent=pend.length+serverRows.length;
  }

  function fmtGB(b){ return ((b||0)/1073741824).toFixed(1)+" GB"; }
  function updateStorage(s){
    if(!s) return;
    var pct=(typeof s.usedPercent==="number")?s.usedPercent:0;
    var fill=el("storageFill");
    fill.style.width=Math.max(0,Math.min(100,pct))+"%";
    fill.className="storage-fill"+(pct>=90?" crit":(pct>=75?" warn":""));
    el("storageStat").innerHTML='<span class="mono">'+pct+'%</span> used &middot; <span class="mono">'+
      fmtGB(s.freeBytes)+'</span> free of <span class="mono">'+fmtGB(s.totalBytes)+'</span>';
  }

  function refresh(){
    fetch(api("/api/artifacts")).then(function(r){
      if(r.status===401){ location.reload(); return null; }  // session expired -> re-login
      return r.json();
    }).then(function(d){
      if(!d) return;
      currentData=d.artifacts||[];
      updateStorage(d.storage);
      // drop any in-flight upload that the controller has now turned into an Artifact
      Object.keys(pendingUploads).forEach(function(k){
        var p=pendingUploads[k];
        if(currentData.some(function(t){ return (t.displayName||t.name)===p.displayName && t.namespace===p.namespace; }))
          delete pendingUploads[k];
      });
      render();
    }).catch(function(){});
  }

  // ---------- theme switch ----------
  (function(){
    var t=el("themeToggle"), lab=el("themeLabel");
    function sync(){
      var dark=document.documentElement.getAttribute("data-theme")==="dark";
      t.checked=dark; lab.textContent=dark?"Light":"Dark";
    }
    sync();
    t.addEventListener("change", function(){
      var next=t.checked?"dark":"light";
      document.documentElement.setAttribute("data-theme", next);
      try{ localStorage.setItem("imagemanager-theme", next); }catch(e){}
      sync();
    });
  })();

  refresh(); setInterval(refresh, 5000);
})();
</script>
</body>
</html>
"""
