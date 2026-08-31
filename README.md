# AquaSentinel AI

A safe, simulated and defensive **Smart Water & Desalination Infrastructure Security Platform** for Haziq Shahzad's EduQual Level 6 Topic 133 oral examination.

> This classroom project uses synthetic telemetry and isolated software components. It does not connect to, operate, or modify a real water utility, desalination plant, SCADA system, PLC, dosing controller, or public-health system.

## What AquaSentinel demonstrates

AquaSentinel combines the Topic 133 requirements in one terminal-first project:

1. OT/SCADA protection and segmented-zone visibility.
2. Real-time water-quality monitoring and cross-sensor validation.
3. ML anomaly detection with IsolationForest plus transparent rule-based checks.
4. Contamination-event prioritization, membrane fouling risk and predictive-maintenance guidance.
5. Energy/resource optimization with quality, cybersecurity and equipment guardrails.
6. Synthetic Zeek/Suricata/SCADA event correlation.
7. DevSecOps evidence, automated tests, linting, security scanning and audit logging.
8. Compliance/public-health evidence mapping for NIST SP 800-82, EPA and WHO water-safety context.

## Architecture

```text
Enterprise / SOC
      |
Industrial DMZ
      |
 OT / SCADA ---------------- Passive synthetic security telemetry
      |
Safety & Quality ----------- Independent quality validation
      |
Synthetic treatment process
      |
Telemetry -> Rules + ML -> Cyber | Quality | Maintenance | Optimization
                                      |
                               Human review
                                      |
                          Live terminal dashboard
                                      |
                              Audit / exam report
```

The simulated treatment path is:

```text
Raw/Sea Water -> Pretreatment -> High-Pressure Pump -> Reverse Osmosis
             -> Post-Treatment/Disinfection -> Storage -> Distribution
```

## Installation

### Windows

```bat
install.bat
```

### Linux/macOS

```bash
chmod +x install.sh
./install.sh
```

Manual installation is also supported:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -e .
aquasentinel doctor
```

## Best exam commands

Start with the environment check:

```bash
aquasentinel doctor
```

Open the low-lag live terminal dashboard:

```bash
aquasentinel live --scenario normal --samples 30
```

Switch to controlled demonstrations:

```bash
aquasentinel live --scenario sensor_anomaly --samples 30
aquasentinel live --scenario quality_anomaly --samples 30
aquasentinel live --scenario dosing_event --samples 30
aquasentinel live --scenario fouling --samples 30
aquasentinel live --scenario optimization --samples 30
```

The live dashboard refresh rate is configurable:

```bash
aquasentinel live --scenario fouling --samples 40 --refresh-rate 4
```

For discrete snapshots instead of a live display:

```bash
aquasentinel run --scenario quality_anomaly --samples 10
```

Other commands:

```bash
aquasentinel architecture
aquasentinel ml-check
aquasentinel compliance
aquasentinel report
aquasentinel demo
```

## What appears on the terminal dashboard

The operator-style terminal view shows the synthetic desalination flow, water-quality evidence, RO pressure/flow/membrane condition, OT-security events, cross-domain correlation, IsolationForest anomaly state, guarded optimization recommendation and the final MONITOR or HUMAN REVIEW decision.

The optimizer is advisory only. If water quality or OT-security evidence is abnormal, it enters `HOLD-SAFE` instead of trying to save energy. This demonstrates the key critical-infrastructure principle that public health, safety and validated process integrity override efficiency.

## Synthetic telemetry

The simulator generates timestamp, pH, conductivity, turbidity, residual chlorine, salinity, feed pressure, RO pressure, flow rate, temperature, tank level, pump state, energy use, membrane health, quality anomaly label and cyber event.

A deterministic seed can be supplied for repeatable exam demonstrations:

```bash
aquasentinel run --scenario fouling --samples 12 --seed 133
```

## Safe examiner demo sequence

A strong short demonstration is:

```text
1. aquasentinel doctor
2. aquasentinel architecture
3. aquasentinel live --scenario normal --samples 10
4. aquasentinel live --scenario quality_anomaly --samples 12
5. aquasentinel live --scenario dosing_event --samples 12
6. aquasentinel live --scenario fouling --samples 15
7. aquasentinel live --scenario optimization --samples 12
8. aquasentinel compliance
9. aquasentinel report
```

Explain that one abnormal sensor is evidence rather than automatic proof of contamination; quality events are cross-validated; cyber alerts are correlated with process consequences; ML prioritizes anomalies; optimization stays inside safety/quality guardrails; and humans retain authority.

## Incident workflow

Unexpected dosing event -> detect synthetic network/control anomaly -> correlate SCADA, cyber and quality evidence -> assess process/public-health consequence -> hold optimization -> request human review -> verify quality independently -> recover validated state -> preserve audit/report evidence.

## Project structure

```text
aquasentinel/
  __main__.py       CLI and exam command routing
  telemetry.py      deterministic synthetic desalination telemetry
  analytics.py      quality, fouling and cyber analysis
  ml.py             IsolationForest anomaly model
  security.py       synthetic Zeek/Suricata/SCADA event correlation
  optimizer.py      guardrailed resource optimization advice
  dashboard.py      terminal dashboard renderer
  live.py           low-lag Rich Live operator view
  doctor.py         environment and safety-boundary checks
  compliance.py     compliance/evidence mapping
  reporting.py      JSON exam evidence report
  audit.py          JSONL audit trail
  scenarios.py      controlled exam scenarios

tests/
  test_analytics.py
  test_ml_security.py
  test_optimizer_doctor.py
.github/workflows/
  ci.yml            tests, lint, security scan and CLI smoke checks
install.bat          Windows setup
install.sh           Linux/macOS setup
```

## DevSecOps

Pull requests run automated checks for:

- Ruff static checks.
- Bandit defensive Python security scanning.
- Pytest unit tests.
- Environment doctor validation.
- Architecture command smoke test.
- Dosing-event scenario smoke test.
- Live terminal dashboard smoke test.
- Exam report generation.

## Exam mapping

- **Architecture:** Enterprise/SOC -> Industrial DMZ -> OT/SCADA -> Safety & Quality -> Treatment Process.
- **OT protection:** segmentation, controlled access, least privilege and passive-monitoring concepts.
- **Quality:** pH, conductivity, turbidity, residual chlorine, salinity, pressure, flow and temperature.
- **AI:** IsolationForest anomaly prioritization, membrane-fouling risk and guarded resource recommendations.
- **Threat response:** synthetic Zeek/Suricata/SCADA evidence is correlated with process/public-health consequence.
- **Resource optimization:** energy and production recommendations are subordinate to quality and equipment constraints.
- **DevSecOps:** testable modules, controlled changes, automated security checks, traceable audit evidence and rollback-oriented design.
- **Compliance:** evidence mapping for NIST SP 800-82, EPA and WHO water-safety context.

## Important limitation

This is an educational simulation. Thresholds, models, regulatory mappings, optimization outputs and response actions are illustrative and must not be treated as operational guidance for real critical infrastructure.
