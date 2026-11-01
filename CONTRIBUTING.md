# Contributing to ARAKNO-AI

Thank you for your interest in contributing to ARAKNO-AI (Advanced Research and Knowledge Architecture for Novel Organism-inspired Biomedical Research).

## Core Principles

Before submitting contributions, review these architectural requirements:

1. **Local-first & privacy**: ARAKNO-AI is designed to run locally. Never commit API keys, personal case data, or telemetry trackers.
2. **Zero-budget execution**: All core platform capabilities (literature retrieval, protein structures, FASTA analysis, evidence tracking) must function without paid API keys.
3. **Objective scientific evidence**: Research summaries and evidence claims must cite verifiable PMIDs or DOIs. Never fabricate citations or claim clinical efficacy.
4. **Clean, direct documentation (Unslop)**: Use sentence-case headings, avoid marketing buzzwords (*delve, pivotal, revolutionize*), and write plain, mechanism-oriented prose.

---

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ (LTS) & npm
- Git

### 1. Backend Setup

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Start the backend server:
```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 2. Frontend Setup

```powershell
cd frontend
npm install
npm run build
```

Start the Vite development server:
```powershell
npm run dev
```

---

## Submitting Pull Requests

1. Fork the repository and create your branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Ensure frontend builds cleanly and backend code compiles:
   ```bash
   python -m compileall backend/app
   npm --prefix frontend run build
   ```
3. Commit your changes with clear, descriptive commit messages:
   ```bash
   git commit -m "feat(proteins): add mmCIF coordinate residue parser"
   ```
4. Push to your fork and submit a Pull Request describing your changes, motivation, and test results.
