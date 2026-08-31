#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -x ".venv/bin/python" ]]; then
  echo "AquaSentinel virtual environment not found. Run ./install.sh first."
  exit 1
fi

source .venv/bin/activate
clear || true
echo "Starting AquaSentinel AI guided Topic 133 exam demo..."
echo
aquasentinel exam-demo
