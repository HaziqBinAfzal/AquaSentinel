# Changelog

## 1.0.0

AquaSentinel AI reaches its first final release as a safe, synthetic and defensive Topic 133 examination platform.

### Final release highlights

- Localhost browser operations dashboard at `http://127.0.0.1:8765/` with live synthetic process, quality, AI, OT-security, risk, optimization and incident-response views.
- Browser scenario selector covering `normal`, `sensor_anomaly`, `quality_anomaly`, `dosing_event`, `fouling` and `optimization`.
- Automatic browser launch from `AquaSentinel.bat` after all verification gates pass.
- Read-only JSON state endpoint used only by the local UI; server is bound to `127.0.0.1` and exposes no control/write API.
- Terminal-first smart water and desalination security simulation remains available alongside the browser UI.
- Segmented Enterprise / DMZ / OT / Safety & Quality architecture view.
- Synthetic desalination telemetry and controlled exam scenarios.
- Rule-based water-quality checks and cross-sensor validation.
- IsolationForest anomaly detection over synthetic process features.
- Simulated Zeek, Suricata and SCADA audit evidence with cyber/process correlation.
- Membrane fouling and predictive-maintenance analytics.
- Guardrailed resource and energy optimization recommendations.
- Low-lag industrial SOC-style Rich live dashboard and full-screen presentation mode.
- Examiner-friendly incident brief and eight-stage response timeline.
- Guided one-command `aquasentinel exam-demo` oral-exam sequence.
- JSONL audit evidence and JSON exam-report export.
- Environment doctor and explicit synthetic/read-only safety checks.
- One-file Windows setup, verification and localhost-dashboard launcher.
- UTF-8-safe Windows Command Prompt support.
- Dedicated Windows CI job running `AquaSentinel.bat --check-only` end-to-end.
- Linux CI with Pytest, Ruff, Bandit, terminal/web functional smoke tests and distribution integrity checks.
- Final Windows ZIP containing application code, browser UI, tests, documentation, assets and `START_HERE.txt`.
- Examiner-facing README, terminal preview, project/viva guide and release documentation.

### Release history

`1.0.0-rc1` was the release-candidate stage used to harden Windows packaging, console compatibility and final verification before promotion to `1.0.0`.

### Safety boundary

AquaSentinel is a classroom simulation only. It does not connect to, control, write to or modify real water utilities, desalination plants, PLCs, SCADA systems, dosing controllers or public-health infrastructure. The localhost UI is a visualization layer only. Thresholds, models, optimization outputs and assurance mappings are illustrative and are not operational guidance, regulatory limits or certification.
