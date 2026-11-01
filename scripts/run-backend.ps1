# ARAKNO-AI Backend Startup Script

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$BackendDir = Join-Path $ProjectRoot "backend"
$VenvPython = Join-Path $BackendDir "venv\Scripts\python.exe"

Write-Host ""
Write-Host "Starting ARAKNO-AI Backend..." -ForegroundColor Cyan
Write-Host ""

# Check venv
if (-not (Test-Path $VenvPython)) {
    Write-Host "ERROR: Virtual environment not found. Run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Set working directory
Push-Location $ProjectRoot

# Set environment
$env:PYTHONPATH = $BackendDir

try {
    Write-Host "Backend starting at http://127.0.0.1:8000" -ForegroundColor Green
    Write-Host "API docs at http://127.0.0.1:8000/docs" -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop." -ForegroundColor DarkGray
    Write-Host ""

    & $VenvPython -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --app-dir $BackendDir
} finally {
    Pop-Location
}
