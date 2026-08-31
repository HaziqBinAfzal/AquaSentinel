# AquaSentinel AI

### Local Water / OT Log and Data Analysis Workstation

[![CI](https://github.com/HaziqBinAfzal/AquaSentinel/actions/workflows/ci.yml/badge.svg?branch=build%2Ftopic-133-exam-platform)](https://github.com/HaziqBinAfzal/AquaSentinel/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-launcher%20verified-556B7D?logo=windows&logoColor=white)
![Interface](https://img.shields.io/badge/interfaces-browser%20%2B%20terminal-4F6B7A)
![Release](https://img.shields.io/badge/release-v1.0.0-516B57)
![Mode](https://img.shields.io/badge/mode-local%20%7C%20defensive%20%7C%20read--only-66737F)

**EduQual Level 6 Diploma in Artificial Intelligence Operations — Topic 133**  
**Student:** Haziq Shahzad  
**Version:** 1.0.0

AquaSentinel is a local analysis tool for water/process telemetry and defensive OT/security logs. It does not start with a prepared incident or preloaded plant dataset. The user provides a file, chooses a browser or terminal interface, and AquaSentinel analyzes that file locally.

> **Safety boundary:** AquaSentinel has no control path to PLCs, SCADA systems, dosing equipment or water utilities. It reads user-supplied files and produces analysis only. Water-quality bands used by the project are illustrative classroom review bands, not regulatory or operating limits.

---

## Topic 133

**Orchestrating Smart Water and Desalination Infrastructure Security Platform with OT Protection, Quality Monitoring, and AI-Driven Resource Optimization for Critical Water Systems.**

The project demonstrates the monitoring and analysis side of this topic: ingesting operational evidence, identifying useful water/process fields, reviewing log severity and OT/security indicators, applying local anomaly detection when the data supports it, and presenting the result for human review.

---

## Start on Windows

Extract the package and double-click:

```text
AquaSentinel.bat
```

The launcher checks Python, creates an isolated environment, installs dependencies, runs the test/security checks and then gives two choices:

```text
[1] Browser interface
[2] Terminal interface
[Q] Quit
```

### Option 1 — Browser interface

AquaSentinel starts a local server on:

```text
http://127.0.0.1:8765/
```

The page starts with **No dataset loaded**. Select a `.log`, `.txt`, `.csv`, `.json` or `.jsonl` file and click **Analyze file**.

The browser view is intentionally restrained and workstation-like rather than a decorative control-room mock-up. It uses a neutral engineering palette and focuses on the actual file, fields and findings.

### Option 2 — Terminal interface

Paste the path to a supported file when prompted. AquaSentinel prints the analysis directly in the terminal.

You can also run it manually:

```bash
aquasentinel analyze "C:\path\to\plant.log"
```

---

## Supported input

| Format | Typical use |
| --- | --- |
| `.log` | application, OT monitoring or system logs |
| `.txt` | plain-text event records |
| `.csv` | telemetry or exported process data |
| `.json` | structured events or telemetry |
| `.jsonl` | line-delimited structured logs |

The normal file-size limit is **8 MB** and the analysis engine caps processing at 10,000 records for a predictable local workstation experience.

For CSV/JSON/JSONL data, AquaSentinel recognizes common field names such as `ph`, `conductivity`, `turbidity`, `residual_chlorine`, `salinity`, `feed_pressure`, `ro_pressure`, `flow_rate`, `temperature`, `tank_level`, `energy_kwh` and `membrane_health` when they are present.

For plain log files it can classify common severity terms and surface configured defensive indicators such as failures, denied/unauthorized events, unexpected activity, SCADA/PLC references, pressure, membrane and water-quality terms.

AquaSentinel does **not** invent missing measurements. If a field is not present in the supplied file, it is not shown as measured data.

---

## What the analysis shows

The browser and terminal interfaces use the same local analysis engine. Depending on the contents of the file, AquaSentinel can show:

- source filename, detected format, record count and discovered fields;
- critical/error/warning counts;
- recognized water/process metric summaries with minimum, average, maximum and latest values;
- configured OT/security and process indicator counts;
- illustrative classroom-band review flags for recognized water fields;
- an explainable review score and `MONITOR` / `REVIEW` disposition;
- local IsolationForest anomaly detection when at least 12 records contain enough complete numeric fields;
- the fields used by the anomaly model and the number of rows it marked unusual; and
- a recent-record view for human inspection.

The anomaly model is fitted to the loaded numeric dataset. It is an advisory signal, not an automated plant decision.

---

## Local browser design

The localhost interface is deliberately simple:

```text
Data source
  -> Select local file
  -> Analyze

Analysis summary
  -> Decision
  -> Review score
  -> Record count
  -> Critical / errors
  -> Review flags
  -> ML anomalies

Detailed review
  -> Source profile
  -> Severity classification
  -> Recognized water/process fields
  -> Observed indicators
  -> Local anomaly model
  -> Human-review items
  -> Recent records
```

The server binds to `127.0.0.1` only. The selected file is sent only to the AquaSentinel process running on the same computer and is analyzed in memory; the web interface does not provide an endpoint for industrial control.

---

## Manual commands

```bash
# Browser interface
aquasentinel web

# Browser on another local port
aquasentinel web --port 9000

# Terminal analysis
aquasentinel analyze plant.log

aquasentinel analyze telemetry.csv

# Environment check
aquasentinel doctor

# Conceptual defensive architecture
aquasentinel architecture

# Educational assurance context
aquasentinel compliance
```

Running `aquasentinel` without a command prints the available interface choices instead of starting a demonstration.

---

## Analysis architecture

```text
User-supplied file
      |
      v
Format parser
(LOG / TXT / CSV / JSON / JSONL)
      |
      v
Field normalization
      |
      +-------------------------+
      |                         |
      v                         v
Log / severity review      Water / process metrics
      |                         |
      +------------+------------+
                   |
                   v
          Defensive indicators
                   |
                   v
       Local anomaly detection
        (when data supports it)
                   |
                   v
          Explainable summary
                   |
          +--------+--------+
          |                 |
          v                 v
     Browser UI          Terminal UI
          |                 |
          +--------+--------+
                   |
                   v
              Human review
```

This is analysis architecture, not a control architecture. No module writes to field devices.

---

## Main files

```text
AquaSentinel.bat             Windows setup, verification and interface menu
aquasentinel/__main__.py     CLI routing
aquasentinel/ingestion.py    File parsing, normalization and dataset analysis
aquasentinel/file_analysis.py Terminal presentation
aquasentinel/webui.py        Localhost browser workstation
aquasentinel/doctor.py       Environment / safety checks
aquasentinel/compliance.py   Educational assurance context
tests/test_ingestion.py      File-ingestion verification
tests/test_webui.py          Browser-interface verification
.github/workflows/ci.yml     Linux and Windows CI
```

The repository still contains supporting analytical modules developed during the project, but the v1.0.0 user workflow is file-driven. No preloaded incident is started by the application, and legacy demo helpers are excluded from the Windows user package.

---

## DevSecOps verification

CI checks the same release branch used to build the Windows package. It performs:

```text
editable installation
Ruff
Bandit
Pytest
environment doctor
architecture check
file-analysis self-check
browser-analysis self-check
real supplied-file CLI analysis
Windows ZIP build
ZIP content verification
```

A separate `windows-latest` job executes:

```bat
AquaSentinel.bat --check-only
```

so the actual Windows launcher is tested without entering an interactive interface.

---

## Data and privacy behavior

AquaSentinel does not require a cloud account or external API for file analysis. The browser interface is served by the local Python process and binds to `127.0.0.1`.

The project is intended for sanitized, authorized learning data. Do not load confidential utility information unless you are permitted to process it on the machine running AquaSentinel.

---

## Standards context

The project references NIST SP 800-82 concepts for OT/industrial-control security and uses EPA/WHO material only as educational water-safety context. It does not claim certification, regulatory compliance or suitability for operating a real water facility.

---

## Final safety statement

**AquaSentinel AI v1.0.0 is a local defensive analysis project.** It reads files supplied by the user and produces review information. It does not connect to or command real PLCs, SCADA systems, dosing equipment or water utilities, and its classroom water-quality checks must not be treated as operational limits or public-health decisions.
