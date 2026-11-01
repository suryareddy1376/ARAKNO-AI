# ARAKNO-AI API Reference

## Base URL

```
http://127.0.0.1:8000/api/v1
```

## Interactive Documentation

When the backend is running:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Endpoints

### Health & System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/system/status` | System status with DB and API connectivity |
| GET | `/system/storage` | Storage usage information |

### Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard/overview` | Dashboard statistics |
| GET | `/dashboard/activity` | Recent research activity |
| GET | `/dashboard/statistics` | Detailed statistics |

### Literature

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/literature/search` | Search PubMed/Europe PMC |
| GET | `/literature` | List saved publications |
| GET | `/literature/{paper_id}` | Get publication details |
| POST | `/literature/save` | Save a publication |
| DELETE | `/literature/{paper_id}` | Delete a publication |
| POST | `/literature/{paper_id}/notes` | Add notes to publication |

### Proteins

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/proteins/search` | Search proteins |
| GET | `/proteins/{accession}` | Get protein by accession |
| GET | `/proteins/{accession}/structures` | Get protein structures |
| POST | `/proteins/resolve-accession` | Resolve accession via UniProt |
| POST | `/proteins/{accession}/download` | Download AlphaFold structure |
| GET | `/proteins/{accession}/confidence` | Get confidence metrics |

### Computational Biology

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/biology/fasta/analyze` | Analyze FASTA sequences |
| POST | `/biology/sequences/compare` | Compare two sequences |
| POST | `/biology/structures/analyze` | Analyze structure file |

### Evidence

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/evidence` | List evidence records |
| POST | `/evidence` | Create evidence record |
| GET | `/evidence/{evidence_id}` | Get evidence details |
| PUT | `/evidence/{evidence_id}` | Update evidence record |
| POST | `/evidence/verify-citation` | Verify a citation |

### Research

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/research/run` | Start a research job |
| GET | `/research/jobs` | List research jobs |
| GET | `/research/jobs/{job_id}` | Get job status |
| GET | `/research/jobs/{job_id}/results` | Get job results |
| POST | `/research/jobs/{job_id}/cancel` | Cancel a job |

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/projects` | List projects |
| POST | `/projects` | Create project |
| GET | `/projects/{project_id}` | Get project details |
| PATCH | `/projects/{project_id}` | Update project |
| DELETE | `/projects/{project_id}` | Delete project |

### Reports

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/reports` | List reports |
| POST | `/reports/generate` | Generate a report |
| GET | `/reports/{report_id}` | Get report |
| GET | `/reports/{report_id}/download` | Download report |

### Settings

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/settings` | Get current settings |
| PATCH | `/settings` | Update settings |
| GET | `/settings/provider-status` | Check LLM provider status |

## Authentication

No authentication is required. The application runs locally on localhost.

## Error Responses

All errors follow this format:
```json
{
  "detail": "Human-readable error message"
}
```

Standard HTTP status codes are used:
- `200` - Success
- `201` - Created
- `400` - Bad request
- `404` - Not found
- `422` - Validation error
- `429` - Rate limited
- `500` - Internal server error
- `503` - Service unavailable (external API down)
