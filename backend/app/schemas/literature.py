"""
Pydantic schemas for literature and scientific publications.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class PublicationSearchQuery(BaseModel):
    query: str
    source: str = "all"  # pubmed, europe_pmc, all
    max_results: int = Field(default=20, ge=1, le=100)
    year_start: Optional[int] = None
    year_end: Optional[int] = None
    publication_type: Optional[str] = None
    open_access_only: bool = False


class PublicationBase(BaseModel):
    title: str
    pmid: Optional[str] = None
    pmc_id: Optional[str] = None
    doi: Optional[str] = None
    authors: Optional[str] = None  # JSON string or comma-separated
    journal: Optional[str] = None
    year: Optional[int] = None
    abstract: Optional[str] = None
    keywords: Optional[str] = None
    publication_type: Optional[str] = None
    source: str = "pubmed"
    url: Optional[str] = None
    notes: Optional[str] = None
    is_favorite: bool = False
    project_id: Optional[str] = None


class PublicationCreate(PublicationBase):
    pass


class PublicationUpdate(BaseModel):
    notes: Optional[str] = None
    is_favorite: Optional[bool] = None
    project_id: Optional[str] = None


class PublicationRead(PublicationBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    citation_count: int = 0
    created_at: datetime
    updated_at: datetime


class PublicationSearchResult(BaseModel):
    title: str
    pmid: Optional[str] = None
    pmc_id: Optional[str] = None
    doi: Optional[str] = None
    authors: List[str] = []
    journal: Optional[str] = None
    year: Optional[int] = None
    abstract: Optional[str] = None
    publication_type: Optional[str] = None
    source: str
    url: Optional[str] = None
    is_open_access: bool = False
    is_saved: bool = False
    saved_id: Optional[str] = None
