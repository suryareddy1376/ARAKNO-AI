"""
Test database models and repository CRUD operations.
"""

import pytest
from app.db.database import get_db_context
from app.db.models.models import ResearchDivision, ResearchProject, Publication
from app.db.repositories.publications import PublicationRepository
from app.db.repositories.projects import ProjectRepository


@pytest.mark.asyncio
async def test_divisions_seeded():
    async with get_db_context() as db:
        repo = ProjectRepository(db)
        divisions = await repo.list_divisions()
        assert len(divisions) == 6
        names = [d.name for d in divisions]
        assert "ARAKNO-SPINE" in names
        assert "ARAKNO-BONE" in names
        assert "ARAKNO-SILK" in names


@pytest.mark.asyncio
async def test_initial_project_seeded():
    async with get_db_context() as db:
        repo = ProjectRepository(db)
        proj = await repo.get_project_by_id("ARAKNO-SPINE-001")
        assert proj is not None
        assert "Spinal Implant Independence" in proj.title
        assert len(proj.questions) >= 3


@pytest.mark.asyncio
async def test_publication_crud():
    async with get_db_context() as db:
        repo = PublicationRepository(db)
        pub = Publication(
            title="Biomechanical Evaluation of Spinal Fusion Scaffolds",
            pmid="99999999",
            doi="10.1000/arakno.test.1",
            journal="Journal of Biomechanics",
            year=2024,
            abstract="Study examining cellular integration and pedicle screw stability.",
        )
        created = await repo.create(pub)
        assert created.id is not None

        found = await repo.get_by_pmid("99999999")
        assert found is not None
        assert found.title == pub.title

        # Cleanup
        await repo.delete(created.id)
        await db.commit()
