# 3-10-01 .gitignoreの設定 のセットアップ / Windows PowerShell
# 何度実行しても同じ結果になる。導入するツールはない。
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
Set-Location -LiteralPath $ScriptDir
$Section = '3-10-01'

Write-Host "[$Section] 前提コマンドを確認します"
foreach ($cmd in @('git')) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Host "[ERROR] 前提コマンドが見つかりません: $cmd"
        exit 1
    }
}
Write-Host "[$Section] git: $(git --version)"

Write-Host "[$Section] 設定ファイルを確認します"
if (-not (Test-Path -LiteralPath '.gitignore' -PathType Leaf)) {
    Write-Host "[ERROR] ファイルがありません: .gitignore"
    exit 1
}
$lines = @(Get-Content -LiteralPath '.gitignore').Count
Write-Host "[$Section] found: .gitignore ($lines lines)"

Write-Host "[$Section] 除外パターンの効きを確認します（git check-ignore）"
foreach ($p in @('__pycache__/x.pyc', 'app.pyc', '.venv/bin/python', 'cdk.out/Stack.template.json', '.cdk.staging/asset', '.DS_Store')) {
    git check-ignore -q $p
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[$Section] ignored: $p"
    } else {
        Write-Host "[ERROR] 除外されていません: $p"
        exit 1
    }
}

Write-Host "[$Section] セットアップが完了しました"
