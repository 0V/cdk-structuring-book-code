#!/usr/bin/env bash
# 3-09-02 cdk-nagのチェック結果と抑制（my_stack.py / stack_suppressions.py）のセットアップ / Linux, macOS
# 何度実行しても同じ状態になる。AWSへのデプロイは行わない。
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECTION="3-09-02"

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

echo "[$SECTION] requirements-dev.txt から依存を導入します（cdk-nag を含みます）"
./.venv/bin/python -m pip install -r requirements-dev.txt

echo "[$SECTION] NagSuppressions が読み込めるか確認します"
./.venv/bin/python -c "from cdk_nag import NagSuppressions; print('cdk-nag import: OK', NagSuppressions)"

echo "[$SECTION] 収録ファイルの構文を確認します"
for f in my_stack.py stack_suppressions.py; do
  ./.venv/bin/python -m py_compile "$f"
  echo "[$SECTION] $f: 構文OK"
done

echo "[$SECTION] セットアップが完了しました"
echo "[$SECTION] my_stack.py と stack_suppressions.py は原稿どおりの断片です（vpc・Stack・Construct が未定義のため単独では実行できません）"
