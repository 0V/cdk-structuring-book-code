#!/usr/bin/env bash
# 3-06-02 Poetry（pyproject.toml）のセットアップ / Linux, macOS
# 何度実行しても同じ状態になる。
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECTION="3-06-02"

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

if command -v poetry >/dev/null 2>&1; then
  POETRY="poetry"
  echo "[$SECTION] 既存の poetry を使用します: $(poetry --version)"
else
  echo "[$SECTION] Poetry をこのディレクトリの .venv に導入します（原稿: pip install poetry）"
  if [ ! -x .venv/bin/python ]; then
    "$PYTHON" -m venv .venv
  fi
  ./.venv/bin/python -m pip install --upgrade pip
  ./.venv/bin/python -m pip install poetry
  POETRY="./.venv/bin/poetry"
  echo "[$SECTION] poetry: $("$POETRY" --version)"
fi

echo "[$SECTION] pyproject.toml を検証します"
if "$POETRY" check; then
  echo "[$SECTION] poetry check: OK"
else
  echo "[WARN] poetry check が指摘を返しました。原稿の pyproject.toml をそのまま収録しているためです"
fi

echo "[$SECTION] セットアップが完了しました"
echo "[$SECTION] 任意検証: $POETRY lock で依存解決、$POETRY install で導入（このサンプルは設定ファイルのみで、パッケージ本体を含みません）"
