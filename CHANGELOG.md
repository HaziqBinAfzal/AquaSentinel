# Changelog

## 1.0.0

AquaSentinel AI v1.0.0 is a local defensive analysis workstation for Topic 133.

### Final workflow

- Replaced the preloaded scenario-first experience with **user-supplied file analysis**.
- Added support for `.log`, `.txt`, `.csv`, `.json` and `.jsonl` input up to 8 MB.
- Added a Windows startup menu with two interfaces:
  - browser analysis on `http://127.0.0.1:8765/`;
  - terminal file analysis.
- Reworked the localhost page into a restrained engineering/workstation layout with neutral colors, conventional tables and factual labels.
- Browser starts with **No dataset loaded** and analyzes only after the user selects a file.
- Added source profiling, severity classification, discovered-field display, water/process metric summaries, defensive indicator counts, review flags and recent-record inspection.
- Added local IsolationForest anomaly detection when the supplied dataset contains enough complete numeric records.
- Added explicit `NOT RUN` behavior when a file does not contain enough data for ML analysis.
- Added `aquasentinel analyze <file>` for terminal analysis of the same input engine used by the browser.
- Removed automatic incident/demo startup from the final launcher and CLI flow.
- Excluded the legacy exam-demo helper and demo guide from the Windows user distribution.
- Kept the localhost service bound to `127.0.0.1` with no PLC/SCADA/control write endpoint.
- Added defensive browser headers and in-memory file analysis.
- Updated Linux CI to test real supplied-file analysis plus browser/file self-checks.
- Kept the dedicated `windows-latest` job running `AquaSentinel.bat --check-only`.
- Updated README, project/viva guide and `START_HERE.txt` for the file-driven workflow.

### Safety boundary

AquaSentinel reads files supplied by the user and produces local defensive analysis. It does not connect to, control, write to or modify real water utilities, desalination plants, PLCs, SCADA systems, dosing controllers or public-health infrastructure. Water-quality review bands are illustrative classroom bands and are not operational or regulatory limits.
