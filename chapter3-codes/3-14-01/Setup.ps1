Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

$Python = $null
foreach ($Candidate in @('py', 'python3.13', 'python')) {
    if (Get-Command $Candidate -ErrorAction SilentlyContinue) {
        $Version = if ($Candidate -eq 'py') { & $Candidate -3.13 --version } else { & $Candidate --version }
        if ($Version -match 'Python 3\.13\.') { $Python = $Candidate; break }
    }
}
if (-not $Python) { throw '[ERROR] Python 3.13 is required' }

$VenvPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $VenvPython)) {
    if ($Python -eq 'py') { & $Python -3.13 -m venv .venv } else { & $Python -m venv .venv }
}
& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install -r requirements-dev.txt
& $VenvPython -m black --check .
& $VenvPython -m isort --check-only .
& $VenvPython -m flake8 .
& $VenvPython -m mypy .
& $VenvPython -m pytest
npm ci
npx cdk synth --quiet | Out-Null
Write-Host 'setup and validation passed: 3-14-01'
