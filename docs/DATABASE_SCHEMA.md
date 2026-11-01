# ARAKNO-AI Database Schema

## Overview

ARAKNO-AI uses SQLite as its primary database. All tables are managed through SQLAlchemy ORM with Alembic migrations.

## Entity Relationship

```
ResearchDivision ─┬── ResearchProject ─┬── ResearchQuestion
                  │                    ├── ResearchReport
                  │                    ├── ResearchJob
                  │                    └── Publication (many-to-many)
                  │
                  ├── Publication ──── EvidenceRecord
                  │
                  └── Protein ──────── ProteinStructure

ResearchActivity (logs all actions across entities)
```

## Tables

### research_divisions
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| code | VARCHAR(20) | UNIQUE, NOT NULL |
| name | VARCHAR(100) | NOT NULL |
| description | TEXT | |
| created_at | DATETIME | DEFAULT now |

### research_projects
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| project_code | VARCHAR(50) | UNIQUE, NOT NULL |
| title | VARCHAR(500) | NOT NULL |
| description | TEXT | |
| division_id | INTEGER | FK → research_divisions |
| status | VARCHAR(20) | DEFAULT 'active' |
| created_at | DATETIME | DEFAULT now |
| updated_at | DATETIME | |

### research_questions
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| project_id | INTEGER | FK → research_projects |
| question | TEXT | NOT NULL |
| hypothesis | TEXT | |
| status | VARCHAR(20) | DEFAULT 'open' |
| created_at | DATETIME | DEFAULT now |

### publications
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| title | TEXT | NOT NULL |
| abstract | TEXT | |
| authors | TEXT | |
| journal | VARCHAR(500) | |
| publication_year | INTEGER | |
| publication_date | VARCHAR(20) | |
| doi | VARCHAR(100) | UNIQUE |
| pmid | VARCHAR(20) | UNIQUE |
| pmcid | VARCHAR(20) | |
| publication_type | VARCHAR(50) | |
| source_database | VARCHAR(20) | |
| open_access_status | BOOLEAN | |
| source_url | TEXT | |
| notes | TEXT | |
| division_id | INTEGER | FK → research_divisions |
| retrieved_at | DATETIME | DEFAULT now |

### proteins
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| gene_symbol | VARCHAR(50) | |
| protein_name | VARCHAR(500) | |
| accession | VARCHAR(20) | UNIQUE, NOT NULL |
| organism | VARCHAR(200) | |
| sequence_length | INTEGER | |
| sequence | TEXT | |
| source | VARCHAR(20) | |
| division_id | INTEGER | FK → research_divisions |
| created_at | DATETIME | DEFAULT now |

### protein_structures
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| protein_id | INTEGER | FK → proteins |
| model_id | VARCHAR(100) | |
| version | INTEGER | |
| format | VARCHAR(10) | |
| local_path | TEXT | |
| confidence | FLOAT | |
| pae_path | TEXT | |
| coverage | FLOAT | |
| retrieved_at | DATETIME | DEFAULT now |

### evidence_records
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| claim | TEXT | NOT NULL |
| publication_id | INTEGER | FK → publications |
| evidence_category | VARCHAR(1) | CHECK (A-E) |
| study_type | VARCHAR(100) | |
| species | VARCHAR(100) | |
| population | VARCHAR(200) | |
| sample_size | VARCHAR(50) | |
| methods | TEXT | |
| findings | TEXT | |
| limitations | TEXT | |
| confidence | VARCHAR(20) | |
| verification_status | VARCHAR(20) | DEFAULT 'unverified' |
| division_id | INTEGER | FK → research_divisions |
| created_at | DATETIME | DEFAULT now |

### research_reports
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| project_id | INTEGER | FK → research_projects |
| title | VARCHAR(500) | NOT NULL |
| research_question | TEXT | |
| report_content | TEXT | |
| format | VARCHAR(10) | DEFAULT 'markdown' |
| generated_at | DATETIME | DEFAULT now |
| verification_status | VARCHAR(20) | DEFAULT 'draft' |

### research_jobs
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| job_id | VARCHAR(36) | UNIQUE, NOT NULL |
| project_id | INTEGER | FK → research_projects |
| question | TEXT | |
| status | VARCHAR(20) | DEFAULT 'pending' |
| current_stage | VARCHAR(50) | |
| progress | FLOAT | DEFAULT 0 |
| result_reference | TEXT | |
| error_message | TEXT | |
| started_at | DATETIME | |
| finished_at | DATETIME | |

### research_activities
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| activity_type | VARCHAR(50) | NOT NULL |
| description | TEXT | |
| reference_id | VARCHAR(100) | |
| division_id | INTEGER | FK → research_divisions |
| created_at | DATETIME | DEFAULT now |

## Indexes

- `idx_publications_doi` on publications(doi)
- `idx_publications_pmid` on publications(pmid)
- `idx_proteins_accession` on proteins(accession)
- `idx_evidence_category` on evidence_records(evidence_category)
- `idx_jobs_job_id` on research_jobs(job_id)
- `idx_activities_created` on research_activities(created_at)
