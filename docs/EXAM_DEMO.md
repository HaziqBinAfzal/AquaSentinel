# Topic 133 — AquaSentinel Oral Exam Demo

## 3–5 minute project demonstration

1. **Boundary:** "This is a synthetic, defensive classroom simulation. It does not connect to a real desalination plant or SCADA system."
2. Run `python -m aquasentinel architecture` and explain Enterprise/SOC -> Industrial DMZ -> OT/SCADA -> Safety & Quality -> treatment process.
3. Run `python -m aquasentinel run --scenario normal --samples 7`. Explain the baseline and sensor meanings.
4. Run `python -m aquasentinel run --scenario quality_anomaly --samples 7`. Explain that one abnormal reading is not proof of contamination; multi-sensor evidence raises priority and independent verification is required.
5. Run `python -m aquasentinel run --scenario dosing_event --samples 7`. Walk through detect -> correlate identity/SCADA/quality -> safe containment -> independent quality verification -> validated recovery -> audit/report.
6. Run `python -m aquasentinel run --scenario fouling --samples 12`. Explain pressure/flow/membrane trends and predictive maintenance.
7. Run `python -m aquasentinel run --scenario optimization --samples 7`. Explain that optimization is advisory and cannot override quality/equipment guardrails.
8. Run `python -m aquasentinel compliance`. Explain evidence mapping, not certification.

## What each subsystem means

- **OT protection:** architectural segmentation and security-event correlation represent how compromise should be contained away from treatment control.
- **Quality monitoring:** pH, conductivity, turbidity, residual chlorine, salinity, pressure, flow and temperature are interpreted together.
- **AI/analytics:** the classroom engine produces quality, fouling, cyber and resource priority/recommendation outputs. It demonstrates the reasoning pipeline; it is not a qualified operational model.
- **Resource optimization:** energy and storage evidence produce a recommendation subject to public-health and equipment constraints.
- **DevSecOps:** source control, tests, CI and audit records make changes/evidence traceable and recoverable.
- **Compliance:** NIST SP 800-82, EPA and WHO are represented as exam-context assurance mappings.

## Examiner-ready limitations

The telemetry is synthetic, the thresholds are illustrative rather than regulatory limits, the analytics are deliberately explainable, no real industrial protocols/controllers are commanded, and all consequential decisions remain human/engineering/public-health responsibilities.
