"""
Pydantic schemas for computational biology operations.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class FastaAnalysisRequest(BaseModel):
    fasta_text: Optional[str] = None
    sequence_type: str = "protein"  # protein, dna, rna


class SequenceRecord(BaseModel):
    id: str
    description: Optional[str] = None
    sequence: str
    length: int
    molecular_weight: Optional[float] = None
    amino_acid_composition: Optional[Dict[str, float]] = None
    gc_content: Optional[float] = None
    isoelectric_point: Optional[float] = None


class FastaAnalysisResponse(BaseModel):
    success: bool
    total_sequences: int
    sequences: List[SequenceRecord]
    warnings: List[str] = []


class SequenceComparisonRequest(BaseModel):
    seq1: str
    seq2: str
    seq1_id: str = "Sequence 1"
    seq2_id: str = "Sequence 2"
    comparison_type: str = "global"  # global, local


class SequenceComparisonResponse(BaseModel):
    alignment_score: float
    identity_percentage: float
    similarity_percentage: float
    aligned_seq1: str
    aligned_seq2: str
    alignment_length: int
    matches: int
    gaps: int


class StructureAnalysisRequest(BaseModel):
    structure_content: Optional[str] = None
    file_format: str = "pdb"  # pdb, mmcif


class StructureAnalysisResponse(BaseModel):
    format: str
    chains: List[str]
    total_residues: int
    total_atoms: int
    residue_counts: Dict[str, int]
    mean_b_factor_or_plddt: Optional[float] = None
    missing_residues: List[str] = []
    secondary_structure_summary: Optional[Dict[str, int]] = None
