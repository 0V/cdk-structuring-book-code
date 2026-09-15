# 3-15-01 CloudFormation Guard のルール定義（security-rules.guard）のセットアップ / Windows PowerShell
# 何度実行しても同じ状態になる。
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
Set-Location -LiteralPath $ScriptDir
$Section = '3-15-01'

Write-Host "[$Section] ルールファイルを確認します"
if (-not (Test-Path -LiteralPath 'security-rules.guard' -PathType Leaf)) {
    Write-Host "[ERROR] ファイルがありません: security-rules.guard"
    exit 1
}
$lines = @(Get-Content -LiteralPath 'security-rules.guard').Count
Write-Host "[$Section] found: security-rules.guard ($lines lines)"

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

Write-Host "[$Section] ルールの構文を検査します"
$parseOut = Join-Path $env:TEMP 'cfn-guard-parse-tree.json'
$parseOk = $false
try {
    cfn-guard parse-tree --rules security-rules.guard --output $parseOut
    $parseOk = ($LASTEXITCODE -eq 0)
} catch {
    $parseOk = $false
}
if ($parseOk) {
    Write-Host "[$Section] security-rules.guard: 構文OK"
} else {
    Write-Host "[WARN] cfn-guard parse-tree で構文検査ができませんでした（cfn-guard のバージョンによりサブコマンドや引数が異なります）"
}

Write-Host "[$Section] セットアップが完了しました"
Write-Host "[$Section] 任意検証: cfn-guard validate --rules security-rules.guard --data <cdk synth で生成したテンプレート> --show-summary all"
