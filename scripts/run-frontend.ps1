# ARAKNO-AI Frontend Startup Script

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$FrontendDir = Join-Path $ProjectRoot "frontend"

Write-Host ""
Write-Host "Starting ARAKNO-AI Frontend..." -ForegroundColor Cyan
Write-Host ""

# Check node_modules
if (-not (Test-Path (Join-Path $FrontendDir "node_modules"))) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
    Push-Location $FrontendDir
    npm install
    Pop-Location
}

Push-Location $FrontendDir

try {
    Write-Host "Frontend starting at http://localhost:5173" -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop." -ForegroundColor DarkGray
    Write-Host ""

    npm run dev
} finally {
    Pop-Location
}
