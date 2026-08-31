# AquaSentinel AI

### Smart Water & Desalination Infrastructure Security Platform

[![CI](https://github.com/HaziqBinAfzal/AquaSentinel/actions/workflows/ci.yml/badge.svg?branch=build%2Ftopic-133-exam-platform)](https://github.com/HaziqBinAfzal/AquaSentinel/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-launcher%20verified-0078D4?logo=windows&logoColor=white)
![Local UI](https://img.shields.io/badge/UI-localhost%20dashboard-14B8A6)
![Release](https://img.shields.io/badge/release-v1.0.0-0A7EA4)
![Project](https://img.shields.io/badge/project-EduQual%20Level%206-4C6EF5)
![Mode](https://img.shields.io/badge/mode-synthetic%20%7C%20defensive%20%7C%20read--only-2E8B57)

**EduQual Level 6 Diploma in Artificial Intelligence Operations — Oral Examination Project, Topic 133**  
**Student:** Haziq Shahzad  
**Final Release:** v1.0.0

> **Examiner quick start:** On Windows, extract the project and double-click `AquaSentinel.bat`. AquaSentinel verifies the environment and project first, then starts a local browser dashboard at **`http://127.0.0.1:8765/`** automatically. The original terminal demonstrations remain available as separate commands.

## Verified Terminal Preview

The preview below represents AquaSentinel's deterministic `dosing_event` classroom scenario. It demonstrates water-quality review, simulated OT/SCADA evidence, cyber-physical correlation, the `HOLD-SAFE` advisory state and the final `HUMAN REVIEW` decision.

![AquaSentinel AI verified terminal preview](assets/aquasentinel-terminal.svg)

> This is a documentation rendering of deterministic project output, not a live industrial plant screen. All telemetry, security events and process conditions are synthetic.

---

## Project Overview

AquaSentinel AI is a safe educational platform demonstrating how artificial intelligence, operational technology security, water-quality monitoring, predictive maintenance and resource optimization can be combined around a modern desalination and critical-water environment.

The project was created for Topic 133:

> **Orchestrating Smart Water and Desalination Infrastructure Security Platform with OT Protection, Quality Monitoring, and AI-Driven Resource Optimization for Critical Water Systems.**

AquaSentinel provides **two presentation interfaces** over the same synthetic analytics engine:

1. a professional localhost browser dashboard for visual demonstration; and
2. an industrial-style terminal/SOC interface for transparent command-line inspection.

The platform generates controlled synthetic desalination telemetry, evaluates water-quality conditions, applies a real `scikit-learn` IsolationForest anomaly model, correlates simulated OT/SCADA evidence, estimates membrane-fouling risk, produces guardrailed resource recommendations and presents the same evidence through both interfaces.

The central design principle is simple: **AI remains advisory**. Water quality, cybersecurity evidence, engineering constraints, public-health considerations and human authority remain above automated recommendations.

> **Safety boundary:** AquaSentinel is a synthetic, defensive classroom project. It does not connect to, operate, control or modify a real water utility, desalination plant, PLC, SCADA system, dosing controller or public-health infrastructure. Thresholds and response logic are illustrative and are not operational or regulatory instructions.

---

## Localhost Operations Dashboard

AquaSentinel includes a full browser UI served entirely from the local machine.

```text
http://127.0.0.1:8765/
```

It uses Python's local HTTP server and the existing AquaSentinel analytics modules. No cloud service, external API, database or real industrial connection is required.

The dashboard displays:

- the complete synthetic desalination process from sea/raw water through storage;
- pH, conductivity, turbidity, residual chlorine and salinity;
- feed pressure, RO pressure, flow, tank level, energy and membrane health;
- rule-based water-quality priority;
- IsolationForest AI anomaly state and ML priority;
- simulated SCADA/Zeek/Suricata-style evidence;
- cyber-physical correlation score and evidence sources;
- predictive-maintenance / membrane-fouling risk;
- guardrailed energy and production optimization mode;
- overall risk and `MONITOR` / `HUMAN REVIEW` decision;
- the complete eight-stage incident-response timeline;
- trust-zone architecture and assurance context;
- selectable `normal`, `sensor_anomaly`, `quality_anomaly`, `dosing_event`, `fouling` and `optimization` scenarios;
- live automatic refresh, pause/resume and frame stepping; and
- a permanent synthetic / defensive / read-only safety banner.

The UI is deliberately bound to **`127.0.0.1` only**. It is a local visualization layer, not a remotely exposed control panel.

### Start the browser UI manually

```bash
aquasentinel web
```

The default browser opens automatically. To choose another local port:

```bash
aquasentinel web --port 9000
```

For automated verification without starting a server:

```bash
aquasentinel web --check-only
```

---

## What AquaSentinel Demonstrates

| Area | Project demonstration |
| --- | --- |
| **Water Treatment / Desalination** | Synthetic raw/sea-water, pretreatment, high-pressure pumping, reverse osmosis, post-treatment and storage context |
| **Local Browser UI** | Real-time localhost operations dashboard showing process, quality, AI, OT evidence, risk, optimization and incident response |
| **OT / SCADA Security** | Segmented architecture and passive synthetic Zeek-style, Suricata-style and SCADA-audit evidence |
| **Water Quality** | pH, conductivity, turbidity, residual chlorine and salinity monitoring with cross-sensor reasoning |
| **Artificial Intelligence** | IsolationForest anomaly detection over multiple process features |
| **Cyber-Physical Correlation** | Security evidence compared with independent quality and process evidence before escalation |
| **Predictive Maintenance** | Membrane health, pressure, flow and energy patterns used for synthetic fouling-risk analysis |
| **Resource Optimization** | Advisory energy and production recommendations with quality, security and equipment guardrails |
| **Incident Response** | Human-led eight-stage response workflow from detection through evidence preservation |
| **DevSecOps** | Pytest, Ruff, Bandit, CI, package-integrity checking, web-dashboard tests and real Windows launcher verification |
| **Audit / Reporting** | JSONL audit evidence and structured JSON exam reports |
| **Assurance Context** | Educational mapping to NIST SP 800-82 concepts and EPA/WHO water-safety context |

---

## System Architecture

```text
                    Enterprise / SOC
                           |
                    Industrial DMZ
                           |
                      OT / SCADA
                           |
             Passive synthetic security evidence
                           |
                   Safety & Quality
                           |
              Independent validation evidence
                           |
              Synthetic treatment process
                           |
                        Telemetry
                           |
          +----------------+----------------+
          |                |                |
     Quality Rules      AI / ML       OT Correlation
          |                |                |
          +----------------+----------------+
                           |
              Maintenance / Optimization
                           |
                      Human Review
                      /         \
            Terminal Console   Localhost UI
                      \         /
                       Audit / Report
```

Synthetic process path:

```text
Raw / Sea Water
      -> Pretreatment
      -> High-Pressure Pump
      -> Reverse Osmosis
      -> Post-Treatment / Disinfection
      -> Storage
      -> Distribution Context
```

AquaSentinel is deliberately read-only from the application's perspective. Both the terminal and browser interfaces analyze synthetic evidence and contain no path for issuing commands to real industrial controllers.

---

## How the Platform Works

### Synthetic telemetry

`telemetry.py` generates deterministic classroom data for pH, conductivity, turbidity, residual chlorine, salinity, feed pressure, RO pressure, flow rate, temperature, tank level, pump state, energy use, membrane health and synthetic cyber events.

### Water-quality analysis

`analytics.py` performs transparent rule-based checks. One abnormal sensor is treated as evidence, not automatic proof of contamination. Related measurements can be cross-checked before priority is raised.

### AI anomaly detection

`ml.py` trains a real IsolationForest model against a synthetic normal baseline. It evaluates multiple process variables together and provides an expected/anomalous state plus an ML priority score. The result is advisory and appears beside transparent rules instead of replacing them.

### OT / SCADA security evidence

`security.py` creates controlled Zeek-style, Suricata-style and SCADA-audit observations for classroom correlation. AquaSentinel does not perform attacks or connect to real OT networks.

### Cyber-physical correlation

A network alert alone does not prove physical impact. AquaSentinel compares cyber evidence with independent process and water-quality evidence before raising a cyber-physical incident priority.

### Predictive maintenance

The `fouling` scenario gradually changes membrane health, pressure, flow and energy demand to demonstrate predictive-maintenance reasoning.

### Guardrailed optimization

`optimizer.py` creates advisory energy and production recommendations. If water quality or security evidence becomes concerning, the platform moves to `HOLD-SAFE` and requests human review rather than continuing to optimize for efficiency.

### Human-led incident response

```text
DETECT -> VALIDATE -> CORRELATE -> ASSESS -> CONTAIN -> VERIFY -> RECOVER -> EVIDENCE
```

The workflow explains safe decision-making without providing real industrial-control instructions.

---

## Industrial Terminal Dashboard

The Rich-based live console remains available for a terminal-first demonstration. It shows the same underlying synthetic process, water-quality, ML, OT security, risk and optimization evidence.

```bash
aquasentinel live --scenario dosing_event --samples 40 --refresh-rate 4 --fullscreen
```

The browser UI and terminal UI are complementary: the browser is better for a visual examiner walkthrough, while the terminal makes the project logic and CLI workflow easy to inspect.

---

## Controlled Demonstration Scenarios

| Scenario | Demonstrates |
| --- | --- |
| `normal` | Expected synthetic desalination operation |
| `sensor_anomaly` | An unusual sensor without automatically declaring contamination |
| `quality_anomaly` | Multiple related quality deviations and cross-sensor validation |
| `dosing_event` | Synthetic OT/SCADA evidence and cyber-physical correlation |
| `fouling` | Membrane degradation and predictive-maintenance reasoning |
| `optimization` | Resource/energy recommendations within safety guardrails |

A deterministic seed allows the same scenario to be reproduced during an oral examination.

---

# Running the Project

## Windows — recommended one-file method

Extract the final package or repository to a normal folder and double-click:

```text
AquaSentinel.bat
```

The launcher automatically:

1. switches Command Prompt to UTF-8 and enables UTF-8 Python I/O;
2. detects `py -3` or `python` and verifies Python 3.10+;
3. creates `.venv` and installs AquaSentinel plus verification tools;
4. runs the environment doctor, Pytest, Ruff and Bandit;
5. smoke-tests architecture, scenarios, incidents, reporting and the local web-dashboard data path;
6. prints `ALL CHECKS PASSED` only when verification succeeds; and
7. starts the localhost dashboard at `http://127.0.0.1:8765/` and opens the browser automatically.

Keep the launcher terminal open while using the local dashboard. Press `Ctrl+C` in that terminal to stop the server.

### Windows compatibility

The launcher explicitly configures UTF-8 before Rich renders Unicode dashboard elements. This prevents legacy Windows code-page failures such as `UnicodeEncodeError` when architecture arrows or dashboard symbols are displayed.

The exact Windows entry point is tested in GitHub Actions on `windows-latest` using:

```bat
AquaSentinel.bat --check-only
```

### Linux / macOS

```bash
chmod +x install.sh run_exam_demo.sh
./install.sh
aquasentinel web
```

### Manual installation

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
pip install -e '.[dev]'
aquasentinel doctor
aquasentinel web
```

---

## One-Command Guided Terminal Oral Exam

```bash
aquasentinel exam-demo
```

The guided terminal sequence covers normal operation, water-quality anomalies, AI anomaly detection, OT/SCADA evidence, cyber-physical correlation, incident response, predictive maintenance, resource optimization, DevSecOps and assurance evidence.

---

## Useful Manual Commands

```bash
aquasentinel web
aquasentinel web --port 9000
aquasentinel doctor
aquasentinel architecture
aquasentinel exam-demo
aquasentinel live --scenario normal --samples 30
aquasentinel live --scenario dosing_event --samples 40 --refresh-rate 4 --fullscreen
aquasentinel run --scenario quality_anomaly --samples 10
aquasentinel incident --scenario dosing_event --step 8
aquasentinel ml-check
aquasentinel compliance
aquasentinel report
```

---

## Recommended Examiner Walkthrough

```text
Download / clone repository
          |
Extract project
          |
Double-click AquaSentinel.bat
          |
Automated setup + verification
          |
ALL CHECKS PASSED
          |
Browser opens on 127.0.0.1:8765
          |
Select scenarios and explain live evidence
          |
Optional terminal exam-demo / SOC dashboard
```

For a visual presentation, start with the browser UI and switch between `normal`, `quality_anomaly`, `dosing_event`, `fouling` and `optimization`. The examiner can then inspect `doctor`, `architecture`, `live`, `incident`, `ml-check`, `compliance` and `report` individually if needed.

---

## Project Structure

```text
AquaSentinel/
|
|-- AquaSentinel.bat          One-file Windows setup / verify / localhost launcher
|-- README.md                 Examiner-facing documentation
|-- CHANGELOG.md              Release history
|-- pyproject.toml            Package metadata and dependencies
|-- requirements.txt          Runtime dependency list
|-- install.bat               Alternative Windows setup
|-- install.sh                Linux/macOS setup
|-- run_exam_demo.bat         Windows guided terminal demo
|-- run_exam_demo.sh          Linux/macOS guided terminal demo
|
|-- aquasentinel/
|   |-- __main__.py           CLI routing
|   |-- webui.py              Localhost browser dashboard + JSON state endpoint
|   |-- live.py               Industrial terminal dashboard
|   |-- telemetry.py          Synthetic process and quality data
|   |-- analytics.py          Transparent rule-based analysis
|   |-- ml.py                 IsolationForest anomaly detection
|   |-- security.py           Synthetic OT/security correlation
|   |-- optimizer.py          Guardrailed resource recommendations
|   |-- incidents.py          Eight-stage response model
|   |-- presenter.py          Examiner incident brief
|   |-- doctor.py             Environment/safety validation
|   |-- reporting.py          Exam-report generation
|   |-- audit.py              JSONL evidence
|   `-- scenarios.py          Controlled demonstrations
|
|-- tests/                    Automated verification including web UI state tests
|-- docs/                     Detailed guides and release documentation
|-- scripts/                  User-package builder
|-- assets/                   Examiner-facing terminal preview
`-- .github/workflows/        Linux + Windows continuous integration
```

---

## DevSecOps and Verification

The Linux CI job performs editable installation, Ruff static checks, Bandit defensive security scanning, Pytest, environment-doctor validation, architecture/scenario/live/**web-dashboard**/incident/exam-demo smoke tests, exam-report generation, the final Windows ZIP build and ZIP-content integrity verification.

A separate `windows-latest` job executes the actual `AquaSentinel.bat --check-only` path end-to-end. That Windows launcher path also validates the web-dashboard state builder before it is allowed to report success.

The generated ZIP is checked to ensure that `aquasentinel/webui.py` and its tests are actually included in the examiner package.

---

## Final Distribution Package

The v1.0.0 build produces:

```text
AquaSentinel-v1.0.0-Windows.zip
```

The distribution contains the browser UI, terminal UI, application code, tests, documentation, assets, launchers, package metadata and `START_HERE.txt`. Generated virtual environments, audit output, reports, caches and development build directories are excluded.

---

## Evidence and Audit Trail

```bash
aquasentinel report
```

The report records controlled scenario telemetry, analytical results, AI state, simulated security evidence and correlation results so the project demonstrates traceability instead of presenting only transient dashboard output.

---

## Standards and Public-Health Context

AquaSentinel references **NIST SP 800-82** concepts for OT/industrial control security, segmentation, monitoring and incident evidence; **EPA context** for water-quality observation and public-health-focused reporting concepts; and **WHO water-safety context** for risk-based monitoring, verification and safety-first decision-making.

These mappings are educational. AquaSentinel does **not** claim certification, formal regulatory compliance or operational suitability for a real utility.

---

## Oral Examination Explanation

The main idea behind AquaSentinel is that AI should support an operator, not silently replace engineering or public-health judgement. The local dashboard makes this relationship visible: water-quality rules, ML, OT evidence, correlation, maintenance and optimization are shown side by side before the final `MONITOR` or `HUMAN REVIEW` decision.

If one sensor becomes unusual, the platform checks other evidence instead of automatically calling it contamination. If a cyber event appears, it compares the cyber observation with process and quality information before judging possible physical impact. If an optimization recommendation conflicts with quality or security conditions, optimization is held and human review is requested.

That relationship between **OT cybersecurity, water quality, AI, engineering constraints and human decision-making** is the core idea demonstrated by the project.

---

## Final Release Status

**AquaSentinel AI v1.0.0** is the examiner-facing release with both terminal and localhost browser interfaces. The release includes Linux verification, package-integrity checking, dedicated Windows launcher testing, Windows-compatible UTF-8 handling and automated local-dashboard verification.

PR #1 remains the controlled release branch until explicit approval is given to merge it into `main`.

---

## Final Safety Statement

**AquaSentinel AI is an educational simulation, not an industrial control product.** All plant data, security events, incidents and optimization outputs are synthetic. The browser server binds only to localhost and the project contains no functionality for connecting to or issuing commands to real PLCs, SCADA systems, dosing equipment or water utilities. Classroom thresholds and assurance mappings are illustrative and must not be treated as real-world operating limits, public-health decisions or regulatory determinations.

---

### AquaSentinel AI v1.0.0

**Topic 133 — Smart Water & Desalination Infrastructure Security**  
*Localhost operations dashboard • OT protection • Water-quality monitoring • AI anomaly detection • Cyber-physical correlation • Predictive maintenance • Guardrailed resource optimization • DevSecOps evidence*
