"""
Pydantic schemas for agentic research jobs and execution tracking.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ResearchRunRequest(BaseModel):
    query: str
    project_id: Optional[str] = None
    division_slug: Optional[str] = "arakno-spine"
    sources: List[str] = ["pubmed", "europe_pmc", "alphafold"]
    max_results: int = 15
    synthesize_ai: bool = False  # Privacy default: disabled unless explicitly requested


class ResearchJobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    job_type: str
    query: str
    parameters: Optional[str] = None
    status: str
    progress: float
    result: Optional[str] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class ResearchJobResult(BaseModel):
    job_id: str
    query: str
    status: str
    publications_found: int = 0
    proteins_analyzed: int = 0
    evidence_extracted: int = 0
    publications: List[Dict[str, Any]] = []
    proteins: List[Dict[str, Any]] = []
    evidence_records: List[Dict[str, Any]] = []
    synthesis_summary: Optional[str] = None
    scientific_disclaimer: str = (
        "ARAKNO-AI is an experimental computational research platform. "
        "Generated interpretations are not clinical advice, diagnoses, or treatment plans."
    )
