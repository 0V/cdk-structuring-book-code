#!/usr/bin/env bash
# 3-06-01 venv（requirements.txt）のセットアップ / Linux, macOS
# 何度実行しても同じ状態になる。
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECTION="3-06-01"

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

echo "[$SECTION] requirements.txt から依存を導入します"
./.venv/bin/python -m pip install -r requirements.txt

echo "[$SECTION] 導入結果を確認します"
./.venv/bin/python -m pip freeze

echo "[$SECTION] 仮想環境のPythonを確認します（原稿の which python に相当）"
./.venv/bin/python -c "import sys; print(sys.executable)"

echo "[$SECTION] セットアップが完了しました"
echo "[$SECTION] 有効化: source .venv/bin/activate"
