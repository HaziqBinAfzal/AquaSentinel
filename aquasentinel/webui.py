from __future__ import annotations

import json
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Timer
from urllib.parse import urlparse

from .ingestion import analyze_content

MAX_BODY_BYTES = 9 * 1024 * 1024

HTML = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AquaSentinel AI — Water & OT Analysis</title>
<style>
:root{--bg:#e9edf0;--paper:#fff;--soft:#f4f6f7;--ink:#17212b;--muted:#63707b;--line:#ccd4da;--head:#172b3a;--blue:#315b75;--green:#35644b;--amber:#856522;--red:#8a3838}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px "Segoe UI",Arial,sans-serif}header{background:var(--head);color:#fff;border-bottom:3px solid #0d1c27;padding:13px 24px;display:flex;justify-content:space-between;align-items:center}.brand{display:flex;gap:12px;align-items:center}.logo{width:38px;height:38px;border:1px solid #8195a4;display:grid;place-items:center;font-weight:700}.brand b{font-size:18px}.brand small{display:block;color:#bac7cf;margin-top:2px}.local{font:11px Consolas,monospace;border:1px solid #647b8c;padding:6px 9px}.wrap{max-width:1440px;margin:18px auto;padding:0 18px 30px}.boundary{font-size:12px;background:#f7f3e8;border:1px solid #d8cba8;padding:9px 12px;margin-bottom:12px}.panel{background:var(--paper);border:1px solid var(--line);margin-bottom:12px}.ph{background:var(--soft);border-bottom:1px solid var(--line);padding:10px 13px;font-weight:600}.pb{padding:13px}.source{display:grid;grid-template-columns:1.5fr 1fr auto;gap:12px;align-items:end}label,.eyebrow{display:block;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.07em;margin-bottom:5px}input{width:100%;padding:9px;border:1px solid #adb9c2;background:#fff}button{padding:10px 16px;background:#244a63;color:#fff;border:1px solid #17364a;font-weight:600;cursor:pointer}.hint{font-size:12px;color:var(--muted);line-height:1.4}.empty{text-align:center;padding:55px 20px;background:#fff;border:1px solid var(--line);color:var(--muted)}.empty b{display:block;font-size:18px;color:#34414a;margin-bottom:7px}#dash{display:none}.kpis{display:grid;grid-template-columns:repeat(6,1fr);gap:9px;margin-bottom:12px}.kpi{background:#fff;border:1px solid var(--line);padding:12px}.kpi strong{display:block;font:600 22px Consolas,monospace;margin-top:5px}.good{color:var(--green)}.warn{color:var(--amber)}.bad{color:var(--red)}.objectives{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}.objective{border:1px solid var(--line);background:#fff;padding:12px}.objective h3{font-size:13px;margin:0 0 8px}.tag{font:600 10px Consolas,monospace;padding:3px 6px;border:1px solid #b7c1c8;display:inline-block;margin-bottom:7px}.objective p{font-size:12px;color:#53606a;line-height:1.45;margin:0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}.wide{grid-column:1/-1}table{border-collapse:collapse;width:100%;font-size:12px}th,td{padding:7px 8px;border-bottom:1px solid #e0e5e8;text-align:left;vertical-align:top}th{background:#f4f6f7;color:#52606b;font-weight:600}.num{text-align:right;font-family:Consolas,monospace}.mono{font-family:Consolas,monospace}.scroll{overflow:auto;max-height:360px}.scroll table{min-width:850px}.chartgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}.chart{border:1px solid #d8dee3;padding:9px}.chart h4{margin:0 0 5px;font-size:11px}.chart svg{width:100%;height:90px;background:#fafbfb}.flag{border-left:3px solid var(--amber);background:#faf7ed;padding:7px 9px;margin:5px 0;font-size:12px}.summary{background:#f5f7f8;border-left:4px solid var(--blue);padding:12px;line-height:1.55}.fields{font:11px Consolas,monospace;color:#5d6972;line-height:1.7;word-break:break-word}.error{display:none;background:#f9eded;border:1px solid #d9b6b6;color:#7b3030;padding:9px;margin-top:8px}.footer{font-size:11px;color:#68747d;padding:7px 0}@media(max-width:1000px){.kpis{grid-template-columns:repeat(3,1fr)}.objectives{grid-template-columns:1fr 1fr}.grid{grid-template-columns:1fr}.wide{grid-column:auto}.source{grid-template-columns:1fr}}@media(max-width:650px){.kpis,.objectives,.chartgrid{grid-template-columns:1fr 1fr}.local{display:none}}
</style></head><body><header><div class="brand"><div class="logo">AS</div><div><b>AquaSentinel AI</b><small>Local analysis workstation • Topic 133 • Water / Desalination Infrastructure</small></div></div><div class="local">127.0.0.1 · READ ONLY</div></header><main class="wrap"><div class="boundary"><b>Safety boundary:</b> local defensive analysis of user-supplied evidence only. No PLC, SCADA, dosing or utility-control path. Water-quality bands are illustrative classroom review bands, not regulatory limits.</div><section class="panel"><div class="ph">Analysis source</div><div class="pb source"><div><label>Authorized data file</label><input id="file" type="file" accept=".log,.txt,.csv,.json,.jsonl"></div><div class="hint">LOG, TXT, CSV, JSON or JSONL · max 8 MB. Nothing is preloaded; analysis starts only after you select a file.</div><button id="analyze">Analyze evidence</button></div><div id="error" class="error"></div></section><div id="empty" class="empty"><b>No dataset loaded</b>Select an authorized water/process telemetry or defensive OT/security log. Results will be organized against the Topic 133 learning objectives.</div><div id="dash"><div class="kpis"><div class="kpi"><span class="eyebrow">Operator disposition</span><strong id="decision">--</strong></div><div class="kpi"><span class="eyebrow">Evidence score</span><strong id="risk">--</strong></div><div class="kpi"><span class="eyebrow">Records analyzed</span><strong id="records">--</strong></div><div class="kpi"><span class="eyebrow">Critical / error</span><strong id="errors">--</strong></div><div class="kpi"><span class="eyebrow">Quality exceptions</span><strong id="flags">--</strong></div><div class="kpi"><span class="eyebrow">ML flagged records</span><strong id="mlcount">--</strong></div></div><section class="panel"><div class="ph">Topic 133 coverage — key learning objectives</div><div class="pb objectives" id="objectives"></div></section><div class="grid"><section class="panel"><div class="ph">1 · Water quality assurance</div><div class="pb"><div class="scroll"><table><thead><tr><th>Measurement</th><th>Samples</th><th>Min</th><th>Average</th><th>Max</th><th>Latest</th></tr></thead><tbody id="metrics"></tbody></table></div><div id="qualityflags"></div></div></section><section class="panel"><div class="ph">2 · Desalination process & predictive maintenance</div><div class="pb" id="maintenance"></div></section><section class="panel wide"><div class="ph">Process telemetry trends</div><div class="pb chartgrid" id="charts"></div></section><section class="panel"><div class="ph">3 · OT / SCADA security evidence</div><div class="pb" id="security"></div></section><section class="panel"><div class="ph">4 · AI anomaly detection</div><div class="pb" id="ml"></div></section><section class="panel wide"><div class="ph">5 · Cyber-physical correlation & response evidence</div><div class="pb" id="correlation"></div></section><section class="panel"><div class="ph">6 · Energy & resource review</div><div class="pb" id="energy"></div></section><section class="panel"><div class="ph">Source profile & audit trail</div><div class="pb" id="source"></div></section><section class="panel wide"><div class="ph">Security / process event timeline</div><div class="pb scroll" id="events"></div></section><section class="panel wide"><div class="ph">Analysis summary for human review</div><div class="pb"><div class="summary" id="summary"></div></div></section><section class="panel wide"><div class="ph">Source records — recent evidence</div><div class="pb scroll" id="recent"></div></section></div><div class="footer">AquaSentinel AI v1.0.0 · Topic 133 · local defensive analysis · human decision authority · No automated industrial control</div></div></main>
<script>
const $=x=>document.getElementById(x),esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const cls=v=>v>=70?'bad':v>=35?'warn':'good';function spark(name,v){let a=v.series||[];if(a.length<2)return'';let lo=Math.min(...a),hi=Math.max(...a),r=hi-lo||1,pts=a.map((x,i)=>`${i/(a.length-1)*100},${82-(x-lo)/r*70}`).join(' ');return `<div class="chart"><h4>${esc(name.replaceAll('_',' '))}</h4><svg viewBox="0 0 100 90" preserveAspectRatio="none"><polyline points="${pts}" fill="none" stroke="#315b75" stroke-width="1.4" vector-effect="non-scaling-stroke"/></svg><span class="hint">min ${v.min} · avg ${v.avg} · max ${v.max}</span></div>`}function render(d){$('empty').style.display='none';$('dash').style.display='block';let s=d.summary,m=d.ml;$('decision').textContent=s.decision;$('decision').className=s.decision==='REVIEW'?'warn':'good';$('risk').textContent=s.risk_score+'/100';$('risk').className=cls(s.risk_score);$('records').textContent=d.source.records;$('errors').textContent=s.critical+' / '+s.errors;$('errors').className=s.critical+s.errors?'bad':'good';$('flags').textContent=s.review_flags;$('flags').className=s.review_flags?'warn':'good';$('mlcount').textContent=m.state==='ANALYZED'?m.anomaly_count:'N/A';$('objectives').innerHTML=d.objectives.map(o=>`<article class="objective"><h3>${esc(o.title)}</h3><span class="tag">${esc(o.status)}</span><p>${esc(o.detail)}</p></article>`).join('');$('metrics').innerHTML=Object.entries(d.metrics).map(([k,v])=>`<tr><td>${esc(k.replaceAll('_',' '))}</td><td class="num">${v.count}</td><td class="num">${v.min}</td><td class="num">${v.avg}</td><td class="num">${v.max}</td><td class="num">${v.last}</td></tr>`).join('')||'<tr><td colspan="6">Not available in source.</td></tr>';$('qualityflags').innerHTML=d.review_flags.length?d.review_flags.map(f=>`<div class="flag"><b>${esc(f.field.replaceAll('_',' '))}</b>: ${f.outside_band}/${f.count} values outside the illustrative classroom band.</div>`).join(''):'<p class="good">No configured classroom-band exceptions found.</p>';$('charts').innerHTML=Object.entries(d.metrics).filter(([k])=>['ph','conductivity','turbidity','residual_chlorine','ro_pressure','flow_rate','energy_kwh','membrane_health'].includes(k)).map(([k,v])=>spark(k,v)).join('')||'<span class="hint">No trendable configured telemetry in source.</span>';$('maintenance').innerHTML=`<table><tbody><tr><th>Membrane fouling review</th><td>${d.maintenance.fouling_review?'<b class="warn">INDICATED</b>':'Not indicated by configured checks'}</td></tr><tr><th>RO pressure</th><td>${d.metrics.ro_pressure?`max ${d.metrics.ro_pressure.max}`:'Not available in source'}</td></tr><tr><th>Flow rate</th><td>${d.metrics.flow_rate?`min ${d.metrics.flow_rate.min}`:'Not available in source'}</td></tr><tr><th>Membrane health</th><td>${d.metrics.membrane_health?`min ${d.metrics.membrane_health.min}`:'Not available in source'}</td></tr></tbody></table>`;let inds=Object.entries(d.security_indicators||{});$('security').innerHTML=inds.length?`<table><thead><tr><th>Evidence term</th><th>Records containing term</th></tr></thead><tbody>${inds.map(([k,v])=>`<tr><td>${esc(k)}</td><td class="num">${v}</td></tr>`).join('')}</tbody></table><p class="hint">Counts are record matches, not unique cyber incidents. Process-only terms are kept separate from security evidence.</p>`:'No configured OT/security evidence terms found.';$('ml').innerHTML=`<b>${esc(m.state)}</b><p>${esc(m.detail)}</p><p><b>Flagged records:</b> ${m.anomaly_indexes?.length?esc(m.anomaly_indexes.join(', ')):'none'}</p><p class="hint">Features: ${esc((m.features||[]).join(', ')||'none')}. Model output is advisory and requires human interpretation.</p>`;let cp=d.cyber_physical;$('correlation').innerHTML=`<table><tbody><tr><th>Correlation state</th><td><b class="${cp.correlated?'warn':'good'}">${cp.correlated?'CORRELATED REVIEW':'NO CORRELATION ESTABLISHED'}</b></td></tr><tr><th>Security keyword-record matches</th><td>${cp.security_matches}</td></tr><tr><th>Quality exception values</th><td>${cp.quality_exception_values}</td></tr><tr><th>Response principle</th><td>Validate evidence → assess public-health/process impact → human-led containment/recovery → preserve audit evidence.</td></tr></tbody></table>`;$('energy').innerHTML=`<table><tbody><tr><th>Energy telemetry</th><td>${d.metrics.energy_kwh?`avg ${d.metrics.energy_kwh.avg} · max ${d.metrics.energy_kwh.max}`:'Not available in source'}</td></tr><tr><th>Energy review</th><td>${esc(d.maintenance.energy_state)}</td></tr><tr><th>Optimization authority</th><td>Advisory only — no automatic process writes.</td></tr></tbody></table>`;$('source').innerHTML=`<table><tbody><tr><th>File</th><td class="mono">${esc(d.source.filename)}</td></tr><tr><th>Format</th><td>${esc(d.source.format.toUpperCase())}</td></tr><tr><th>Records</th><td>${d.source.records}</td></tr><tr><th>Fields</th><td>${d.source.fields.length}</td></tr></tbody></table><div class="fields">${esc(d.source.fields.join(' · '))}</div>`;let ev=d.security_events;$('events').innerHTML=ev.length?`<table><thead><tr><th>#</th><th>Timestamp</th><th>Severity</th><th>Source</th><th>Event</th><th>Security evidence</th><th>Message</th></tr></thead><tbody>${ev.map(x=>`<tr><td>${x.index}</td><td class="mono">${esc(x.timestamp)}</td><td>${esc(x.severity)}</td><td>${esc(x.source)}</td><td>${esc(x.event)}</td><td>${esc(x.evidence)}</td><td>${esc(x.message)}</td></tr>`).join('')}</tbody></table>`:'No security/review events identified.';let reasons=[];if(s.critical||s.errors)reasons.push(`${s.critical} critical and ${s.errors} error records`);if(d.review_flags.length)reasons.push(`${d.review_flags.length} water/process fields with review exceptions`);if(m.anomaly_count)reasons.push(`${m.anomaly_count} records flagged by IsolationForest`);if(cp.correlated)reasons.push('security evidence coincides with process/quality exceptions');$('summary').innerHTML=`<b>Disposition: ${esc(s.decision)}</b><br>${reasons.length?'Review is driven by '+esc(reasons.join(', '))+'.':'No configured evidence currently requires escalation.'}<br><br>The result supports human decision-making for water-quality assurance, OT threat review, predictive maintenance and resource management; it does not issue plant-control commands.`;let rows=d.recent_records,keys=[];rows.forEach(x=>Object.keys(x.record).forEach(k=>{if(!keys.includes(k)&&keys.length<10)keys.push(k)}));$('recent').innerHTML=rows.length?`<table><thead><tr><th>#</th>${keys.map(k=>`<th>${esc(k)}</th>`).join('')}</tr></thead><tbody>${rows.map(x=>`<tr><td>${x.index}</td>${keys.map(k=>`<td class="mono">${esc(x.record[k]??'')}</td>`).join('')}</tr>`).join('')}</tbody></table>`:'No records available.'}$('analyze').onclick=async()=>{let f=$('file').files[0];if(!f){$('error').textContent='Select a supported file first.';$('error').style.display='block';return}if(f.size>8*1024*1024){$('error').textContent='Selected file exceeds 8 MB.';$('error').style.display='block';return}let b=$('analyze');b.disabled=true;b.textContent='Analyzing…';try{let r=await fetch('/api/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({filename:f.name,content:await f.text()})}),d=await r.json();if(!r.ok)throw new Error(d.error||'Analysis failed');$('error').style.display='none';render(d)}catch(e){$('error').textContent=e.message;$('error').style.display='block'}finally{b.disabled=false;b.textContent='Analyze evidence'}};
</script></body></html>'''


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
