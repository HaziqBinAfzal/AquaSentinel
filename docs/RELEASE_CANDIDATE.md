# AquaSentinel AI v1.0.0 Final Release

## Purpose

AquaSentinel AI v1.0.0 packages Topic 133 as a safe, examiner-ready learning product with both a localhost browser dashboard and terminal interfaces while preserving the synthetic, defensive and read-only safety boundary.

## Recommended Windows start

1. Extract `AquaSentinel-v1.0.0-Windows.zip` to a normal folder.
2. Double-click `AquaSentinel.bat`.
3. Let the launcher complete environment, test, lint, security and functional checks.
4. After `ALL CHECKS PASSED`, AquaSentinel starts the local dashboard and opens the browser automatically.
5. Default address: `http://127.0.0.1:8765/`.
6. Keep the terminal open while using the browser dashboard. Press `Ctrl+C` in the terminal to stop the localhost server.

The original guided terminal exam mode remains available with:

```text
.venv\Scripts\python.exe -m aquasentinel exam-demo
```

## Linux/macOS

```bash
chmod +x install.sh run_exam_demo.sh
./install.sh
aquasentinel web
```

## Recommended exam commands

```bash
aquasentinel web
aquasentinel doctor
aquasentinel exam-demo
aquasentinel live --scenario dosing_event --samples 40 --refresh-rate 4 --fullscreen
aquasentinel incident --scenario dosing_event --step 8
aquasentinel report --output reports/aquasentinel_exam_report.json
```

## Local dashboard scope

The browser UI shows the synthetic desalination process, water-quality measurements, process telemetry, IsolationForest anomaly status, OT/SCADA evidence, cyber-physical correlation, overall risk, predictive maintenance, resource optimization, incident response, trust-zone architecture and assurance context. It supports all six controlled scenarios and automatic or manual frame progression.

The web server binds to `127.0.0.1` only and provides visualization/state endpoints only. It has no real industrial-control write path.

## Final release gates

The v1.0.0 release is accepted only when all of the following pass on the exact final head commit:

- editable package installation
- runtime/package version consistency
- Ruff static checks
- Bandit defensive security scan
- Pytest including localhost-dashboard tests
- environment doctor
- architecture smoke test
- dosing-event scenario smoke test
- terminal live-dashboard smoke test
- localhost dashboard `--check-only` smoke test
- incident presentation smoke test
- guided exam-demo smoke test
- exam-report generation
- Windows distribution build
- ZIP content integrity check including `aquasentinel/webui.py`
- dedicated `windows-latest` execution of `AquaSentinel.bat --check-only`

## Windows compatibility

The Windows launcher explicitly switches Command Prompt to UTF-8 and enables UTF-8 Python I/O before Rich output is rendered. It also validates the local dashboard data path before starting the browser server.

## Exam safety statement

> AquaSentinel is a synthetic defensive learning lab. It does not connect to or control a real desalination plant, water utility, SCADA system, PLC or dosing controller. The localhost page is a read-only visualization layer. AI and optimization are advisory, and human/public-health authority remains in control.

## Final release procedure

1. Confirm Linux and Windows CI are green on the exact final v1.0.0 head commit.
2. Confirm the generated `AquaSentinel-v1.0.0-Windows.zip` passes package-integrity verification and contains the browser UI.
3. Review PR #1, README and project/viva guide.
4. Confirm runtime and package metadata both report `1.0.0`.
5. Only after explicit merge approval, merge PR #1 into `main`.
6. After merge, create the `v1.0.0` Git tag/release and attach the verified final Windows distribution if desired.

Do not use this project as operational guidance for real critical infrastructure.
