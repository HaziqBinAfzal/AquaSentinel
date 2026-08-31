# AquaSentinel AI — Project & Viva Guide

## 1. What the project is

AquaSentinel AI v1.0.0 is a local defensive analysis workstation for water/process telemetry and OT/security logs. It is designed for Topic 133 and has two interfaces over the same analysis engine:

- a browser interface served on `http://127.0.0.1:8765/`; and
- a terminal interface for direct file analysis.

The important change in the final workflow is that AquaSentinel does **not** start with a prepared incident or built-in dataset. The user supplies a `.log`, `.txt`, `.csv`, `.json` or `.jsonl` file and the program analyzes the evidence in that file.

A useful viva sentence is:

> AquaSentinel does not pretend that a plant is already connected. I provide a log or telemetry export, and the system analyzes only the data that is actually present.

## 2. Why this fits Topic 133

Critical water infrastructure combines process engineering, water quality and operational technology. In a real environment, analysts often work from exported telemetry, alarms, security logs and incident evidence rather than allowing an AI model to control plant equipment directly.

AquaSentinel therefore focuses on the monitoring and decision-support side of the topic:

```text
User-supplied evidence
      |
      v
Parsing and field normalization
      |
      +---------------------+
      |                     |
      v                     v
OT / log review        Water / process data
      |                     |
      +----------+----------+
                 |
                 v
        Defensive indicators
                 |
                 v
        Local anomaly analysis
                 |
                 v
          Human-readable result
             /          \
      Browser UI      Terminal UI
                 |
                 v
            Human review
```

There is no control path to PLCs, SCADA systems, dosing equipment or utilities.

## 3. The two user interfaces

After `AquaSentinel.bat` completes its checks, the user sees:

```text
[1] Browser interface
[2] Terminal interface
[Q] Quit
```

### Browser interface

The browser opens on:

```text
http://127.0.0.1:8765/
```

The page initially says **No dataset loaded**. The user selects a local file and clicks **Analyze file**. The page then shows the source profile, record count, fields, severity classification, recognized water/process values, defensive indicators, anomaly-model status, review flags and recent records.

The browser design is deliberately plain and workstation-like: neutral background, white data panels, dark steel/navy header, muted status colors, conventional tables and restrained wording. It is meant to look like an engineering analysis tool rather than a decorative control-room mock-up.

### Terminal interface

The user pastes a local file path. The terminal shows the same core analysis in Rich tables.

Manual command:

```bash
aquasentinel analyze "C:\path\to\file.log"
```

## 4. Supported input formats

AquaSentinel accepts:

```text
.log
.txt
.csv
.json
.jsonl
```

The normal file-size limit is 8 MB and processing is capped at 10,000 records to keep local analysis predictable.

For structured data, AquaSentinel recognizes common field names for pH, conductivity, turbidity, residual chlorine, salinity, feed pressure, RO pressure, flow rate, temperature, tank level, energy use and membrane health when those fields are present.

For text logs, the parser extracts common `key=value` / `key:value` pairs, timestamps when visible, severity words and configured defensive indicator terms.

AquaSentinel does not invent a missing sensor value. If a field does not exist in the file, it is not shown as measured telemetry.

## 5. File parsing and normalization

`ingestion.py` is the main input engine. It detects the supplied format from the filename, parses the content and normalizes field names so that common variations can be compared consistently.

Examples:

```text
flow
flow_rate
flowrate
```

can be recognized as the same type of process measurement.

Nested JSON fields are flattened for inspection. Plain-text logs are kept as original messages while useful key/value information is extracted when possible.

## 6. Water and process review

When recognized water/process fields are present, AquaSentinel calculates:

- sample count;
- minimum;
- average;
- maximum; and
- latest value.

The project also applies a small set of **illustrative classroom review bands** to recognized fields. These are not regulatory limits and are not presented as a substitute for engineering or public-health requirements.

A useful viva sentence is:

> The thresholds are explainable teaching checks. They help me demonstrate review logic, but I do not claim that they are legal or operational limits.

## 7. Log and OT/security review

AquaSentinel classifies common log severity terms such as critical, error, warning and info. It also counts configured defensive indicator terms including examples such as denied, unauthorized, unexpected, SCADA, PLC, timeout, pressure, membrane and water-quality terms.

This is passive file analysis. The project does not scan an OT network, send protocol commands or attempt to reach industrial devices.

## 8. Local AI anomaly detection

When a loaded dataset contains at least 12 rows and at least two complete recognized numeric telemetry fields, AquaSentinel fits an IsolationForest model to the numeric data in that file.

