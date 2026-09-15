#!/usr/bin/env bash
# 3-05-03 CODEOWNERSファイルの活用 のセットアップ / Linux, macOS
# 何度実行しても同じ結果になる。導入するツールはない。
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECTION="3-05-03"

echo "[$SECTION] 前提コマンドを確認します"
for cmd in git; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "[ERROR] 前提コマンドが見つかりません: $cmd" >&2
    exit 1
  fi
done
echo "[$SECTION] git: $(git --version)"

echo "[$SECTION] 設定ファイルを確認します"
for f in CODEOWNERS; do
  if [ ! -f "$f" ]; then
    echo "[ERROR] ファイルがありません: $f" >&2
    exit 1
  fi
  echo "[$SECTION] found: $f ($(wc -l < "$f" | tr -d ' ') lines)"
done

echo "[$SECTION] CODEOWNERSはGitホスティングサービスがリポジトリ直下・.github・docsのいずれかで読み取ります"
echo "[$SECTION] 実際に使うときは対象リポジトリの該当位置へ配置し、@infra-team などを自分たちのチーム名に置き換えてください"
echo "[$SECTION] セットアップが完了しました"
