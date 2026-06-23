"""Self-contained upload web UI (no external assets), served at GET /.

Styled to match the Nokia EDA GUI (MUI-based design tokens): light page with
white cards, Nokia-blue (#005AFF) accent, soft shadows, "Nokia Pure Text" font,
and a LIGHT/DARK toggle whose palette mirrors EDA's own appearance themes
(light surfaces #F7F9FD/#FFFFFF, dark surfaces #101824/#1A222E)."""

INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>EDA Image Manager</title>
<style>
  :root {
    --bg:#f7f9fd; --topbar:#ffffff; --panel:#ffffff; --panel2:#f2f4f8; --input-bg:#ffffff;
    --line:#d9dee7; --fg:#2b2b2b; --muted:#687282; --accent:#005aff; --accent2:#0a44ad;
    --accent-soft:#ecf3ff; --row-hover:rgba(0,90,255,.04);
    --ok-fg:#00822b; --ok-bg:#e3fcec; --ok-bd:#24d45e;
    --info-fg:#0a44ad; --info-bg:#ecf3ff; --info-bd:#0a44ad;
    --err-fg:#911a1a; --err-bg:#ffeded; --err-bd:#d32f2f;
    --neutral-fg:#687282; --neutral-bg:#f2f2f2; --neutral-bd:#cfcfcf;
    --shadow:0 1px 8px rgba(0,0,0,.08);
  }
  html[data-theme="dark"] {
    --bg:#101824; --topbar:#101824; --panel:#1a222e; --panel2:#2e353e; --input-bg:#222c37;
    --line:#2c3644; --fg:#e6edf3; --muted:#8b98a6; --accent:#4d8dff; --accent2:#6aa4ff;
    --accent-soft:#1b2740; --row-hover:rgba(255,255,255,.03);
    --ok-fg:#5ee58b; --ok-bg:rgba(36,212,94,.13); --ok-bd:#24d45e;
    --info-fg:#90b7ff; --info-bg:rgba(144,183,255,.12); --info-bd:#4d8dff;
    --err-fg:#ff9b9b; --err-bg:rgba(211,47,47,.16); --err-bd:#d32f2f;
    --neutral-fg:#abb4c2; --neutral-bg:rgba(171,180,194,.12); --neutral-bd:#3a4452;
    --shadow:0 1px 4px rgba(0,0,0,.35);
  }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--fg);
    font:14px/1.5 "Nokia Pure Text","Inter","Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
  header { height:52px; padding:0 22px; border-bottom:1px solid var(--line);
    background:var(--topbar); display:flex; align-items:center; gap:14px; }
  .brand { display:flex; align-items:center; gap:10px; }
  .brand-mark { width:16px; height:16px; border-radius:4px; background:var(--accent);
    box-shadow:0 0 0 3px color-mix(in srgb,var(--accent) 20%,transparent); }
  .brand-name { font-size:16px; font-weight:600; letter-spacing:.01em; }
  header .sub { color:var(--muted); font-size:12.5px; }
  .ghostbtn { margin-left:auto; background:transparent; border:1px solid var(--line);
    color:var(--muted); border-radius:4px; padding:6px 12px; font-size:12.5px; cursor:pointer; }
  .ghostbtn:hover { background:var(--panel2); color:var(--fg); }
  main { max-width:1180px; margin:0 auto; padding:24px 20px 40px; }
  .card { background:var(--panel); border:1px solid var(--line); border-radius:8px;
    box-shadow:var(--shadow); padding:20px 22px; margin-bottom:20px; }
  .card h2 { margin:0; font-size:15px; font-weight:600; }
  .card .cardsub { color:var(--muted); font-size:12.5px; margin:3px 0 16px; }
  .grid { display:grid; grid-template-columns:1fr 1fr; gap:15px 18px; }
  .field { display:flex; flex-direction:column; gap:5px; }
  .field.full { grid-column:1 / -1; }
  label { font-size:12px; color:var(--muted); font-weight:500; }
  input[type=text], input[type=file] { background:var(--input-bg); border:1px solid var(--line);
    color:var(--fg); border-radius:4px; padding:9px 11px; font-size:13px; width:100%; }
  input[type=text]:focus { outline:none; border-color:var(--accent);
    box-shadow:0 0 0 3px color-mix(in srgb,var(--accent) 18%,transparent); }
  input[type=text]:disabled { opacity:.5; cursor:not-allowed; }
  input[type=file]::file-selector-button { background:var(--accent); color:#fff; border:0;
    border-radius:4px; padding:7px 14px; margin-right:11px; cursor:pointer; font-weight:600;
    font-size:12.5px; }
  input[type=file]::file-selector-button:hover { background:var(--accent2); }
  .hint { font-size:11.5px; color:var(--muted); }
  .row { display:flex; align-items:center; gap:14px; margin-top:18px; }
  button.primary { background:var(--accent); color:#fff; border:0; border-radius:4px;
    padding:9px 20px; font-size:13.5px; font-weight:600; cursor:pointer; }
  button.primary:hover { background:var(--accent2); }
  button.primary:disabled { background:var(--neutral-bd); cursor:not-allowed; }
  .progwrap { flex:1; display:none; }
  .progress { height:7px; background:var(--panel2); border-radius:4px; overflow:hidden; }
  .progress > div { height:100%; width:0; background:var(--accent); transition:width .15s; }
  .progtext { font-size:12px; color:var(--muted); margin-top:6px;
    font-family:ui-monospace,SFMono-Regular,Menlo,monospace; }
  .msg { margin-top:15px; padding:11px 14px; border-radius:4px; font-size:13px; display:none;
    white-space:pre-wrap; word-break:break-word; border:1px solid transparent; }
  .msg.ok { background:var(--ok-bg); border-color:var(--ok-bd); color:var(--ok-fg); display:block; }
  .msg.err { background:var(--err-bg); border-color:var(--err-bd); color:var(--err-fg); display:block; }
  table { width:100%; border-collapse:collapse; font-size:13px; }
  th, td { text-align:left; padding:10px 12px; border-bottom:1px solid var(--line); vertical-align:top; }
  thead th { color:var(--muted); font-weight:600; font-size:11px; text-transform:uppercase;
    letter-spacing:.05em; border-bottom:1px solid var(--line); }
  tbody tr:hover { background:var(--row-hover); }
  td.mono, .mono { font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:12px; }
  .badge { display:inline-block; padding:2px 10px; border-radius:11px; font-size:11px;
    font-weight:600; border:1px solid transparent; }
  .b-Available { background:var(--ok-bg); color:var(--ok-fg); border-color:var(--ok-bd); }
  .b-InProgress { background:var(--info-bg); color:var(--info-fg); border-color:var(--info-bd); }
  .b-Error, .b-Failed { background:var(--err-bg); color:var(--err-fg); border-color:var(--err-bd); }
  .b-NoArtifact, .b-empty { background:var(--neutral-bg); color:var(--neutral-fg); border-color:var(--neutral-bd); }
  .empty { color:var(--muted); padding:18px 4px; }
  .iconbtn { background:var(--panel2); border:1px solid var(--line); color:var(--fg);
    border-radius:4px; padding:4px 10px; font-size:11.5px; cursor:pointer; }
  .iconbtn:hover { border-color:var(--accent); color:var(--accent); }
  .delbtn { background:transparent; border-color:var(--err-bd); color:var(--err-fg); }
  .delbtn:hover { background:var(--err-bg); border-color:var(--err-bd); color:var(--err-fg); }
  .reason { color:var(--err-fg); font-size:12px; margin-top:4px; }
  pre.snippet { margin:6px 0 0; padding:8px 10px; background:var(--panel2); border:1px solid var(--line);
    border-radius:4px; font:12px ui-monospace,SFMono-Regular,Menlo,monospace; white-space:pre;
    overflow-x:auto; color:var(--fg); }
