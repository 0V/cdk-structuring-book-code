#!/usr/bin/env bash
# 3-06-03 依存関係の固定（requirements.txt / requirements-dev.txt）のセットアップ / Linux, macOS
# 何度実行しても同じ状態になる。
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECTION="3-06-03"

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

echo "[$SECTION] requirements-dev.txt から依存を導入します（-r requirements.txt で本番用も含まれます）"
./.venv/bin/python -m pip install -r requirements-dev.txt

echo "[$SECTION] 導入したバージョンを固定します（原稿: pip freeze > requirements-lock.txt）"
./.venv/bin/python -m pip freeze > requirements-lock.txt
echo "[$SECTION] requirements-lock.txt を出力しました（$(wc -l < requirements-lock.txt | tr -d ' ') lines）"

echo "[$SECTION] セットアップが完了しました"
echo "[$SECTION] 有効化: source .venv/bin/activate"
