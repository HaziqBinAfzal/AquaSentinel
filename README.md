# AquaSentinel AI

### Smart Water & Desalination Infrastructure Security Platform

**EduQual Level 6 Diploma in Artificial Intelligence Operations — Oral Examination Project, Topic 133**  
**Student:** Haziq Shahzad  
**Release Candidate:** v1.0.0-rc1

---

## Project Overview

AquaSentinel AI is a terminal-first educational platform created to demonstrate how artificial intelligence, operational technology security, water-quality monitoring and resource optimization can be brought together around a modern desalination and critical-water environment.

The project was designed around Topic 133:

> **Orchestrating Smart Water and Desalination Infrastructure Security Platform with OT Protection, Quality Monitoring, and AI-Driven Resource Optimization for Critical Water Systems.**

Rather than presenting the topic only as theory, AquaSentinel turns the main ideas into an interactive, explainable demonstration. It generates controlled synthetic desalination telemetry, evaluates water-quality conditions, applies an IsolationForest anomaly model, correlates simulated OT/SCADA security evidence, estimates membrane-fouling risk, produces guarded optimization recommendations and presents the result through an industrial-style terminal dashboard.

The most important design principle is that **AI remains advisory**. Water quality, engineering constraints, cybersecurity evidence, public-health considerations and human authority remain above automated recommendations.

> **Safety boundary:** AquaSentinel is a synthetic, defensive classroom project. It does not connect to, operate, control or modify a real water utility, desalination plant, PLC, SCADA system, dosing controller or public-health infrastructure. Thresholds and response logic are illustrative and are not operational or regulatory instructions.

---

## Why This Project Was Built

Modern water and desalination facilities are cyber-physical systems. Their security cannot be understood only as an IT problem because network activity, industrial equipment, water quality, energy consumption and public-health consequences are connected.

AquaSentinel was therefore built around a simple question:

**How can we combine cyber evidence, process telemetry, water-quality evidence and AI-assisted analysis without allowing AI to override safety?**

The project demonstrates one answer: collect independent evidence, analyze it in separate layers, correlate the results, prioritize what deserves attention, and leave the final decision with a human operator.

This gives the oral presentation a working project that connects the technical areas of the topic instead of showing them as unrelated concepts.

---

## What AquaSentinel Demonstrates

| Area | Project demonstration |
| --- | --- |
| **Water Treatment / Desalination** | Synthetic raw/sea-water, pretreatment, high-pressure pumping, reverse-osmosis, post-treatment and storage process context |
| **OT / SCADA Security** | Segmented architecture concepts and passive synthetic Zeek-style, Suricata-style and SCADA-audit evidence |
| **Water Quality** | pH, conductivity, turbidity, residual chlorine and salinity monitoring with cross-sensor validation |
| **Artificial Intelligence** | IsolationForest-based multivariable anomaly detection trained on a reproducible synthetic normal baseline |
| **Cyber-Physical Correlation** | Security evidence is correlated with independent process and quality evidence before escalation |
| **Predictive Maintenance** | Membrane-health, pressure, flow and energy patterns contribute to synthetic fouling-risk analysis |
| **Resource Optimization** | Advisory energy and production recommendations with quality, cybersecurity and equipment guardrails |
| **Incident Response** | An eight-stage human-led response model from detection through evidence preservation |
| **DevSecOps** | Automated tests, linting, defensive security scanning, repeatable builds and CI validation |
| **Audit / Reporting** | JSONL audit evidence and a generated exam evidence report |
| **Assurance Context** | Educational mapping to NIST SP 800-82 concepts and EPA/WHO water-safety context |

---

## System Architecture

AquaSentinel uses a deliberately segmented conceptual architecture so that enterprise activity, industrial control, safety/quality evidence and analytics are not treated as one unrestricted network.

```text
                         AQUASENTINEL AI

                    Enterprise / SOC Layer
                             |
                    +-------------------+
                    |   Industrial DMZ  |
                    +-------------------+
                             |
                    +-------------------+
                    |     OT / SCADA    |------ Passive synthetic
                    +-------------------+       security evidence
                             |
                    +-------------------+
                    | Safety & Quality  |------ Independent quality
                    +-------------------+       verification
                             |
               Synthetic Desalination Process
                             |
                          Telemetry
                             |
             +---------------+---------------+
             |               |               |
        Quality Rules    AI / ML       OT Correlation
             |               |               |
             +---------------+---------------+
                             |
                 Maintenance / Optimization
                             |
                       Human Review
                             |
                Industrial Terminal Console
                             |
                    Audit / Exam Report
```

The simulated physical process follows:

