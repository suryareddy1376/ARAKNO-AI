"""
Repository for EvidenceRecord database operations.
"""

from typing import List, Optional, Tuple
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.models import EvidenceRecord


class EvidenceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, evidence_id: str) -> Optional[EvidenceRecord]:
        result = await self.session.execute(
            select(EvidenceRecord).where(EvidenceRecord.id == evidence_id)
        )
        return result.scalar_one_or_none()

    async def list_evidence(
        self,
        project_id: Optional[str] = None,
        publication_id: Optional[str] = None,
        evidence_type: Optional[str] = None,
        strength: Optional[str] = None,
        verified: Optional[bool] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> Tuple[List[EvidenceRecord], int]:
        stmt = select(EvidenceRecord)
        count_stmt = select(func.count(EvidenceRecord.id))

        filters = []
        if project_id:
            filters.append(EvidenceRecord.project_id == project_id)
        if publication_id:
            filters.append(EvidenceRecord.publication_id == publication_id)
        if evidence_type:
            filters.append(EvidenceRecord.evidence_type == evidence_type)
        if strength:
            filters.append(EvidenceRecord.strength == strength)
        if verified is not None:
            filters.append(EvidenceRecord.verified == verified)

        for f in filters:
            stmt = stmt.where(f)
            count_stmt = count_stmt.where(f)

        total_count = (await self.session.execute(count_stmt)).scalar() or 0
        stmt = stmt.order_by(EvidenceRecord.created_at.desc()).offset(skip).limit(limit)
        items = (await self.session.execute(stmt)).scalars().all()

        return list(items), total_count

    async def create(self, record: EvidenceRecord) -> EvidenceRecord:
        self.session.add(record)
        await self.session.flush()
        return record

    async def update(self, evidence_id: str, **fields) -> Optional[EvidenceRecord]:
        record = await self.get_by_id(evidence_id)
        if record:
            for k, v in fields.items():
                if hasattr(record, k) and v is not None:
                    setattr(record, k, v)
            await self.session.flush()
        return record

    async def delete(self, evidence_id: str) -> bool:
        record = await self.get_by_id(evidence_id)
        if record:
            await self.session.delete(record)
            await self.session.flush()
            return True
        return False
