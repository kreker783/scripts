
$Root = $PSScriptRoot
$Python = Join-Path $Root "runtime\python\python.exe"
$Main = Join-Path $Root "start.py"

if (!(Test-Path $Python)) {
    Write-Host "Python runtime missing!" -ForegroundColor Red
    exit 1
}

& $Python $Main