```text
Raw / Sea Water
      |
Pretreatment
      |
High-Pressure Pump
      |
Reverse Osmosis
      |
Post-Treatment / Disinfection
      |
Storage
      |
Distribution Context
```

The architecture is intentionally **read-only from the application's perspective**. AquaSentinel analyzes synthetic evidence; it contains no path for writing commands to industrial controllers.

---

## How the Platform Works

### 1. Synthetic plant telemetry

`telemetry.py` generates deterministic classroom data representing the desalination process. Measurements include pH, conductivity, turbidity, residual chlorine, salinity, feed pressure, RO pressure, flow rate, temperature, tank level, pump state, energy consumption and membrane health.

Using synthetic data makes demonstrations repeatable and prevents the project from requiring access to real critical infrastructure.

### 2. Transparent water-quality analysis

`analytics.py` applies understandable classroom checks to the telemetry. The purpose is not to claim that a single measurement proves contamination. Instead, AquaSentinel demonstrates **cross-sensor reasoning**.

For example, one unusual sensor can indicate a sensor or process issue. Several related quality measurements moving together provide stronger evidence and increase the priority for human investigation.

### 3. AI anomaly detection

`ml.py` trains a real `scikit-learn` IsolationForest model against synthetic normal operating data. The model evaluates multiple process features together and returns an expected/anomalous state and priority score.

The model does not control the plant. Its purpose is to help answer:

> *Does this combination of measurements look unusual compared with the learned synthetic baseline?*

The rules remain visible alongside the ML result so the operator is not asked to trust an unexplained AI decision.

### 4. OT / SCADA security evidence

`security.py` produces controlled, simulated evidence inspired by the types of observations that network and industrial monitoring tools can provide. AquaSentinel uses Zeek-style, Suricata-style and SCADA-audit evidence without attempting to attack, control or connect to a real industrial system.

### 5. Cyber-physical correlation

A cyber alert by itself does not automatically mean water has been affected. AquaSentinel therefore correlates the synthetic security evidence with independent quality/process evidence.

This is an important part of the project: **network evidence tells us something unusual may have happened; process and quality evidence help us understand whether there may also be a physical consequence.**

### 6. Predictive maintenance

The fouling scenario gradually changes membrane health, pressure, flow and energy demand. AquaSentinel uses these relationships to demonstrate how analytics can support predictive-maintenance prioritization rather than waiting only for equipment failure.

### 7. Guardrailed resource optimization

`optimizer.py` produces advisory recommendations for energy and production behavior. Efficiency is never the highest priority. If quality or security evidence is concerning, the optimizer moves to a `HOLD-SAFE` recommendation and requests human review instead of continuing to optimize for energy savings.

### 8. Human-led incident response

The incident demonstration follows eight safe stages:

```text
DETECT
  -> VALIDATE
  -> CORRELATE
  -> ASSESS
  -> CONTAIN
  -> VERIFY
  -> RECOVER
  -> PRESERVE EVIDENCE
```

This demonstrates response reasoning without providing commands for operating real industrial equipment.

---

## Industrial Terminal Dashboard

AquaSentinel is intentionally terminal-first. The live console is designed to look and behave more like an operations/SOC view than a normal Python script.

The dashboard presents:

- desalination process stages;
- live synthetic pressure, flow, tank and membrane conditions;
- water-quality measurements and validation flags;
- AI anomaly state and priority;
- OT/SCADA security evidence;
- cyber-physical correlation;
- overall risk level;
- predictive-maintenance information;
- guarded optimization recommendations;
- recent events and audit state;
- a permanent synthetic/read-only safety boundary.

Example:

```bash
aquasentinel live --scenario dosing_event --samples 40 --refresh-rate 4 --fullscreen
```

The live mode is optimized to update one terminal layout rather than repeatedly printing large dashboards, keeping the demonstration responsive and readable.

---

## Controlled Demonstration Scenarios

AquaSentinel includes six reproducible scenarios.

| Scenario | Purpose |
| --- | --- |
| `normal` | Establishes the expected synthetic operating baseline |
| `sensor_anomaly` | Demonstrates how an unusual measurement is prioritized by rules/AI without being treated automatically as contamination |
| `quality_anomaly` | Produces related water-quality deviations for cross-sensor validation |
| `dosing_event` | Demonstrates synthetic OT/SCADA evidence and cyber-physical correlation |
| `fouling` | Demonstrates membrane degradation, efficiency loss and predictive-maintenance reasoning |
| `optimization` | Demonstrates energy/resource advice inside quality and safety guardrails |

A deterministic seed is used so the same scenario can be reproduced during an examination.

---