The output shows:

- whether ML analysis ran;
- which fields were used; and
- how many rows were marked unusual.

If the file does not contain enough suitable data, the interface says **NOT RUN** and explains why instead of fabricating an AI result.

A useful viva sentence is:

> The AI only runs when the supplied dataset has enough numeric evidence. Otherwise AquaSentinel says that the model was not run.

## 9. Review score and decision

AquaSentinel combines visible evidence such as critical/error/warning entries, classroom-band exceptions and local anomaly counts into an explainable review score from 0 to 100.

The final disposition is intentionally simple:

```text
MONITOR
or
REVIEW
```

This is a prioritization aid, not an automated public-health or industrial-control decision.

## 10. Localhost safety design

`webui.py` uses Python's standard-library HTTP server and binds only to:

```text
127.0.0.1
```

The browser sends the selected file content to the AquaSentinel process running on the same computer. Analysis is performed in memory. The interface does not expose a PLC/SCADA write endpoint.

The server also sends defensive browser headers including `X-Content-Type-Options`, `X-Frame-Options`, `Cache-Control: no-store` and a Content Security Policy.

## 11. Windows launcher

`AquaSentinel.bat` performs setup and verification before presenting the interface menu. It:

1. configures UTF-8 terminal handling;
2. detects `py -3` or `python`;
3. verifies Python 3.10+;
4. creates `.venv` if needed;
5. installs the project and verification tools;
6. runs the environment doctor;
7. runs Pytest;
8. runs Ruff and Bandit;
9. runs file-analysis and browser self-checks; and
10. presents the browser/terminal choice.

`--check-only` allows CI to verify the launcher without waiting for interactive input.

## 12. DevSecOps

The Linux CI job verifies installation, Ruff, Bandit, Pytest, the environment doctor, architecture command, file-analysis self-check, browser self-check and a real CLI analysis of a supplied CSV file. It then builds the Windows ZIP and checks required package contents.

A separate `windows-latest` job runs:

```bat
AquaSentinel.bat --check-only
```

This verifies the actual Windows setup path.

## 13. Important files

```text
AquaSentinel.bat              setup, verification and interface selection
aquasentinel/__main__.py      CLI routing
aquasentinel/ingestion.py     log/data parsing and analysis
aquasentinel/file_analysis.py terminal presentation
aquasentinel/webui.py         localhost browser workstation
aquasentinel/doctor.py        environment and safety checks
aquasentinel/compliance.py    educational assurance context
tests/test_ingestion.py       input-engine tests
tests/test_webui.py           browser UI tests
.github/workflows/ci.yml      Linux + Windows verification
```

Supporting analytical modules from the development process remain in the repository, but the final user workflow is file-driven and does not automatically launch synthetic scenarios.

## 14. Recommended exam demonstration

1. Double-click `AquaSentinel.bat`.
2. Explain that the setup and security checks run before analysis.
3. Choose **Option 1** to show the browser interface.
4. Point out that the page starts with **No dataset loaded**.
5. Load a prepared, sanitized CSV or log file that you are allowed to use.
6. Explain the source profile and fields AquaSentinel actually detected.
7. Show severity/indicator results and recognized water/process metrics.
8. Explain whether the IsolationForest model ran and why.
9. Explain the `MONITOR` or `REVIEW` result.
10. Return to the launcher and choose **Option 2** to analyze the same file in the terminal, showing that both interfaces use the same analysis engine.

## 15. Likely viva questions

### Is AquaSentinel connected to a real plant?
No. The final project analyzes files supplied by the user. It does not connect to a PLC, SCADA server, dosing controller or utility.

### Why use files instead of a live SCADA connection?
It is safer for an educational project and more realistic for offline incident review. It also avoids pretending that classroom software has authorization to operate critical infrastructure.

### What happens if a file has no water-quality fields?
AquaSentinel still analyzes the log structure, severity and configured indicators. It does not invent water values.

### When does the AI model run?
Only when the loaded data has enough complete numeric records for local anomaly analysis.

### Why have both browser and terminal interfaces?
The browser is easier to present visually, while the terminal is useful for transparent technical inspection and repeatable command-line analysis.

### What makes the project DevSecOps?
Code quality, security scanning, tests, file-analysis checks, package validation and the real Windows launcher are automatically verified in CI.

## 16. Final explanation

AquaSentinel demonstrates a practical monitoring approach to smart water security: accept authorized evidence, normalize it, inspect log/security context, summarize process and water measurements when present, apply AI only when the dataset supports it, and present a clear result for a human analyst. The project remains local, defensive and read-only throughout.
