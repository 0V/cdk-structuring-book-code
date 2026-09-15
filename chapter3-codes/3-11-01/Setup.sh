#!/usr/bin/env bash
# 3-11-01 Pre-commitフックの設定（.pre-commit-config.yaml）のセットアップ / Linux, macOS
# 何度実行しても同じ状態になる。
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECTION="3-11-01"

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
for cmd in git; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "[ERROR] 前提コマンドが見つかりません: $cmd" >&2
    exit 1
  fi
done
echo "[$SECTION] git: $(git --version)"

echo "[$SECTION] 仮想環境 .venv を用意します"
if [ ! -x .venv/bin/python ]; then
  "$PYTHON" -m venv .venv
fi

echo "[$SECTION] pip を更新します"
./.venv/bin/python -m pip install --upgrade pip

echo "[$SECTION] pre-commit を導入します（原稿: pip install pre-commit）"
./.venv/bin/python -m pip install pre-commit
echo "[$SECTION] pre-commit: $(./.venv/bin/pre-commit --version)"

echo "[$SECTION] .pre-commit-config.yaml を検証します"
./.venv/bin/pre-commit validate-config .pre-commit-config.yaml
echo "[$SECTION] .pre-commit-config.yaml: 妥当な設定です"

echo "[$SECTION] セットアップが完了しました"
echo "[$SECTION] pre-commit install はこのリポジトリ全体の .git/hooks を書き換えるため、このスクリプトでは実行しません"
echo "[$SECTION] 自分のプロジェクトで使う場合は、リポジトリ直下にこの設定を置いて pre-commit install を実行してください"
echo "[$SECTION] 任意検証: ./.venv/bin/pre-commit run --all-files（初回はフック環境の構築のため通信が発生します）"
