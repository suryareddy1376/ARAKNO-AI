# ARAKNO-AI Privacy Policy

## Data Handling Principles

1. **Local-First**: All data is stored locally on your machine
2. **No Cloud Dependencies**: Core features work without internet
3. **Explicit Consent**: No data is sent externally without user action
4. **Isolation**: Private medical data is separated from research data

## Data Storage

### Research Data
- Publications, proteins, evidence records stored in local SQLite database
- Downloaded structure files stored in `data/structures/`
- Generated reports stored in `data/reports/`
- API response cache stored in `data/cache/`

### Private Case Data
- Stored separately in `data/private_case/`
- Never included in research indexing unless explicitly initiated
- Never sent to external services
- Not included in Git

## External API Communications

The application communicates with these external services **only when you initiate a search**:

| Service | Data Sent | Purpose |
|---------|-----------|---------|
| PubMed (NCBI) | Search queries | Literature search |
| Europe PMC | Search queries | Literature search |
| AlphaFold DB | Protein accessions | Structure retrieval |
| UniProt | Protein accessions | Protein metadata |

### What is NOT sent externally:
- Private medical records
- Personal patient information
- Local database contents
- Research notes
- Evidence assessments

## LLM Privacy

- LLM is disabled by default
- When enabled, only research queries are sent (never private data)
- `ALLOW_REMOTE_MEDICAL_DATA=false` by default
- API keys are never logged or returned in API responses
- Paid requests are blocked by default

## Network Security

- Backend bound to `127.0.0.1` (localhost only)
- Frontend served on `localhost` only
- No external network listeners
- No incoming connections accepted

## File Security

- File uploads validated for type and size
- Path traversal attacks prevented
- Downloaded files verified before storage
- `.env` excluded from Git
