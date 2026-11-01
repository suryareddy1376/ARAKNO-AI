"""
Repository for ResearchReport operations.
"""

from typing import List, Optional, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.models import ResearchReport


class ReportRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, report_id: str) -> Optional[ResearchReport]:
        result = await self.session.execute(
            select(ResearchReport).where(ResearchReport.id == report_id)
        )
        return result.scalar_one_or_none()

    async def list_reports(
        self,
        project_id: Optional[str] = None,
        report_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> Tuple[List[ResearchReport], int]:
        stmt = select(ResearchReport)
        count_stmt = select(func.count(ResearchReport.id))

        filters = []
        if project_id:
            filters.append(ResearchReport.project_id == project_id)
        if report_type:
            filters.append(ResearchReport.report_type == report_type)

        for f in filters:
            stmt = stmt.where(f)
            count_stmt = count_stmt.where(f)

        total = (await self.session.execute(count_stmt)).scalar() or 0
        stmt = stmt.order_by(ResearchReport.created_at.desc()).offset(skip).limit(limit)
        items = (await self.session.execute(stmt)).scalars().all()
        return list(items), total

    async def create(self, report: ResearchReport) -> ResearchReport:
        self.session.add(report)
        await self.session.flush()
        return report

    async def delete(self, report_id: str) -> bool:
        report = await self.get_by_id(report_id)
        if report:
            await self.session.delete(report)
            await self.session.flush()
            return True
        return False
