"""
Repository for Publication database operations.
"""

from typing import List, Optional, Tuple
from sqlalchemy import select, func, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.models import Publication


class PublicationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, pub_id: str) -> Optional[Publication]:
        result = await self.session.execute(
            select(Publication).where(Publication.id == pub_id)
        )
        return result.scalar_one_or_none()

    async def get_by_pmid(self, pmid: str) -> Optional[Publication]:
        result = await self.session.execute(
            select(Publication).where(Publication.pmid == pmid)
        )
        return result.scalar_one_or_none()

    async def get_by_doi(self, doi: str) -> Optional[Publication]:
        result = await self.session.execute(
            select(Publication).where(Publication.doi == doi)
        )
        return result.scalar_one_or_none()

    async def list_publications(
        self,
        query: Optional[str] = None,
        project_id: Optional[str] = None,
        is_favorite: Optional[bool] = None,
        source: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> Tuple[List[Publication], int]:
        stmt = select(Publication)
        count_stmt = select(func.count(Publication.id))

        filters = []
        if query:
            q_term = f"%{query}%"
            filters.append(
                or_(
                    Publication.title.ilike(q_term),
                    Publication.abstract.ilike(q_term),
                    Publication.authors.ilike(q_term),
                    Publication.pmid.ilike(q_term),
                    Publication.doi.ilike(q_term),
                )
            )
        if project_id:
            filters.append(Publication.project_id == project_id)
        if is_favorite is not None:
            filters.append(Publication.is_favorite == is_favorite)
        if source:
            filters.append(Publication.source == source)

        if filters:
            for f in filters:
                stmt = stmt.where(f)
                count_stmt = count_stmt.where(f)

        total_count = (await self.session.execute(count_stmt)).scalar() or 0
        stmt = stmt.order_by(Publication.created_at.desc()).offset(skip).limit(limit)
        items = (await self.session.execute(stmt)).scalars().all()

        return list(items), total_count

    async def create(self, pub: Publication) -> Publication:
        self.session.add(pub)
        await self.session.flush()
        return pub

    async def delete(self, pub_id: str) -> bool:
        pub = await self.get_by_id(pub_id)
        if pub:
            await self.session.delete(pub)
            await self.session.flush()
            return True
        return False
