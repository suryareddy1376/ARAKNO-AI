"""
Pydantic schemas for scientific reports.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ResearchReportCreate(BaseModel):
    title: str
    project_id: Optional[str] = None
    report_type: str = "literature_review"  # summary, literature_review, evidence_map, full
    format: str = "markdown"
    content: Optional[str] = None


class ResearchReportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    project_id: Optional[str] = None
    title: str
    report_type: str
    content: Optional[str] = None
    format: str
    file_path: Optional[str] = None
    status: str
    word_count: int
    created_at: datetime
    updated_at: datetime
