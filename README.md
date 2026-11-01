# ARAKNO-AI

**An Open-Source AI-Powered Biomedical Research Intelligence Initiative**  
*Advanced Research and Knowledge Architecture for Novel Organism-inspired Biomedical Research*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![Python: 3.11 | 3.12](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)]()
[![Node: 18+ LTS](https://img.shields.io/badge/Node.js-18%2B%20LTS-339933.svg?logo=node.js&logoColor=white)]()
[![Zero-Cost Ready](https://img.shields.io/badge/Zero--Cost-Ready%20(No%20Paid%20API)-green.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## Project Overview

ARAKNO-AI is an open-source initiative dedicated to exploring the intersection of Artificial Intelligence, Computational Biology, Biomedical Engineering, and Bioinspired Science.

Our primary aim is to develop an intelligent research ecosystem that accelerates scientific discovery through automated literature analysis, protein structure exploration, biological data analysis, evidence synthesis, and interdisciplinary collaboration.

---

## Main Research Mission

To investigate human biological systems and explore scientifically supported possibilities for tissue regeneration, advanced biomaterials, bone healing, spinal reconstruction, and long-term implant independence.

---

## Research Divisions

ARAKNO-AI organizes biomedical investigations into six specialized research domains:

- **ARAKNO-SPINE:** Spinal biomechanics, spinal fusion, implant integration, and hardware-removal research.
- **ARAKNO-BONE:** Bone biology, collagen synthesis, mineralization, and osteogenic regeneration.
- **ARAKNO-MUSCLE:** Skeletal muscle biology, tendon biomechanics, and musculoskeletal tissue repair.
- **ARAKNO-SENSE:** Mechanoreceptors, biological sensory systems, and bioinspired strain-sensing structures.
- **ARAKNO-SILK:** Spider silk proteins, spidroins, recombinant biomaterials, and regenerative scaffolds.
- **ARAKNO-NEURO:** Neural signalling, sensory-motor coordination, and peripheral nerve regeneration.

---

## User Interface & Screenshots

### 1. Research Lab Overview & Metrics
Real-time dashboard summarizing active biomedical projects, evidence strength distributions, saved literature records, 3D structures, and local system diagnostics.

![Research Lab Overview](docs/images/dashboard-overview.png)

### 2. Protein Structure Explorer & AlphaFold 3D Viewer
Interactive 3D molecular viewer with residue wireframes, pLDDT prediction confidence metrics, and UniProt biological annotation records.

![Protein Structure Explorer](docs/images/protein-structure-explorer.png)

### 3. Scientific Intelligence Dossier & Research Reports
Structured multi-section research dossiers with verified PubMed/Europe PMC citation audits, biological targets, traceable evidence synthesis matrices, and publication-ready print/PDF export.

![Research Reports Dossier](docs/images/research-reports-dossier.png)

---

## Technology and Research

ARAKNO-AI combines Agentic AI, LangGraph, Python, React, FastAPI, computational biology, and publicly accessible scientific resources including PubMed, Europe PMC, UniProt, and the AlphaFold Protein Structure Database.

### Technology Stack
| Layer | Technologies | Purpose |
|---|---|---|
| **Frontend** | React 18, TypeScript, Tailwind CSS, Vite, Recharts, 3Dmol.js | Responsive researcher UI, 3D molecular viewer, evidence charts |
| **Backend** | Python 3.11+, FastAPI, SQLAlchemy (Async), Pydantic v2 | High-performance async REST API, validation, local routing |
| **Database** | SQLite with FTS5 Full-Text Search | Zero-configuration local database, full-text literature index |
| **AI / Orchestration** | LangGraph, LangChain (Optional LLM support) | Deterministic staged research workflows, synthesis pipelines |
| **Biology & Bioinformatics** | Biopython, UniProt API, AlphaFold DB | Sequence alignment, FASTA parsing, PDB coordinate retrieval |
| **Scientific APIs** | PubMed (NCBI E-utilities), Europe PMC, AlphaFold, UniProt | Open-access biomedical publications and macromolecular databases |

### Core Capabilities
- 📚 **Literature Intelligence:** Search PubMed and Europe PMC; automatically save and organize publications with verified PMIDs and DOIs.
- 🧬 **Protein Explorer:** Query UniProt metadata and load predicted AlphaFold coordinates in an interactive in-browser 3D viewer.
- 🔬 **Computational Biology Lab:** FASTA parsing, sequence comparison, and pairwise alignment powered by Biopython.
- 📊 **Evidence Library:** Structured evidence claims classified into methodological quality categories (A through E).
- 🤖 **Agentic Research Workflows:** LangGraph-powered automated research pipelines with reproducible audit steps.
- 📝 **Verifiable Research Dossiers:** Structured reports featuring executive summaries, biological targets, evidence matrices, and bibliography.
- 🖨️ **Publication-Grade Print & PDF:** Dedicated print layout ensuring complete evidence matrices and citations print cleanly.
- 🔒 **Privacy-First & Local:** Runs completely on `127.0.0.1` with no external telemetry, no cloud dependencies, and zero data exfiltration.

---

## Architecture

```
┌────────────────────────────────────────────────────────┐
│                   BROWSER / CLIENT                     │
│   React 18 + TypeScript + Tailwind CSS + 3Dmol.js     │
└───────────────────────────┬────────────────────────────┘
                            │ HTTP / REST (localhost:5173)
                            ▼
┌────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND                      │
│                (localhost:8000/api/v1)                 │
│                                                        │
│  ┌──────────────────┐  ┌────────────────────────────┐  │
│  │ Routers & Schemas│  │ LangGraph Research Engine  │  │
│  └────────┬─────────┘  └─────────────┬──────────────┘  │
│           │                          │                 │
│  ┌────────▼─────────┐  ┌─────────────▼──────────────┐  │
│  │  SQLAlchemy Async│  │ Computational Biology Lab  │  │
│  │   Repositories   │  │   (Biopython + Parsers)    │  │
│  └────────┬─────────┘  └─────────────┬──────────────┘  │
└───────────┼──────────────────────────┼─────────────────┘
            │                          │
            ▼                          ▼
┌───────────────────────────┐  ┌─────────────────────────┐
│   LOCAL PERSISTENCE       │  │ PUBLIC SCIENTIFIC APIS  │
│   SQLite Database (FTS5)  │  │ - PubMed / Europe PMC   │
│   Cached PDB Structures   │  │ - UniProt REST API      │
│   Private Case Isolation  │  │ - AlphaFold Structure DB│
└───────────────────────────┘  └─────────────────────────┘
```

- **Frontend and backend are strictly decoupled.**
- **All scientific integrations route through the backend** to respect rate limits and enforce caching.
- **Zero paid keys required:** Out of the box, all core literature, protein, and computational features run at zero financial cost (`LLM_PROVIDER=none`).

---

## Quick Start

### Prerequisites
- **Python 3.11+** (Python 3.12 recommended)
- **Node.js 18+ LTS** & **npm**
- **Git**
- Compatible with **Windows 10/11**, **Ubuntu / Debian Linux**, and **macOS**.

### Option A: Automated Setup (Windows)

```powershell
# 1. Clone the repository
git clone https://github.com/suryareddy1376/ARAKNO-AI.git
cd ARAKNO-AI

# 2. Run the automated setup script
.\scripts\setup.ps1

# 3. Start both backend and frontend services
.\scripts\run-all.ps1
```

### Option B: Manual Cross-Platform Setup (Linux / macOS / Windows)

```bash
# 1. Clone the repository
git clone https://github.com/suryareddy1376/ARAKNO-AI.git
cd ARAKNO-AI

# 2. Configure environment
cp .env.example .env

# 3. Set up Python backend
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# 4. Initialize database
python3 -c "import sys; sys.path.insert(0, 'backend'); import asyncio; from app.db.database import init_db; asyncio.run(init_db())"

# 5. Set up React frontend
cd frontend
npm install
npm run build
cd ..
```

### Running the Services

```bash
# Terminal 1: Backend (http://127.0.0.1:8000)
cd backend
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Frontend (http://localhost:5173)
cd frontend
npm run dev
```

Visit **http://localhost:5173** in your browser.

To access interactive backend API documentation, visit **http://127.0.0.1:8000/docs** (Swagger UI) or **http://127.0.0.1:8000/redoc** (ReDoc).

---

## Configuration & Zero-Cost Privacy

ARAKNO-AI is configured via `.env` with secure, privacy-first defaults:

```ini
# Core LLM Mode: 'none' executes zero-cost deterministic synthesis without external paid APIs
LLM_PROVIDER=none

# Privacy & Security
ALLOW_PAID_REQUESTS=false
REMOTE_LLM_FREE_ONLY=true
ALLOW_REMOTE_MEDICAL_DATA=false

# NCBI / PubMed (Enter your email to comply with NCBI E-utilities guidelines)
NCBI_EMAIL=your-email@example.com
```

- **Local-Only Execution:** Services bind strictly to `127.0.0.1` and `localhost`.
- **Zero Data Exfiltration:** Patient notes and private records stored in `data/private_case/` are excluded from version control and never transmitted to external APIs.
- **Optional LLM Integration:** If desired, you may connect local LLMs via Ollama (`http://localhost:11434`) or external providers by configuring `.env`.

---

## Project Structure

```
ARAKNO-AI/
├── backend/
│   ├── app/
│   │   ├── agents/          # LangGraph research workflows and synthesis nodes
│   │   ├── api/v1/          # FastAPI routers (health, literature, proteins, biology, etc.)
│   │   ├── biology/         # Biopython alignment, FASTA parsing, PDB parsing
│   │   ├── core/            # Configuration, logging, security, and masking
│   │   ├── db/              # SQLAlchemy async models, repositories, and SQLite engine
│   │   ├── integrations/    # External clients (PubMed, Europe PMC, UniProt, AlphaFold)
│   │   ├── schemas/         # Pydantic v2 validation models
│   │   └── services/        # Business logic and research pipeline services
│   ├── pyproject.toml       # Build configuration
│   └── requirements.txt     # Python dependency specifications
├── frontend/
│   ├── src/
│   │   ├── components/      # Common UI, layout (Sidebar, Header), proteins, reports
│   │   ├── features/        # Pages (Dashboard, Divisions, Literature, Proteins, Reports)
│   │   ├── services/        # Axios API clients
│   │   ├── stores/          # Zustand state management
│   │   └── styles/          # Tailwind CSS and publication print stylesheet
│   ├── package.json         # Node.js dependencies
│   └── vite.config.ts       # Vite build configuration
├── data/                    # Persistent local storage (gitignored except .gitkeep)
│   ├── database/            # Local SQLite database (arakno.db)
│   ├── papers/              # Downloaded scientific publications
│   ├── structures/          # Cached AlphaFold PDB coordinate files
│   ├── reports/             # Generated Markdown research dossiers
│   └── private_case/        # Isolated private data storage
├── docs/                    # Technical documentation and guides
│   ├── images/              # Application screenshots and visual assets
│   ├── ARCHITECTURE.md      # Detailed system architecture
│   ├── API_REFERENCE.md     # Endpoint descriptions
│   └── SCIENTIFIC_METHOD.md # Evidence grading and attribution guidelines
├── scripts/                 # Windows PowerShell setup and launch utilities
├── .env.example             # Documented configuration template
├── CONTRIBUTING.md           # Contribution guidelines and developer onboarding
├── CODE_OF_CONDUCT.md      # Contributor Covenant v2.1
├── SECURITY.md              # Vulnerability disclosure policy
├── CITATION.cff             # Academic citation metadata
└── LICENSE                  # MIT License
```

---

## Open Collaboration & Contributing

We welcome contributions from AI developers, Python engineers, computational biologists, biomedical researchers, clinicians, biotechnology students, and scientific enthusiasts.

Whether you want to implement a new bioinformatics algorithm, add a data source, curate research questions for one of the six divisions, or improve documentation, please read our [**Contributing Guide**](CONTRIBUTING.md) and [**Code of Conduct**](CODE_OF_CONDUCT.md).

```bash
# Verify your local changes before submitting a PR
python -m compileall backend/app
npm --prefix frontend run build
```

---

## Scientific Limitations & Disclaimer

This software is an exploratory computational research platform. It is **not** a certified medical device, clinical diagnostic tool, or clinical decision support system.

- **Computational Hypotheses:** AI-generated syntheses and workflow outputs represent computational interpretations of literature, not experimentally established medical facts.
- **Structural Models:** AlphaFold protein structure predictions are computational models with variable confidence metrics (pLDDT); they do not substitute for experimental structures (X-ray crystallography, Cryo-EM, NMR).
- **Primary Source Verification:** All findings and claims should be cross-referenced with primary peer-reviewed scientific literature.
- **No Clinical Decisions:** No clinical decisions, diagnosis, or patient treatments should ever be formulated based on this software's output.

---

## Acknowledgements

PROJECT ARAKNO-AI builds upon open-access scientific infrastructure and open-source software:

- **[UniProt Consortium](https://www.uniprot.org/):** Universal Protein Resource for canonical sequence and biological annotation data.
- **[AlphaFold Protein Structure Database](https://alphafold.ebi.ac.uk/):** EMBL-EBI and DeepMind for open-access predicted 3D coordinate models.
- **[National Center for Biotechnology Information (NCBI)](https://pubmed.ncbi.nlm.nih.gov/):** PubMed and E-utilities for biomedical literature indexing.
- **[Europe PMC](https://europepmc.org/):** Comprehensive open-access life sciences publication repository.
- **[Biopython Project](https://biopython.org/):** Computational tools for biological sequence manipulation and FASTA processing.
- **[LangGraph & LangChain](https://github.com/langchain-ai/langgraph):** Flexible agentic workflow orchestration.
- **[3Dmol.js](https://3dmol.csb.pitt.edu/):** High-performance WebGL-based molecular graphics for in-browser macromolecular visualization.
- **[FastAPI](https://fastapi.tiangolo.com/) & [React](https://react.dev/):** Modern frameworks powering our backend and frontend layers.

---

## Citation

If you use ARAKNO-AI in your academic research, computational studies, or bioinspired engineering projects, please cite it using the metadata in [**`CITATION.cff`**](CITATION.cff).

---

## License

This project is open-source software licensed under the **[MIT License](LICENSE)**.
