#!/usr/bin/env bash
# 3-07-04 ツールの統合実行（Makefile / scripts/check.sh）のセットアップ / Linux, macOS
# 何度実行しても同じ状態になる。
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECTION="3-07-04"

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

if command -v make >/dev/null 2>&1; then
  echo "[$SECTION] make: $(make --version | head -1)"
else
  echo "[WARN] make が見つかりません。Makefile の代わりに scripts/check.sh を使ってください"
fi

echo "[$SECTION] 仮想環境 .venv を用意します"
if [ ! -x .venv/bin/python ]; then
  "$PYTHON" -m venv .venv
fi

echo "[$SECTION] pip を更新します"
./.venv/bin/python -m pip install --upgrade pip

echo "[$SECTION] requirements-dev.txt から依存を導入します"
./.venv/bin/python -m pip install -r requirements-dev.txt

echo "[$SECTION] scripts/check.sh に実行権限を付与します"
chmod +x scripts/check.sh

echo "[$SECTION] Makefile のターゲットを確認します"
grep -E '^[a-z-]+:' Makefile

echo "[$SECTION] セットアップが完了しました"
echo "[$SECTION] 実行例: PATH=\"\$PWD/.venv/bin:\$PATH\" make all"
echo "[$SECTION] 実行例: PATH=\"\$PWD/.venv/bin:\$PATH\" ./scripts/check.sh"
