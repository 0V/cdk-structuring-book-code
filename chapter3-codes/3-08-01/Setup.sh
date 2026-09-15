#!/usr/bin/env bash
# 3-08-01 VS Code設定の統一 のセットアップ / Linux, macOS
# 何度実行しても同じ結果になる。パッケージの導入はない（JSONの妥当性だけ確認する）。
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECTION="3-08-01"

echo "[$SECTION] 前提コマンドを確認します"
PYTHON=""
for c in python3.12 python3 python; do
  if command -v "$c" >/dev/null 2>&1; then PYTHON="$c"; break; fi
done
if [ -z "$PYTHON" ]; then
  echo "[ERROR] Python が見つかりません（JSONの検証に使用します）" >&2
  exit 1
fi
if ! "$PYTHON" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)'; then
  echo "[ERROR] Python 3.12 or later is required" >&2
  exit 1
fi
echo "[$SECTION] python: $("$PYTHON" --version 2>&1) ($PYTHON)"

echo "[$SECTION] 設定ファイルを検証します"
for f in .vscode/settings.json .vscode/extensions.json; do
  if [ ! -f "$f" ]; then
    echo "[ERROR] ファイルがありません: $f" >&2
    exit 1
  fi
  "$PYTHON" -c "import json,sys; json.load(open(sys.argv[1], encoding='utf-8'))" "$f"
  echo "[$SECTION] valid JSON: $f"
done

if command -v code >/dev/null 2>&1; then
  echo "[$SECTION] code コマンドを検出しました: $(code --version | head -1)"
  echo "[$SECTION] このディレクトリを 'code .' で開くと推奨拡張機能のインストールを促されます"
else
  echo "[$SECTION] code コマンドはありません。VS Code本体の導入は手動で行ってください（設定ファイル自体はこのままで有効です）"
fi

echo "[$SECTION] セットアップが完了しました"
