# Contributing to ARAKNO-AI

Thank you for your interest in contributing to **ARAKNO-AI** (*Advanced Research and Knowledge Architecture for Novel Organism-inspired Biomedical Research*).

ARAKNO-AI is an open-source initiative uniting Artificial Intelligence, Computational Biology, Bioinspired Science, and Regenerative Medicine. We welcome contributions from developers, researchers, bioengineers, and students worldwide.

---

## Core Contribution Principles

All contributions must adhere to these foundational principles:

1. **Local-First & Strict Privacy:** ARAKNO-AI operates locally. Never commit API keys, personal credentials, patient data, or telemetry trackers.
2. **Zero-Budget Execution:** Core platform workflows (literature search, UniProt queries, AlphaFold structure discovery, FASTA alignment, report generation) must function at zero cost (`LLM_PROVIDER=none`) without requiring paid third-party API subscriptions.
3. **Traceable Scientific Evidence:** Research summaries, evidence claims, and dossiers must cite authentic, verifiable sources (PubMed PMIDs or DOIs). Never fabricate citations or make clinical efficacy claims.
4. **Responsible Scientific Disclaimer:** ARAKNO-AI is an exploratory research platform, not a certified clinical or diagnostic tool. Hypotheses must always be distinguished from experimentally confirmed findings.

---

## How You Can Contribute

We welcome diverse skill sets across multiple domains:

### 🤖 AI & Agent Developers
- Design and optimize **LangGraph** research workflow nodes.
- Implement robust local LLM support via Ollama (e.g. Llama 3, Mistral, BioMistral).
- Improve structured evidence extraction and automated citation verification nodes.
- Enhance deterministic fallback synthesis algorithms when LLMs are inactive.

### 🐍 Python & Backend Engineers
- Expand **FastAPI** REST endpoints in `backend/app/api/v1/`.
- Enhance SQLite full-text search (FTS5) queries and asynchronous SQLAlchemy repositories.
- Add rate-limiting, retry policies, and disk caching for external bioinformatics APIs.
- Build automated unit and integration tests.

### 🧬 Computational Biologists & Bioinformaticians
- Add molecular structure analysis algorithms (e.g., secondary structure assignment, mmCIF coordinate parsing).
- Expand **Biopython** workflows (Needleman-Wunsch / Smith-Waterman alignment, motif detection).
- Integrate additional public databases (e.g. PDB, Ensembl, STRING, ChEMBL, DisGeNET).
- Develop automated pLDDT confidence scoring and structural quality assessments.

### 🔬 Biomedical Researchers & Clinicians
- Curate research questions, literature benchmarks, and evidence criteria for the 6 research divisions:
  - **ARAKNO-SPINE:** Spinal fusion, pedicle screw biomechanics, implant removal criteria.
  - **ARAKNO-BONE:** Bone mineralization, osteogenesis, collagen scaffold integration.
  - **ARAKNO-MUSCLE:** Tendon repair, skeletal muscle regeneration, mechanobiology.
  - **ARAKNO-SENSE:** Slit sensilla mechanics, biological strain sensors, proprioception.
  - **ARAKNO-SILK:** Spidroin proteins, recombinant spider silk, biocompatible scaffolds.
  - **ARAKNO-NEURO:** Nerve guidance conduits, neuroplasticity, sensory-motor repair.
- Validate synthesized reports against primary literature to establish benchmark accuracy.

### 🎓 Students & Scientific Enthusiasts
- Create step-by-step tutorials and workflow walkthroughs.
- Identify and report documentation gaps, typos, or setup friction.
- Test installation scripts across different operating systems (Windows, Ubuntu, macOS).

---

## Development Setup

### Prerequisites
- **Python 3.11+** (Python 3.12 recommended)
- **Node.js 18+ (LTS)** & **npm**
- **Git**

### 1. Fork and Clone

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ARAKNO-AI.git
cd ARAKNO-AI

# Add upstream remote
git remote add upstream https://github.com/suryareddy1376/ARAKNO-AI.git
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Start backend server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Interactive API documentation will be available at **http://127.0.0.1:8000/docs**.

### 3. Frontend Setup

```bash
cd frontend

# Install Node dependencies
npm install

# Start Vite development server
npm run dev
```

The frontend will be available at **http://localhost:5173**.

---

## Verification Before Submitting

Before submitting changes, verify that your code adheres to project standards and compiles cleanly:

```bash
# 1. Verify backend Python compilation
python -m compileall backend/app

# 2. Verify frontend TypeScript compilation and production build
cd frontend
npm run build
cd ..

# 3. Check for unintended file modifications or committed secrets
git status
```

---

## Submitting Pull Requests

1. **Create a descriptive feature branch:**
   ```bash
   git checkout -b feat/add-mmcif-parser
   ```
2. **Follow conventional commit messages:**
   - `feat(biology): add mmCIF coordinate parser`
   - `fix(frontend): resolve print table header pagination`
   - `docs(readme): add Linux setup instructions`
   - `perf(db): optimize FTS5 full-text search query`
3. **Push to your fork and open a Pull Request:**
   - Clearly describe your changes and the scientific or software motivation.
   - Fill out the [Pull Request Checklist](.github/PULL_REQUEST_TEMPLATE.md).
   - Ensure that zero API keys, personal machine paths, or private case files are included.

---

## Code of Conduct

All contributors are expected to uphold the [Contributor Covenant v2.1](CODE_OF_CONDUCT.md). Please treat all community members with respect, collaboration, and constructive feedback.

Thank you for helping advance open-source biomedical research with ARAKNO-AI!
