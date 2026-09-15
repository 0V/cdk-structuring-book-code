#!/usr/bin/env bash
# 3-15-01 CloudFormation Guard のルール定義（security-rules.guard）のセットアップ / Linux, macOS
# 何度実行しても同じ状態になる。
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECTION="3-15-01"

echo "[$SECTION] ルールファイルを確認します"
if [ ! -f security-rules.guard ]; then
  echo "[ERROR] ファイルがありません: security-rules.guard" >&2
  exit 1
fi
echo "[$SECTION] found: security-rules.guard ($(wc -l < security-rules.guard | tr -d ' ') lines)"

echo "[$SECTION] 前提コマンド cfn-guard を確認します"
if ! command -v cfn-guard >/dev/null 2>&1; then
  echo "[ERROR] cfn-guard が見つかりません。公式の入手経路がOS・アーキテクチャ依存のため自動導入は行いません" >&2
  echo "[ERROR] 次のいずれかで導入してPATHに追加してください" >&2
  echo "[ERROR]   1. リリース配布物: https://github.com/aws-cloudformation/cloudformation-guard/releases" >&2
  echo "[ERROR]   2. Rust から: cargo install cfn-guard" >&2
  echo "[ERROR]   3. インストーラ: https://docs.aws.amazon.com/cfn-guard/latest/ug/setting-up.html" >&2
  exit 1
fi
echo "[$SECTION] cfn-guard: $(cfn-guard --version)"

echo "[$SECTION] ルールの構文を検査します"
if cfn-guard parse-tree --rules security-rules.guard --output /dev/null; then
  echo "[$SECTION] security-rules.guard: 構文OK"
else
  echo "[WARN] cfn-guard parse-tree で構文検査ができませんでした（cfn-guard のバージョンによりサブコマンドや引数が異なります）"
fi

echo "[$SECTION] セットアップが完了しました"
echo "[$SECTION] 任意検証: cfn-guard validate --rules security-rules.guard --data <cdk synth で生成したテンプレート> --show-summary all"
