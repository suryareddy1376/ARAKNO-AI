"""
Repository for ResearchJob background task tracking.
"""

from typing import List, Optional, Tuple
from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.models import ResearchJob


class JobRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, job_id: str) -> Optional[ResearchJob]:
        result = await self.session.execute(
            select(ResearchJob).where(ResearchJob.id == job_id)
        )
        return result.scalar_one_or_none()

    async def list_jobs(
        self,
        status: Optional[str] = None,
        job_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List[ResearchJob], int]:
        stmt = select(ResearchJob)
        count_stmt = select(func.count(ResearchJob.id))

        if status:
            stmt = stmt.where(ResearchJob.status == status)
            count_stmt = count_stmt.where(ResearchJob.status == status)
        if job_type:
            stmt = stmt.where(ResearchJob.job_type == job_type)
            count_stmt = count_stmt.where(ResearchJob.job_type == job_type)

        total = (await self.session.execute(count_stmt)).scalar() or 0
        stmt = stmt.order_by(ResearchJob.created_at.desc()).offset(skip).limit(limit)
        items = (await self.session.execute(stmt)).scalars().all()
        return list(items), total

    async def create(self, job: ResearchJob) -> ResearchJob:
        self.session.add(job)
        await self.session.flush()
        return job

    async def update_status(
        self,
        job_id: str,
        status: str,
        progress: Optional[float] = None,
        result: Optional[str] = None,
        error_message: Optional[str] = None,
    ) -> Optional[ResearchJob]:
        job = await self.get_by_id(job_id)
        if job:
            job.status = status
            if progress is not None:
                job.progress = progress
            if result is not None:
                job.result = result
            if error_message is not None:
                job.error_message = error_message
            if status == "running" and not job.started_at:
                job.started_at = datetime.now(timezone.utc)
            elif status in ("completed", "failed", "cancelled"):
                job.completed_at = datetime.now(timezone.utc)
            await self.session.flush()
        return job
