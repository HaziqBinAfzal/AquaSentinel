# AquaSentinel AI v1.0.0-rc1 Release Candidate

## Purpose

This release candidate packages the Topic 133 project as a terminal-first, examiner-ready learning product while preserving the synthetic, defensive and read-only safety boundary.

## Fast installation

### Windows

1. Open the AquaSentinel folder.
2. Run `install.bat` once.
3. Run `run_exam_demo.bat` for the guided demonstration.

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

## Release gates

The candidate is ready for final release review only when all of the following pass on the final head commit:

- editable package installation
- Ruff static checks
- Bandit defensive security scan
- Pytest unit tests including package-version consistency
- environment doctor
- architecture smoke test
- dosing-event scenario smoke test
- live terminal smoke test
- incident presentation smoke test
- guided exam-demo smoke test
- exam-report generation

## Exam safety statement

Use this statement before the demonstration:

> AquaSentinel is a synthetic defensive learning lab. It does not connect to or control a real desalination plant, water utility, SCADA system, PLC or dosing controller. AI and optimization are advisory, and human/public-health authority remains in control.

## Final release procedure

1. Confirm CI is green on the final release-candidate commit.
2. Review the PR diff and documentation.
3. Confirm version `1.0.0rc1` is consistent in package metadata and runtime code.
4. Perform the Windows installation and guided-demo path on a clean machine if available.
5. Only after explicit approval, merge PR #1.
6. After merge, promote the version to `1.0.0`, create the final tag/release, and attach any user distribution archive if desired.

Do not use this project as operational guidance for real critical infrastructure.
