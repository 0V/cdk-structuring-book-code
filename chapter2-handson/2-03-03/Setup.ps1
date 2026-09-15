Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$Python = $null
foreach ($Candidate in @('py', 'python3.12', 'python')) {
    if (Get-Command $Candidate -ErrorAction SilentlyContinue) {
        $Version = if ($Candidate -eq 'py') { & $Candidate -3.12 --version } else { & $Candidate --version }
        if ($Version -match 'Python 3\.12\.') { $Python = $Candidate; break }
    }
}
if (-not $Python) { throw '[ERROR] Python 3.12 is required' }
$VenvPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $VenvPython)) {
    if ($Python -eq 'py') { & $Python -3.12 -m venv .venv } else { & $Python -m venv .venv }
}
& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install -r requirements.txt -r requirements-dev.txt
& $VenvPython -m pytest
& $VenvPython app.py | Out-Null
Write-Host 'setup and validation passed: 2-03-03'
