# AquaSentinel AI

### Smart Water & Desalination Infrastructure Security Platform

[![CI](https://github.com/HaziqBinAfzal/AquaSentinel/actions/workflows/ci.yml/badge.svg?branch=build%2Ftopic-133-exam-platform)](https://github.com/HaziqBinAfzal/AquaSentinel/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-launcher%20verified-0078D4?logo=windows&logoColor=white)
![Release](https://img.shields.io/badge/release-v1.0.0-0A7EA4)
![Project](https://img.shields.io/badge/project-EduQual%20Level%206-4C6EF5)
![Mode](https://img.shields.io/badge/mode-synthetic%20%7C%20defensive%20%7C%20read--only-2E8B57)

**EduQual Level 6 Diploma in Artificial Intelligence Operations — Oral Examination Project, Topic 133**  
**Student:** Haziq Shahzad  
**Final Release:** v1.0.0

> **Examiner quick start:** On Windows, download or clone the repository, extract it to a normal folder and double-click `AquaSentinel.bat`. It configures UTF-8 terminal output, verifies Python 3.10+, creates an isolated environment, installs the project, runs automated quality/security checks and functional smoke tests, then starts the guided Topic 133 demonstration.

## Verified Terminal Preview

The preview below represents AquaSentinel's deterministic `dosing_event` classroom scenario. It demonstrates water-quality review, simulated OT/SCADA evidence, cyber-physical correlation, the `HOLD-SAFE` advisory state and the final `HUMAN REVIEW` decision.

![AquaSentinel AI verified terminal preview](assets/aquasentinel-terminal.svg)

> This is a documentation rendering of deterministic project output, not a live industrial plant screen. All telemetry, security events and process conditions are synthetic.

---

## Project Overview

AquaSentinel AI is a terminal-first educational platform demonstrating how artificial intelligence, operational technology security, water-quality monitoring, predictive maintenance and resource optimization can be combined around a modern desalination and critical-water environment.

The project was created for Topic 133:

> **Orchestrating Smart Water and Desalination Infrastructure Security Platform with OT Protection, Quality Monitoring, and AI-Driven Resource Optimization for Critical Water Systems.**

Instead of presenting the topic only as theory, AquaSentinel turns the main concepts into an interactive and explainable demonstration. It generates controlled synthetic desalination telemetry, evaluates water-quality conditions, applies a real `scikit-learn` IsolationForest anomaly model, correlates simulated OT/SCADA evidence, estimates membrane-fouling risk, produces guardrailed resource recommendations and presents the result through an industrial-style terminal dashboard.

The central design principle is simple: **AI remains advisory**. Water quality, cybersecurity evidence, engineering constraints, public-health considerations and human authority remain above automated recommendations.

> **Safety boundary:** AquaSentinel is a synthetic, defensive classroom project. It does not connect to, operate, control or modify a real water utility, desalination plant, PLC, SCADA system, dosing controller or public-health infrastructure. Thresholds and response logic are illustrative and are not operational or regulatory instructions.

---

## What AquaSentinel Demonstrates

| Area | Project demonstration |
| --- | --- |
| **Water Treatment / Desalination** | Synthetic raw/sea-water, pretreatment, high-pressure pumping, reverse osmosis, post-treatment and storage context |
| **OT / SCADA Security** | Segmented architecture and passive synthetic Zeek-style, Suricata-style and SCADA-audit evidence |
| **Water Quality** | pH, conductivity, turbidity, residual chlorine and salinity monitoring with cross-sensor reasoning |
| **Artificial Intelligence** | IsolationForest anomaly detection over multiple process features |
| **Cyber-Physical Correlation** | Security evidence compared with independent quality and process evidence before escalation |
| **Predictive Maintenance** | Membrane health, pressure, flow and energy patterns used for synthetic fouling-risk analysis |
| **Resource Optimization** | Advisory energy and production recommendations with quality, security and equipment guardrails |
| **Incident Response** | Human-led eight-stage response workflow from detection through evidence preservation |
| **DevSecOps** | Pytest, Ruff, Bandit, CI, package-integrity checking and real Windows launcher verification |
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
                           |
                 Terminal Dashboard
                           |
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

AquaSentinel is deliberately read-only from the application's perspective. It analyzes synthetic evidence and contains no path for issuing commands to real industrial controllers.

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

The Rich-based live console is designed to feel closer to an operator/SOC view than a normal Python script while remaining lightweight enough for an exam laptop. It shows the desalination process, live synthetic measurements, water-quality status, AI anomaly state, simulated OT evidence, cyber-physical correlation, overall risk, maintenance information, guardrailed optimization advice, recent events and the permanent synthetic/read-only boundary.

```bash
aquasentinel live --scenario dosing_event --samples 40 --refresh-rate 4 --fullscreen
```

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

The launcher automatically switches Command Prompt to UTF-8, enables UTF-8 Python I/O, detects `py -3` or `python`, verifies Python 3.10+, creates `.venv`, installs AquaSentinel and verification dependencies, runs the environment doctor, Pytest, Ruff, Bandit and functional smoke tests, and starts the complete guided Topic 133 demo only if every check passes.

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

```bash
aquasentinel exam-demo
```

The guided sequence covers normal operation, water-quality anomalies, AI anomaly detection, OT/SCADA evidence, cyber-physical correlation, incident response, predictive maintenance, resource optimization, DevSecOps and assurance evidence.

---

## Useful Manual Commands

```bash
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
Guided Topic 133 demonstration
```

The examiner can also inspect `doctor`, `architecture`, `live`, `incident`, `ml-check`, `compliance` and `report` individually.

---

## Project Structure

```text
AquaSentinel/
|
|-- AquaSentinel.bat          One-file Windows setup / verify / start launcher
|-- README.md                 Examiner-facing documentation
|-- CHANGELOG.md              Release history
|-- pyproject.toml            Package metadata and dependencies
|-- requirements.txt          Runtime dependency list
|-- install.bat               Alternative Windows setup
|-- install.sh                Linux/macOS setup
|-- run_exam_demo.bat         Windows guided-demo launcher
|-- run_exam_demo.sh          Linux/macOS guided-demo launcher
|
|-- aquasentinel/             Application modules
|-- tests/                    Automated verification
|-- docs/                     Detailed guides and release documentation
|-- scripts/                  User-package builder
|-- assets/                   Examiner-facing terminal preview
`-- .github/workflows/        Linux + Windows continuous integration
```

---

## DevSecOps and Verification

The Linux CI job performs editable installation, Ruff static checks, Bandit defensive security scanning, Pytest, environment-doctor validation, architecture/scenario/live/incident/exam-demo smoke tests, exam-report generation, the final Windows ZIP build and ZIP-content integrity verification.

A separate `windows-latest` job executes the actual `AquaSentinel.bat --check-only` path end-to-end. The test suite also confirms that the runtime package version matches the package metadata version.

---

## Final Distribution Package

The v1.0.0 build produces:

```text
AquaSentinel-v1.0.0-Windows.zip
```

The distribution contains the application code, tests, documentation, assets, launchers, package metadata and `START_HERE.txt`. CI opens the generated ZIP and verifies required files before uploading it. Generated virtual environments, audit output, reports, caches and development build directories are excluded.

---

## Evidence and Audit Trail

```bash
aquasentinel report
```

The report records controlled scenario telemetry, analytical results, AI state, simulated security evidence and correlation results so the project demonstrates traceability instead of presenting only transient terminal output.

---

## Standards and Public-Health Context

AquaSentinel references **NIST SP 800-82** concepts for OT/industrial control security, segmentation, monitoring and incident evidence; **EPA context** for water-quality observation and public-health-focused reporting concepts; and **WHO water-safety context** for risk-based monitoring, verification and safety-first decision-making.

These mappings are educational. AquaSentinel does **not** claim certification, formal regulatory compliance or operational suitability for a real utility.

---

## Oral Examination Explanation

The main idea behind AquaSentinel is that AI should support an operator, not silently replace engineering or public-health judgement. If one sensor becomes unusual, the platform checks other evidence instead of automatically calling it contamination. If a cyber event appears, it compares the cyber observation with process and quality information before judging possible physical impact. If an optimization recommendation conflicts with quality or security conditions, optimization is held and human review is requested.

That relationship between **OT cybersecurity, water quality, AI, engineering constraints and human decision-making** is the core idea demonstrated by the project.

---

## Final Release Status

**AquaSentinel AI v1.0.0** is the final examiner-facing release. It includes Linux verification, package-integrity checking, dedicated Windows launcher testing and a Windows-compatible UTF-8 terminal path.

PR #1 remains the controlled release branch until explicit approval is given to merge it into `main`.

---

## Final Safety Statement

**AquaSentinel AI is an educational simulation, not an industrial control product.** All plant data, security events, incidents and optimization outputs are synthetic. The project contains no functionality for connecting to or issuing commands to real PLCs, SCADA systems, dosing equipment or water utilities. Classroom thresholds and assurance mappings are illustrative and must not be treated as real-world operating limits, public-health decisions or regulatory determinations.

---

### AquaSentinel AI v1.0.0

**Topic 133 — Smart Water & Desalination Infrastructure Security**  
*OT protection • Water-quality monitoring • AI anomaly detection • Cyber-physical correlation • Predictive maintenance • Guardrailed resource optimization • DevSecOps evidence*
