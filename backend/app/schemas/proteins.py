"""
Pydantic schemas for proteins and AlphaFold structures.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProteinStructureBase(BaseModel):
    source: str = "alphafold"  # alphafold, pdb
    structure_id: Optional[str] = None
    file_path: Optional[str] = None
    file_format: str = "pdb"
    resolution: Optional[float] = None
    confidence_score: Optional[float] = None  # pLDDT
    confidence_data: Optional[str] = None  # JSON string
    method: Optional[str] = None


class ProteinStructureRead(ProteinStructureBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    protein_id: str
    created_at: datetime


class ProteinBase(BaseModel):
    accession: str
    entry_name: Optional[str] = None
    protein_name: Optional[str] = None
    gene_name: Optional[str] = None
    organism: Optional[str] = None
    organism_id: Optional[int] = None
    sequence: Optional[str] = None
    sequence_length: Optional[int] = None
    function_description: Optional[str] = None
    subcellular_location: Optional[str] = None
    go_terms: Optional[str] = None
    keywords: Optional[str] = None
    database_references: Optional[str] = None
    existence_evidence: Optional[str] = None
    annotation_score: Optional[int] = None


class ProteinCreate(ProteinBase):
    pass


class ProteinRead(ProteinBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
    structures: List[ProteinStructureRead] = []


class ProteinResolveRequest(BaseModel):
    query: str  # gene symbol, accession, or protein name


class AlphaFoldPredictionInfo(BaseModel):
    entry_id: str
    gene: Optional[str] = None
    uniprot_accession: str
    uniprot_id: Optional[str] = None
    uniprot_description: Optional[str] = None
    tax_id: Optional[int] = None
    organism_scientific_name: Optional[str] = None
    pdb_url: Optional[str] = None
    cif_url: Optional[str] = None
    pae_image_url: Optional[str] = None
    pae_doc_url: Optional[str] = None
    global_plddt: Optional[float] = None
    model_version: Optional[int] = None
