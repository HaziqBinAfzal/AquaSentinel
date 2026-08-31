# AquaSentinel AI — Project & Viva Guide

## 1. What the project is

AquaSentinel AI v1.0.0 is a synthetic, defensive demonstration of a smart water and desalination infrastructure security platform. It combines process visibility, OT cybersecurity, water-quality monitoring, AI anomaly detection, membrane-health analysis, resource optimization, incident response, DevSecOps evidence and assurance context without connecting to a real plant.

The project has two user interfaces over the same analysis engine:

- a local browser dashboard at `http://127.0.0.1:8765/`; and
- an industrial terminal/SOC interface.

The browser UI is the recommended visual examiner experience, while the terminal remains useful for showing commands, verification and detailed output.

## 2. The simulated desalination process

```text
Raw / Sea Water
      |
Pretreatment
      |
High-Pressure Pump
      |
Reverse Osmosis Membranes
      |
Post-Treatment / Disinfection
      |
Storage
      |
Distribution
```

Pretreatment reduces contaminants before the membrane stage. The high-pressure pump supplies the pressure needed for reverse osmosis. RO membranes separate salts and other dissolved material. Post-treatment stabilizes/disinfects the water before it enters storage and distribution.

## 3. Why SCADA and OT matter

SCADA provides supervisory monitoring of industrial processes. OT includes the industrial systems that observe or influence the physical process. In this educational project there is no real control path. Instead, AquaSentinel creates synthetic telemetry and synthetic security evidence so the student can explain how monitoring and incident reasoning work safely.

The trust-zone model is:

```text
Enterprise / SOC
      |
Industrial DMZ
      |
OT / SCADA
      |
Safety & Quality
      |
Synthetic Treatment Process
```

The Industrial DMZ demonstrates separation between enterprise systems and OT. The Safety & Quality layer represents independent verification rather than assuming that a SCADA value is automatically trustworthy.

## 4. Telemetry and water-quality monitoring

`telemetry.py` generates repeatable synthetic observations including pH, conductivity, turbidity, residual chlorine, salinity, feed pressure, RO pressure, flow, temperature, tank level, pump state, energy use and membrane health.

`analytics.py` evaluates that evidence with transparent classroom rules. These are illustrative teaching thresholds, not regulatory operating limits. Multiple abnormal measurements produce higher concern than a single unexpected reading because cross-sensor evidence is stronger.

A useful viva sentence is:

> A sensor anomaly is evidence, not automatic proof of contamination. I cross-check independent process and quality measurements before escalating.

## 5. AI anomaly detection

`ml.py` trains an IsolationForest model on synthetic baseline data. IsolationForest is useful for anomaly detection because it learns the shape of normal multivariable observations and can identify unusual combinations without needing a labeled example of every possible incident.

The ML model does not control the simulated plant. Its purpose is prioritization. Deterministic rules stay visible for explainability, while ML adds another signal when the combination of measurements looks unusual.

A useful viva sentence is:

> The AI is advisory. It supports anomaly prioritization, while validated quality rules, engineering constraints and human authority remain above the model.

## 6. OT cybersecurity correlation

`security.py` creates safe synthetic security observations inspired by the kinds of evidence that tools such as Zeek, Suricata and SCADA audit logs can provide. It does not scan, attack or command a real industrial network.

For the `dosing_event` scenario, the system correlates an unexpected synthetic control event with process/quality evidence. This demonstrates why a SOC alert should not be assessed only as an IT event — the possible physical consequence matters.

The incident reasoning chain is:

```text
Detect -> Validate -> Correlate -> Assess consequence -> Hold unsafe optimization
       -> Human review -> Verify quality -> Recover -> Preserve evidence
```

## 7. Membrane fouling and predictive maintenance

The `fouling` scenario gradually lowers synthetic membrane health, raises pressure demand, reduces flow and increases energy consumption. `analytics.py` converts these related process changes into a fouling-risk score and maintenance recommendation.

This demonstrates predictive maintenance: trends can be used to prioritize inspection or maintenance instead of waiting only for complete equipment failure.

## 8. AI-driven resource optimization

`optimizer.py` recommends one of several advisory modes:

- `BALANCED` for ordinary safe operation.
- `ENERGY-SAVER` when storage is healthy and energy consumption is high.
- `SUPPLY-RECOVERY` when storage reserve is low.
- `MAINTENANCE-AWARE` when membrane condition makes aggressive production inefficient.
- `HOLD-SAFE` when quality or cybersecurity evidence requires verification.

The optimizer cannot override quality/security concerns. Efficiency is subordinate to validated safe operation.

## 9. Localhost browser dashboard

`webui.py` serves a responsive AquaSentinel dashboard on `127.0.0.1` only. It uses the Python standard-library HTTP server, so no separate web framework or cloud service is required.

Start it with:

```bash
aquasentinel web
```

Default address:

```text
http://127.0.0.1:8765/
```

The dashboard shows the synthetic desalination process, live telemetry, water quality, IsolationForest state, OT/SCADA evidence, cyber-physical correlation, overall priority, membrane/fouling status, optimization mode, final `MONITOR` or `HUMAN REVIEW` decision, eight-stage incident response, trust zones and assurance context.

The scenario selector allows the examiner to switch among `normal`, `sensor_anomaly`, `quality_anomaly`, `dosing_event`, `fouling` and `optimization`. The display refreshes automatically and also supports pause/resume and manual frame stepping.

The local server exposes only read-only visualization endpoints. It has no endpoint for PLC, SCADA, dosing or utility control and binds only to the loopback interface.

