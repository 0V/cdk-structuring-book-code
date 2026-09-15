#!/usr/bin/env bash
# 3-07-02 各ツールの実行例（sample_code.py / type_error_sample.py）のセットアップ / Linux, macOS
# 何度実行しても同じ状態になる。
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECTION="3-07-02"

echo "[$SECTION] 前提コマンドを確認します"
PYTHON=""
for c in python3.12 python3 python; do
  if command -v "$c" >/dev/null 2>&1; then PYTHON="$c"; break; fi
done
if [ -z "$PYTHON" ]; then
  echo "[ERROR] Python が見つかりません。Python 3.12 以上を導入してください" >&2
  exit 1
fi
if ! "$PYTHON" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)'; then
  echo "[ERROR] Python 3.12 or later is required" >&2
  exit 1
fi
echo "[$SECTION] python: $("$PYTHON" --version 2>&1) ($PYTHON)"

echo "[$SECTION] 仮想環境 .venv を用意します"
if [ ! -x .venv/bin/python ]; then
  "$PYTHON" -m venv .venv
fi

echo "[$SECTION] pip を更新します"
./.venv/bin/python -m pip install --upgrade pip

echo "[$SECTION] requirements-dev.txt から依存を導入します"
./.venv/bin/python -m pip install -r requirements-dev.txt

echo "[$SECTION] インストール確認（原稿の各ツールのバージョン確認に相当）"
./.venv/bin/black --version
./.venv/bin/flake8 --version
./.venv/bin/mypy --version
./.venv/bin/isort --version

echo "[$SECTION] セットアップが完了しました"
echo "[$SECTION] sample_code.py と type_error_sample.py は意図的に問題を含むコードです（各ツールが指摘を出すのが正しい状態です）"
echo "[$SECTION] 任意検証: ./.venv/bin/black --check sample_code.py / ./.venv/bin/isort --check-only sample_code.py"
echo "[$SECTION] 任意検証: ./.venv/bin/flake8 sample_code.py / ./.venv/bin/mypy type_error_sample.py"
