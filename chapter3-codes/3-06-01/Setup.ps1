# 3-06-01 venv（requirements.txt）のセットアップ / Windows PowerShell
# 何度実行しても同じ状態になる。
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
Set-Location -LiteralPath $ScriptDir
$Section = '3-06-01'

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

Write-Host "[$Section] requirements.txt から依存を導入します"
& $venvPython -m pip install -r requirements.txt

Write-Host "[$Section] 導入結果を確認します"
& $venvPython -m pip freeze

Write-Host "[$Section] 仮想環境のPythonを確認します"
& $venvPython -c "import sys; print(sys.executable)"

Write-Host "[$Section] セットアップが完了しました"
Write-Host "[$Section] 有効化: .\.venv\Scripts\Activate.ps1"