A useful viva sentence is:

> The browser dashboard does not add a new control layer. It visualizes the same synthetic evidence and advisory decisions produced by the core AquaSentinel modules.

## 10. Industrial terminal dashboard

`live.py` uses Rich Live to refresh one operator-style terminal view instead of continuously scrolling output. The terminal view shows the same major evidence categories as the local browser dashboard.

```bash
aquasentinel live --scenario normal --samples 30
```

For a full-screen terminal incident demonstration:

```bash
aquasentinel live --scenario dosing_event --samples 40 --refresh-rate 4 --fullscreen
```

## 11. One-file Windows experience

`AquaSentinel.bat` is the recommended Windows entry point. It configures UTF-8, validates Python 3.10+, creates the virtual environment, installs the project, runs the doctor, Pytest, Ruff, Bandit and functional smoke checks, verifies the web-dashboard data path and then starts the localhost browser UI.

The browser opens automatically at `127.0.0.1:8765`. The terminal window remains open because it hosts the local server. `Ctrl+C` stops it.

The original guided terminal exam sequence remains available with:

```text
.venv\Scripts\python.exe -m aquasentinel exam-demo
```

## 12. Audit and evidence

`audit.py` writes JSONL evidence for scenario observations and analysis. `reporting.py` produces an exam-oriented JSON report. This demonstrates traceability: the system can explain what data was observed, what analysis was produced and what decision was recommended.

## 13. Compliance framing

`compliance.py` maps project evidence to educational context around NIST SP 800-82, EPA and WHO water-safety principles. It does not claim certification or regulatory compliance.

The project demonstrates ideas such as segmentation, monitored access, passive OT visibility, quality verification, risk-based escalation, audit evidence and public-health-first response.

## 14. DevSecOps

The GitHub Actions pipeline verifies the project before merge. The Linux job installs the package, runs Ruff, Bandit, Pytest, the environment doctor, architecture, scenario, terminal-live, localhost-web, incident, exam-demo and report smoke checks, then builds and inspects the Windows distribution ZIP.

A separate `windows-latest` job runs the actual `AquaSentinel.bat --check-only` launcher. This verifies the real Windows setup path, including UTF-8 handling and the local-dashboard self-check.

## 15. Important files

```text
AquaSentinel.bat            Windows setup / verification / localhost start
aquasentinel/__main__.py    command-line interface
aquasentinel/webui.py       localhost browser dashboard and JSON state API
aquasentinel/telemetry.py   synthetic process and quality data
aquasentinel/analytics.py   transparent rule-based analysis
aquasentinel/ml.py          IsolationForest anomaly detection
aquasentinel/security.py    synthetic OT/security correlation
aquasentinel/optimizer.py   safe resource recommendations
aquasentinel/incidents.py   eight-stage response model
aquasentinel/dashboard.py   terminal snapshot visualization
aquasentinel/live.py        low-lag terminal live view
aquasentinel/doctor.py      exam-machine checks
aquasentinel/audit.py       JSONL evidence
aquasentinel/reporting.py   exam report export
aquasentinel/compliance.py  assurance-framework mapping
aquasentinel/scenarios.py   controlled demonstrations
tests/                      automated verification
.github/workflows/ci.yml    Linux + Windows DevSecOps pipeline
```

## 16. Recommended 3–5 minute project demonstration

1. Double-click `AquaSentinel.bat` and briefly explain that setup/security verification runs first.
2. When the browser opens, explain the localhost/read-only safety banner.
3. Show `normal` and explain the baseline desalination flow and telemetry.
4. Select `quality_anomaly` and explain cross-sensor evidence plus AI prioritization.
5. Select `dosing_event` and explain synthetic OT evidence, correlation, `HOLD-SAFE` and `HUMAN REVIEW`.
6. Select `fouling` and explain membrane health and predictive maintenance.
7. Select `optimization` and explain resource advice and safety guardrails.
8. Point to the incident timeline, trust zones and assurance context.
9. If time permits, switch to `aquasentinel exam-demo` or the terminal live mode to show that the same engine also has a CLI/SOC interface.

## 17. Likely viva questions

### Why not let AI automatically change the process?
Because water infrastructure is safety and public-health critical. AI can recommend or prioritize, but changes need validated engineering constraints, authorization and human oversight.

### Is the localhost page controlling a plant?
No. It is a visualization interface for synthetic evidence. It binds only to `127.0.0.1` and has no plant-control write path.

### Why do you use both rules and ML?
Rules are explainable and deterministic. ML can identify unusual combinations that may not match one fixed threshold. Using both creates layered evidence.

### Why is network segmentation important?
It reduces unnecessary communication paths and limits how a compromise in an enterprise environment could reach OT assets.

### Why cross-check sensors?
A single sensor can drift, fail or be spoofed. Independent measurements and process context help distinguish a sensor problem from a genuine water-quality event.

### What makes this DevSecOps?
Tests, static checks, security scanning, localhost-dashboard verification, package validation and runtime smoke tests are automated in the pull-request workflow.

### Is the project connected to a real desalination plant?
No. It is intentionally synthetic and defensive. That makes it safe and repeatable for an oral examination.

## 18. Final explanation to the examiner

AquaSentinel demonstrates that smart water security is not simply an antivirus system for SCADA. It is a layered approach combining OT architecture, independent water-quality evidence, process-aware cybersecurity, AI-supported anomaly detection, predictive maintenance, safe resource optimization, human oversight, DevSecOps and traceable assurance evidence. The localhost dashboard brings those layers together visually, while the terminal interface keeps the underlying project transparent and easy to inspect.
