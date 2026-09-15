# 3-07-03 設定ファイル（pyproject.toml / .flake8）のセットアップ / Windows PowerShell
# 何度実行しても同じ状態になる。
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
Set-Location -LiteralPath $ScriptDir
$Section = '3-07-03'

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

Write-Host "[$Section] requirements-dev.txt から依存を導入します"
& $venvPython -m pip install -r requirements-dev.txt

Write-Host "[$Section] 設定ファイルが読み込まれているか確認します"
& $venvPython -m black --version
& $venvPython -m flake8 --version
Write-Host "[$Section] pyproject.toml の設定値:"
foreach ($line in Get-Content -LiteralPath 'pyproject.toml') {
    if ($line -and -not $line.StartsWith('[')) { Write-Host "  $line" }
}
Write-Host "[$Section] .flake8 の設定値:"
foreach ($line in Get-Content -LiteralPath '.flake8') {
    if ($line -and -not $line.StartsWith('[')) { Write-Host "  $line" }
}

Write-Host "[$Section] セットアップが完了しました"
Write-Host "[$Section] 任意検証: .\.venv\Scripts\python.exe -m flake8 . / -m mypy . / -m isort --check-only ."
