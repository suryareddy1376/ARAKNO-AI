"""
Repository for Protein and ProteinStructure database operations.
"""

from typing import List, Optional, Tuple
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.models import Protein, ProteinStructure


class ProteinRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, protein_id: str) -> Optional[Protein]:
        result = await self.session.execute(
            select(Protein)
            .options(selectinload(Protein.structures))
            .where(Protein.id == protein_id)
        )
        return result.scalar_one_or_none()

    async def get_by_accession(self, accession: str) -> Optional[Protein]:
        result = await self.session.execute(
            select(Protein)
            .options(selectinload(Protein.structures))
            .where(Protein.accession == accession.strip().upper())
        )
        return result.scalar_one_or_none()

    async def list_proteins(
        self,
        query: Optional[str] = None,
        organism: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> Tuple[List[Protein], int]:
        stmt = select(Protein).options(selectinload(Protein.structures))
        count_stmt = select(func.count(Protein.id))

        filters = []
        if query:
            q_term = f"%{query}%"
            filters.append(
                or_(
                    Protein.accession.ilike(q_term),
                    Protein.gene_name.ilike(q_term),
                    Protein.protein_name.ilike(q_term),
                )
            )
        if organism:
            filters.append(Protein.organism.ilike(f"%{organism}%"))

        if filters:
            for f in filters:
                stmt = stmt.where(f)
                count_stmt = count_stmt.where(f)

        total_count = (await self.session.execute(count_stmt)).scalar() or 0
        stmt = stmt.order_by(Protein.created_at.desc()).offset(skip).limit(limit)
        items = (await self.session.execute(stmt)).scalars().all()

        return list(items), total_count

    async def create_or_update(self, protein: Protein) -> Protein:
        existing = await self.get_by_accession(protein.accession)
        if existing:
            existing.protein_name = protein.protein_name or existing.protein_name
            existing.gene_name = protein.gene_name or existing.gene_name
            existing.sequence = protein.sequence or existing.sequence
            existing.sequence_length = protein.sequence_length or existing.sequence_length
            existing.function_description = protein.function_description or existing.function_description
            await self.session.flush()
            return existing
        else:
            self.session.add(protein)
            await self.session.flush()
            return protein

    async def add_structure(self, structure: ProteinStructure) -> ProteinStructure:
        self.session.add(structure)
        await self.session.flush()
        return structure

    async def get_structures(self, protein_id: str) -> List[ProteinStructure]:
        result = await self.session.execute(
            select(ProteinStructure).where(ProteinStructure.protein_id == protein_id)
        )
        return list(result.scalars().all())
