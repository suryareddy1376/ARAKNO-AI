"""
Pydantic schemas for research divisions, projects, and questions.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ResearchDivisionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: Optional[str] = None
    color: str
    icon: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ResearchQuestionBase(BaseModel):
    question: str
    hypothesis: Optional[str] = None
    status: str = "open"  # open, investigating, answered, closed
    priority: int = 0
    answer: Optional[str] = None


class ResearchQuestionCreate(ResearchQuestionBase):
    project_id: str


class ResearchQuestionRead(ResearchQuestionBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    project_id: str
    created_at: datetime
    updated_at: datetime


class ResearchProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    division_id: Optional[int] = None
    status: str = "active"  # active, paused, completed, archived
    tags: Optional[str] = None
    notes: Optional[str] = None


class ResearchProjectCreate(ResearchProjectBase):
    id: Optional[str] = None


class ResearchProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    division_id: Optional[int] = None
    status: Optional[str] = None
    tags: Optional[str] = None
    notes: Optional[str] = None


class ResearchProjectRead(ResearchProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
    division: Optional[ResearchDivisionRead] = None
    questions: List[ResearchQuestionRead] = []
