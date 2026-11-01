"""
Evidence management and citation verification API router.
Categorizes claims into categories A-E and verifies traceability to literature.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_db
from app.db.models.models import EvidenceRecord, Publication
from app.db.repositories.evidence import EvidenceRepository
from app.db.repositories.publications import PublicationRepository
from app.integrations.pubmed.client import PubMedClient
from app.integrations.europe_pmc.client import EuropePMCClient
from app.schemas.evidence import (
    EvidenceRecordCreate,
    EvidenceRecordRead,
    EvidenceRecordUpdate,
    CitationVerificationRequest,
    CitationVerificationResult,
)
from app.schemas.common import PaginatedResponse

router = APIRouter(prefix="/evidence", tags=["Evidence"])


@router.get("", response_model=PaginatedResponse[EvidenceRecordRead])
async def list_evidence(
    project_id: Optional[str] = None,
    publication_id: Optional[str] = None,
    evidence_type: Optional[str] = None,
    strength: Optional[str] = None,
    verified: Optional[bool] = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List scientific evidence records with multi-criteria filtering."""
    repo = EvidenceRepository(db)
    skip = (page - 1) * page_size
    items, total = await repo.list_evidence(
        project_id=project_id,
        publication_id=publication_id,
        evidence_type=evidence_type,
        strength=strength,
        verified=verified,
        skip=skip,
        limit=page_size,
    )
    total_pages = (total + page_size - 1) // page_size if page_size else 1
    return PaginatedResponse(
        items=[EvidenceRecordRead.model_validate(e) for e in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.post("", response_model=EvidenceRecordRead)
async def create_evidence(
    record_in: EvidenceRecordCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new scientific evidence record linked to a source publication."""
    repo = EvidenceRepository(db)
    record = EvidenceRecord(**record_in.model_dump())
    created = await repo.create(record)
    await db.commit()
    return EvidenceRecordRead.model_validate(created)


@router.get("/{evidence_id}", response_model=EvidenceRecordRead)
async def get_evidence(
    evidence_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve an evidence record by ID."""
    repo = EvidenceRepository(db)
    record = await repo.get_by_id(evidence_id)
    if not record:
        raise HTTPException(status_code=404, detail="Evidence record not found")
    return EvidenceRecordRead.model_validate(record)


@router.put("/{evidence_id}", response_model=EvidenceRecordRead)
async def update_evidence(
    evidence_id: str,
    update_data: EvidenceRecordUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update evidence evaluation or verification status."""
    repo = EvidenceRepository(db)
    updated = await repo.update(evidence_id, **update_data.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Evidence record not found")
    await db.commit()
    return EvidenceRecordRead.model_validate(updated)


@router.post("/verify-citation", response_model=CitationVerificationResult)
async def verify_citation(
    req: CitationVerificationRequest,
    db: AsyncSession = Depends(get_db),
):
    """Verify that a DOI or PMID corresponds to a real publication and validate source."""
    pub_repo = PublicationRepository(db)

    # Check local database first
    if req.pmid:
        local_pub = await pub_repo.get_by_pmid(req.pmid)
        if local_pub:
            return CitationVerificationResult(
                valid=True,
                source_found=True,
                title=local_pub.title,
                journal=local_pub.journal,
                year=local_pub.year,
                pmid=local_pub.pmid,
                doi=local_pub.doi,
                verification_message="Verified in local scientific database.",
                matched_abstract_excerpt=local_pub.abstract[:300] if local_pub.abstract else None,
            )
    if req.doi:
        local_pub = await pub_repo.get_by_doi(req.doi)
        if local_pub:
            return CitationVerificationResult(
                valid=True,
                source_found=True,
                title=local_pub.title,
                journal=local_pub.journal,
                year=local_pub.year,
                pmid=local_pub.pmid,
                doi=local_pub.doi,
                verification_message="Verified in local scientific database.",
                matched_abstract_excerpt=local_pub.abstract[:300] if local_pub.abstract else None,
            )

    # Check PubMed external
    if req.pmid:
        pubmed = PubMedClient()
        summaries = await pubmed.fetch_summaries([req.pmid])
        if summaries:
            s = summaries[0]
            abstracts = await pubmed.fetch_abstracts([req.pmid])
            return CitationVerificationResult(
                valid=True,
                source_found=True,
                title=s.get("title"),
                journal=s.get("journal"),
                year=s.get("year"),
                pmid=s.get("pmid"),
                doi=s.get("doi"),
                verification_message="Verified externally via NCBI PubMed E-Utilities.",
                matched_abstract_excerpt=abstracts.get(req.pmid, "")[:300],
            )

    # Check Europe PMC external
    if req.doi:
        epmc = EuropePMCClient()
        res = await epmc.search(f"DOI:\"{req.doi}\"", max_results=1)
        if res:
            item = res[0]
            return CitationVerificationResult(
                valid=True,
                source_found=True,
                title=item.get("title"),
                journal=item.get("journal"),
                year=item.get("year"),
                pmid=item.get("pmid"),
                doi=item.get("doi"),
                verification_message="Verified externally via Europe PMC API.",
                matched_abstract_excerpt=item.get("abstract", "")[:300],
            )

    return CitationVerificationResult(
        valid=False,
        source_found=False,
        verification_message="Could not verify citation with provided PMID or DOI.",
    )
