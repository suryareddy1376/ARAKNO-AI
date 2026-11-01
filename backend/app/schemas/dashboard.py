"""
Pydantic schemas for the dashboard overview and metrics.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class DashboardStatistics(BaseModel):
    total_publications: int = 0
    total_proteins: int = 0
    total_structures: int = 0
    total_evidence_records: int = 0
    total_projects: int = 0
    total_reports: int = 0
    active_jobs: int = 0


class ActivityItem(BaseModel):
    id: int
    activity_type: str
    description: str
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    created_at: datetime


class PublicationsByMonthItem(BaseModel):
    month: str
    count: int


class DivisionStatsItem(BaseModel):
    division_name: str
    division_slug: str
    color: str
    project_count: int = 0
    publication_count: int = 0


class EvidenceDistributionItem(BaseModel):
    strength: str
    count: int


class DashboardOverviewResponse(BaseModel):
    statistics: DashboardStatistics
    recent_activities: List[ActivityItem] = []
    publications_by_month: List[PublicationsByMonthItem] = []
    division_distribution: List[DivisionStatsItem] = []
    evidence_distribution: List[EvidenceDistributionItem] = []
    backend_status: str = "operational"
