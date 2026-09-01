# AquaSentinel

## Water Security & Resilience Evidence Workstation

[![CI](https://github.com/HaziqBinAfzal/AquaSentinel/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/HaziqBinAfzal/AquaSentinel/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-workstation-0078D4?logo=windows&logoColor=white)
![Mode](https://img.shields.io/badge/mode-local%20%7C%20read--only%20%7C%20defensive-0B7285)

**EduQual Level 6 Diploma in Artificial Intelligence Operations — Topic 133**

**Topic:** *Orchestrating Smart Water and Desalination Infrastructure Security Platform with OT Protection, Quality Monitoring, and AI-Driven Resource Optimization for Critical Water Systems.*

AquaSentinel is a local, schema-driven analysis workstation for user-supplied water, desalination, operational-technology, security, maintenance, energy and assurance evidence. It does not require fixed filenames, a fixed number of files, or a predefined telemetry schema. The analysis is built from the evidence actually supplied.

> **Safety boundary:** AquaSentinel is read-only and educational. It does not connect to or control PLCs, SCADA systems, pumps, valves, dosing controllers, treatment equipment or water utilities. An anomaly is not proof of contamination, unsafe water or cyber compromise. Findings require qualified human review.

---

## What AquaSentinel does

AquaSentinel accepts one or many evidence files, inspects their structure, identifies useful fields, infers the likely evidence domain, measures data quality, discovers suitable numeric features, applies anomaly analysis only when the data supports it, checks compatible timestamp windows across files, calculates an advisory evidence-risk view, and presents the result in a professional terminal command center.

The same analyzed evidence package can also be published as Prometheus metrics for a local Grafana dashboard and exported as a Markdown Evidence & Assurance Report containing SHA-256 provenance fingerprints and analysis limitations.

AquaSentinel follows a simple rule:

**No evidence → no metric → no fabricated finding.**

---

## Evidence-driven analysis path

```text
USER-SUPPLIED WATER / OT EVIDENCE
             |
             v
       FILE INGESTION
             |
             v
       SHA-256 PROVENANCE
             |
             v
       SCHEMA PROFILING
             |
             v
       DOMAIN INFERENCE
             |
             v
       DATA QUALITY CHECK
             |
             v
       FEATURE DISCOVERY
             |
             v
   AI / ROBUST ANOMALY ANALYSIS
             |
             v
   CROSS-SOURCE TIME EVIDENCE
             |
             v
   ADVISORY RISK PRIORITIZATION
             |
      +------+------+
      |             |
      v             v
 TERMINAL        PROMETHEUS
 COMMAND CENTER      |
      |              v
      |           GRAFANA
      +------+-------+
             |
             v
   EVIDENCE / ASSURANCE REPORT
             |
             v
        HUMAN REVIEW
```

This is an analysis architecture, not an industrial control architecture.

---

## Supported evidence formats

| Format | Example evidence |
| --- | --- |
| `.csv` | telemetry, process exports, audit tables, event records |
| `.json` | structured OT/security/process evidence |
| `.jsonl` | line-delimited event or telemetry evidence |
| `.xlsx` | spreadsheet exports and assessment evidence |

A directory can also be supplied; AquaSentinel will analyze the supported files it contains.

There is no required column list. Names such as pH, turbidity, conductivity, chlorine, flow, pressure, energy, membrane health, access events or audit fields are semantic clues when present, not mandatory inputs.

---

## Dynamic evidence domains

AquaSentinel currently infers a primary evidence domain from the supplied schema using semantic signals such as:

- **SCADA / OT**
- **WATER QUALITY**
- **DESALINATION / PROCESS**
- **ENERGY / RESOURCE**
- **MAINTENANCE / ASSET**
- **ACCESS / IDENTITY**
- **COMPLIANCE / AUDIT**
- **GENERAL / UNKNOWN** when the evidence is insufficient for a more specific classification

Unknown evidence is not forced into a water or cybersecurity category.

---

## AI and anomaly analysis

AquaSentinel automatically discovers suitable numeric features rather than relying on a hard-coded sensor list.

For larger usable datasets, it uses a deterministic **Isolation Forest** model. Smaller datasets with enough records use a robust median/MAD method. If there are too few complete numeric observations to support a defensible anomaly finding, AquaSentinel reports the limitation and leaves the anomaly result at zero instead of inventing a result.

The model output is an advisory prioritization signal only. It does not diagnose contamination, confirm an attack, certify water safety or authorize operational action.

---

## Evidence provenance and time correlation

Every analyzed file receives a **SHA-256 fingerprint** in the evidence package and exported report so the source used for analysis can be identified later.

AquaSentinel also searches for timestamp-like fields and validates whether their values can be parsed. When two evidence files contain compatible overlapping UTC windows, the workstation records that overlap as **cross-source time evidence**.

An overlapping time window only means the evidence was recorded during the same period. AquaSentinel does not automatically claim causal correlation between events.

---

## Start on Windows

Clone or extract the repository and double-click:

```text
AquaSentinel.bat
```

The launcher checks Python 3.10+, creates a local `.venv` when needed, installs AquaSentinel and opens the workstation menu:

```text
[1] LOAD EVIDENCE + TERMINAL COMMAND CENTER
[2] COMMAND CENTER + LIVE GRAFANA MONITORING
[3] ANALYZE EVIDENCE + EXPORT ASSURANCE REPORT
[4] OPEN GRAFANA
[5] OPEN PROMETHEUS
[6] OPEN RAW METRICS
[7] SYSTEM DIAGNOSTICS
[8] ARCHITECTURE & ASSURANCE
[Q] QUIT
```

For evidence options, enter one file or folder at a time. Windows drag-and-drop paths are supported. Press Enter on an empty line when all evidence paths have been added.

---

## Terminal Command Center

The command center is generated from the active evidence package. It displays only information supported by the supplied files, including:

- evidence source and record counts;
- inferred evidence domains and confidence;
- discovered numeric features;
- missing-data percentage;
- analysis method used;
- advisory anomaly pressure and model flags;
- inferred timestamp field;
- shortened SHA-256 fingerprint;
- evidence priority queue;
- cross-source overlapping timestamp windows; and
- explicit safety and human-review boundaries.

The interface is designed as a water-security and resilience workstation rather than a simulated game or fake plant-control panel.

---

## Grafana and Prometheus

Optional local monitoring uses Docker Compose.

```text
Grafana:    http://localhost:3001/d/aquasentinel-main
Prometheus: http://localhost:9091
Metrics:    http://localhost:9118/metrics
```

The metrics exporter publishes the analyzed evidence package. It does not poll industrial devices or retrieve live plant data.

The Grafana dashboard can display evidence-source count, indexed records, advisory risk, model flags, per-source anomaly pressure, data quality and evidence inventory information.

---

## Evidence & Assurance Report

AquaSentinel can export a Markdown report for the analyzed evidence package.

The report contains:

- generation time;
- evidence source inventory;
- SHA-256 fingerprints;
- file types, row counts and discovered columns;
- inferred domains and confidence;
- numeric features used by the model;
- missingness and analysis method;
- anomaly pressure and flags;
- inferred evidence windows;
- compatible cross-source time evidence;
- analysis limitations; and
- assurance/safety boundary statements.

The Windows launcher generates timestamped reports under `reports/`.

Manual example:

```bash
python -m aquasentinel --files evidence.csv --command-center --report reports/evidence.md
```

---

## Manual CLI examples

```bash
# Analyze one file in the terminal command center
python -m aquasentinel --files evidence.csv --command-center

# Analyze several files
python -m aquasentinel --files quality.csv ot-events.json energy.xlsx --command-center

# Analyze every supported file in a directory
python -m aquasentinel --files evidence_folder --command-center

# Export an evidence report
python -m aquasentinel --files evidence_folder --command-center --report reports/evidence.md

# Publish the analyzed package as Prometheus metrics
python -m aquasentinel --files evidence_folder --monitor

# CLI self-check
python -m aquasentinel --self-check

# Conceptual defensive architecture
python -m aquasentinel --architecture

# Educational assurance context
python -m aquasentinel --compliance
```

---

## Main implementation

```text
AquaSentinel.bat                         Windows workstation launcher
aquasentinel/__main__.py                 Evidence-driven CLI routing
aquasentinel/evidence.py                 Schema profiling, domain inference, AI analysis,
                                         provenance and timestamp-window logic
aquasentinel/terminal_command_center.py  Rich terminal operations view
aquasentinel/evidence_metrics.py         Prometheus metrics publication
aquasentinel/evidence_report.py          Evidence & Assurance Report export
aquasentinel/dashboard.py                Conceptual defensive architecture view
aquasentinel/compliance.py               Educational assurance context
monitoring/prometheus.yml                 Local Prometheus configuration
monitoring/grafana/                       Provisioned Grafana datasource/dashboard
docker-compose.yml                        Local Grafana + Prometheus stack
tests/test_evidence.py                    Schema/provenance/correlation tests
.github/workflows/ci.yml                  Linux and Windows CI
```

Legacy guided exam-demo launchers and the old pre-scripted demonstration module have been removed from the development branch. Synthetic data may still exist in historical/supporting modules or test fixtures, but the normal AquaSentinel workflow does not automatically load a scenario or pretend that user evidence contains specific sensors.

---

## DevSecOps verification

GitHub Actions validates the development workflow on Linux and Windows. Current checks include package installation, Ruff static analysis, Bandit security analysis, pytest, CLI self-check, architecture/assurance commands, a real schema-driven CSV analysis and Evidence & Assurance Report generation.

The release process should not treat CI as complete until all jobs are green. Development changes remain on `develop` until they are verified and intentionally promoted to `main`.

---

## Privacy and authorized-use guidance

AquaSentinel performs its analysis locally and does not require a cloud API or external AI service. Use only sanitized evidence or information you are authorized to process.

The workstation is intended for education, demonstrations, defensive analysis and software-development practice. It is not a qualified operational water-quality instrument, a regulatory compliance system, a public-health decision system or an industrial control platform.

---

## Safety statement

AquaSentinel analyzes evidence; it does not operate infrastructure.

It does **not** connect to real PLC/SCADA equipment, issue pump/valve commands, alter chemical dosing, perform destructive industrial actions, provide attack tooling or claim that an anomaly proves contamination or compromise. Consequential decisions remain with qualified human operators, engineers, security teams and public-health authorities.
