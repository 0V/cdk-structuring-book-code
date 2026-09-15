#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v python3.13 >/dev/null 2>&1; then
  echo "[ERROR] Python 3.13 is required" >&2
  exit 1
fi
if [ ! -x .venv/bin/python ]; then
  python3.13 -m venv .venv
fi
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements-dev.txt
./.venv/bin/black --check .
./.venv/bin/isort --check-only .
./.venv/bin/flake8 .
./.venv/bin/mypy .
./.venv/bin/python -m pytest
npm ci
PATH="$SCRIPT_DIR/.venv/bin:$PATH" npx cdk synth --quiet >/dev/null
echo "setup and validation passed: 3-14-01"
