"""
Scientific research report generation and export API router.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_db
from app.db.models.models import ResearchReport, ResearchActivity
from app.db.repositories.reports import ReportRepository
from app.schemas.reports import (
    ResearchReportCreate,
    ResearchReportRead,
)

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("", response_model=List[ResearchReportRead])
async def list_reports(
    project_id: Optional[str] = None,
    report_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List generated research dossiers and reviews."""
    repo = ReportRepository(db)
    reports, _ = await repo.list_reports(project_id=project_id, report_type=report_type, limit=50)
    return [ResearchReportRead.model_validate(r) for r in reports]


@router.post("/generate", response_model=ResearchReportRead)
async def create_report(
    report_in: ResearchReportCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create or manually save a research report."""
    repo = ReportRepository(db)
    word_count = len(report_in.content.split()) if report_in.content else 0

    report = ResearchReport(
        title=report_in.title,
        project_id=report_in.project_id,
        report_type=report_in.report_type,
        format=report_in.format,
        content=report_in.content,
        status="completed",
        word_count=word_count,
    )
    created = await repo.create(report)

    activity = ResearchActivity(
        activity_type="generate",
        description=f"Generated report: '{created.title}'",
        entity_type="report",
        entity_id=created.id,
    )
    db.add(activity)
    await db.commit()

    return ResearchReportRead.model_validate(created)


@router.get("/{report_id}", response_model=ResearchReportRead)
async def get_report(
    report_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve full research report content by ID."""
    repo = ReportRepository(db)
    report = await repo.get_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return ResearchReportRead.model_validate(report)


@router.get("/{report_id}/download")
async def download_report(
    report_id: str,
    format: str = Query(default="markdown", pattern="^(markdown|html|txt)$"),
    db: AsyncSession = Depends(get_db),
):
    """Download a report as a markdown or text file."""
    repo = ReportRepository(db)
    report = await repo.get_by_id(report_id)
    if not report or not report.content:
        raise HTTPException(status_code=404, detail="Report content not found")

    filename = f"{report.title[:30].replace(' ', '_')}.{ 'md' if format == 'markdown' else format }"
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}

    return Response(
        content=report.content,
        media_type="text/markdown" if format == "markdown" else "text/plain",
        headers=headers,
    )


@router.delete("/{report_id}")
async def delete_report(
    report_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Delete a research report."""
    repo = ReportRepository(db)
    deleted = await repo.delete(report_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Report not found")
    await db.commit()
    return {"success": True, "message": "Report deleted"}
