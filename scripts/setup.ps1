# ARAKNO-AI Setup Script for Windows
# Advanced Research and Knowledge Architecture for Novel Organism-inspired Biomedical Research

param(
    [switch]$SkipBackend,
    [switch]$SkipFrontend,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  ARAKNO-AI Setup Script" -ForegroundColor Cyan
Write-Host "  Biomedical Research Intelligence Platform" -ForegroundColor DarkCyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# --- Check Prerequisites ---
Write-Host "[1/8] Checking prerequisites..." -ForegroundColor Yellow

# Python
try {
    $pyVersion = python --version 2>&1
    Write-Host "  Python: $pyVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Python not found. Install Python 3.11+ from python.org" -ForegroundColor Red
    exit 1
}

# Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "  Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Node.js not found. Install from nodejs.org" -ForegroundColor Red
    exit 1
}

# npm
try {
    $npmVersion = npm --version 2>&1
    Write-Host "  npm: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: npm not found." -ForegroundColor Red
    exit 1
}

# --- Create Data Directories ---
Write-Host ""
Write-Host "[2/8] Creating data directories..." -ForegroundColor Yellow

$dataDirs = @(
    "data\database",
    "data\papers",
    "data\structures",
    "data\embeddings",
    "data\reports",
    "data\cache",
    "data\private_case"
)

foreach ($dir in $dataDirs) {
    $fullPath = Join-Path $ProjectRoot $dir
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor DarkGreen
    }
}
Write-Host "  Data directories ready." -ForegroundColor Green

# --- Create .env if not exists ---
Write-Host ""
Write-Host "[3/8] Checking environment configuration..." -ForegroundColor Yellow

$envFile = Join-Path $ProjectRoot ".env"
$envExample = Join-Path $ProjectRoot ".env.example"

if (-not (Test-Path $envFile)) {
    if (Test-Path $envExample) {
        Copy-Item $envExample $envFile
        Write-Host "  Created .env from .env.example" -ForegroundColor Green
        Write-Host "  IMPORTANT: Edit .env to configure your settings" -ForegroundColor Yellow
    } else {
        Write-Host "  WARNING: No .env.example found" -ForegroundColor Yellow
    }
} else {
    Write-Host "  .env already exists." -ForegroundColor Green
}

# --- Backend Setup ---
if (-not $SkipBackend) {
    Write-Host ""
    Write-Host "[4/8] Setting up Python backend..." -ForegroundColor Yellow

    $backendDir = Join-Path $ProjectRoot "backend"
    $venvDir = Join-Path $backendDir "venv"
    $venvPython = Join-Path $venvDir "Scripts\python.exe"
    $venvPip = Join-Path $venvDir "Scripts\pip.exe"

    # Create virtual environment
    if (-not (Test-Path $venvPython) -or $Force) {
        Write-Host "  Creating virtual environment..." -ForegroundColor DarkYellow
        Push-Location $backendDir
        python -m venv venv
        Pop-Location
        Write-Host "  Virtual environment created." -ForegroundColor Green
    } else {
        Write-Host "  Virtual environment exists." -ForegroundColor Green
    }

    # Upgrade pip
    Write-Host "  Upgrading pip..." -ForegroundColor DarkYellow
    & $venvPython -m pip install --upgrade pip --quiet 2>&1 | Out-Null

    # Install requirements
    $reqFile = Join-Path $backendDir "requirements.txt"
    if (Test-Path $reqFile) {
        Write-Host "  Installing backend dependencies..." -ForegroundColor DarkYellow
        & $venvPip install -r $reqFile 2>&1 | ForEach-Object {
            if ($_ -match "ERROR|error") { Write-Host "  $_" -ForegroundColor Red }
        }
        Write-Host "  Backend dependencies installed." -ForegroundColor Green
    } else {
        Write-Host "  WARNING: requirements.txt not found at $reqFile" -ForegroundColor Yellow
    }

    # Initialize database
    Write-Host ""
    Write-Host "[5/8] Initializing database..." -ForegroundColor Yellow
    Push-Location $ProjectRoot
    try {
        & $venvPython -c "
import sys
sys.path.insert(0, 'backend')
import asyncio
from app.db.database import init_db
asyncio.run(init_db())
print('Database initialized successfully.')
"
        Write-Host "  Database ready." -ForegroundColor Green
    } catch {
        Write-Host "  WARNING: Database initialization will happen on first run." -ForegroundColor Yellow
    }
    Pop-Location
} else {
    Write-Host ""
    Write-Host "[4/8] Skipping backend setup." -ForegroundColor DarkGray
    Write-Host "[5/8] Skipping database setup." -ForegroundColor DarkGray
}

# --- Frontend Setup ---
if (-not $SkipFrontend) {
    Write-Host ""
    Write-Host "[6/8] Setting up React frontend..." -ForegroundColor Yellow

    $frontendDir = Join-Path $ProjectRoot "frontend"

    if (Test-Path (Join-Path $frontendDir "package.json")) {
        Push-Location $frontendDir
        Write-Host "  Installing frontend dependencies..." -ForegroundColor DarkYellow
        npm install 2>&1 | ForEach-Object {
            if ($_ -match "ERR!|error") { Write-Host "  $_" -ForegroundColor Red }
        }
        Write-Host "  Frontend dependencies installed." -ForegroundColor Green
        Pop-Location
    } else {
        Write-Host "  WARNING: package.json not found. Frontend may not be initialized." -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "[6/8] Skipping frontend setup." -ForegroundColor DarkGray
}

# --- Validate Configuration ---
Write-Host ""
Write-Host "[7/8] Validating configuration..." -ForegroundColor Yellow

$checks = @(
    @{ Name = "Backend directory"; Path = Join-Path $ProjectRoot "backend\app\main.py" },
    @{ Name = "Frontend directory"; Path = Join-Path $ProjectRoot "frontend\package.json" },
    @{ Name = "Database directory"; Path = Join-Path $ProjectRoot "data\database" },
    @{ Name = "Environment file"; Path = $envFile }
)

$allGood = $true
foreach ($check in $checks) {
    if (Test-Path $check.Path) {
        Write-Host "  OK: $($check.Name)" -ForegroundColor Green
    } else {
        Write-Host "  MISSING: $($check.Name) ($($check.Path))" -ForegroundColor Red
        $allGood = $false
    }
}

# --- Health Check ---
Write-Host ""
Write-Host "[8/8] Setup complete!" -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  ARAKNO-AI Setup Complete" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the application:" -ForegroundColor White
Write-Host "  .\scripts\run-all.ps1" -ForegroundColor Green
Write-Host ""
Write-Host "Or start services individually:" -ForegroundColor White
Write-Host "  .\scripts\run-backend.ps1   (http://127.0.0.1:8000)" -ForegroundColor Green
Write-Host "  .\scripts\run-frontend.ps1  (http://localhost:5173)" -ForegroundColor Green
Write-Host ""
Write-Host "API Documentation:" -ForegroundColor White
Write-Host "  http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host ""

if (-not $allGood) {
    Write-Host "WARNING: Some components are missing. Check the output above." -ForegroundColor Yellow
}
