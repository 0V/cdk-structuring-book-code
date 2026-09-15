# 3-06-02 Poetry（pyproject.toml）のセットアップ / Windows PowerShell
# 何度実行しても同じ状態になる。
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
Set-Location -LiteralPath $ScriptDir
$Section = '3-06-02'

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

$poetry = $null
if (Get-Command poetry -ErrorAction SilentlyContinue) {
    $poetry = 'poetry'
    Write-Host "[$Section] 既存の poetry を使用します: $(poetry --version)"
} else {
    Write-Host "[$Section] Poetry をこのディレクトリの .venv に導入します（原稿: pip install poetry）"
    $venvPython = Join-Path $ScriptDir '.venv\Scripts\python.exe'
    if (-not (Test-Path -LiteralPath $venvPython -PathType Leaf)) {
        & $python -m venv .venv
    }
    & $venvPython -m pip install --upgrade pip
    & $venvPython -m pip install poetry
    $poetry = Join-Path $ScriptDir '.venv\Scripts\poetry.exe'
    Write-Host "[$Section] poetry: $(& $poetry --version)"
}

Write-Host "[$Section] pyproject.toml を検証します"
$checkOk = $false
try {
    & $poetry check
    $checkOk = ($LASTEXITCODE -eq 0)
} catch {
    $checkOk = $false
}
if ($checkOk) {
    Write-Host "[$Section] poetry check: OK"
} else {
    Write-Host "[WARN] poetry check が指摘を返しました。原稿の pyproject.toml をそのまま収録しているためです"
}

Write-Host "[$Section] セットアップが完了しました"
Write-Host "[$Section] 任意検証: poetry lock で依存解決、poetry install で導入（このサンプルは設定ファイルのみで、パッケージ本体を含みません）"
