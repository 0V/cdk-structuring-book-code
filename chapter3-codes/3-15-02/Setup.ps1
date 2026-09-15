# 3-15-02 CloudFormation Guard とCDKの統合（scripts/policy-check.sh）のセットアップ / Windows PowerShell
# 何度実行しても同じ状態になる。AWSへのデプロイは行わない。
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
Set-Location -LiteralPath $ScriptDir
$Section = '3-15-02'

Write-Host "[$Section] 収録ファイルを確認します"
if (-not (Test-Path -LiteralPath 'scripts/policy-check.sh' -PathType Leaf)) {
    Write-Host "[ERROR] ファイルがありません: scripts/policy-check.sh"
    exit 1
}
$lines = @(Get-Content -LiteralPath 'scripts/policy-check.sh').Count
Write-Host "[$Section] found: scripts/policy-check.sh ($lines lines)"

Write-Host "[$Section] 前提コマンド cfn-guard を確認します"
if (-not (Get-Command cfn-guard -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] cfn-guard が見つかりません。公式の入手経路がOS・アーキテクチャ依存のため自動導入は行いません"
    Write-Host "[ERROR] 次のいずれかで導入してPATHに追加してください"
    Write-Host "[ERROR]   1. リリース配布物: https://github.com/aws-cloudformation/cloudformation-guard/releases"
    Write-Host "[ERROR]   2. Rust から: cargo install cfn-guard"
    Write-Host "[ERROR]   3. セットアップ手順: https://docs.aws.amazon.com/cfn-guard/latest/ug/setting-up.html"
    exit 1
}
Write-Host "[$Section] cfn-guard: $(cfn-guard --version)"

if (Get-Command bash -ErrorAction SilentlyContinue) {
    Write-Host "[$Section] bash を検出しました。scripts/policy-check.sh はこの bash から実行できます"
} else {
    Write-Host "[$Section] bash はありません。policy-check.sh は Git Bash か WSL から実行してください"
}

if (Get-Command cdk -ErrorAction SilentlyContinue) {
    Write-Host "[$Section] cdk CLI を検出しました"
} else {
    Write-Host "[$Section] cdk CLI はありません。policy-check.sh を実際に動かすには CDK プロジェクトと cdk CLI が必要です"
}

Write-Host "[$Section] セットアップが完了しました"
Write-Host "[$Section] policy-check.sh は原稿どおりの断片で、CDKプロジェクトと organization-policies.guard を前提とします（3-15-01 のルールは security-rules.guard という名前です）"
