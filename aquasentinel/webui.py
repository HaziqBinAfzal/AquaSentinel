from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Timer
from urllib.parse import urlparse
import webbrowser

from .ingestion import analyze_content

MAX_BODY_BYTES = 9 * 1024 * 1024

HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AquaSentinel AI — Analysis Workstation</title>
<style>
:root{
  --bg:#eef1f3;--surface:#ffffff;--surface2:#f7f8f9;--ink:#1f2933;--muted:#66737f;
  --line:#d7dde2;--navy:#20384d;--steel:#3f627c;--green:#3f6f57;--amber:#8a6a2f;--red:#8a4343;
}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:"Segoe UI",Arial,sans-serif;font-size:14px}
header{height:64px;background:var(--navy);color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 28px;border-bottom:4px solid #182b3b}
.brand{display:flex;align-items:center;gap:12px}.mark{width:34px;height:34px;border:1px solid #90a5b5;display:grid;place-items:center;font-weight:700;font-size:12px}
.brand h1{font-size:18px;margin:0;font-weight:600;letter-spacing:.01em}.brand small{display:block;color:#c7d1d9;margin-top:2px;font-size:11px;font-weight:400}
.status{font-size:11px;color:#dce5eb;border:1px solid #667d90;padding:6px 9px}.wrap{max-width:1380px;margin:22px auto;padding:0 20px 30px}
.notice{background:#f8f4e8;border:1px solid #d9cba5;color:#5f553e;padding:10px 12px;margin-bottom:14px;font-size:12px}
.panel{background:var(--surface);border:1px solid var(--line);margin-bottom:14px}.panel-h{padding:11px 14px;border-bottom:1px solid var(--line);background:var(--surface2);font-weight:600;color:#34414c}.panel-b{padding:14px}
.source{display:grid;grid-template-columns:minmax(280px,1.5fr) 1fr auto;gap:12px;align-items:end}.field label{display:block;font-size:11px;color:var(--muted);margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em}
input[type=file]{width:100%;border:1px solid #bdc7cf;background:#fff;padding:9px}.hint{color:var(--muted);font-size:12px;line-height:1.45}
button{border:1px solid #27455d;background:#294c67;color:#fff;padding:10px 17px;font-weight:600;cursor:pointer}button:hover{background:#203f58}button:disabled{opacity:.55;cursor:not-allowed}
#empty{padding:54px 20px;text-align:center;color:#6c7780;background:#fff;border:1px solid var(--line)}#empty strong{display:block;color:#3f4a54;font-size:18px;margin-bottom:8px;font-weight:600}
#dashboard{display:none}.cards{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:14px}.card{background:#fff;border:1px solid var(--line);padding:13px}.label{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}.value{font-family:Consolas,"Courier New",monospace;font-size:23px;font-weight:600;margin-top:6px}.sub{font-size:11px;color:var(--muted);margin-top:4px}.good{color:var(--green)}.warn{color:var(--amber)}.bad{color:var(--red)}
.grid{display:grid;grid-template-columns:1.25fr 1fr;gap:14px}.span{grid-column:1/-1}table{border-collapse:collapse;width:100%;font-size:12px}th,td{padding:8px 9px;border-bottom:1px solid #e1e5e8;text-align:left;vertical-align:top}th{background:#f6f7f8;color:#53606b;font-weight:600}td.num{text-align:right;font-family:Consolas,"Courier New",monospace}
.pills{display:flex;flex-wrap:wrap;gap:6px}.pill{border:1px solid #c9d1d7;background:#f8f9fa;padding:5px 8px;font-size:11px}.flag{border-left:3px solid var(--amber);background:#fbf8ef;padding:8px 10px;margin-bottom:7px;font-size:12px}.mlbox{border:1px solid #cfd7dd;background:#f8fafb;padding:11px;line-height:1.55}.mono{font-family:Consolas,"Courier New",monospace}.records{max-height:370px;overflow:auto}.records table{min-width:860px}.footer{color:#6b747b;font-size:11px;margin-top:14px;padding:8px 0}.error{display:none;background:#fbefef;border:1px solid #ddbcbc;color:#7b3434;padding:10px 12px;margin-top:10px}
@media(max-width:1000px){.cards{grid-template-columns:repeat(3,1fr)}.grid{grid-template-columns:1fr}.span{grid-column:auto}.source{grid-template-columns:1fr}}@media(max-width:620px){header{padding:0 14px}.status{display:none}.wrap{padding:0 10px}.cards{grid-template-columns:repeat(2,1fr)}}
</style>
</head>
<body>
<header><div class="brand"><div class="mark">AS</div><div><h1>AquaSentinel AI</h1><small>Local analysis workstation • v1.0.0</small></div></div><div class="status">127.0.0.1 • LOCAL ONLY</div></header>
<div class="wrap">
<div class="notice"><b>Analysis boundary:</b> Files are processed by the AquaSentinel process running on this computer. The local interface does not provide PLC, SCADA, dosing or plant-control functions. Classroom water-quality bands are illustrative, not regulatory limits.</div>
<div class="panel"><div class="panel-h">Data source</div><div class="panel-b source">
  <div class="field"><label>Select file</label><input id="file" type="file" accept=".log,.txt,.csv,.json,.jsonl"></div>
  <div class="hint">Supported: LOG, TXT, CSV, JSON and JSONL. Maximum file size: 8 MB. Nothing is preloaded; analysis begins only after a file is selected.</div>
  <button id="analyze">Analyze file</button>
</div><div id="error" class="error"></div></div>
<div id="empty"><strong>No dataset loaded</strong>Select a local log or telemetry file above. AquaSentinel will summarize the source, identify recognized process fields, classify log severity, surface configured indicators and run local anomaly detection when enough numeric data is available.</div>
<div id="dashboard">
<div class="cards">
 <div class="card"><div class="label">Decision</div><div class="value" id="decision">--</div><div class="sub">operator disposition</div></div>
 <div class="card"><div class="label">Review score</div><div class="value" id="risk">--</div><div class="sub">0–100 evidence score</div></div>
 <div class="card"><div class="label">Records</div><div class="value" id="records">--</div><div class="sub" id="format">--</div></div>
 <div class="card"><div class="label">Critical / errors</div><div class="value" id="errors">--</div><div class="sub">classified log entries</div></div>
 <div class="card"><div class="label">Review flags</div><div class="value" id="flags">--</div><div class="sub">illustrative bands</div></div>
 <div class="card"><div class="label">ML anomalies</div><div class="value" id="mlcount">--</div><div class="sub" id="mlstate">--</div></div>
</div>
<div class="grid">
 <section class="panel"><div class="panel-h">Source profile</div><div class="panel-b" id="source"></div></section>
 <section class="panel"><div class="panel-h">Severity classification</div><div class="panel-b" id="severity"></div></section>
 <section class="panel span"><div class="panel-h">Recognized water / process fields</div><div class="panel-b"><div class="records"><table><thead><tr><th>Field</th><th>Samples</th><th>Minimum</th><th>Average</th><th>Maximum</th><th>Latest</th></tr></thead><tbody id="metrics"></tbody></table></div></div></section>
 <section class="panel"><div class="panel-h">Observed indicators</div><div class="panel-b" id="indicators"></div></section>
 <section class="panel"><div class="panel-h">Local anomaly model</div><div class="panel-b" id="ml"></div></section>
 <section class="panel span"><div class="panel-h">Items for human review</div><div class="panel-b" id="review"></div></section>
 <section class="panel span"><div class="panel-h">Recent records</div><div class="panel-b records" id="recent"></div></section>
</div>
<div class="footer">AquaSentinel AI • Local defensive analysis • User-supplied data only • No automated industrial control</div>
</div></div>
<script>
const $=id=>document.getElementById(id);const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function riskClass(v){return v>=70?'bad':v>=35?'warn':'good'}
function render(d){$('empty').style.display='none';$('dashboard').style.display='block';$('error').style.display='none';
 const s=d.summary,src=d.source,m=d.ml;$('decision').textContent=s.decision;$('decision').className='value '+(s.decision==='REVIEW'?'warn':'good');$('risk').textContent=s.risk_score;$('risk').className='value '+riskClass(s.risk_score);$('records').textContent=src.records;$('format').textContent=src.format.toUpperCase();$('errors').textContent=`${s.critical} / ${s.errors}`;$('errors').className='value '+((s.critical+s.errors)>0?'bad':'good');$('flags').textContent=s.review_flags;$('flags').className='value '+(s.review_flags?'warn':'good');$('mlcount').textContent=m.anomaly_count||0;$('mlstate').textContent=m.state;
 $('source').innerHTML=`<table><tbody><tr><th>File</th><td class="mono">${esc(src.filename)}</td></tr><tr><th>Format</th><td>${esc(src.format.toUpperCase())}</td></tr><tr><th>Records read</th><td>${src.records}</td></tr><tr><th>Fields detected</th><td>${src.fields.length}</td></tr></tbody></table><div class="pills" style="margin-top:10px">${src.fields.map(x=>`<span class="pill mono">${esc(x)}</span>`).join('')}</div>`;
 const sev=d.severity_counts;let sevRows=Object.keys(sev).sort().map(k=>`<tr><td>${esc(k)}</td><td class="num">${sev[k]}</td></tr>`).join('');$('severity').innerHTML=sevRows?`<table><thead><tr><th>Class</th><th>Count</th></tr></thead><tbody>${sevRows}</tbody></table>`:'No severity terms were identified.';
 let metricRows=Object.entries(d.metrics).map(([k,v])=>`<tr><td class="mono">${esc(k)}</td><td class="num">${v.count}</td><td class="num">${v.min}</td><td class="num">${v.avg}</td><td class="num">${v.max}</td><td class="num">${v.last}</td></tr>`).join('');$('metrics').innerHTML=metricRows||'<tr><td colspan="6">No configured water/process telemetry fields were recognized in this file.</td></tr>';
 const inds=Object.entries(d.indicators);$('indicators').innerHTML=inds.length?`<table><thead><tr><th>Term</th><th>Count</th></tr></thead><tbody>${inds.map(([k,v])=>`<tr><td class="mono">${esc(k)}</td><td class="num">${v}</td></tr>`).join('')}</tbody></table>`:'No configured log or OT/security indicators were found.';
 $('ml').innerHTML=`<div class="mlbox"><b>${esc(m.state)}</b><br>${esc(m.detail)}<br><br><span class="mono">Features: ${esc((m.features||[]).join(', ')||'none')}</span></div>`;
 $('review').innerHTML=d.review_flags.length?d.review_flags.map(f=>`<div class="flag"><b class="mono">${esc(f.field)}</b> — ${f.outside_band} of ${f.count} values outside the illustrative classroom review band.</div>`).join(''):`<span class="good">No configured classroom-band exceptions were found.</span>`;
 const rows=d.recent_records;if(!rows.length){$('recent').textContent='No records available.';return}let keys=[];rows.forEach(x=>Object.keys(x.record).forEach(k=>{if(!keys.includes(k)&&keys.length<10)keys.push(k)}));$('recent').innerHTML=`<table><thead><tr><th>#</th>${keys.map(k=>`<th>${esc(k)}</th>`).join('')}</tr></thead><tbody>${rows.map(x=>`<tr><td class="num">${x.index}</td>${keys.map(k=>`<td class="mono">${esc(x.record[k]??'')}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
}
$('analyze').onclick=async()=>{const f=$('file').files[0];if(!f){$('error').textContent='Select a supported file first.';$('error').style.display='block';return}if(f.size>8*1024*1024){$('error').textContent='The selected file is larger than 8 MB.';$('error').style.display='block';return}const btn=$('analyze');btn.disabled=true;btn.textContent='Analyzing…';try{const content=await f.text();const r=await fetch('/api/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({filename:f.name,content})});const d=await r.json();if(!r.ok)throw new Error(d.error||'Analysis failed');render(d)}catch(e){$('error').textContent=e.message;$('error').style.display='block'}finally{btn.disabled=false;btn.textContent='Analyze file'}};
</script>
</body></html>'''


class _Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, content_type: str, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send(200, "text/html; charset=utf-8", HTML.encode("utf-8"))
            return
        if parsed.path == "/api/health":
            body = json.dumps({"ok": True, "mode": "local-file-analysis", "version": "1.0.0"}).encode()
            self._send(200, "application/json; charset=utf-8", body)
            return
        self._send(404, "text/plain; charset=utf-8", b"Not found")

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/analyze":
            self._send(404, "text/plain; charset=utf-8", b"Not found")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send(400, "application/json; charset=utf-8", b'{"error":"Invalid content length"}')
            return
        if length <= 0 or length > MAX_BODY_BYTES:
            self._send(413, "application/json; charset=utf-8", b'{"error":"Request is empty or too large"}')
            return
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            filename = Path(str(payload.get("filename", ""))).name
            content = payload.get("content", "")
            if not filename or not isinstance(content, str):
                raise ValueError("A filename and text content are required")
            result = analyze_content(filename, content)
            body = json.dumps(result, ensure_ascii=False).encode("utf-8")
            self._send(200, "application/json; charset=utf-8", body)
        except (ValueError, json.JSONDecodeError) as exc:
            body = json.dumps({"error": str(exc)}).encode("utf-8")
            self._send(400, "application/json; charset=utf-8", body)

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        return


def run_web(port: int = 8765, open_browser: bool = True, check_only: bool = False) -> None:
    if not 1024 <= int(port) <= 65535:
        raise SystemExit("--port must be between 1024 and 65535")
    if check_only:
        probe = "timestamp,severity,ph,turbidity\n2026-01-01T00:00:00Z,info,7.2,0.3\n"
        result = analyze_content("check.csv", probe)
        if result["source"]["records"] != 1 or result["source"]["format"] != "csv":
            raise SystemExit("Local web analysis self-check failed")
        print("Local web dashboard check passed")
        return

    address = ("127.0.0.1", int(port))
    url = f"http://127.0.0.1:{port}/"
    server = ThreadingHTTPServer(address, _Handler)
    print("AquaSentinel AI — local analysis workstation")
    print(f"Open: {url}")
    print("Select a local .log, .txt, .csv, .json or .jsonl file in the browser.")
    print("No data is preloaded. The server is bound to 127.0.0.1 only.")
    print("Press Ctrl+C to stop.")
    if open_browser:
        Timer(0.7, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever(poll_interval=0.3)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("AquaSentinel local analysis workstation stopped")
