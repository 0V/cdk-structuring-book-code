Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$ScriptDir = $PSScriptRoot
$Root = (Resolve-Path (Join-Path $ScriptDir '..\..')).Path
$Python = $null
foreach ($Candidate in @('python', 'py', 'python3')) {
    if (Get-Command $Candidate -ErrorAction SilentlyContinue) { $Python = $Candidate; break }
}
if (-not $Python) { throw '[ERROR] Python was not found' }
& $Python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)"
if ($LASTEXITCODE -ne 0) { throw '[ERROR] Python 3.12 or later is required' }
& $Python (Join-Path $Root 'scripts\verify_samples.py') --root $Root --section 4-06-02
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
