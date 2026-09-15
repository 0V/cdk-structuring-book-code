# 3-05-03 CODEOWNERSファイルの活用 のセットアップ / Windows PowerShell
# 何度実行しても同じ結果になる。導入するツールはない。
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
Set-Location -LiteralPath $ScriptDir
$Section = '3-05-03'

Write-Host "[$Section] 前提コマンドを確認します"
foreach ($cmd in @('git')) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Host "[ERROR] 前提コマンドが見つかりません: $cmd"
        exit 1
    }
}
Write-Host "[$Section] git: $(git --version)"

Write-Host "[$Section] 設定ファイルを確認します"
foreach ($f in @('CODEOWNERS')) {
    if (-not (Test-Path -LiteralPath $f -PathType Leaf)) {
        Write-Host "[ERROR] ファイルがありません: $f"
        exit 1
    }
    $lines = @(Get-Content -LiteralPath $f).Count
    Write-Host "[$Section] found: $f ($lines lines)"
}

Write-Host "[$Section] CODEOWNERSはGitホスティングサービスがリポジトリ直下・.github・docsのいずれかで読み取ります"
Write-Host "[$Section] 実際に使うときは対象リポジトリの該当位置へ配置し、@infra-team などを自分たちのチーム名に置き換えてください"
Write-Host "[$Section] セットアップが完了しました"
