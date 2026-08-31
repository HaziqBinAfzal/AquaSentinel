# AquaSentinel AI

A safe, simulated and defensive **Smart Water & Desalination Infrastructure Security Platform** for Haziq Shahzad's EduQual Level 6 Topic 133 oral examination.

> This classroom project uses synthetic telemetry and isolated software components. It does not connect to, operate, or modify a real water utility, desalination plant, SCADA system, PLC, dosing controller, or public-health system.

## What the demo proves

AquaSentinel combines six exam capabilities in one terminal-first lab:

1. OT/SCADA protection and segmented-zone visibility.
2. Real-time water-quality monitoring and cross-sensor validation.
3. AI-style anomaly scoring, contamination-event prioritization, fouling prediction and predictive maintenance.
4. Energy/resource optimization with quality and equipment guardrails.
5. DevSecOps evidence, vulnerability/patch-status simulation and audit logging.
6. Compliance/public-health reporting mapped to EPA/WHO context and NIST SP 800-82.

## Architecture

```text
Enterprise / SOC
      |
Industrial DMZ
      |
 OT / SCADA ---------------- Network security events
      |
Safety & Quality ----------- Quality validation
      |
Synthetic treatment process
      |
Telemetry -> Analytics -> Cyber | Quality | Optimization
                              |
                       Terminal dashboard
                              |
                     Audit / exam report
```

The synthetic process follows the learning-book flow: raw/sea water -> pretreatment -> high-pressure pumping -> reverse osmosis -> post-treatment/disinfection -> storage -> distribution.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m aquasentinel demo
```

Other commands:

```bash
python -m aquasentinel run --scenario normal --samples 20
python -m aquasentinel run --scenario sensor_anomaly --samples 20
python -m aquasentinel run --scenario quality_anomaly --samples 20
python -m aquasentinel run --scenario dosing_event --samples 20
python -m aquasentinel run --scenario fouling --samples 20
python -m aquasentinel run --scenario optimization --samples 20
python -m aquasentinel architecture
python -m aquasentinel compliance
```

## Synthetic telemetry

The simulator generates: timestamp, pH, conductivity, turbidity, residual chlorine, salinity, feed pressure, RO pressure, flow rate, temperature, tank level, pump state, energy use, membrane health, quality anomaly label and cyber event.

## Safe examiner demo

Use `python -m aquasentinel demo`. It walks through a normal baseline followed by safe synthetic scenarios. Explain that an abnormal sensor is evidence, not automatic proof of contamination; quality events are cross-validated; AI recommends/prioritizes rather than blindly controlling the process; and incident response protects safe water/public health first.

## Incident workflow

Unexpected dosing event -> detect network/control anomaly -> correlate identity, SCADA and quality evidence -> contain the simulated access path -> independently verify quality -> restore validated state -> preserve audit/report evidence.

## Project structure

```text
aquasentinel/
  __main__.py       CLI
  telemetry.py      synthetic desalination telemetry
  analytics.py      quality, fouling, cyber and optimization analytics
  dashboard.py      terminal SCADA/security dashboard
  compliance.py     compliance/evidence mapping
  audit.py          JSONL audit trail
  scenarios.py      controlled exam scenarios
tests/
  test_analytics.py
```

## Exam mapping

- Architecture: Enterprise/SOC -> Industrial DMZ -> OT/SCADA -> Safety & Quality -> Treatment Process.
- OT protection: segmentation, controlled access, least privilege and passive-monitoring concepts.
- Quality: pH, conductivity, turbidity, residual chlorine, salinity, pressure, flow and temperature.
- AI: anomaly prioritization, membrane-fouling risk, demand/energy recommendation and predictive maintenance.
- Response: cyber evidence is correlated with process/public-health consequence before safe containment.
- DevSecOps: testable modules, controlled changes, traceable audit evidence and rollback-oriented design.
- Compliance: evidence mapping for NIST SP 800-82, EPA and WHO water-safety context.

## Limitation

This is an educational simulation. Thresholds, models, regulatory mappings and response actions are illustrative and must not be treated as operational guidance for real critical infrastructure.
