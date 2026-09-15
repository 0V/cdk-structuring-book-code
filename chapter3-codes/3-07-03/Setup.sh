#!/usr/bin/env bash
# 3-07-03 設定ファイル（pyproject.toml / .flake8）のセットアップ / Linux, macOS
# 何度実行しても同じ状態になる。
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECTION="3-07-03"

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

echo "[$SECTION] 設定ファイルが読み込まれているか確認します"
./.venv/bin/black --version
./.venv/bin/flake8 --version
echo "[$SECTION] pyproject.toml の設定値:"
sed -n 's/^\([^[].*\)$/  \1/p' pyproject.toml
echo "[$SECTION] .flake8 の設定値:"
sed -n 's/^\([^[].*\)$/  \1/p' .flake8

echo "[$SECTION] セットアップが完了しました"
echo "[$SECTION] 任意検証: ./.venv/bin/flake8 . / ./.venv/bin/mypy . / ./.venv/bin/isort --check-only ."
