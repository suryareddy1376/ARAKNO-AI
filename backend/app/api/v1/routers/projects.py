"""
Research project and research division API router.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_db
from app.db.models.models import ResearchProject, ResearchDivision, ResearchQuestion, ResearchActivity
from app.db.repositories.projects import ProjectRepository
from app.schemas.projects import (
    ResearchProjectCreate,
    ResearchProjectRead,
    ResearchProjectUpdate,
    ResearchDivisionRead,
    ResearchQuestionCreate,
    ResearchQuestionRead,
)

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/divisions", response_model=List[ResearchDivisionRead])
async def list_divisions(db: AsyncSession = Depends(get_db)):
    """List the 6 independent ARAKNO research divisions."""
    repo = ProjectRepository(db)
    divisions = await repo.list_divisions()
    return [ResearchDivisionRead.model_validate(d) for d in divisions]


@router.get("", response_model=List[ResearchProjectRead])
async def list_projects(
    division_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List all research projects with optional division and status filters."""
    repo = ProjectRepository(db)
    projects, _ = await repo.list_projects(division_id=division_id, status=status, limit=100)
    return [ResearchProjectRead.model_validate(p) for p in projects]


@router.post("", response_model=ResearchProjectRead)
async def create_project(
    project_in: ResearchProjectCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new scientific research project."""
    repo = ProjectRepository(db)
    proj_data = project_in.model_dump()
    if not proj_data.get("id"):
        proj_data.pop("id", None)
    project = ResearchProject(**proj_data)
    created = await repo.create_project(project)

    activity = ResearchActivity(
        activity_type="create",
        description=f"Created project: '{created.title}'",
        entity_type="project",
        entity_id=created.id,
    )
    db.add(activity)
    await db.commit()

    # Re-fetch with relationships
    full = await repo.get_project_by_id(created.id)
    return ResearchProjectRead.model_validate(full)


@router.get("/{project_id}", response_model=ResearchProjectRead)
async def get_project(
    project_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get project details, linked research questions, and division."""
    repo = ProjectRepository(db)
    project = await repo.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ResearchProjectRead.model_validate(project)


@router.patch("/{project_id}", response_model=ResearchProjectRead)
async def update_project(
    project_id: str,
    update_data: ResearchProjectUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update project status, description, notes, or tags."""
    repo = ProjectRepository(db)
    updated = await repo.update_project(project_id, **update_data.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found")
    await db.commit()
    full = await repo.get_project_by_id(project_id)
    return ResearchProjectRead.model_validate(full)


@router.post("/{project_id}/questions", response_model=ResearchQuestionRead)
async def add_research_question(
    project_id: str,
    q_in: ResearchQuestionCreate,
    db: AsyncSession = Depends(get_db),
):
    """Add a new research question to an existing project."""
    repo = ProjectRepository(db)
    project = await repo.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    question = ResearchQuestion(
        project_id=project_id,
        question=q_in.question,
        hypothesis=q_in.hypothesis,
        status=q_in.status,
        priority=q_in.priority,
    )
    created = await repo.add_question(question)
    await db.commit()
    return ResearchQuestionRead.model_validate(created)
