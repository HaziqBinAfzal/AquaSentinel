# AquaSentinel AI — Project & Viva Guide

## 1. What the project is

AquaSentinel AI is a synthetic, terminal-first demonstration of a smart water and desalination infrastructure security platform. It combines process visibility, OT cybersecurity, water-quality monitoring, AI anomaly detection, membrane-health analysis, resource optimization, DevSecOps evidence and compliance reporting without connecting to a real plant.

The central idea is that critical water infrastructure cannot be protected by looking at cybersecurity, process engineering or water quality separately. AquaSentinel correlates all three and then asks for human review when the evidence could affect safety or public health.

## 2. The simulated desalination process

The project models this simplified process:

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

SCADA provides supervisory monitoring of industrial processes. OT includes the industrial systems that observe or influence the physical process. In this educational project there is no real control path. Instead, AquaSentinel creates synthetic telemetry and synthetic security evidence so the student can explain how monitoring and incident reasoning would work safely.

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

This is a simple demonstration of predictive maintenance: rather than waiting for complete equipment failure, trends can be used to prioritize inspection or maintenance.

## 8. AI-driven resource optimization

`optimizer.py` recommends one of several advisory modes:

- `BALANCED` for ordinary safe operation.
- `ENERGY-SAVER` when storage is healthy and energy consumption is high.
- `SUPPLY-RECOVERY` when storage reserve is low.
- `MAINTENANCE-AWARE` when membrane condition makes aggressive production inefficient.
- `HOLD-SAFE` when quality or cybersecurity evidence requires verification.

The important design principle is that the optimizer cannot override quality/security concerns. Efficiency is subordinate to validated safe operation.

## 9. Live terminal dashboard

`live.py` uses Rich Live to refresh one operator-style terminal view instead of continuously scrolling output. This reduces terminal clutter and creates a more realistic exam demonstration.

The dashboard shows:

```text
Synthetic process flow
Water quality
RO/process condition
OT-security evidence
Cross-domain correlation
ML anomaly state
Optimization mode
Final MONITOR / HUMAN REVIEW decision
```

Run it with:

```bash
aquasentinel live --scenario normal --samples 30
```

## 10. Audit and evidence

`audit.py` writes JSONL evidence for scenario observations and analysis. `reporting.py` produces an exam-oriented JSON report. This demonstrates traceability: the system can explain what data was observed, what analysis was produced and what decision was recommended.

## 11. Compliance framing

`compliance.py` maps project evidence to educational context around NIST SP 800-82, EPA and WHO water-safety principles. It does not claim certification or regulatory compliance.

The project demonstrates ideas such as segmentation, monitored access, passive OT visibility, quality verification, risk-based escalation, audit evidence and public-health-first response.

## 12. DevSecOps

The GitHub Actions pipeline verifies the project before merge. It installs the package, runs Ruff static checks, Bandit security scanning, Pytest tests, the environment doctor, architecture command, dosing-event scenario, live dashboard smoke check and report generation.

This demonstrates DevSecOps as security and quality controls integrated into the development lifecycle rather than added only after deployment.

## 13. Important files

```text
aquasentinel/__main__.py   command-line interface
aquasentinel/telemetry.py  synthetic process and quality data
aquasentinel/analytics.py  transparent rule-based analysis
aquasentinel/ml.py         IsolationForest anomaly detection
aquasentinel/security.py   synthetic OT/security correlation
aquasentinel/optimizer.py  safe resource recommendations
aquasentinel/dashboard.py  terminal visualization
aquasentinel/live.py       low-lag live refresh
aquasentinel/doctor.py     exam-machine checks
aquasentinel/audit.py      JSONL evidence
aquasentinel/reporting.py  exam report export
aquasentinel/compliance.py assurance-framework mapping
aquasentinel/scenarios.py  controlled demonstrations
tests/                     automated verification
.github/workflows/ci.yml   DevSecOps pipeline
```

## 14. Recommended 3–5 minute project demonstration

1. Run `aquasentinel doctor` and explain that the environment and safety boundary are checked.
2. Run `aquasentinel architecture` and explain Enterprise -> DMZ -> OT -> Safety/Quality -> Process.
3. Show `normal` and explain the baseline.
4. Show `quality_anomaly` and explain cross-sensor verification plus ML prioritization.
5. Show `dosing_event` and explain cyber/process correlation and human review.
6. Show `fouling` and explain predictive maintenance.
7. Show `optimization` and explain that resource recommendations never override quality.
8. Run `aquasentinel compliance` or `aquasentinel report` and explain audit/evidence preservation.

## 15. Likely viva questions

### Why not let AI automatically change the process?
Because water infrastructure is safety and public-health critical. AI can recommend or prioritize, but changes need validated engineering constraints, authorization and human oversight.

### Why do you use both rules and ML?
Rules are explainable and deterministic. ML can identify unusual combinations that may not match one fixed threshold. Using both creates layered evidence.

### Why is network segmentation important?
It reduces unnecessary communication paths and limits how a compromise in an enterprise environment could reach OT assets.

### Why cross-check sensors?
A single sensor can drift, fail or be spoofed. Independent measurements and process context help distinguish a sensor problem from a genuine water-quality event.

### What makes this DevSecOps?
Tests, static checks, security scanning, packaging validation and runtime smoke tests are automated in the pull-request workflow.

### Is the project connected to a real desalination plant?
No. It is intentionally synthetic and defensive. That makes it safe and repeatable for an oral examination.

## 16. Final explanation to the examiner

AquaSentinel demonstrates that smart water security is not simply an antivirus system for SCADA. It is a layered approach combining OT architecture, independent water-quality evidence, process-aware cybersecurity, AI-supported anomaly detection, predictive maintenance, safe resource optimization, human oversight, DevSecOps and traceable compliance evidence.
