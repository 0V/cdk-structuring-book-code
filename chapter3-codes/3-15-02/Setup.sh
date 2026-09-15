#!/usr/bin/env bash
# 3-15-02 CloudFormation Guard とCDKの統合（scripts/policy-check.sh）のセットアップ / Linux, macOS
# 何度実行しても同じ状態になる。AWSへのデプロイは行わない。
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECTION="3-15-02"

echo "[$SECTION] 収録ファイルを確認します"
if [ ! -f scripts/policy-check.sh ]; then
  echo "[ERROR] ファイルがありません: scripts/policy-check.sh" >&2
  exit 1
fi

echo "[$SECTION] 前提コマンド bash を確認します"
if ! command -v bash >/dev/null 2>&1; then
  echo "[ERROR] 前提コマンドが見つかりません: bash" >&2
  exit 1
fi
echo "[$SECTION] bash: $(bash --version | head -1)"

echo "[$SECTION] scripts/policy-check.sh の構文を確認します"
bash -n scripts/policy-check.sh
echo "[$SECTION] scripts/policy-check.sh: 構文OK"

echo "[$SECTION] scripts/policy-check.sh に実行権限を付与します"
chmod +x scripts/policy-check.sh

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

if command -v cdk >/dev/null 2>&1; then
  echo "[$SECTION] cdk CLI: $(cdk --version)"
else
  echo "[$SECTION] cdk CLI はありません。policy-check.sh を実際に動かすには CDK プロジェクトと cdk CLI が必要です"
fi

echo "[$SECTION] セットアップが完了しました"
echo "[$SECTION] policy-check.sh は原稿どおりの断片で、CDKプロジェクトと organization-policies.guard を前提とします（3-15-01 のルールは security-rules.guard という名前です）"
