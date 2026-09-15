# 3-08-01 VS Code設定の統一 のセットアップ / Windows PowerShell
# 何度実行しても同じ結果になる。パッケージの導入はない（JSONの妥当性だけ確認する）。
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
Set-Location -LiteralPath $ScriptDir
$Section = '3-08-01'

Write-Host "[$Section] 前提コマンドを確認します"
Write-Host "[$Section] powershell: $($PSVersionTable.PSVersion.ToString())"

Write-Host "[$Section] 設定ファイルを検証します"
foreach ($f in @('.vscode/settings.json', '.vscode/extensions.json')) {
    if (-not (Test-Path -LiteralPath $f -PathType Leaf)) {
        Write-Host "[ERROR] ファイルがありません: $f"
        exit 1
    }
    $null = Get-Content -LiteralPath $f -Raw | ConvertFrom-Json
    Write-Host "[$Section] valid JSON: $f"
}

if (Get-Command code -ErrorAction SilentlyContinue) {
    Write-Host "[$Section] code コマンドを検出しました"
    Write-Host "[$Section] このディレクトリを 'code .' で開くと推奨拡張機能のインストールを促されます"
} else {
    Write-Host "[$Section] code コマンドはありません。VS Code本体の導入は手動で行ってください（設定ファイル自体はこのままで有効です）"
}

Write-Host "[$Section] セットアップが完了しました"
