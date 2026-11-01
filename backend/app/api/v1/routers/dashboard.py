"""
Dashboard overview, activity timeline, and statistics endpoints.
All data is derived from actual SQLite database records.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_db
from app.db.models.models import (
    Publication,
    Protein,
    ProteinStructure,
    EvidenceRecord,
    ResearchProject,
    ResearchReport,
    ResearchJob,
    ResearchActivity,
    ResearchDivision,
)
from app.schemas.dashboard import (
    DashboardOverviewResponse,
    DashboardStatistics,
    ActivityItem,
    PublicationsByMonthItem,
    DivisionStatsItem,
    EvidenceDistributionItem,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/overview", response_model=DashboardOverviewResponse)
async def get_dashboard_overview(db: AsyncSession = Depends(get_db)):
    """Retrieve full dashboard metrics and distribution charts."""
    # 1. Total counts
    pub_count = (await db.execute(select(func.count(Publication.id)))).scalar() or 0
    protein_count = (await db.execute(select(func.count(Protein.id)))).scalar() or 0
    structure_count = (await db.execute(select(func.count(ProteinStructure.id)))).scalar() or 0
    evidence_count = (await db.execute(select(func.count(EvidenceRecord.id)))).scalar() or 0
    project_count = (await db.execute(select(func.count(ResearchProject.id)))).scalar() or 0
    report_count = (await db.execute(select(func.count(ResearchReport.id)))).scalar() or 0
    active_jobs = (
        await db.execute(
            select(func.count(ResearchJob.id)).where(ResearchJob.status == "running")
        )
    ).scalar() or 0

    stats = DashboardStatistics(
        total_publications=pub_count,
        total_proteins=protein_count,
        total_structures=structure_count,
        total_evidence_records=evidence_count,
        total_projects=project_count,
        total_reports=report_count,
        active_jobs=active_jobs,
    )

    # 2. Recent activities
    activities_query = (
        select(ResearchActivity)
        .order_by(ResearchActivity.created_at.desc())
        .limit(10)
    )
    activities = (await db.execute(activities_query)).scalars().all()
    activity_items = [
        ActivityItem(
            id=a.id,
            activity_type=a.activity_type,
            description=a.description,
            entity_type=a.entity_type,
            entity_id=a.entity_id,
            created_at=a.created_at,
        )
        for a in activities
    ]

    # 3. Division distribution
    divisions = (await db.execute(select(ResearchDivision))).scalars().all()
    div_distribution = []
    for div in divisions:
        # count projects for division
        p_count = (
            await db.execute(
                select(func.count(ResearchProject.id)).where(ResearchProject.division_id == div.id)
            )
        ).scalar() or 0
        div_distribution.append(
            DivisionStatsItem(
                division_name=div.name,
                division_slug=div.slug,
                color=div.color,
                project_count=p_count,
                publication_count=0,
            )
        )

    # 4. Evidence distribution by strength
    strengths = ["strong", "moderate", "weak", "contradictory"]
    ev_distribution = []
    for s in strengths:
        cnt = (
            await db.execute(
                select(func.count(EvidenceRecord.id)).where(EvidenceRecord.strength == s)
            )
        ).scalar() or 0
        ev_distribution.append(EvidenceDistributionItem(strength=s.capitalize(), count=cnt))

    # 5. Publications by month (aggregate or empty)
    pub_month_items = []
    if pub_count > 0:
        pub_month_items.append(PublicationsByMonthItem(month="Recent", count=pub_count))

    return DashboardOverviewResponse(
        statistics=stats,
        recent_activities=activity_items,
        publications_by_month=pub_month_items,
        division_distribution=div_distribution,
        evidence_distribution=ev_distribution,
        backend_status="operational",
    )