</style>
<script>try{var _t=localStorage.getItem("imagemanager-theme")||"light";document.documentElement.setAttribute("data-theme",_t);}catch(e){}</script>
</head>
<body>
<header>
  <div class="brand"><span class="brand-mark"></span><span class="brand-name">EDA Image Manager</span></div>
  <span class="sub">Upload a NOS image &rarr; hosted in-cluster &rarr; Artifact created &rarr; eda-asvr re-hosts it</span>
  <button id="themeBtn" class="ghostbtn" title="Toggle light / dark appearance">Dark mode</button>
</header>
<main>
  <div class="card">
    <h2>Upload image</h2>
    <div class="cardsub">Upload a raw <span class="mono">.bin</span>, or the vendor <span class="mono">.zip</span> (the bin + its md5 are extracted automatically).</div>
    <div class="grid">
      <div class="field full">
        <label>Image file — <span class="mono">.bin</span> or vendor <span class="mono">.zip</span> (required)</label>
        <input type="file" id="binFile" accept=".bin,.zip">
        <span class="hint" id="binHint"></span>
      </div>
      <div class="field full">
        <label>MD5 checksum (optional)</label>
        <input type="text" id="md5Hash" placeholder="e.g. d41d8cd98f00b204e9800998ecf8427e" maxlength="64">
        <span class="hint" id="md5Note"></span>
      </div>
      <div class="field">
        <label>Namespace</label>
        <input type="text" id="namespace" list="nslist" placeholder="eda">
        <datalist id="nslist"></datalist>
      </div>
      <div class="field">
        <label>Image name (used as the artifact name + URL)</label>
        <input type="text" id="imageName" placeholder="SRLinux-26.3.2">
        <span class="hint">SR Linux images are auto-named <span class="mono">SRLinux-&lt;version&gt;</span>; edit if needed.</span>
      </div>
    </div>
    <div class="row">
      <button class="primary" id="uploadBtn">Upload &amp; create Artifact</button>
      <div class="progwrap" id="progwrap">
        <div class="progress"><div id="progressBar"></div></div>
        <div class="progtext" id="progText"></div>
      </div>
    </div>
    <div class="msg" id="msg"></div>
  </div>

  <div class="card">
    <h2>Artifacts <span class="cardsub" id="refreshNote" style="display:inline"></span></h2>
    <div class="cardsub">Each row becomes a NodeProfile snippet once <span class="mono">eda-asvr</span> reports it <span class="mono">Available</span>.</div>
    <table>
      <thead><tr>
        <th>Name</th><th>Namespace</th>
        <th>Size</th><th>Status</th><th>NodeProfile image</th><th></th>
      </tr></thead>
      <tbody id="rows"><tr><td colspan="6" class="empty">Loading&hellip;</td></tr></tbody>
    </table>
  </div>