# Running the Project

## Recommended Windows method — one file

The easiest way to review the complete project is:

```text
AquaSentinel.bat
```

On Windows, double-click **`AquaSentinel.bat`** from the repository folder.

The launcher automatically:

1. checks that Python is available;
2. creates an isolated virtual environment when needed;
3. installs AquaSentinel and its verification dependencies;
4. runs the environment and safety doctor;
5. executes the automated tests;
6. runs Ruff code-quality checks;
7. runs Bandit defensive security analysis;
8. smoke-tests the architecture, scenarios, incident workflow and report generation;
9. stops clearly if a verification stage fails; and
10. if everything passes, starts the complete guided Topic 133 demonstration.

This means an examiner does not need to memorize a list of setup commands to inspect the project.

### Linux / macOS

```bash
chmod +x install.sh run_exam_demo.sh
./install.sh
./run_exam_demo.sh
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
```

---

## One-Command Guided Oral Exam

After installation, the complete guided demonstration can be started with:

```bash
aquasentinel exam-demo
```

The sequence automatically walks through:

```text
Normal desalination operation
        |
Water-quality anomaly
        |
AI anomaly detection
        |
OT / SCADA security evidence
        |
Cyber-physical correlation
        |
Human-led incident response
        |
Predictive maintenance
        |
Resource optimization
        |
DevSecOps / assurance evidence
```

Each section explains what is being demonstrated before presenting the project output, making the mode useful both for an oral examination and for reviewing how the modules connect.

---

## Useful Manual Commands

```bash
# Environment and safety checks
aquasentinel doctor

# Architecture view
aquasentinel architecture

# Guided complete demonstration
aquasentinel exam-demo

# Industrial live console
aquasentinel live --scenario normal --samples 30

# App-like full-screen incident demonstration
aquasentinel live --scenario dosing_event --samples 40 --refresh-rate 4 --fullscreen

# Water-quality scenario
aquasentinel run --scenario quality_anomaly --samples 10

# Examiner-friendly incident reasoning
aquasentinel incident --scenario dosing_event --step 8

# Compare ML behavior across scenarios
aquasentinel ml-check

# Assurance/compliance context
aquasentinel compliance

# Generate JSON evidence report
aquasentinel report
```

---

## Example Examiner Walkthrough

A short way to review the project manually is:

```text
1. AquaSentinel.bat
       or
   aquasentinel doctor

2. aquasentinel architecture

3. aquasentinel live --scenario normal --samples 10

4. aquasentinel live --scenario quality_anomaly --samples 12

5. aquasentinel live --scenario dosing_event --samples 12

6. aquasentinel incident --scenario dosing_event --step 8

7. aquasentinel live --scenario fouling --samples 15

8. aquasentinel live --scenario optimization --samples 12

9. aquasentinel compliance

10. aquasentinel report
```

Or simply run `aquasentinel exam-demo` to let AquaSentinel guide the sequence automatically.

---

## Project Structure

```text
AquaSentinel/
|
|-- AquaSentinel.bat          Main Windows setup / verification / start file
|-- README.md                 Examiner-facing project documentation
|-- START_HERE.txt            Short distribution instructions
|-- CHANGELOG.md              Release history
|-- pyproject.toml            Python package metadata and dependencies
|-- requirements.txt          Runtime dependency list
|-- install.bat               Windows installation alternative
|-- install.sh                Linux/macOS installation alternative
|-- run_exam_demo.bat         Windows demo-only launcher
|-- run_exam_demo.sh          Linux/macOS demo-only launcher
|
|-- aquasentinel/
|   |-- __main__.py           CLI and command routing
|   |-- exam_demo.py          Guided oral-exam presentation
|   |-- telemetry.py          Synthetic desalination telemetry
|   |-- analytics.py          Quality/fouling/cyber analysis
|   |-- ml.py                 IsolationForest anomaly model
|   |-- security.py           Synthetic OT security evidence + correlation
|   |-- optimizer.py          Guardrailed optimization advice
|   |-- incidents.py          Safe incident-response stages
|   |-- presenter.py          Examiner incident brief
|   |-- dashboard.py          Snapshot terminal dashboard
|   |-- live.py               Industrial low-lag live console
|   |-- doctor.py             Environment/safety validation
|   |-- compliance.py         Assurance-context mapping
|   |-- reporting.py          Exam evidence report generation
|   |-- audit.py              JSONL audit trail
|   `-- scenarios.py          Controlled demonstration scenarios
|
|-- tests/                    Automated verification
|-- docs/                     Detailed project/release documentation
|-- tools/                    Distribution build tooling
`-- .github/workflows/        Continuous-integration pipeline
```

