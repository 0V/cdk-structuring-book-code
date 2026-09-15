# 3-11-01 Pre-commitフックの設定（.pre-commit-config.yaml）のセットアップ / Windows PowerShell
# 何度実行しても同じ状態になる。
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
Set-Location -LiteralPath $ScriptDir
$Section = '3-11-01'

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
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] 前提コマンドが見つかりません: git"
    exit 1
}
Write-Host "[$Section] git: $(git --version)"

Write-Host "[$Section] 仮想環境 .venv を用意します"
$venvPython = Join-Path $ScriptDir '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $venvPython -PathType Leaf)) {
    & $python -m venv .venv
}

Write-Host "[$Section] pip を更新します"
& $venvPython -m pip install --upgrade pip

Write-Host "[$Section] pre-commit を導入します（原稿: pip install pre-commit）"
& $venvPython -m pip install pre-commit
Write-Host "[$Section] pre-commit: $(& $venvPython -m pre_commit --version)"

Write-Host "[$Section] .pre-commit-config.yaml を検証します"
& $venvPython -m pre_commit validate-config .pre-commit-config.yaml
Write-Host "[$Section] .pre-commit-config.yaml: 妥当な設定です"

Write-Host "[$Section] セットアップが完了しました"
Write-Host "[$Section] pre-commit install はこのリポジトリ全体の .git/hooks を書き換えるため、このスクリプトでは実行しません"
Write-Host "[$Section] 自分のプロジェクトで使う場合は、リポジトリ直下にこの設定を置いて pre-commit install を実行してください"
