# ARAKNO-AI - Start All Services

$ErrorActionPreference = "Continue"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  ARAKNO-AI - Starting All Services" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Start Backend in background
Write-Host "Starting backend server..." -ForegroundColor Yellow
$backendScript = Join-Path $PSScriptRoot "run-backend.ps1"
$backendJob = Start-Process powershell -ArgumentList "-NoExit", "-File", $backendScript -PassThru -WindowStyle Normal

Start-Sleep -Seconds 3

# Start Frontend in background
Write-Host "Starting frontend dev server..." -ForegroundColor Yellow
$frontendScript = Join-Path $PSScriptRoot "run-frontend.ps1"
$frontendJob = Start-Process powershell -ArgumentList "-NoExit", "-File", $frontendScript -PassThru -WindowStyle Normal

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  ARAKNO-AI Services Started" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Backend:  http://127.0.0.1:8000" -ForegroundColor White
Write-Host "  API Docs: http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "  Frontend: http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "  Backend PID:  $($backendJob.Id)" -ForegroundColor DarkGray
Write-Host "  Frontend PID: $($frontendJob.Id)" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  To stop all services: .\scripts\stop-all.ps1" -ForegroundColor Yellow
Write-Host ""

# Save PIDs for stop script
$pidFile = Join-Path $ProjectRoot "data\.service_pids"
@"
BACKEND_PID=$($backendJob.Id)
FRONTEND_PID=$($frontendJob.Id)
"@ | Set-Content $pidFile

# Wait for health check
Write-Host "Checking backend health..." -ForegroundColor Yellow
$maxRetries = 10
$retryCount = 0
$healthy = $false

while ($retryCount -lt $maxRetries -and -not $healthy) {
    Start-Sleep -Seconds 2
    try {
        $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/health" -TimeoutSec 5 -ErrorAction Stop
        if ($response.status -eq "healthy") {
            $healthy = $true
            Write-Host "  Backend is healthy!" -ForegroundColor Green
        }
    } catch {
        $retryCount++
        Write-Host "  Waiting for backend... ($retryCount/$maxRetries)" -ForegroundColor DarkYellow
    }
}

if (-not $healthy) {
    Write-Host "  WARNING: Backend health check failed. It may still be starting." -ForegroundColor Yellow
}
