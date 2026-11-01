"""
SQLAlchemy ORM models for ARAKNO-AI.

Defines all database tables with proper relationships,
indexes, and constraints.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


def generate_uuid() -> str:
    """Generate a new UUID string."""
    return str(uuid.uuid4())


def utcnow() -> datetime:
    """Get current UTC timestamp."""
    return datetime.now(timezone.utc)


class ResearchDivision(Base):
    """Research division / category for organizing research."""

    __tablename__ = "research_divisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    color: Mapped[str] = mapped_column(String(7), nullable=False, default="#3B82F6")
    icon: Mapped[str] = mapped_column(String(50), nullable=False, default="folder")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    # Relationships
    projects: Mapped[list["ResearchProject"]] = relationship(
        back_populates="division", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<ResearchDivision(id={self.id}, name='{self.name}')>"


class ResearchProject(Base):
    """Research project within a division."""

    __tablename__ = "research_projects"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    division_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("research_divisions.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="active"
    )  # active, paused, completed, archived
    tags: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )  # JSON-encoded list
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    # Relationships
    division: Mapped[Optional["ResearchDivision"]] = relationship(
        back_populates="projects"
    )
    questions: Mapped[list["ResearchQuestion"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    publications: Mapped[list["Publication"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    evidence_records: Mapped[list["EvidenceRecord"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    reports: Mapped[list["ResearchReport"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_project_division", "division_id"),
        Index("idx_project_status", "status"),
        Index("idx_project_created", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<ResearchProject(id='{self.id}', title='{self.title[:50]}')>"


class ResearchQuestion(Base):
    """Research question within a project."""

    __tablename__ = "research_questions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False
    )
    question: Mapped[str] = mapped_column(Text, nullable=False)
    hypothesis: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="open"
    )  # open, investigating, answered, closed
    priority: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    # Relationships
    project: Mapped["ResearchProject"] = relationship(back_populates="questions")

    __table_args__ = (
        Index("idx_question_project", "project_id"),
        Index("idx_question_status", "status"),
    )


class Publication(Base):
    """Saved publication / literature reference."""

    __tablename__ = "publications"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    pmid: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    pmc_id: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    doi: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    authors: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON list
    journal: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    abstract: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    keywords: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON list
    publication_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    source: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pubmed"
    )  # pubmed, europe_pmc, manual
    url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    citation_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    project_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("research_projects.id", ondelete="SET NULL"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    # Relationships
    project: Mapped[Optional["ResearchProject"]] = relationship(
        back_populates="publications"
    )
    evidence_records: Mapped[list["EvidenceRecord"]] = relationship(
        back_populates="publication", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_pub_pmid", "pmid"),
        Index("idx_pub_doi", "doi"),
        Index("idx_pub_title", "title"),
        Index("idx_pub_year", "year"),
        Index("idx_pub_project", "project_id"),
        Index("idx_pub_source", "source"),
        UniqueConstraint("pmid", "source", name="uq_pub_pmid_source"),
    )

    def __repr__(self) -> str:
        return f"<Publication(id='{self.id}', pmid='{self.pmid}', title='{self.title[:50]}')>"


class Protein(Base):
    """Protein information from UniProt."""

    __tablename__ = "proteins"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    accession: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    entry_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    protein_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    gene_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    organism: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    organism_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    sequence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sequence_length: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    function_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    subcellular_location: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    go_terms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    keywords: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    database_references: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )  # JSON
    existence_evidence: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    annotation_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    # Relationships
    structures: Mapped[list["ProteinStructure"]] = relationship(
        back_populates="protein", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_protein_accession", "accession"),
        Index("idx_protein_gene", "gene_name"),
        Index("idx_protein_organism", "organism"),
    )

    def __repr__(self) -> str:
        return f"<Protein(accession='{self.accession}', name='{self.protein_name}')>"


class ProteinStructure(Base):
    """Protein 3D structure data from AlphaFold or PDB."""

    __tablename__ = "protein_structures"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    protein_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("proteins.id", ondelete="CASCADE"), nullable=False
    )
    source: Mapped[str] = mapped_column(
        String(20), nullable=False, default="alphafold"
    )  # alphafold, pdb
    structure_id: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )  # AlphaFold model ID or PDB ID
    file_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    file_format: Mapped[str] = mapped_column(
        String(10), nullable=False, default="pdb"
    )  # pdb, cif, mmcif
    resolution: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    confidence_score: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True
    )  # AlphaFold pLDDT
    confidence_data: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )  # JSON per-residue confidence
    method: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )  # X-ray, NMR, Cryo-EM, AlphaFold
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )

    # Relationships
    protein: Mapped["Protein"] = relationship(back_populates="structures")

    __table_args__ = (
        Index("idx_structure_protein", "protein_id"),
        Index("idx_structure_source", "source"),
    )


class EvidenceRecord(Base):
    """Evidence record linking claims to sources."""

    __tablename__ = "evidence_records"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    project_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("research_projects.id", ondelete="SET NULL"),
        nullable=True,
    )
    publication_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("publications.id", ondelete="SET NULL"),
        nullable=True,
    )
    claim: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evidence_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="citation"
    )  # citation, experimental, computational, review
    strength: Mapped[str] = mapped_column(
        String(20), nullable=False, default="moderate"
    )  # strong, moderate, weak, contradictory
    confidence_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verification_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_section: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )  # e.g., "Methods", "Results"
    tags: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON list
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    # Relationships
    project: Mapped[Optional["ResearchProject"]] = relationship(
        back_populates="evidence_records"
    )
    publication: Mapped[Optional["Publication"]] = relationship(
        back_populates="evidence_records"
    )

    __table_args__ = (
        Index("idx_evidence_project", "project_id"),
        Index("idx_evidence_publication", "publication_id"),
        Index("idx_evidence_type", "evidence_type"),
        Index("idx_evidence_strength", "strength"),
    )


class ResearchReport(Base):
    """Generated research report."""

    __tablename__ = "research_reports"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    project_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("research_projects.id", ondelete="SET NULL"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    report_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="summary"
    )  # summary, literature_review, evidence_map, full
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    format: Mapped[str] = mapped_column(
        String(10), nullable=False, default="markdown"
    )  # markdown, html, pdf
    file_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )  # JSON metadata
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="draft"
    )  # draft, generating, completed, failed
    word_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    # Relationships
    project: Mapped[Optional["ResearchProject"]] = relationship(
        back_populates="reports"
    )

    __table_args__ = (
        Index("idx_report_project", "project_id"),
        Index("idx_report_type", "report_type"),
        Index("idx_report_status", "status"),
    )


class ResearchJob(Base):
    """Background research job tracking."""

    __tablename__ = "research_jobs"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    job_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # literature_search, protein_analysis, evidence_extraction, full_research
    query: Mapped[str] = mapped_column(Text, nullable=False)
    parameters: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending"
    )  # pending, running, completed, failed, cancelled
    progress: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    result: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON results
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    __table_args__ = (
        Index("idx_job_type", "job_type"),
        Index("idx_job_status", "status"),
        Index("idx_job_created", "created_at"),
    )


class ResearchActivity(Base):
    """Activity log for tracking research actions."""

    __tablename__ = "research_activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    activity_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # search, save, analyze, generate, export
    description: Mapped[str] = mapped_column(Text, nullable=False)
    entity_type: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )  # publication, protein, evidence, report, project
    entity_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    metadata_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )

    __table_args__ = (
        Index("idx_activity_type", "activity_type"),
        Index("idx_activity_entity", "entity_type", "entity_id"),
        Index("idx_activity_created", "created_at"),
    )
