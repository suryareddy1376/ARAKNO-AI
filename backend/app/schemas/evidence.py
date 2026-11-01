"""
Pydantic schemas for evidence records and citation verification.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class EvidenceRecordBase(BaseModel):
    claim: str
    evidence_text: Optional[str] = None
    evidence_type: str = "citation"  # citation, experimental, computational, review
    strength: str = "moderate"  # strong, moderate, weak, contradictory
    confidence_score: Optional[float] = None
    verified: bool = False
    verification_notes: Optional[str] = None
    source_section: Optional[str] = None
    tags: Optional[str] = None
    project_id: Optional[str] = None
    publication_id: Optional[str] = None


class EvidenceRecordCreate(EvidenceRecordBase):
    pass


class EvidenceRecordUpdate(BaseModel):
    claim: Optional[str] = None
    evidence_text: Optional[str] = None
    evidence_type: Optional[str] = None
    strength: Optional[str] = None
    confidence_score: Optional[float] = None
    verified: Optional[bool] = None
    verification_notes: Optional[str] = None
    source_section: Optional[str] = None
    tags: Optional[str] = None
    project_id: Optional[str] = None
    publication_id: Optional[str] = None


class EvidenceRecordRead(EvidenceRecordBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime


class CitationVerificationRequest(BaseModel):
    doi: Optional[str] = None
    pmid: Optional[str] = None
    title: Optional[str] = None
    claim_text: Optional[str] = None


class CitationVerificationResult(BaseModel):
    valid: bool
    source_found: bool
    title: Optional[str] = None
    journal: Optional[str] = None
    year: Optional[int] = None
    pmid: Optional[str] = None
    doi: Optional[str] = None
    verification_message: str
    matched_abstract_excerpt: Optional[str] = None
