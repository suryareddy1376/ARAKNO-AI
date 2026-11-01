# ARAKNO-AI Installation Guide

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Operating System | Windows 10 | Windows 11 |
| Python | 3.11 | 3.12+ |
| Node.js | 18 LTS | 22 LTS |
| npm | 9+ | 10+ |
| RAM | 4 GB | 8 GB+ |
| Disk Space | 2 GB | 5 GB+ |

## Step 1: Clone or Download

Place the ARAKNO-AI folder in your preferred location.

## Step 2: Run Setup

Open PowerShell and navigate to the project:

```powershell
cd path\to\ARAKNO-AI
.\scripts\setup.ps1
```

This script will:
1. Verify Python, Node.js, and npm are installed
2. Create data directories
3. Create `.env` from `.env.example`
4. Create Python virtual environment
5. Install backend dependencies
6. Install frontend dependencies
7. Initialize the SQLite database
8. Run validation checks

## Step 3: Configure Environment

Edit `.env` to customize your settings:

```ini
# Recommended: Set your email for PubMed access
NCBI_EMAIL=your.email@example.com

# Optional: Configure an LLM provider
LLM_PROVIDER=none  # Options: none, ollama, openrouter, gemini
```

> **Important**: The application works fully without an LLM. AI features enhance but are not required for core functionality.

## Step 4: Start the Application

```powershell
.\scripts\run-all.ps1
```

Or start services individually:

```powershell
# Terminal 1: Backend
.\scripts\run-backend.ps1

# Terminal 2: Frontend  
.\scripts\run-frontend.ps1
```

## Step 5: Verify

1. Open http://localhost:5173 in your browser
2. Check the dashboard for backend connectivity status
3. Try a PubMed search to verify API access

## Troubleshooting

See TROUBLESHOOTING.md for common issues and solutions.

## Manual Setup

If the setup script fails, follow these manual steps:

### Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

### Frontend

```powershell
cd frontend
npm install
cd ..
```

### Database

The database is created automatically on first backend startup.