The modules are deliberately separated so telemetry generation, AI, security correlation, optimization, reporting and presentation logic can be understood and tested independently.

---

## DevSecOps and Verification

AquaSentinel is not presented as a single untested demonstration script. The repository includes an automated CI pipeline that verifies the project after changes.

The pipeline performs:

```text
Install project
     |
Ruff static checks
     |
Bandit defensive security scan
     |
Pytest automated tests
     |
Environment doctor
     |
Architecture smoke test
     |
Scenario smoke test
     |
Live dashboard smoke test
     |
Incident-response smoke test
     |
Full guided exam-demo smoke test
     |
Exam report generation
     |
Build distributable Windows ZIP
```

The test suite also verifies that the Python package and project metadata report the same version.

This is included to demonstrate the DevSecOps side of Topic 133: changes should be testable, repeatable and reviewable rather than manually trusted.

---

## Evidence and Audit Trail

AquaSentinel can preserve synthetic analysis evidence as JSONL audit records and can generate a structured exam report.

```bash
aquasentinel report
```

The report evaluates the controlled scenarios and records telemetry, analytical results, AI state, simulated security evidence and correlation results. This provides a traceable artifact showing how the platform reached its conclusions during the classroom demonstration.

---

## Standards and Public-Health Context

The project references three areas of assurance context:

- **NIST SP 800-82** — industrial control/OT security concepts such as segmentation, monitoring, controlled access, incident response and audit evidence;
- **EPA context** — traceable water-quality observations, contamination-event escalation and public-health-focused reporting concepts; and
- **WHO water-safety context** — risk-based monitoring, verification and the principle that quality/safety guardrails should remain above efficiency optimization.

These mappings are included for educational discussion. AquaSentinel does **not** claim regulatory certification, regulatory compliance, or operational suitability for a real water utility.

---

## Key Engineering Decisions

### Why use both rules and machine learning?

Rules are transparent and easy to explain. ML is useful for identifying unusual combinations across many measurements. Using both allows the project to demonstrate AI while retaining understandable evidence for the operator.

### Why correlate cyber and quality evidence?

A network alert alone does not prove physical impact. Correlation helps distinguish a security observation from a potentially cyber-physical event by looking for supporting process or quality evidence.

### Why is optimization advisory?

Saving energy is useful only while quality, safety and equipment constraints remain acceptable. AquaSentinel therefore gives quality/security evidence the ability to override optimization recommendations.

### Why use synthetic telemetry?

It provides safe, reproducible scenarios and makes it possible to demonstrate critical-infrastructure concepts without requiring or risking access to a real plant.

### Why a terminal interface?

The terminal keeps the project lightweight and makes the data-processing pipeline visible. The industrial live layout provides an operator-style view without introducing a separate web application or unnecessary infrastructure.

---

## What I Would Explain During the Oral Examination

The central idea of AquaSentinel is not that AI should run a water plant by itself. The project demonstrates the opposite: AI can help an operator identify patterns, prioritize anomalies and understand a complex situation, but important decisions need independent evidence and human authority.

If one sensor becomes unusual, I do not automatically call it contamination. I compare other measurements. If a cyber alert appears, I do not automatically assume the water has changed. I correlate that alert with process and quality evidence. If an optimization algorithm suggests saving energy while quality evidence is concerning, the quality guardrail wins and the system recommends a safe hold for human review.

That relationship between **OT cybersecurity, water quality, AI, engineering constraints and human decision-making** is the main idea the project is intended to demonstrate.

---

## Release Candidate

Current project version:

```text
AquaSentinel AI v1.0.0-rc1
```

The repository includes a distribution builder that produces:

```text
AquaSentinel-v1.0.0rc1-Windows.zip
```

The package is intended to provide a clean copy of the project with `AquaSentinel.bat` as the main Windows entry point.

See `CHANGELOG.md` and `docs/RELEASE_CANDIDATE.md` for release details.

---

## Final Safety Statement

**AquaSentinel AI is an educational simulation, not an industrial control product.**

All plant data, network evidence, incidents and optimization outputs are synthetic. The software has no functionality for connecting to or issuing commands to real PLCs, SCADA systems, dosing equipment or water utilities. Classroom thresholds and regulatory mappings are illustrative and must not be treated as real-world operating limits, safety decisions or regulatory determinations.

---

### AquaSentinel AI

**Topic 133 — Smart Water & Desalination Infrastructure Security**  
*OT protection • Water-quality monitoring • AI anomaly detection • Cyber-physical correlation • Predictive maintenance • Guardrailed resource optimization • DevSecOps evidence*
