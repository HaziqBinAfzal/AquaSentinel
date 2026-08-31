# AquaSentinel AI v1.0.0 Final Release

## Purpose

AquaSentinel AI v1.0.0 is packaged as a local defensive analysis workstation for Topic 133. The final user experience is file-driven: AquaSentinel does not preload a plant incident or automatically run a synthetic scenario.

## Recommended Windows start

1. Extract `AquaSentinel-v1.0.0-Windows.zip` to a normal folder.
2. Double-click `AquaSentinel.bat`.
3. Allow the launcher to complete environment, test, lint, security and local-analysis checks.
4. After `ALL CHECKS PASSED`, choose:

```text
[1] Browser interface
[2] Terminal interface
[Q] Quit
```

### Browser

The browser interface runs on:

```text
http://127.0.0.1:8765/
```

It starts with no dataset loaded. Select a local `.log`, `.txt`, `.csv`, `.json` or `.jsonl` file and click **Analyze file**.

### Terminal

Paste the path to a supported file. The same analysis engine prints its findings in the terminal.

Manual command:

```bash
aquasentinel analyze "C:\path\to\file.log"
```

## Linux/macOS

```bash
chmod +x install.sh
./install.sh
aquasentinel web
# or
aquasentinel analyze /path/to/file.csv
```

## File-analysis scope

AquaSentinel can inspect source format, fields, record count, severity terms, configured OT/security indicators and recognized water/process metrics. When enough complete numeric rows are present, it fits a local IsolationForest model and reports unusual rows. If the file does not contain enough suitable data, the ML state is reported as `NOT RUN`.

Recognized classroom water/process checks are advisory and use illustrative teaching bands only.

## Final release gates

The release is accepted only when all of the following pass on the same head commit:

- editable package installation
- runtime/package version consistency
- Ruff static checks
- Bandit defensive security scan
- Pytest including ingestion and browser-interface tests
- environment doctor
- architecture command
- file-analysis self-check
- localhost analysis self-check
- real CLI analysis of a supplied CSV file
- Windows distribution build
- ZIP content integrity verification including `ingestion.py`, `file_analysis.py` and `webui.py`
- dedicated `windows-latest` execution of `AquaSentinel.bat --check-only`

## Localhost security boundary

The browser server binds only to `127.0.0.1`. Selected files are analyzed in memory by the local AquaSentinel process. The browser interface has no endpoint for PLC, SCADA, dosing or utility control.

## Windows compatibility

The launcher switches Command Prompt to UTF-8, enables UTF-8 Python I/O, supports both `py -3` and `python`, and verifies Python 3.10 or newer.

## Exam safety statement

> AquaSentinel is a local defensive analysis project. It reads files supplied by the user and does not connect to or control a desalination plant, water utility, SCADA system, PLC or dosing controller. Its classroom review bands and AI output are advisory and are not operational or regulatory decisions.

## Final release procedure

1. Confirm Linux and Windows CI are green on the exact final v1.0.0 head commit.
2. Confirm `AquaSentinel-v1.0.0-Windows.zip` passes package-integrity verification.
3. Review PR #1, README and project/viva guide.
4. Confirm the browser starts empty and the launcher offers browser/terminal selection.
5. Confirm a supplied file can be analyzed through both interfaces.
6. Only after explicit merge approval, merge PR #1 into `main`.
7. After merge, create the `v1.0.0` Git tag/release if desired.

Do not use this project as operational guidance for real critical infrastructure.
