# 3-09-02 cdk-nagのチェック結果と抑制（my_stack.py / stack_suppressions.py）のセットアップ / Windows PowerShell
# 何度実行しても同じ状態になる。AWSへのデプロイは行わない。
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
Set-Location -LiteralPath $ScriptDir
$Section = '3-09-02'

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

Write-Host "[$Section] 仮想環境 .venv を用意します"
$venvPython = Join-Path $ScriptDir '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $venvPython -PathType Leaf)) {
    & $python -m venv .venv
}

Write-Host "[$Section] pip を更新します"
& $venvPython -m pip install --upgrade pip

Write-Host "[$Section] requirements-dev.txt から依存を導入します（cdk-nag を含みます）"
& $venvPython -m pip install -r requirements-dev.txt

Write-Host "[$Section] NagSuppressions が読み込めるか確認します"
& $venvPython -c "from cdk_nag import NagSuppressions; print('cdk-nag import: OK', NagSuppressions)"

Write-Host "[$Section] 収録ファイルの構文を確認します"
foreach ($f in @('my_stack.py', 'stack_suppressions.py')) {
    & $venvPython -m py_compile $f
    Write-Host "[$Section] ${f}: 構文OK"
}

Write-Host "[$Section] セットアップが完了しました"
Write-Host "[$Section] my_stack.py と stack_suppressions.py は原稿どおりの断片です（vpc・Stack・Construct が未定義のため単独では実行できません）"
