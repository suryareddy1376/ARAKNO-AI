# Changelog

All notable changes to PROJECT ARAKNO-AI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-11-01

### Added
- **Six Specialized Research Divisions**:
  - `ARAKNO-SPINE`: Spinal biomechanics, posterior instrumentation, fusion biology, and pseudarthrosis.
  - `ARAKNO-BONE`: Osteogenesis, bone remodelling, collagen architecture, and tissue engineering.
  - `ARAKNO-MUSCLE`: Skeletal muscle architecture, actin/myosin dynamics, and connective tissue healing.
  - `ARAKNO-SENSE`: Biological sensory mechanoreceptors, trichobothria, and slit sensilla.
  - `ARAKNO-SILK`: Spider silk biomaterials, spidroins, and tensile structural scaffolds.
  - `ARAKNO-NEURO`: Neural signalling, peripheral nerve regeneration, and neuromuscular repair.
- **FastAPI Asynchronous Backend**:
  - SQLite local database with AsyncSQLAlchemy and aiosqlite.
  - Full CRUD operations for Research Divisions, Projects, Literature Records, Protein Records, and Structured Reports.
  - Live PubMed integration via NCBI E-utilities (ESearch, ESummary, EFetch) with automatic rate limiting and retry backoff.
  - Live UniProt and AlphaFold integration with automatic Swiss-Prot canonical accession resolution (e.g., gene symbol `ACTB` -> `P60709`).
  - Optional multi-provider LLM research synthesis client (Ollama local, OpenRouter, Google Gemini, NVIDIA NIM) with deterministic zero-cost fallback when no provider is active.
- **React 18 + TypeScript + Tailwind CSS Frontend**:
  - Dark-mode, low-glare scientific user interface styled with clean typography and Tailwind CSS.
  - Interactive 3D molecular structure visualizer powered by 3Dmol.js (cartoon, stick, sphere, surface representations, rainbow/pLDDT coloring).
  - Structured scientific report viewer with GitHub Flavored Markdown (tables, callout alerts, code blocks).
  - Division explorer, literature search with live PubMed querying and local caching, interactive research laboratory, and customizable settings panel.
- **Security & Privacy Infrastructure**:
  - Strict zero-external-transmission default (`LLM_PROVIDER=none`).
  - Sensitive field masking in audit logs and API responses.
  - Local database storage with zero telemetry or tracking.
- **Developer Experience**:
  - Windows PowerShell automation scripts for dependency installation (`scripts/setup.ps1`), backend launch (`scripts/run-backend.ps1`), frontend launch (`scripts/run-frontend.ps1`), and all-in-one runner (`scripts/run-all.ps1`).
  - GitHub Actions CI workflow for Python 3.12 test matrix and Node.js 20 production builds.
  - Complete open-source documentation suite (`README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CITATION.cff`).

### Security
- Verified zero hardcoded credentials across repository.
- Sanitized environment variable configuration templates.
