"""
Repository for ResearchProject, ResearchDivision, and ResearchQuestion operations.
"""

from typing import List, Optional, Tuple
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.models import ResearchProject, ResearchDivision, ResearchQuestion


class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_divisions(self) -> List[ResearchDivision]:
        result = await self.session.execute(
            select(ResearchDivision).order_by(ResearchDivision.id)
        )
        return list(result.scalars().all())

    async def get_division_by_slug(self, slug: str) -> Optional[ResearchDivision]:
        result = await self.session.execute(
            select(ResearchDivision).where(ResearchDivision.slug == slug)
        )
        return result.scalar_one_or_none()

    async def get_project_by_id(self, project_id: str) -> Optional[ResearchProject]:
        result = await self.session.execute(
            select(ResearchProject)
            .options(
                selectinload(ResearchProject.division),
                selectinload(ResearchProject.questions),
            )
            .where(ResearchProject.id == project_id)
        )
        return result.scalar_one_or_none()

    async def list_projects(
        self,
        division_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> Tuple[List[ResearchProject], int]:
        stmt = select(ResearchProject).options(
            selectinload(ResearchProject.division),
            selectinload(ResearchProject.questions),
        )
        count_stmt = select(func.count(ResearchProject.id))

        filters = []
        if division_id is not None:
            filters.append(ResearchProject.division_id == division_id)
        if status:
            filters.append(ResearchProject.status == status)

        for f in filters:
            stmt = stmt.where(f)
            count_stmt = count_stmt.where(f)

        total = (await self.session.execute(count_stmt)).scalar() or 0
        stmt = stmt.order_by(ResearchProject.created_at.desc()).offset(skip).limit(limit)
        items = (await self.session.execute(stmt)).scalars().all()
        return list(items), total

    async def create_project(self, project: ResearchProject) -> ResearchProject:
        self.session.add(project)
        await self.session.flush()
        return project

    async def update_project(self, project_id: str, **fields) -> Optional[ResearchProject]:
        proj = await self.get_project_by_id(project_id)
        if proj:
            for k, v in fields.items():
                if hasattr(proj, k) and v is not None:
                    setattr(proj, k, v)
            await self.session.flush()
        return proj

    async def add_question(self, question: ResearchQuestion) -> ResearchQuestion:
        self.session.add(question)
        await self.session.flush()
        return question
