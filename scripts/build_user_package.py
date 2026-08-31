from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PACKAGE_NAME = "AquaSentinel-v1.0.0rc1-Windows"
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

# Tests are intentionally included because AquaSentinel.bat verifies the
# distributed copy before launching. Assets are included so the examiner-facing
# README renders exactly as it does in the repository.
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
            "AQUASENTINEL AI - QUICK START\n"
            "=============================\n\n"
            "Windows:\n"
            "1. Extract this ZIP to a normal folder.\n"
            "2. Double-click AquaSentinel.bat.\n"
            "3. The launcher creates the environment, installs dependencies, runs checks, and starts the guided demo.\n\n"
            "Requirement: Python 3.10 or newer must be installed and available as 'py' or 'python'.\n\n"
            "SAFETY BOUNDARY\n"
            "This is a synthetic, defensive, read-only classroom simulation. It does not connect to or control real PLC, SCADA, dosing, water-treatment or public-health infrastructure.\n"
        )
        archive.writestr(f"{PACKAGE_NAME}/START_HERE.txt", quick_start)

    print(f"Built {OUTPUT}")


if __name__ == "__main__":
    main()
