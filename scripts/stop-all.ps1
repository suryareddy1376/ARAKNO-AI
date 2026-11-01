# ARAKNO-AI - Stop All Services

$ErrorActionPreference = "Continue"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host ""
Write-Host "Stopping ARAKNO-AI services..." -ForegroundColor Yellow

$pidFile = Join-Path $ProjectRoot "data\.service_pids"

if (Test-Path $pidFile) {
    $content = Get-Content $pidFile
    foreach ($line in $content) {
        if ($line -match '=(\d+)$') {
            $pid = $matches[1]
            try {
                $proc = Get-Process -Id $pid -ErrorAction Stop
                Stop-Process -Id $pid -Force
                Write-Host "  Stopped process $pid ($($proc.ProcessName))" -ForegroundColor Green
            } catch {
                Write-Host "  Process $pid already stopped." -ForegroundColor DarkGray
            }
        }
    }
    Remove-Item $pidFile -Force
} else {
    Write-Host "  No PID file found. Attempting to stop by port..." -ForegroundColor Yellow

    # Stop anything on port 8000
    $backend = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
    if ($backend) {
        Stop-Process -Id $backend.OwningProcess -Force -ErrorAction SilentlyContinue
        Write-Host "  Stopped backend (port 8000)" -ForegroundColor Green
    }

    # Stop anything on port 5173
    $frontend = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue
    if ($frontend) {
        Stop-Process -Id $frontend.OwningProcess -Force -ErrorAction SilentlyContinue
        Write-Host "  Stopped frontend (port 5173)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "All ARAKNO-AI services stopped." -ForegroundColor Green
Write-Host ""
