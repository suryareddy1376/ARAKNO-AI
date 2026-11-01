"""
Database configuration and session management.

Uses SQLAlchemy async engine with aiosqlite for SQLite.
Provides session factory and database initialization.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


# Engine and session factory (initialized lazily)
_engine = None
_async_session_factory = None


def get_engine():
    """Get or create the async database engine."""
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            pool_pre_ping=True,
            # SQLite-specific settings
            connect_args={"check_same_thread": False},
        )
    return _engine


def get_session_factory():
    """Get or create the async session factory."""
    global _async_session_factory
    if _async_session_factory is None:
        engine = get_engine()
        _async_session_factory = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _async_session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.

    Usage in FastAPI:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for database sessions outside of FastAPI dependencies.

    Usage:
        async with get_db_context() as db:
            result = await db.execute(...)
    """
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize the database.

    Creates all tables and seeds initial data.
    """
    from app.db.models.models import (
        ResearchDivision,
        ResearchProject,
        ResearchQuestion,
        Publication,
        Protein,
        ProteinStructure,
        EvidenceRecord,
        ResearchReport,
        ResearchJob,
        ResearchActivity,
    )

    engine = get_engine()

    # Enable WAL mode for better concurrent access (SQLite)
    async with engine.begin() as conn:
        await conn.execute(text("PRAGMA journal_mode=WAL"))
        await conn.execute(text("PRAGMA foreign_keys=ON"))

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database initialized successfully")

    # Seed divisions
    await seed_divisions()


async def seed_divisions() -> None:
    """Seed the 6 ARAKNO research divisions and initial project if they don't exist."""
    from app.db.models.models import ResearchDivision, ResearchProject, ResearchQuestion

    divisions = [
        {
            "name": "ARAKNO-SPINE",
            "slug": "arakno-spine",
            "description": "Human spinal anatomy, biomechanics, thoracolumbar deformity, vertebral fractures, osteotomies, spinal fusion biology, posterior instrumentation, pedicle screw mechanics, interbody cages, bone grafting, cage integration, pseudarthrosis, hardware removal, spinal reconstruction, and long-term spinal stability.",
            "color": "#3B82F6",
            "icon": "activity",
        },
        {
            "name": "ARAKNO-BONE",
            "slug": "arakno-bone",
            "description": "Bone biology, osteoblasts, osteoclasts, osteocytes, collagen, bone mineralization, osteogenesis, bone remodelling, bone regeneration, bone tissue engineering, osteogenesis imperfecta, and bone graft substitutes.",
            "color": "#10B981",
            "icon": "shield",
        },
        {
            "name": "ARAKNO-MUSCLE",
            "slug": "arakno-muscle",
            "description": "Skeletal muscle biology, muscle architecture, muscle fibres, actin and myosin, tendons, ligaments, connective tissues, muscle regeneration, musculoskeletal biomechanics, and physical rehabilitation research.",
            "color": "#F59E0B",
            "icon": "flame",
        },
        {
            "name": "ARAKNO-SENSE",
            "slug": "arakno-sense",
            "description": "Mechanoreceptors, sensory biology, spider trichobothria, slit sensilla, vibration detection, air movement perception, and biological sensory systems.",
            "color": "#06B6D4",
            "icon": "radar",
        },
        {
            "name": "ARAKNO-SILK",
            "slug": "arakno-silk",
            "description": "Spider silk biology, spidroins, major ampullate silk proteins, recombinant protein production, silk biomaterials, protein assembly, biomimetic fibres, tissue engineering scaffolds, and bioinspired material science.",
            "color": "#8B5CF6",
            "icon": "git-merge",
        },
        {
            "name": "ARAKNO-NEURO",
            "slug": "arakno-neuro",
            "description": "Nervous system biology, neural signalling, peripheral nerves, sensory-motor coordination, neuromuscular connections, neural regeneration, and neuroplasticity.",
            "color": "#EC4899",
            "icon": "cpu",
        },
    ]

    async with get_db_context() as db:
        from sqlalchemy import select

        result = await db.execute(select(ResearchDivision))
        existing = result.scalars().all()

        if not existing:
            div_map = {}
            for div_data in divisions:
                division = ResearchDivision(**div_data)
                db.add(division)
                div_map[div_data["name"]] = division
            await db.flush()

            # Seed initial project ARAKNO-SPINE-001
            spine_div = div_map.get("ARAKNO-SPINE")
            initial_project = ResearchProject(
                id="ARAKNO-SPINE-001",
                title="Complete Spinal Implant Independence: Evidence, Biomechanics and Regenerative Biomaterials",
                description="Investigating scientific questions concerning spinal fusion, bone healing, implant integration, structural stability, and the biological and biomechanical potential for long-term independence from spinal instrumentation.",
                division_id=spine_div.id if spine_div else None,
                status="active",
                notes="Initial flagship research project for ARAKNO-SPINE division. All clinical conclusions are labelled as research findings, not individualized medical advice.",
            )
            db.add(initial_project)
            await db.flush()

            # Seed initial research questions
            questions = [
                "What biomechanical conditions and biological fusion criteria allow for safe posterior instrumentation removal?",
                "How do bioactive regenerative biomaterials and osteoinductive scaffolds compare to autograft in achieving long-term anterior column fusion?",
                "What are the recorded pseudarthrosis and revision rates following instrumentation removal after solid thoracolumbar fusion?",
            ]
            for q_text in questions:
                q = ResearchQuestion(
                    project_id=initial_project.id,
                    question=q_text,
                    status="open",
                    priority=1,
                )
                db.add(q)

            await db.commit()
            logger.info("Seeded 6 ARAKNO research divisions and initial project ARAKNO-SPINE-001")
        else:
            logger.info(
                "Research divisions already exist",
                count=len(existing),
            )


async def close_db() -> None:
    """Close the database engine and clean up connections."""
    global _engine, _async_session_factory
    if _engine:
        await _engine.dispose()
        _engine = None
        _async_session_factory = None
        logger.info("Database connections closed")
