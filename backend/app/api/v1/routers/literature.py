"""
Literature explorer API router.
Connects with PubMed and Europe PMC, manages saved publications.
"""

import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_db
from app.db.models.models import Publication, ResearchActivity
from app.db.repositories.publications import PublicationRepository
from app.integrations.pubmed.client import PubMedClient
from app.integrations.europe_pmc.client import EuropePMCClient
from app.schemas.literature import (
    PublicationSearchQuery,
    PublicationSearchResult,
    PublicationCreate,
    PublicationRead,
    PublicationUpdate,
)
from app.schemas.common import PaginatedResponse

router = APIRouter(prefix="/literature", tags=["Literature"])


@router.post("/search", response_model=List[PublicationSearchResult])
async def search_literature(
    query_body: PublicationSearchQuery,
    db: AsyncSession = Depends(get_db),
):
    """Search scientific literature across PubMed and Europe PMC with deduplication."""
    articles = []
    pubmed_client = PubMedClient()
    europe_pmc_client = EuropePMCClient()

    if query_body.source in ("pubmed", "all"):
        pm_results = await pubmed_client.search_and_fetch(
            query=query_body.query,
            max_results=query_body.max_results,
            year_start=query_body.year_start,
            year_end=query_body.year_end,
        )
        articles.extend(pm_results)

    if query_body.source in ("europe_pmc", "all"):
        epmc_results = await europe_pmc_client.search(
            query=query_body.query,
            max_results=query_body.max_results,
            open_access_only=query_body.open_access_only,
            year_start=query_body.year_start,
            year_end=query_body.year_end,
        )
        articles.extend(epmc_results)

    # Check which items are already saved in the local database
    repo = PublicationRepository(db)
    results: List[PublicationSearchResult] = []
    seen_keys = set()

    for item in articles:
        pmid = item.get("pmid")
        doi = item.get("doi")
        key = pmid or doi or item.get("title")

        if key in seen_keys:
            continue
        seen_keys.add(key)

        is_saved = False
        saved_id = None
        if pmid:
            saved = await repo.get_by_pmid(pmid)
            if saved:
                is_saved = True
                saved_id = saved.id
        elif doi:
            saved = await repo.get_by_doi(doi)
            if saved:
                is_saved = True
                saved_id = saved.id

        authors_val = item.get("authors", [])
        if isinstance(authors_val, str):
            try:
                authors_val = json.loads(authors_val)
            except Exception:
                authors_val = [authors_val]

        results.append(
            PublicationSearchResult(
                title=item.get("title", ""),
                pmid=pmid,
                pmc_id=item.get("pmc_id"),
                doi=doi,
                authors=authors_val if isinstance(authors_val, list) else [],
                journal=item.get("journal"),
                year=item.get("year"),
                abstract=item.get("abstract"),
                publication_type=item.get("publication_type"),
                source=item.get("source", "pubmed"),
                url=item.get("url"),
                is_open_access=item.get("is_open_access", False),
                is_saved=is_saved,
                saved_id=saved_id,
            )
        )

    return results


@router.get("", response_model=PaginatedResponse[PublicationRead])
async def list_saved_publications(
    query: Optional[str] = None,
    project_id: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve saved publications from SQLite with pagination and search filtering."""
    repo = PublicationRepository(db)
    skip = (page - 1) * page_size
    items, total = await repo.list_publications(
        query=query, project_id=project_id, skip=skip, limit=page_size
    )

    total_pages = (total + page_size - 1) // page_size if page_size else 1
    return PaginatedResponse(
        items=[PublicationRead.model_validate(p) for p in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.post("/save", response_model=PublicationRead)
async def save_publication(
    pub_in: PublicationCreate,
    db: AsyncSession = Depends(get_db),
):
    """Save a publication record to local SQLite storage."""
    repo = PublicationRepository(db)

    # Check for existing duplicate
    if pub_in.pmid:
        existing = await repo.get_by_pmid(pub_in.pmid)
        if existing:
            return PublicationRead.model_validate(existing)
    elif pub_in.doi:
        existing = await repo.get_by_doi(pub_in.doi)
        if existing:
            return PublicationRead.model_validate(existing)

    pub = Publication(**pub_in.model_dump())
    created = await repo.create(pub)

    # Log activity
    activity = ResearchActivity(
        activity_type="save",
        description=f"Saved publication: '{created.title[:60]}...'",
        entity_type="publication",
        entity_id=created.id,
    )
    db.add(activity)
    await db.commit()

    return PublicationRead.model_validate(created)


@router.get("/{paper_id}", response_model=PublicationRead)
async def get_publication(
    paper_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get single publication record by ID."""
    repo = PublicationRepository(db)
    pub = await repo.get_by_id(paper_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Publication not found")
    return PublicationRead.model_validate(pub)


@router.delete("/{paper_id}")
async def delete_publication(
    paper_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Delete a saved publication from local database."""
    repo = PublicationRepository(db)
    deleted = await repo.delete(paper_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Publication not found")
    await db.commit()
    return {"success": True, "message": "Publication deleted"}


@router.post("/{paper_id}/notes", response_model=PublicationRead)
async def update_publication_notes(
    paper_id: str,
    update_data: PublicationUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Add or update notes on a saved publication."""
    repo = PublicationRepository(db)
    pub = await repo.get_by_id(paper_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Publication not found")

    if update_data.notes is not None:
        pub.notes = update_data.notes
    if update_data.is_favorite is not None:
        pub.is_favorite = update_data.is_favorite
    if update_data.project_id is not None:
        pub.project_id = update_data.project_id

    await db.commit()
    return PublicationRead.model_validate(pub)
