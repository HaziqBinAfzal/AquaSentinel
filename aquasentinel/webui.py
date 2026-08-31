from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Timer
from urllib.parse import parse_qs, urlparse
import webbrowser

from .analytics import analyze
from .incidents import incident_severity, response_plan
from .ml import QualityMLModel
from .optimizer import optimize
from .scenarios import SCENARIOS
from .security import correlate, events_for
from .telemetry import sample

_MODEL: QualityMLModel | None = None


def _model() -> QualityMLModel:
    global _MODEL
    if _MODEL is None:
        _MODEL = QualityMLModel.train_default()
    return _MODEL


def build_state(scenario: str = "normal", step: int = 0, seed: int = 133) -> dict:
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario}")
    step = max(0, int(step))
    telemetry = sample(scenario, step, seed=seed)
    result = analyze(telemetry)
    ml_result = _model().score(telemetry)
    security_events = events_for(telemetry.cyber_event)
    correlation = correlate(security_events, result["quality_flags"])

    result["priority"] = max(
        result["priority"],
        ml_result["ml_priority"],
        correlation["correlation_score"],
    )
    if ml_result["ml_state"] == "ANOMALOUS" or correlation["correlation_score"] >= 70:
        result["human_review_required"] = True

    optimization = optimize(telemetry, result).dict()
    plan = response_plan(result, correlation)

    return {
        "product": "AquaSentinel AI",
        "version": "1.0.0",
        "scenario": scenario,
        "scenario_description": SCENARIOS[scenario],
        "step": step,
        "telemetry": telemetry.dict(),
        "analysis": result,
        "ml": ml_result,
        "security_events": [event.dict() for event in security_events],
        "correlation": correlation,
        "optimization": optimization,
        "incident": {
            "severity": incident_severity(result, correlation),
            "steps": [
                {"stage": item.stage, "action": item.action, "purpose": item.purpose}
                for item in plan
            ],
        },
        "architecture": ["Enterprise / SOC", "Industrial DMZ", "OT / SCADA", "Safety & Quality", "Synthetic Treatment Process", "Analytics", "Human Review", "Audit / Report"],
        "process": ["SEA / RAW", "PRETREAT", "HP PUMP", "REVERSE OSMOSIS", "POST-TREAT", "STORAGE"],
        "assurance": [
            "NIST SP 800-82 educational OT-security context",
            "EPA water-quality / public-health reporting context",
            "WHO risk-based water-safety context",
        ],
        "safety": "Synthetic, defensive, read-only classroom simulation. No real PLC, SCADA, dosing or utility control path.",
    }


HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AquaSentinel AI — Local Operations Dashboard</title>
<style>
:root{--bg:#07121b;--panel:#0c1d28;--panel2:#102735;--line:#173d4d;--text:#e8f5f8;--muted:#85a7b4;--cyan:#3cd9e6;--blue:#4aa3ff;--green:#39d98a;--amber:#ffbf5f;--red:#ff5d73;--purple:#ba8cff}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 80% 0,#0b2938 0,#07121b 35%,#050b11 100%);color:var(--text);font-family:Inter,Segoe UI,Arial,sans-serif;min-height:100vh}.shell{max-width:1500px;margin:auto;padding:22px}.top{display:flex;align-items:center;justify-content:space-between;gap:18px;margin-bottom:18px}.brand{display:flex;gap:14px;align-items:center}.logo{width:46px;height:46px;border:1px solid #2b8094;border-radius:14px;display:grid;place-items:center;background:linear-gradient(145deg,#123849,#09202c);box-shadow:0 0 28px #1f859733;font-weight:800;color:var(--cyan)}h1{font-size:23px;margin:0;letter-spacing:.03em}.sub{color:var(--muted);font-size:12px;margin-top:4px}.badge{font-size:11px;border:1px solid #256377;background:#0b2b37;padding:7px 10px;border-radius:999px;color:#aeeaf0}.controls{display:flex;gap:9px;align-items:center;flex-wrap:wrap}.controls select,.controls button{background:#0b202c;border:1px solid #245065;color:var(--text);padding:9px 12px;border-radius:9px;font-weight:600}.controls button{cursor:pointer}.controls button.primary{background:#0a5968;border-color:#2ec9d7}.banner{border:1px solid #26576a;background:#0a202b;border-radius:12px;padding:10px 14px;color:#b9d9e1;font-size:12px;margin-bottom:16px}.banner b{color:var(--green)}.metrics{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:12px}.metric,.card{background:linear-gradient(180deg,#0d202c,#0a1821);border:1px solid #183b4b;border-radius:13px;box-shadow:0 14px 40px #0005}.metric{padding:14px}.k{color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.12em}.v{font-size:24px;font-weight:750;margin-top:6px}.small{font-size:11px;color:var(--muted);margin-top:4px}.grid{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:12px}.card{padding:15px;min-width:0}.card h2{font-size:12px;letter-spacing:.12em;color:#a7d7e2;margin:0 0 13px;text-transform:uppercase}.process{grid-column:1/-1}.stages{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}.stage{padding:12px 7px;text-align:center;border-radius:10px;background:#0d2633;border:1px solid #1d5062;position:relative;font-size:11px;color:#bdeaf1}.stage:not(:last-child):after{content:'›';position:absolute;right:-8px;top:50%;transform:translateY(-50%);color:var(--cyan);font-size:23px;z-index:2}.stage strong{display:block;color:white;font-size:12px;margin-bottom:5px}.bar{height:8px;border-radius:8px;background:#071016;overflow:hidden;margin-top:8px}.fill{height:100%;width:0;background:linear-gradient(90deg,var(--green),var(--cyan));transition:width .35s}.fill.warn{background:linear-gradient(90deg,var(--amber),var(--red))}.rows{display:grid;gap:8px}.row{display:flex;justify-content:space-between;gap:10px;padding-bottom:7px;border-bottom:1px solid #153240;font-size:12px}.row span:first-child{color:var(--muted)}.state{font-weight:750}.good{color:var(--green)}.warn{color:var(--amber)}.bad{color:var(--red)}.purple{color:var(--purple)}.chart{height:165px;width:100%;display:block}.event{border-left:3px solid var(--cyan);padding:8px 10px;background:#0c2531;border-radius:5px;margin:7px 0;font-size:11px}.event.red{border-color:var(--red)}.decision{font-size:22px;font-weight:800;margin:7px 0}.timeline{display:grid;grid-template-columns:repeat(8,1fr);gap:6px}.tick{background:#0b2330;border:1px solid #1a4658;border-radius:8px;padding:8px;font-size:9px;min-height:68px}.tick b{display:block;color:#bcecf2;font-size:10px;margin-bottom:5px}.architecture{display:flex;gap:5px;flex-wrap:wrap;align-items:center}.zone{padding:7px 9px;border:1px solid #235568;background:#0c2632;border-radius:7px;font-size:10px}.arrow{color:var(--cyan)}.footer{margin-top:12px;color:#6f939f;text-align:center;font-size:10px}.span2{grid-column:span 2}@media(max-width:1050px){.metrics{grid-template-columns:repeat(3,1fr)}.grid{grid-template-columns:1fr 1fr}.process{grid-column:1/-1}.span2{grid-column:1/-1}.timeline{grid-template-columns:repeat(4,1fr)}}@media(max-width:680px){.shell{padding:12px}.top{align-items:flex-start;flex-direction:column}.metrics,.grid{grid-template-columns:1fr 1fr}.stages{grid-template-columns:repeat(2,1fr)}.stage:after{display:none}.timeline{grid-template-columns:repeat(2,1fr)}}
</style>
</head>
<body><div class="shell">
<div class="top"><div class="brand"><div class="logo">AS</div><div><h1>AquaSentinel AI <span style="color:#5fa8bc;font-size:13px">v1.0.0</span></h1><div class="sub">SMART WATER & DESALINATION • LOCAL OPERATIONS / SOC DASHBOARD</div></div></div><div class="controls"><span class="badge">● LOCALHOST / READ ONLY</span><select id="scenario"></select><button id="toggle" class="primary">Pause</button><button id="next">Next frame</button></div></div>
<div class="banner"><b>SAFE DEMO BOUNDARY:</b> Synthetic telemetry and simulated security evidence only. AI is advisory. No connection or write path to real PLC, SCADA, dosing controllers, utilities or public-health infrastructure.</div>
<div class="metrics">
<div class="metric"><div class="k">Overall priority</div><div class="v" id="priority">--</div><div class="bar"><div class="fill" id="prioritybar"></div></div></div>
<div class="metric"><div class="k">Water quality</div><div class="v" id="quality">--</div><div class="small" id="qualityscore">--</div></div>
<div class="metric"><div class="k">AI / ML state</div><div class="v" id="ml">--</div><div class="small" id="mlscore">--</div></div>
<div class="metric"><div class="k">OT correlation</div><div class="v" id="corr">--</div><div class="small" id="corrstate">--</div></div>
<div class="metric"><div class="k">Optimization</div><div class="v" id="opt">--</div><div class="small">guardrailed advisory</div></div>
<div class="metric"><div class="k">Decision</div><div class="v" id="decision">--</div><div class="small" id="severity">--</div></div>
</div>
<div class="grid">
<div class="card process"><h2>Synthetic desalination process</h2><div class="stages" id="stages"></div></div>
<div class="card"><h2>Water quality + process telemetry</h2><div class="rows" id="telemetry"></div></div>
<div class="card"><h2>AI + predictive maintenance</h2><div class="rows" id="airows"></div><canvas class="chart" id="chart"></canvas></div>
<div class="card"><h2>OT / SCADA security</h2><div class="rows" id="security"></div><div id="events"></div></div>
<div class="card"><h2>Resource optimizer</h2><div class="rows" id="optimizer"></div></div>
<div class="card span2"><h2>Cyber-physical incident response</h2><div class="decision" id="incidentSeverity">--</div><div class="timeline" id="timeline"></div></div>
<div class="card"><h2>Architecture / trust zones</h2><div class="architecture" id="architecture"></div><h2 style="margin-top:18px">Assurance context</h2><div id="assurance"></div></div>
</div><div class="footer">AquaSentinel AI • Topic 133 • Browser UI served only on 127.0.0.1 • Synthetic / defensive / read-only</div></div>
<script>
const scenarios=['normal','sensor_anomaly','quality_anomaly','dosing_event','fouling','optimization'];const sel=document.getElementById('scenario');scenarios.forEach(x=>{let o=document.createElement('option');o.value=x;o.textContent=x.replace('_',' ').toUpperCase();sel.appendChild(o)});sel.value='normal';let step=0,running=true,hist=[];
const $=id=>document.getElementById(id);const cls=(v,bad=70,warn=35)=>v>=bad?'bad':v>=warn?'warn':'good';const row=(a,b)=>`<div class="row"><span>${a}</span><strong>${b}</strong></div>`;
function drawChart(){let c=$('chart'),dpr=window.devicePixelRatio||1,w=c.clientWidth,h=c.clientHeight;c.width=w*dpr;c.height=h*dpr;let x=c.getContext('2d');x.scale(dpr,dpr);x.clearRect(0,0,w,h);x.strokeStyle='#173c4b';x.lineWidth=1;for(let i=1;i<4;i++){x.beginPath();x.moveTo(0,h*i/4);x.lineTo(w,h*i/4);x.stroke()}if(hist.length<2)return;function line(key,color,max=100){x.strokeStyle=color;x.lineWidth=2;x.beginPath();hist.forEach((p,i)=>{let px=i*w/Math.max(hist.length-1,1),py=h-(Math.min(max,p[key])/max)*(h-10)-5;i?x.lineTo(px,py):x.moveTo(px,py)});x.stroke()}line('priority','#ff6b7f');line('ml','#bb8cff');line('mem','#3cd9e6')}
function render(d){let t=d.telemetry,a=d.analysis,m=d.ml,c=d.correlation,o=d.optimization;$('priority').textContent=Math.round(a.priority)+'%';$('priority').className='v '+cls(a.priority,85,45);$('prioritybar').style.width=Math.min(100,a.priority)+'%';$('prioritybar').className='fill '+(a.priority>=60?'warn':'');$('quality').textContent=a.quality_state;$('quality').className='v '+(a.quality_score>0?'warn':'good');$('qualityscore').textContent='Rule priority '+a.quality_score+'%';$('ml').textContent=m.ml_state;$('ml').className='v '+(m.ml_state==='ANOMALOUS'?'purple':'good');$('mlscore').textContent='ML priority '+m.ml_priority+'%';$('corr').textContent=c.correlation_score+'%';$('corr').className='v '+cls(c.correlation_score,70,30);$('corrstate').textContent=c.disposition;$('opt').textContent=o.mode;$('opt').className='v '+(o.mode==='HOLD-SAFE'?'warn':'good');let review=a.human_review_required||m.ml_state==='ANOMALOUS'||c.correlation_score>=70;$('decision').textContent=review?'HUMAN REVIEW':'MONITOR';$('decision').className='v '+(review?'warn':'good');$('severity').textContent=d.incident.severity;
let vals=[['SEA / RAW','Sal '+t.salinity],['PRETREAT','Turb '+t.turbidity],['HP PUMP',t.feed_pressure+' bar'],['REVERSE OSMOSIS',t.ro_pressure+' bar • Mem '+t.membrane_health+'%'],['POST-TREAT','Cl '+t.residual_chlorine],['STORAGE','Tank '+t.tank_level+'%']];$('stages').innerHTML=vals.map(v=>`<div class="stage"><strong>${v[0]}</strong>${v[1]}</div>`).join('');
$('telemetry').innerHTML=row('pH',t.ph)+row('Conductivity',t.conductivity)+row('Turbidity',t.turbidity)+row('Residual chlorine',t.residual_chlorine)+row('Salinity',t.salinity)+row('Flow rate',t.flow_rate)+row('Tank level',t.tank_level+'%')+row('Energy',t.energy_kwh+' kWh');
$('airows').innerHTML=row('IsolationForest',m.ml_state)+row('ML priority',m.ml_priority+'%')+row('Membrane health',t.membrane_health+'%')+row('Fouling risk',a.fouling_risk+'%')+row('Maintenance',a.maintenance);
$('security').innerHTML=row('SCADA evidence',t.cyber_event)+row('Correlation',c.correlation_score+'%')+row('Cyber-physical',c.cyber_physical?'YES':'NO')+row('Evidence sources',c.sources.join(', '));$('events').innerHTML=d.security_events.map(e=>`<div class="event ${e.severity>=70?'red':''}">${e.source||'security'} • ${e.event||e.kind||'observation'} • severity ${e.severity}</div>`).join('')||'<div class="event">Baseline synthetic monitoring • no notable OT event</div>';
$('optimizer').innerHTML=row('Mode',o.mode)+row('Energy target',o.energy_target_pct+'%')+row('Production target',o.production_target_pct+'%')+row('Quality guardrail',o.quality_guardrail)+row('Control writes','DISABLED');$('incidentSeverity').textContent=d.incident.severity;$('incidentSeverity').className='decision '+(review?'warn':'good');$('timeline').innerHTML=d.incident.steps.map(s=>`<div class="tick"><b>${s.stage}</b>${s.action}</div>`).join('');$('architecture').innerHTML=d.architecture.map((z,i)=>`<span class="zone">${z}</span>${i<d.architecture.length-1?'<span class="arrow">›</span>':''}`).join('');$('assurance').innerHTML=d.assurance.map(x=>`<div class="event">${x}</div>`).join('');hist.push({priority:a.priority,ml:m.ml_priority,mem:t.membrane_health});if(hist.length>32)hist.shift();drawChart()}
async function load(){try{let r=await fetch(`/api/state?scenario=${encodeURIComponent(sel.value)}&step=${step}`);if(!r.ok)throw Error(await r.text());render(await r.json());}catch(e){console.error(e)}}sel.onchange=()=>{step=0;hist=[];load()};$('toggle').onclick=()=>{running=!running;$('toggle').textContent=running?'Pause':'Resume'};$('next').onclick=()=>{step++;load()};window.onresize=drawChart;load();setInterval(()=>{if(running){step++;load()}},1200);
</script></body></html>'''


class _Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, content_type: str, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send(200, "text/html; charset=utf-8", HTML.encode("utf-8"))
            return
        if parsed.path == "/api/health":
            body = json.dumps({"ok": True, "mode": "synthetic-read-only", "version": "1.0.0"}).encode()
            self._send(200, "application/json; charset=utf-8", body)
            return
        if parsed.path == "/api/state":
            query = parse_qs(parsed.query)
            scenario = query.get("scenario", ["normal"])[0]
            try:
                step = int(query.get("step", ["0"])[0])
                state = build_state(scenario, step)
            except (ValueError, TypeError) as exc:
                self._send(400, "application/json; charset=utf-8", json.dumps({"error": str(exc)}).encode())
                return
            self._send(200, "application/json; charset=utf-8", json.dumps(state).encode("utf-8"))
            return
        self._send(404, "text/plain; charset=utf-8", b"Not found")

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        return


def run_web(port: int = 8765, open_browser: bool = True, check_only: bool = False) -> None:
    if not 1024 <= int(port) <= 65535:
        raise SystemExit("--port must be between 1024 and 65535")
    if check_only:
        state = build_state("dosing_event", 8)
        if not state["safety"].startswith("Synthetic"):
            raise RuntimeError("Local dashboard safety boundary check failed")
        if state["optimization"]["mode"] != "HOLD-SAFE":
            raise RuntimeError("Local dashboard guardrail check failed")
        print("Local web dashboard check passed")
        return

    address = ("127.0.0.1", int(port))
    url = f"http://127.0.0.1:{port}/"
    server = ThreadingHTTPServer(address, _Handler)
    print("AquaSentinel AI local dashboard")
    print(f"Open: {url}")
    print("BOUNDARY: localhost only; synthetic / defensive / read-only")
    print("Press Ctrl+C to stop the local dashboard.")
    if open_browser:
        Timer(0.7, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever(poll_interval=0.3)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("AquaSentinel local dashboard stopped")
