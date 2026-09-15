#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
if ! command -v python3.12 >/dev/null 2>&1; then
  echo "[ERROR] Python 3.12 is required" >&2
  exit 1
fi
if [ ! -x .venv/bin/python ]; then python3.12 -m venv .venv; fi
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements.txt -r requirements-dev.txt
./.venv/bin/python -m pytest
./.venv/bin/python app.py >/dev/null
echo "setup and validation passed: 2-03-04"
