#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"

"$PYTHON_BIN" -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
aquasentinel doctor

echo
echo "AquaSentinel installed successfully."
echo "Activate later with: source .venv/bin/activate"
echo "Start the exam dashboard with: aquasentinel live --scenario normal"
