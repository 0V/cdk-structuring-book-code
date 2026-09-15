# 3-09-01 cdk-nagのインストールと基本設定（app.py）のセットアップ / Windows PowerShell
# 何度実行しても同じ状態になる。AWSへのデプロイは行わない。
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
Set-Location -LiteralPath $ScriptDir
$Section = '3-09-01'

Write-Host "[$Section] 前提コマンドを確認します"
$python = $null
foreach ($c in @('python', 'py', 'python3')) {
    if (Get-Command $c -ErrorAction SilentlyContinue) { $python = $c; break }
}
if (-not $python) {
    Write-Host "[ERROR] Python が見つかりません。Python 3.12 以上を導入してください"
    exit 1
}
& $python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)"
if ($LASTEXITCODE -ne 0) { throw '[ERROR] Python 3.12 or later is required' }
Write-Host "[$Section] python: $(& $python --version) ($python)"

if (Get-Command cdk -ErrorAction SilentlyContinue) {
    Write-Host "[$Section] cdk CLI を検出しました"
} else {
    Write-Host "[$Section] cdk CLI はありません（このセットアップには不要です。cdk synth を試す場合は npm install -g aws-cdk で導入してください）"
}

Write-Host "[$Section] 仮想環境 .venv を用意します"
$venvPython = Join-Path $ScriptDir '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $venvPython -PathType Leaf)) {
    & $python -m venv .venv
}

Write-Host "[$Section] pip を更新します"
& $venvPython -m pip install --upgrade pip

Write-Host "[$Section] requirements-dev.txt から依存を導入します（cdk-nag を含みます）"
& $venvPython -m pip install -r requirements-dev.txt

Write-Host "[$Section] cdk-nag が読み込めるか確認します"
& $venvPython -c "from cdk_nag import AwsSolutionsChecks; print('cdk-nag import: OK', AwsSolutionsChecks)"

Write-Host "[$Section] app.py の構文を確認します"
& $venvPython -m py_compile app.py
Write-Host "[$Section] app.py: 構文OK"

Write-Host "[$Section] セットアップが完了しました"
Write-Host "[$Section] app.py は原稿どおりの断片で、Stackの定義を含まないため cdk synth は実行できません"
