# ARAKNO-AI

## Advanced Research and Knowledge Architecture for Novel Organism-inspired Biomedical Research

![Status](https://img.shields.io/badge/status-active-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)
![Node](https://img.shields.io/badge/node-18%2B%20LTS-green)

ARAKNO-AI is an AI-powered biomedical research intelligence platform designed for investigating human biological systems, spinal biomechanics, bone regeneration, tissue engineering, biomaterials, protein structures, muscle biology, sensory systems, and spider-inspired biological materials.

> **Important**: This platform is intended for scientific literature exploration and computational research, not diagnosis, treatment planning, or medical decision-making.

---

## Features

### Research Divisions
- **ARAKNO-SPINE** — Spinal anatomy, biomechanics, fusion biology, instrumentation
- **ARAKNO-BONE** — Bone biology, regeneration, tissue engineering
- **ARAKNO-MUSCLE** — Skeletal muscle, tendons, connective tissues
- **ARAKNO-SENSE** — Mechanoreceptors, sensory biology, spider sensilla
- **ARAKNO-SILK** — Spider silk proteins, biomaterials, scaffolds
- **ARAKNO-NEURO** — Neural signalling, regeneration, neuroplasticity

### Core Capabilities
- 📚 **Literature Intelligence** — Search PubMed and Europe PMC, save and organize publications
- 🧬 **Protein Explorer** — UniProt metadata + AlphaFold structure predictions with 3D viewer
- 🔬 **Computational Biology** — FASTA analysis, sequence alignment, structure parsing
- 📊 **Evidence Library** — Structured evidence records with quality categorization
- 🤖 **AI Research Workflows** — LangGraph-powered research automation
- 📝 **Research Reports** — Generated, traceable scientific reports
- 🔒 **Privacy-First** — Local-only, no cloud dependencies, no data exfiltration

### Technology Stack
| Layer | Technologies |
|-------|-------------|
| Frontend | React, TypeScript, Tailwind CSS, Vite, Recharts, 3Dmol.js |
| Backend | Python, FastAPI, SQLAlchemy, Pydantic |
| Database | SQLite with FTS5 |
| AI | LangGraph, LangChain (optional LLM) |
| Biology | Biopython |
| APIs | PubMed, Europe PMC, AlphaFold DB, UniProt |

---

## Quick Start

### Prerequisites
- Python 3.11+ 
- Node.js 18+ LTS
- npm
- Windows 10/11

### Installation

```powershell
cd ARAKNO-AI
.\scripts\setup.ps1
```

### Configuration

1. Copy `.env.example` to `.env` (done automatically by setup)
2. Edit `.env` to set your NCBI email (recommended for PubMed access)
3. Optionally configure an LLM provider

### Running

```powershell
# Start both services
.\scripts\run-all.ps1

# Or start individually
.\scripts\run-backend.ps1   # http://127.0.0.1:8000
.\scripts\run-frontend.ps1  # http://localhost:5173
```

### Stopping

```powershell
.\scripts\stop-all.ps1
```

---

## Architecture

```
Frontend (React)  ←→  Backend (FastAPI)  ←→  Scientific APIs
     ↓                      ↓                       ↓
  Browser              SQLite DB            PubMed, UniProt,
  UI/UX               Local Files          AlphaFold, Europe PMC
```

- Frontend and backend are independent
- All scientific integrations go through the backend
- No API keys stored in frontend
- All data persisted locally in SQLite

---

## Privacy & Security

- **Local-only**: Bound to 127.0.0.1 / localhost
- **No cloud dependencies**: Works fully offline (except API searches)
- **LLM disabled by default**: No paid API calls without explicit configuration
- **Private data isolation**: Medical records stored separately
- **No data exfiltration**: No automatic uploads to external services
- **API key protection**: Never logged, never returned in responses

---

## API Documentation

When the backend is running, visit:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## Project Structure

```
ARAKNO-AI/
├── frontend/          # React + TypeScript + Tailwind
├── backend/           # Python FastAPI
├── data/              # Local data storage
│   ├── database/      # SQLite database
│   ├── papers/        # Downloaded papers
│   ├── structures/    # Protein structures
│   ├── reports/       # Generated reports
│   ├── cache/         # API response cache
│   └── private_case/  # Private medical data (isolated)
├── scripts/           # Setup and launch scripts
├── docs/              # Documentation
└── .env               # Configuration (not in git)
```

---

## Disclaimer

This software is a research tool for scientific literature exploration and computational biology research. It is **not** a medical device, diagnostic tool, or clinical decision support system.

- AI-generated analyses are computational interpretations, not clinical evidence
- Protein structure predictions are models, not experimental results
- All research findings should be verified against primary literature
- No clinical decisions should be based solely on this software's output

---

## Contributing

We welcome community contributions! Please read our [Contributing Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting issues or pull requests.

## Security

Please report security vulnerabilities responsibly as described in [SECURITY.md](SECURITY.md).

## Citation

If you use ARAKNO-AI in your academic research or computational studies, please cite it using the metadata in [CITATION.cff](CITATION.cff).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
