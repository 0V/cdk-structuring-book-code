#!/usr/bin/env bash
# 3-10-01 .gitignoreの設定 のセットアップ / Linux, macOS
# 何度実行しても同じ結果になる。導入するツールはない。
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECTION="3-10-01"

echo "[$SECTION] 前提コマンドを確認します"
for cmd in git; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "[ERROR] 前提コマンドが見つかりません: $cmd" >&2
    exit 1
  fi
done
echo "[$SECTION] git: $(git --version)"

echo "[$SECTION] 設定ファイルを確認します"
if [ ! -f .gitignore ]; then
  echo "[ERROR] ファイルがありません: .gitignore" >&2
  exit 1
fi
echo "[$SECTION] found: .gitignore ($(wc -l < .gitignore | tr -d ' ') lines)"

echo "[$SECTION] 除外パターンの効きを確認します（git check-ignore）"
for p in __pycache__/x.pyc app.pyc .venv/bin/python cdk.out/Stack.template.json .cdk.staging/asset .DS_Store; do
  if git check-ignore -q "$p"; then
    echo "[$SECTION] ignored: $p"
  else
    echo "[ERROR] 除外されていません: $p" >&2
    exit 1
  fi
done

echo "[$SECTION] セットアップが完了しました"
