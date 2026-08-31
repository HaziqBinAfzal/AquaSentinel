# AquaSentinel AI v1.0.0 Final Release

## Purpose

AquaSentinel AI v1.0.0 packages the Topic 133 project as a terminal-first, examiner-ready learning product while preserving the synthetic, defensive and read-only safety boundary.

## Fast installation

### Windows — recommended

1. Extract `AquaSentinel-v1.0.0-Windows.zip` to a normal folder.
2. Double-click `AquaSentinel.bat`.
3. The launcher verifies Python 3.10+, configures UTF-8 terminal output, creates the isolated environment, installs dependencies, runs tests/security/quality checks and functional smoke tests, then starts the guided examination demonstration.

Alternative Windows setup remains available through `install.bat` and `run_exam_demo.bat`.

### Linux/macOS

```bash
chmod +x install.sh run_exam_demo.sh
./install.sh
./run_exam_demo.sh
```

## Recommended exam commands

```bash
aquasentinel doctor
aquasentinel exam-demo
aquasentinel live --scenario dosing_event --samples 40 --refresh-rate 4 --fullscreen
aquasentinel incident --scenario dosing_event --step 8
aquasentinel report --output reports/aquasentinel_exam_report.json
```

## Final release gates

The v1.0.0 release is considered verified only when all of the following pass on the same final head commit:

- editable package installation
- runtime/package version consistency
- Ruff static checks
- Bandit defensive security scan
- Pytest unit tests
- environment doctor
- architecture smoke test
- dosing-event scenario smoke test
- live terminal smoke test
- incident presentation smoke test
- guided exam-demo smoke test
- exam-report generation
- Windows ZIP build
- ZIP content integrity verification
- dedicated `windows-latest` execution of `AquaSentinel.bat --check-only`

## Windows compatibility

The Windows launcher explicitly switches Command Prompt to UTF-8 and enables UTF-8 Python I/O before Rich output is rendered. This avoids legacy Windows code-page failures when dashboard symbols or architecture arrows are displayed.

## Exam safety statement

> AquaSentinel is a synthetic defensive learning lab. It does not connect to or control a real desalination plant, water utility, SCADA system, PLC or dosing controller. AI and optimization are advisory, and human/public-health authority remains in control.

## Final release procedure

1. Confirm Linux CI and the dedicated Windows launcher CI job are green on the final `1.0.0` head commit.
2. Confirm the generated `AquaSentinel-v1.0.0-Windows.zip` passes package-integrity verification.
3. Review PR #1 and the final documentation.
4. Confirm runtime and package metadata both report `1.0.0`.
5. Only after explicit merge approval, merge PR #1 into `main`.
6. After merge, create the `v1.0.0` Git tag/release and attach the verified final Windows distribution if desired.

Do not use this project as operational guidance for real critical infrastructure.
