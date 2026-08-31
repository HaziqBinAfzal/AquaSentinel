from __future__ import annotations

import json
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Timer
from urllib.parse import urlparse

from .ingestion import analyze_content

MAX_BODY_BYTES = 9 * 1024 * 1024

HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AquaSentinel AI — Water & OT Analysis</title>
<style>
:root{
  --bg:#07151c;--bg2:#0b2028;--surface:#102a33;--surface2:#143640;--panel:#f6fbfc;
  --panel2:#eef6f7;--ink:#15313a;--muted:#658089;--line:#cfe0e4;--teal:#0f7f83;
  --teal2:#19a4a8;--blue:#246a8a;--green:#2f7d5b;--amber:#b47a1f;--red:#aa4040;
  --white:#ffffff;--shadow:0 12px 30px rgba(0,0,0,.12)
}
*{box-sizing:border-box}
body{margin:0;background:linear-gradient(180deg,var(--bg) 0,var(--bg2) 220px,#dfeaec 220px,#eaf1f2 100%);color:var(--ink);font:14px "Segoe UI",Arial,sans-serif;min-height:100vh}
header{padding:22px 28px 18px;color:#fff;display:flex;justify-content:space-between;align-items:center;max-width:1480px;margin:auto}
.brand{display:flex;gap:14px;align-items:center}.logo{width:46px;height:46px;border-radius:12px;background:linear-gradient(135deg,#1ba0a4,#155a72);display:grid;place-items:center;font-weight:800;letter-spacing:.04em;box-shadow:0 8px 20px rgba(0,0,0,.25)}
.brand b{font-size:21px;letter-spacing:.01em}.brand small{display:block;color:#b7d6dc;margin-top:4px}.local{font:11px Consolas,monospace;border:1px solid rgba(255,255,255,.28);background:rgba(255,255,255,.06);padding:7px 10px;border-radius:8px;color:#d9f0f2}
.wrap{max-width:1480px;margin:0 auto;padding:0 18px 34px}.boundary{font-size:12px;background:#fff8e8;border:1px solid #e9d9ae;border-left:4px solid var(--amber);padding:10px 13px;margin-bottom:13px;border-radius:9px;box-shadow:var(--shadow)}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;margin-bottom:13px;overflow:hidden;box-shadow:var(--shadow)}.ph{background:linear-gradient(180deg,#f7fbfc,#edf5f7);border-bottom:1px solid var(--line);padding:12px 14px;font-weight:700;color:#173b45}.pb{padding:14px}.source{display:grid;grid-template-columns:1.5fr 1fr auto;gap:13px;align-items:end}
label,.eyebrow{display:block;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.09em;margin-bottom:6px;font-weight:700}input{width:100%;padding:10px;border:1px solid #abc4ca;background:#fff;border-radius:8px}button{padding:10px 18px;background:linear-gradient(135deg,var(--teal),#176883);color:#fff;border:0;border-radius:8px;font-weight:700;cursor:pointer;box-shadow:0 5px 14px rgba(15,127,131,.22)}button:hover{filter:brightness(1.06)}
.hint{font-size:12px;color:var(--muted);line-height:1.45}.empty{text-align:center;padding:62px 20px;background:rgba(255,255,255,.96);border:1px solid var(--line);border-radius:12px;color:var(--muted);box-shadow:var(--shadow)}.empty b{display:block;font-size:20px;color:#264c57;margin-bottom:7px}#dash{display:none}
.kpis{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:13px}.kpi{background:linear-gradient(180deg,#fff,#f2f8f9);border:1px solid var(--line);border-radius:11px;padding:13px;box-shadow:var(--shadow);position:relative;overflow:hidden}.kpi:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:#9bbfc5}.kpi strong{display:block;font:700 23px Consolas,monospace;margin-top:6px;color:#173b45}.good{color:var(--green)!important}.warn{color:var(--amber)!important}.bad{color:var(--red)!important}
.objectives{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.objective{border:1px solid var(--line);background:#fff;padding:13px;border-radius:10px}.objective h3{font-size:13px;margin:0 0 8px;color:#1e4853}.tag{font:700 10px Consolas,monospace;padding:4px 7px;border-radius:999px;border:1px solid #b9d0d5;background:#edf7f8;display:inline-block;margin-bottom:8px}.objective p{font-size:12px;color:#526d75;line-height:1.5;margin:0}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:13px}.wide{grid-column:1/-1}table{border-collapse:separate;border-spacing:0;width:100%;font-size:12px;border:1px solid #dce9ec;border-radius:9px;overflow:hidden}th,td{padding:8px 9px;border-bottom:1px solid #e3edef;text-align:left;vertical-align:top}tr:last-child td,tr:last-child th{border-bottom:0}th{background:#eaf4f6;color:#3f6069;font-weight:700;white-space:nowrap}.num{text-align:right;font-family:Consolas,monospace}.mono{font-family:Consolas,monospace}.scroll{overflow:auto;max-height:390px}.scroll table{min-width:900px}
.chartgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:11px}.chart{border:1px solid #d4e4e7;padding:10px;border-radius:9px;background:#fff}.chart h4{margin:0 0 5px;font-size:11px;color:#355861;text-transform:capitalize}.chart svg{width:100%;height:92px;background:linear-gradient(180deg,#fbfefe,#edf7f8);border-radius:6px}.flag{border-left:4px solid var(--amber);background:#fff8e8;padding:8px 10px;margin:6px 0;font-size:12px;border-radius:6px}.summary{background:linear-gradient(135deg,#e8f5f6,#f7fbfc);border-left:4px solid var(--teal);padding:13px;line-height:1.58;border-radius:8px}.fields{font:11px Consolas,monospace;color:#60767d;line-height:1.7;word-break:break-word;margin-top:8px}.error{display:none;background:#fff0f0;border:1px solid #e5bbbb;color:#842f2f;padding:10px;margin-top:8px;border-radius:8px}.footer{font-size:11px;color:#5a7077;padding:9px 2px}.note{margin-top:9px;padding:9px 10px;border-radius:8px;background:#edf7f8;color:#42646d;font-size:12px;line-height:1.45}.metric-label{font-weight:700;color:#294e59}
@media(max-width:1000px){.kpis{grid-template-columns:repeat(3,1fr)}.objectives{grid-template-columns:1fr 1fr}.grid{grid-template-columns:1fr}.wide{grid-column:auto}.source{grid-template-columns:1fr}}
@media(max-width:650px){header{padding:16px}.kpis,.objectives,.chartgrid{grid-template-columns:1fr}.local{display:none}.wrap{padding:0 10px 24px}}
</style>
</head>
<body>
<header><div class="brand"><div class="logo">AS</div><div><b>AquaSentinel AI</b><small>Local analysis workstation • Topic 133 • Water / Desalination Infrastructure</small></div></div><div class="local">127.0.0.1 · READ ONLY</div></header>
<main class="wrap">
<div class="boundary"><b>Safety boundary:</b> local defensive analysis of user-supplied evidence only. No PLC, SCADA, dosing or utility-control path. Water-quality bands are illustrative classroom review bands, not regulatory limits.</div>
<section class="panel"><div class="ph">Analysis source</div><div class="pb source"><div><label>Authorized data file</label><input id="file" type="file" accept=".log,.txt,.csv,.json,.jsonl"></div><div class="hint">LOG, TXT, CSV, JSON or JSONL · max 8 MB. Nothing is preloaded; analysis starts only after you select a file.</div><button id="analyze">Analyze evidence</button></div><div id="error" class="error"></div></section>
<div id="empty" class="empty"><b>No dataset loaded</b>Select an authorized water/process telemetry or defensive OT/security log. Results will be organized against the Topic 133 learning objectives.</div>
<div id="dash">
<div class="kpis"><div class="kpi"><span class="eyebrow">Operator disposition</span><strong id="decision">--</strong></div><div class="kpi"><span class="eyebrow">Evidence score</span><strong id="risk">--</strong></div><div class="kpi"><span class="eyebrow">Records analyzed</span><strong id="records">--</strong></div><div class="kpi"><span class="eyebrow">Critical / error</span><strong id="errors">--</strong></div><div class="kpi"><span class="eyebrow">Fields with exceptions</span><strong id="flags">--</strong></div><div class="kpi"><span class="eyebrow">ML flagged records</span><strong id="mlcount">--</strong></div></div>
<section class="panel"><div class="ph">Topic 133 coverage — key learning objectives</div><div class="pb objectives" id="objectives"></div></section>
<div class="grid">
<section class="panel"><div class="ph">1 · Water quality assurance</div><div class="pb"><div class="scroll"><table><thead><tr><th>Measurement</th><th>Samples</th><th>Min</th><th>Average</th><th>Max</th><th>Latest</th></tr></thead><tbody id="metrics"></tbody></table></div><div id="qualityflags"></div></div></section>
<section class="panel"><div class="ph">2 · Desalination process & predictive maintenance</div><div class="pb" id="maintenance"></div></section>
<section class="panel wide"><div class="ph">Process telemetry trends</div><div class="pb chartgrid" id="charts"></div></section>
<section class="panel"><div class="ph">3 · OT / SCADA security evidence</div><div class="pb" id="security"></div></section>
<section class="panel"><div class="ph">4 · AI anomaly detection</div><div class="pb" id="ml"></div></section>
<section class="panel wide"><div class="ph">5 · Cyber-physical correlation & response evidence</div><div class="pb" id="correlation"></div></section>
<section class="panel"><div class="ph">6 · Energy & resource review</div><div class="pb" id="energy"></div></section>
<section class="panel"><div class="ph">Source profile & audit trail</div><div class="pb" id="source"></div></section>
<section class="panel wide"><div class="ph">Security / process event timeline</div><div class="pb scroll" id="events"></div></section>
<section class="panel wide"><div class="ph">Analysis summary for human review</div><div class="pb"><div class="summary" id="summary"></div></div></section>
<section class="panel wide"><div class="ph">Source records — recent evidence</div><div class="pb scroll" id="recent"></div></section>
</div><div class="footer">AquaSentinel AI v1.0.0 · Topic 133 · local defensive analysis · human decision authority · No automated industrial control</div></div>
</main>
<script>
const $=x=>document.getElementById(x);
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const cls=v=>v>=70?'bad':v>=35?'warn':'good';
function spark(name,v){let a=v.series||[];if(a.length<2)return'';let lo=Math.min(...a),hi=Math.max(...a),r=hi-lo||1,pts=a.map((x,i)=>`${i/(a.length-1)*100},${82-(x-lo)/r*70}`).join(' ');return `<div class="chart"><h4>${esc(name.replaceAll('_',' '))}</h4><svg viewBox="0 0 100 90" preserveAspectRatio="none"><polyline points="${pts}" fill="none" stroke="#0f7f83" stroke-width="1.8" vector-effect="non-scaling-stroke"/></svg><span class="hint">min ${v.min} · avg ${v.avg} · max ${v.max}</span></div>`}
function render(d){
  $('empty').style.display='none';$('dash').style.display='block';let s=d.summary,m=d.ml;
  $('decision').textContent=s.decision;$('decision').className=s.decision==='REVIEW'?'warn':'good';
  $('risk').textContent=s.risk_score+'/100';$('risk').className=cls(s.risk_score);$('records').textContent=d.source.records;
  $('errors').textContent=s.critical+' / '+s.errors;$('errors').className=s.critical+s.errors?'bad':'good';
  $('flags').textContent=s.review_flags;$('flags').className=s.review_flags?'warn':'good';$('mlcount').textContent=m.state==='ANALYZED'?m.anomaly_count:'N/A';
  $('objectives').innerHTML=d.objectives.map(o=>`<article class="objective"><h3>${esc(o.title)}</h3><span class="tag">${esc(o.status)}</span><p>${esc(o.detail)}</p></article>`).join('');
  $('metrics').innerHTML=Object.entries(d.metrics).map(([k,v])=>`<tr><td class="metric-label">${esc(k.replaceAll('_',' '))}</td><td class="num">${v.count}</td><td class="num">${v.min}</td><td class="num">${v.avg}</td><td class="num">${v.max}</td><td class="num">${v.last}</td></tr>`).join('')||'<tr><td colspan="6">Not available in source.</td></tr>';
  $('qualityflags').innerHTML=d.review_flags.length?d.review_flags.map(f=>`<div class="flag"><b>${esc(f.field.replaceAll('_',' '))}</b>: ${f.outside_band}/${f.count} values outside the illustrative classroom band.</div>`).join(''):'<p class="good">No configured classroom-band exceptions found.</p>';
  $('charts').innerHTML=Object.entries(d.metrics).filter(([k])=>['ph','conductivity','turbidity','residual_chlorine','ro_pressure','flow_rate','energy_kwh','membrane_health'].includes(k)).map(([k,v])=>spark(k,v)).join('')||'<span class="hint">No trendable configured telemetry in source.</span>';
  const foul=d.maintenance.fouling_review;let reason=[];if(d.metrics.membrane_health)reason.push(`membrane health min ${d.metrics.membrane_health.min}`);if(d.metrics.ro_pressure)reason.push(`RO pressure max ${d.metrics.ro_pressure.max}`);if(d.metrics.flow_rate)reason.push(`flow min ${d.metrics.flow_rate.min}`);
  $('maintenance').innerHTML=`<table><tbody><tr><th>Membrane fouling review</th><td>${foul?'<b class="warn">INDICATED</b>':'Not indicated by configured checks'}</td></tr><tr><th>RO pressure</th><td>${d.metrics.ro_pressure?`max ${d.metrics.ro_pressure.max}`:'Not available in source'}</td></tr><tr><th>Flow rate</th><td>${d.metrics.flow_rate?`min ${d.metrics.flow_rate.min}`:'Not available in source'}</td></tr><tr><th>Membrane health</th><td>${d.metrics.membrane_health?`min ${d.metrics.membrane_health.min}`:'Not available in source'}</td></tr></tbody></table>${foul?`<div class="note"><b>Why this needs review:</b> ${esc(reason.join(' · '))}. This is an advisory maintenance signal, not an automated control action.</div>`:''}`;
  let inds=Object.entries(d.security_indicators||{}),routine=(d.security_indicators||{}).scada||0,securityTotal=inds.reduce((a,[,v])=>a+v,0),reviewRelevant=Math.max(0,securityTotal-routine);
  $('security').innerHTML=inds.length?`<div class="note"><b>Interpretation:</b> ${routine} routine SCADA-context matches are separated from ${reviewRelevant} other security-relevant keyword matches. These are evidence matches, not automatically confirmed incidents.</div><table><thead><tr><th>Evidence term</th><th>Records containing term</th></tr></thead><tbody>${inds.map(([k,v])=>`<tr><td>${esc(k)}</td><td class="num">${v}</td></tr>`).join('')}</tbody></table><p class="hint">Counts are record matches, not unique cyber incidents. Process-only terms are kept separate from security evidence.</p>`:'No configured OT/security evidence terms found.';
  $('ml').innerHTML=`<b>${esc(m.state)}</b><p>${esc(m.detail)}</p><p><b>Flagged records:</b> ${m.anomaly_indexes?.length?esc(m.anomaly_indexes.join(', ')):'none'}</p><p class="hint">Features: ${esc((m.features||[]).join(', ')||'none')}. Model output is advisory and requires human interpretation.</p>`;
  let cp=d.cyber_physical;$('correlation').innerHTML=`<table><tbody><tr><th>Correlation state</th><td><b class="${cp.correlated?'warn':'good'}">${cp.correlated?'CORRELATED REVIEW':'NO CORRELATION ESTABLISHED'}</b></td></tr><tr><th>Security keyword-record matches</th><td>${cp.security_matches}</td></tr><tr><th>Total out-of-band observations</th><td>${cp.quality_exception_values}</td></tr><tr><th>Response principle</th><td>Validate evidence → assess public-health/process impact → human-led containment/recovery → preserve audit evidence.</td></tr></tbody></table><div class="note">Top KPI counts <b>fields with exceptions</b>; this panel counts the <b>individual out-of-band observations</b> across those fields.</div>`;
  let energy=d.metrics.energy_kwh,energyDelta=energy&&energy.avg?(((energy.max-energy.avg)/energy.avg)*100).toFixed(1):null;$('energy').innerHTML=`<table><tbody><tr><th>Energy telemetry</th><td>${energy?`avg ${energy.avg} · max ${energy.max}`:'Not available in source'}</td></tr><tr><th>Energy review</th><td>${esc(d.maintenance.energy_state)}</td></tr><tr><th>Peak vs average</th><td>${energyDelta!==null?`${energyDelta}% above average`:'Not available'}</td></tr><tr><th>Optimization authority</th><td>Advisory only — no automatic process writes.</td></tr></tbody></table>`;
  $('source').innerHTML=`<table><tbody><tr><th>File</th><td class="mono">${esc(d.source.filename)}</td></tr><tr><th>Format</th><td>${esc(d.source.format.toUpperCase())}</td></tr><tr><th>Records</th><td>${d.source.records}</td></tr><tr><th>Fields</th><td>${d.source.fields.length}</td></tr></tbody></table><div class="fields">${esc(d.source.fields.join(' · '))}</div>`;
  let ev=d.security_events;$('events').innerHTML=ev.length?`<table><thead><tr><th>#</th><th>Timestamp</th><th>Severity</th><th>Source</th><th>Event</th><th>Security evidence</th><th>Message</th></tr></thead><tbody>${ev.map(x=>`<tr><td>${x.index}</td><td class="mono">${esc(x.timestamp)}</td><td>${esc(x.severity)}</td><td>${esc(x.source)}</td><td>${esc(x.event)}</td><td>${esc((x.security_evidence||[]).join(', '))}</td><td>${esc(x.message)}</td></tr>`).join('')}</tbody></table>`:'No security/process review events identified.';
  $('summary').innerHTML=`<b>Disposition: ${esc(s.decision)}</b><br>${esc(s.explanation||s.detail||'Human review is based on the evidence summarized above.')}<br><br>The result supports human decision-making for water-quality assurance, OT threat review, predictive maintenance and resource management; it does not issue plant-control commands.`;
  let rows=d.recent_records||d.records||[],cols=d.source.fields.slice(0,10);$('recent').innerHTML=rows.length?`<table><thead><tr><th>#</th>${cols.map(c=>`<th>${esc(c)}</th>`).join('')}</tr></thead><tbody>${rows.slice(-12).map((r,i)=>`<tr><td>${Math.max(1,d.source.records-rows.slice(-12).length+i+1)}</td>${cols.map(c=>`<td>${esc(r[c])}</td>`).join('')}</tr>`).join('')}</tbody></table>`:'No source rows available.';
}
$('analyze').addEventListener('click',async()=>{let f=$('file').files[0];$('error').style.display='none';if(!f){$('error').textContent='Select an authorized file first.';$('error').style.display='block';return}if(f.size>8*1024*1024){$('error').textContent='File exceeds the 8 MB limit.';$('error').style.display='block';return}try{let content=await f.text(),r=await fetch('/api/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({filename:f.name,content})}),d=await r.json();if(!r.ok)throw new Error(d.error||'Analysis failed');render(d)}catch(e){$('error').textContent=e.message;$('error').style.display='block'}});
</script>
</body>
</html>'''


class _Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, content_type: str, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; "
            "connect-src 'self'; frame-ancestors 'none'",
        )
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/":
            self._send(200, "text/html; charset=utf-8", HTML.encode("utf-8"))
            return
        if path == "/api/health":
            body = json.dumps(
                {"ok": True, "mode": "local-file-analysis", "version": "1.0.0"}
            ).encode()
            self._send(200, "application/json; charset=utf-8", body)
            return
        self._send(404, "text/plain; charset=utf-8", b"Not found")

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/analyze":
            self._send(404, "text/plain; charset=utf-8", b"Not found")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_BODY_BYTES:
                raise ValueError("Invalid or oversized request")

            payload = json.loads(self.rfile.read(length))
            filename = Path(str(payload.get("filename", ""))).name
            content = payload.get("content", "")
            if not filename or not isinstance(content, str):
                raise ValueError("filename and text content are required")

            result = analyze_content(filename, content)
            body = json.dumps(result, ensure_ascii=False).encode("utf-8")
            self._send(200, "application/json; charset=utf-8", body)
        except (ValueError, json.JSONDecodeError) as exc:
            body = json.dumps({"error": str(exc)}).encode()
            self._send(400, "application/json; charset=utf-8", body)

    def log_message(self, format: str, *args: object) -> None:
        return


def run_web_ui(
    host: str = "127.0.0.1", port: int = 8765, open_browser: bool = True
) -> None:
    if host not in {"127.0.0.1", "localhost"}:
        raise ValueError("AquaSentinel web UI may only bind to localhost")

    server = ThreadingHTTPServer((host, port), _Handler)
    url = f"http://127.0.0.1:{port}/"
    if open_browser:
        Timer(0.7, lambda: webbrowser.open(url)).start()

    print(f"AquaSentinel local analysis workstation: {url}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def self_check() -> dict[str, object]:
    result = analyze_content(
        "check.csv",
        "timestamp,severity,ph,turbidity,energy_kwh,membrane_health\n"
        "2026-01-01T00:00:00Z,info,7.2,0.3,390,92\n"
        "2026-01-01T00:01:00Z,warning,6.1,2.2,430,65\n",
    )
    if (
        result["source"]["records"] != 2
        or "Topic 133" not in HTML
        or "objectives" not in result
    ):
        raise RuntimeError("web UI self-check failed")
    return {
        "ok": True,
        "records": 2,
        "mode": "local-file-analysis",
        "topic": "133",
    }
