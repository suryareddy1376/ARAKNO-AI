"""
State definitions for ARAKNO-AI research workflows.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ResearchWorkflowState(BaseModel):
    """Explicit typed state for research execution workflow."""

    query: str
    project_id: Optional[str] = None
    division_slug: Optional[str] = "arakno-spine"
    sources: List[str] = ["pubmed", "europe_pmc", "alphafold"]
    max_results: int = 15
    synthesize_ai: bool = False

    # Pipeline stages data
    identified_entities: List[str] = []
    protein_targets: List[str] = []
    publications: List[Dict[str, Any]] = []
    protein_records: List[Dict[str, Any]] = []
    evidence_claims: List[Dict[str, Any]] = []
    contradictions: List[Dict[str, Any]] = []
    citations_verified: bool = False
    verification_summary: Optional[str] = None

    # Final generated report
    executive_summary: Optional[str] = None
    report_markdown: Optional[str] = None
    execution_log: List[str] = []
    error: Optional[str] = None
