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

## Browser evidence workstation

AquaSentinel now includes a local interactive browser interface that uses the same schema-driven evidence engine as the terminal workflow. Start `AquaSentinel.bat` and choose **9 — WEB EVIDENCE WORKSTATION**, or run:

```bash
python -m aquasentinel.webapp
```

The browser opens on `http://127.0.0.1:8765`. Upload one or more CSV, JSON, JSONL or XLSX files and the page analyzes the actual files locally. It displays evidence counts, advisory risk, inferred domain, domain confidence, discovered numeric features, missingness, anomaly method and pressure, flags, timestamp evidence, SHA-256 provenance, analysis notes and compatible cross-source time evidence.

Uploads are stored only in a temporary local directory for the request and are removed after analysis. The browser workstation is bound to localhost by default and does not create a cloud upload service or an industrial-control connection.

## What AquaSentinel does

AquaSentinel accepts one or many evidence files, inspects their structure, identifies useful fields, infers the likely evidence domain, measures data quality, discovers suitable numeric features, applies anomaly analysis only when the data supports it, checks compatible timestamp windows across files, calculates an advisory evidence-risk view, and presents the result in a professional terminal or browser command center.

The same analyzed evidence package can also be published as Prometheus metrics for a local Grafana dashboard and exported as an Evidence & Assurance Report containing SHA-256 provenance fingerprints and analysis limitations.

AquaSentinel follows a simple rule:

**No evidence → no metric → no fabricated finding.**

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
 TERMINAL / WEB   PROMETHEUS
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

## Supported evidence formats

| Format | Example evidence |
| --- | --- |
| `.csv` | telemetry, process exports, audit tables, event records |
| `.json` | structured OT/security/process evidence |
| `.jsonl` | line-delimited event or telemetry evidence |
| `.xlsx` | spreadsheet exports and assessment evidence |

A directory can also be supplied from the terminal workflow; the browser workstation accepts multiple file uploads.

There is no required column list. Names such as pH, turbidity, conductivity, chlorine, flow, pressure, energy, membrane health, access events or audit fields are semantic clues when present, not mandatory inputs.

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

## AI and anomaly analysis

AquaSentinel automatically discovers suitable numeric features rather than relying on a hard-coded sensor list.

For larger usable datasets, it uses a deterministic **Isolation Forest** model. Smaller datasets with enough records use a robust median/MAD method. If there are too few complete numeric observations to support a defensible anomaly finding, AquaSentinel reports the limitation and leaves the anomaly result at zero instead of inventing a result.

The model output is an advisory prioritization signal only. It does not diagnose contamination, confirm an attack, certify water safety or authorize operational action.

## Evidence provenance and time correlation

Every analyzed file receives a **SHA-256 fingerprint** in the evidence package and exported report so the source used for analysis can be identified later.

AquaSentinel also searches for timestamp-like fields and validates whether their values can be parsed. When two evidence files contain compatible overlapping UTC windows, the workstation records that overlap as **cross-source time evidence**.

An overlapping time window only means the evidence was recorded during the same period. AquaSentinel does not automatically claim causal correlation between events.

## Start on Windows

Clone or extract the repository and double-click:

```text
AquaSentinel.bat
```

The launcher checks Python 3.10+, creates a local `.venv` when needed, installs AquaSentinel and opens the workstation menu, including the terminal workflow, Grafana/Prometheus monitoring, reporting and the local browser evidence workstation.

For terminal evidence options, enter one file or folder at a time. Windows drag-and-drop paths are supported. Press Enter on an empty line when all evidence paths have been added.

## Terminal Command Center

The command center is generated from the active evidence package. It displays only information supported by the supplied files, including evidence source and record counts, inferred evidence domains and confidence, discovered numeric features, missing-data percentage, analysis method used, advisory anomaly pressure and model flags, inferred timestamp field, shortened SHA-256 fingerprint, evidence priority and compatible cross-source timestamp windows.

The interface is designed as a water-security and resilience workstation rather than a simulated game or fake plant-control panel.

## Grafana and Prometheus

Optional local monitoring uses Docker Compose.

```text
Grafana:    http://localhost:3001/d/aquasentinel-main
Prometheus: http://localhost:9091
Metrics:    http://localhost:9118/metrics
```

All monitoring remains local and read-only.