</main>
<script>
(function(){
  var apiBase = location.pathname.replace(/\/+$/, "");
  function api(p){ return apiBase + p; }
  var maxBytes = 4096*1024*1024;
  var MD5_DEFAULT_NOTE = "If given, the EDA artifact server verifies the image against this hash and reports a mismatch below. The app does no checksum verification itself.";

  var el = function(id){ return document.getElementById(id); };
  var binFile=el("binFile"), md5Hash=el("md5Hash"), md5Note=el("md5Note"),
      ns=el("namespace"), imageName=el("imageName"), btn=el("uploadBtn"),
      progwrap=el("progwrap"), bar=el("progressBar"), progText=el("progText"),
      msg=el("msg"), binHint=el("binHint"), rows=el("rows");
  md5Note.textContent = MD5_DEFAULT_NOTE;

  function fmtBytes(n){
    if(n==null) return "";
    var u=["B","KiB","MiB","GiB","TiB"], i=0; n=Number(n);
    while(n>=1024 && i<u.length-1){ n/=1024; i++; }
    return n.toFixed(i?1:0)+" "+u[i];
  }
  function isZip(name){ return /\.zip$/i.test(name||""); }
  function show(kind, text){ msg.className="msg "+kind; msg.textContent=text; }
  function esc(s){ return String(s==null?"":s).replace(/[&<>"]/g,function(m){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[m]; }); }
  function deriveName(fn){
    var base=(fn||"").split(/[\\/]/).pop();
    var stem=base.replace(/\.[A-Za-z0-9]+$/,"");
    if(/sr[ _-]?linux/i.test(base)){
      var m=base.match(/(\d+\.\d+\.\d+(?:-\d+)?)/);
      if(m) return "SRLinux-"+m[1];
    }
    return stem||"image";
  }

  fetch(api("/api/config")).then(function(r){return r.json();}).then(function(c){
    if(c.defaultArtifactNamespace){ ns.placeholder=c.defaultArtifactNamespace; ns.value=ns.value||c.defaultArtifactNamespace; }
    if(c.maxUploadMiB) maxBytes=c.maxUploadMiB*1024*1024;
    binHint.textContent="Maximum upload size: "+c.maxUploadMiB+" MiB.";
  }).catch(function(){});

  fetch(api("/api/namespaces")).then(function(r){return r.json();}).then(function(d){
    var dl=el("nslist"); (d.namespaces||[]).forEach(function(n){
      var o=document.createElement("option"); o.value=n; dl.appendChild(o);
    });
  }).catch(function(){});

  binFile.addEventListener("change", function(){
    var f=binFile.files[0];
    if(!f) return;
    imageName.value=deriveName(f.name);
    binHint.textContent=f.name+" — "+fmtBytes(f.size);
    var zip=isZip(f.name);
    md5Hash.disabled=zip;
    md5Note.textContent = zip
      ? "A vendor zip was selected — its packaged MD5 is used; anything typed here is ignored."
      : MD5_DEFAULT_NOTE;
  });

  btn.addEventListener("click", function(){
    var f=binFile.files[0];
    if(!f){ show("err","Select a .bin or .zip file first."); return; }
    if(f.size>maxBytes){ show("err","File is "+fmtBytes(f.size)+", over the "+fmtBytes(maxBytes)+" limit."); return; }
    var zip=isZip(f.name);
    var qs=new URLSearchParams({ filename:f.name,
      namespace:ns.value||ns.placeholder, name:imageName.value||deriveName(f.name) });
    var mh=(md5Hash.value||"").trim().toLowerCase();
    if(mh && !zip) qs.set("md5", mh);
    var xhr=new XMLHttpRequest();
    xhr.open("POST", api("/api/upload")+"?"+qs.toString());
    btn.disabled=true; progwrap.style.display="block"; bar.style.width="0"; progText.textContent="";
    msg.className="msg"; msg.style.display="none";
    var startT=Date.now();
    xhr.upload.onprogress=function(e){
      if(!e.lengthComputable) return;
      var pct=e.loaded/e.total*100;
      bar.style.width=pct.toFixed(1)+"%";
      var elapsed=(Date.now()-startT)/1000;
      var speed=elapsed>0 ? (e.loaded/1048576/elapsed) : 0;
      progText.textContent=fmtBytes(e.loaded)+" / "+fmtBytes(e.total)+
        "  ("+pct.toFixed(0)+"%)  ·  "+speed.toFixed(1)+" MB/s"+(zip?"  ·  extracting after upload":"");
    };
    xhr.onload=function(){
      btn.disabled=false; progwrap.style.display="none";
      var r={}; try{ r=JSON.parse(xhr.responseText);}catch(e){}
      if(xhr.status>=200 && xhr.status<300 && r.ok){
        var from = r.fromZip ? (" Extracted "+(r.filename||"image")+" from the zip.") : "";
        var note = r.md5 ? (" The artifact server will verify it against MD5 "+r.md5+".") : "";
        show("ok","Uploaded "+f.name+"."+from+" Artifact "+r.namespace+"/"+r.artifactName+" created."+note);
        binFile.value=""; md5Hash.value=""; md5Hash.disabled=false; md5Note.textContent=MD5_DEFAULT_NOTE; refresh();
      } else { show("err", (r.error||("HTTP "+xhr.status))); if(r.uploadId) refresh(); }
    };
    xhr.onerror=function(){ btn.disabled=false; progwrap.style.display="none";
      show("err","Network error during upload."); };
    xhr.send(f);
  });

  function badge(s){ var c=s||"NoArtifact"; return '<span class="badge b-'+(c||"empty")+'">'+(c||"-")+'</span>'; }

  function imDelete(uid, nsv, name){
    if(!confirm("Delete artifact \""+name+"\"?\nThis removes it from EDA and the artifact server, and deletes the local copy.")) return;
    var qs=new URLSearchParams({uploadId:uid||"", namespace:nsv||"", name:name||""});
    fetch(api("/api/delete")+"?"+qs.toString(), {method:"POST"})
      .then(function(r){return r.json();})
      .then(function(d){ if(d && d.ok){ refresh(); } else { alert("Delete failed: "+((d&&d.error)||"unknown")); } })
      .catch(function(){ alert("Delete failed (network)."); });
  }

  // Delegated click handling for the table buttons (avoids inline-onclick quoting bugs).
  rows.addEventListener("click", function(e){
    var b = e.target.closest("button[data-act]");
    if(!b) return;
    if(b.getAttribute("data-act")==="copysnip"){
      var s=b.getAttribute("data-snip")||"";
      if(navigator.clipboard) navigator.clipboard.writeText(s);
      var t0=b.textContent; b.textContent="copied"; setTimeout(function(){ b.textContent=t0; }, 1200);
    } else if(b.getAttribute("data-act")==="del"){
      imDelete(b.getAttribute("data-uid"), b.getAttribute("data-ns"), b.getAttribute("data-name"));
    }
  });

  function refresh(){
    fetch(api("/api/artifacts")).then(function(r){return r.json();}).then(function(d){
      var a=d.artifacts||[];
      if(!a.length){ rows.innerHTML='<tr><td colspan="6" class="empty">No uploads yet.</td></tr>'; el("refreshNote").textContent=""; return; }
      rows.innerHTML=a.map(function(t){
        var snip=t.imagePath?("images:\n  - image: "+t.imagePath+(t.md5Path?("\n    imageMd5: "+t.md5Path):"")):"";
        var np=snip?('<button class="iconbtn" data-act="copysnip" data-snip="'+esc(snip)+'">copy</button><pre class="snippet">'+esc(snip)+'</pre>'):'<span class="mono" style="color:var(--muted)">— ready when Available</span>';
        var reason=t.statusReason?('<div class="reason">'+esc(t.statusReason)+'</div>'):'';
        var del='<button class="iconbtn delbtn" data-act="del" data-uid="'+esc(t.uploadId||"")+'" data-ns="'+esc(t.namespace||"")+'" data-name="'+esc(t.name||"")+'">delete</button>';
        return '<tr><td class="mono">'+esc(t.displayName||t.name)+'</td><td>'+esc(t.namespace)+'</td><td>'+fmtBytes(t.sizeBytes)+'</td><td>'+badge(t.downloadStatus)+reason+'</td><td>'+np+'</td><td>'+del+'</td></tr>';
      }).join("");
      el("refreshNote").textContent="("+a.length+")";
    }).catch(function(){});
  }
  (function(){
    var tb=el("themeBtn"); if(!tb) return;
    function lbl(){ tb.textContent = document.documentElement.getAttribute("data-theme")==="dark" ? "Light mode" : "Dark mode"; }
    lbl();
    tb.addEventListener("click", function(){
      var next = document.documentElement.getAttribute("data-theme")==="dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      try{ localStorage.setItem("imagemanager-theme", next); }catch(e){}
      lbl();
    });
  })();

  refresh(); setInterval(refresh, 5000);
})();
</script>
</body>
</html>
"""
