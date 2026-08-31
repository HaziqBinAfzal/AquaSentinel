from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PACKAGE_NAME = "AquaSentinel-v1.0.0-Windows"
OUTPUT = DIST / f"{PACKAGE_NAME}.zip"

ROOT_FILES = [
    "AquaSentinel.bat",
    "README.md",
    "pyproject.toml",
    "requirements.txt",
    "install.bat",
    "install.sh",
    "run_exam_demo.bat",
    "run_exam_demo.sh",
    "CHANGELOG.md",
]

# Tests are included because AquaSentinel.bat verifies the distributed copy
# before opening either interface. Documentation is kept with the package so
# the examiner can inspect the design without a separate download.
INCLUDE_DIRS = ["aquasentinel", "tests", "docs", "assets"]
EXCLUDED_PARTS = {"__pycache__", ".pytest_cache", ".ruff_cache", ".venv", "audit", "reports", "dist"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def allowed(path: Path) -> bool:
    if any(part in EXCLUDED_PARTS for part in path.parts):
        return False
    if path.suffix in EXCLUDED_SUFFIXES:
        return False
    return path.is_file()


def add_file(archive: ZipFile, source: Path) -> None:
    relative = source.relative_to(ROOT)
    archive.write(source, Path(PACKAGE_NAME) / relative)


def main() -> None:
    DIST.mkdir(exist_ok=True)
    if OUTPUT.exists():
        OUTPUT.unlink()

    with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as archive:
        for name in ROOT_FILES:
            path = ROOT / name
            if path.exists() and allowed(path):
                add_file(archive, path)

        for directory in INCLUDE_DIRS:
            base = ROOT / directory
            if not base.exists():
                continue
            for path in sorted(base.rglob("*")):
                if allowed(path):
                    add_file(archive, path)

        quick_start = (
            "AQUASENTINEL AI v1.0.0 - QUICK START\n"
            "====================================\n\n"
            "1. Extract this ZIP to a normal folder.\n"
            "2. Double-click AquaSentinel.bat.\n"
            "3. After verification choose one interface:\n"
            "   [1] Browser - choose a local file in the localhost page.\n"
            "   [2] Terminal - paste the path of a local file.\n\n"
            "Supported input: .log, .txt, .csv, .json and .jsonl (up to 8 MB).\n"
            "No dataset or incident demo is preloaded. AquaSentinel analyzes the file you provide.\n\n"
            "Requirement: Python 3.10 or newer must be available as 'py' or 'python'.\n\n"
            "SAFETY BOUNDARY\n"
            "AquaSentinel is a local defensive analysis project. It does not connect to or control real PLC, SCADA, dosing, water-treatment or public-health infrastructure.\n"
        )
        archive.writestr(f"{PACKAGE_NAME}/START_HERE.txt", quick_start)

    print(f"Built {OUTPUT}")


if __name__ == "__main__":
    main()
