# ARAKNO-AI Architecture

## System Overview

ARAKNO-AI is a modular, local-first biomedical research platform with clear separation between frontend and backend.

## Component Architecture

```
┌─────────────────────────────────────────────────────┐
│                    USER BROWSER                      │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │           React Frontend (Vite)                │  │
│  │                                               │  │
│  │  ┌─────────┐ ┌──────────┐ ┌──────────────┐  │  │
│  │  │  Pages  │ │Components│ │   Services   │  │  │
│  │  └────┬────┘ └────┬─────┘ └──────┬───────┘  │  │
│  │       │           │              │           │  │
│  │  ┌────┴───────────┴──────────────┴────────┐  │  │
│  │  │     TanStack Query + Zustand State     │  │  │
│  │  └────────────────┬───────────────────────┘  │  │
│  └───────────────────┼───────────────────────────┘  │
│                      │ HTTP/REST                     │
└──────────────────────┼──────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│               FastAPI Backend                         │
│                                                      │
│  ┌─────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │ Routers │→ │ Services │→ │  Integrations     │  │
│  └─────────┘  └──────────┘  │  ┌─────────────┐  │  │
│       │            │        │  │   PubMed    │  │  │
│       │            │        │  │ Europe PMC  │  │  │
│  ┌────┴────┐  ┌────┴─────┐ │  │  AlphaFold  │  │  │
│  │ Schemas │  │   Repos  │ │  │   UniProt   │  │  │
│  └─────────┘  └────┬─────┘ │  └─────────────┘  │  │
│                    │        └───────────────────┘  │
│               ┌────┴─────┐                        │
│               │  SQLite  │                        │
│               └──────────┘                        │
│                                                    │
│  ┌─────────────────────────────────────────────┐  │
│  │          LangGraph Research Engine           │  │
│  │  Intake → Retrieval → Evidence → Report     │  │
│  └─────────────────────────────────────────────┘  │
│                                                    │
│  ┌──────────────┐  ┌───────────────────────────┐  │
│  │  LLM Layer   │  │   Biology (Biopython)     │  │
│  │  (Optional)  │  │   FASTA, Sequences,       │  │
│  │  none/local/ │  │   Structures              │  │
│  │  remote      │  └───────────────────────────┘  │
│  └──────────────┘                                  │
└──────────────────────────────────────────────────────┘
```

## Data Flow

### Literature Search
1. User enters search query in frontend
2. Frontend sends POST to `/api/v1/literature/search`
3. Backend queries PubMed/Europe PMC APIs
4. Results are normalized and deduplicated
5. Response returned to frontend for display
6. User can save publications to local SQLite

### Protein Research
1. User enters UniProt accession
2. Backend verifies accession with UniProt API
3. Backend queries AlphaFold for structural predictions
4. Structure file downloaded and cached locally
5. Frontend renders 3D model using 3Dmol.js
6. Confidence metrics displayed alongside

### Research Workflow (LangGraph)
1. User submits research question
2. Intake node analyzes question and selects sources
3. Literature node searches and retrieves publications
4. Protein node resolves relevant protein data
5. Evidence node extracts structured evidence
6. Quality node categorizes evidence
7. Citation node verifies all references
8. Report node generates traceable research report

## Security Model

- All services bound to localhost only
- No API keys stored in frontend code
- API keys masked in settings responses
- File uploads validated for type and size
- Path traversal prevented in all file operations
- Private medical data isolated from research data
- LLM calls require explicit user configuration

## Database Schema

See DATABASE_SCHEMA.md for full entity-relationship diagram and table definitions.
