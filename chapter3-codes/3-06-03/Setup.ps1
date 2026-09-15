# 3-06-03 依存関係の固定（requirements.txt / requirements-dev.txt）のセットアップ / Windows PowerShell
# 何度実行しても同じ状態になる。
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
Set-Location -LiteralPath $ScriptDir
$Section = '3-06-03'

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

Write-Host "[$Section] requirements-dev.txt から依存を導入します（-r requirements.txt で本番用も含まれます）"
& $venvPython -m pip install -r requirements-dev.txt

Write-Host "[$Section] 導入したバージョンを固定します（原稿: pip freeze > requirements-lock.txt）"
& $venvPython -m pip freeze | Set-Content -LiteralPath 'requirements-lock.txt' -Encoding utf8
$lines = @(Get-Content -LiteralPath 'requirements-lock.txt').Count
Write-Host "[$Section] requirements-lock.txt を出力しました（$lines lines）"

Write-Host "[$Section] セットアップが完了しました"
Write-Host "[$Section] 有効化: .\.venv\Scripts\Activate.ps1"
