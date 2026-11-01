"""
Computational biology API router using Biopython.
Provides FASTA analysis, pairwise sequence alignment, and macromolecular structure parsing.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional

from app.biology.fasta import parse_fasta_string
from app.biology.sequence import (
    analyze_protein_sequence,
    analyze_nucleotide_sequence,
    align_sequences,
)
from app.biology.structure import parse_structure_content
from app.schemas.biology import (
    FastaAnalysisRequest,
    FastaAnalysisResponse,
    SequenceRecord,
    SequenceComparisonRequest,
    SequenceComparisonResponse,
    StructureAnalysisRequest,
    StructureAnalysisResponse,
)

router = APIRouter(prefix="/biology", tags=["Computational Biology"])


@router.post("/fasta/analyze", response_model=FastaAnalysisResponse)
async def analyze_fasta(request: FastaAnalysisRequest):
    """Parse and analyze FASTA sequences from JSON text input."""
    fasta_text = request.fasta_text or ""
    seq_type = request.sequence_type or "protein"

    if not fasta_text.strip():
        raise HTTPException(status_code=400, detail="Must provide fasta_text.")

    return _process_fasta_text(fasta_text, seq_type)


@router.post("/fasta/upload", response_model=FastaAnalysisResponse)
async def upload_fasta(
    file: UploadFile = File(...),
    sequence_type: str = Form("protein"),
):
    """Parse and analyze FASTA sequences from an uploaded file."""
    content = await file.read()
    fasta_text = content.decode("utf-8", errors="replace")
    if not fasta_text.strip():
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    return _process_fasta_text(fasta_text, sequence_type)


def _process_fasta_text(fasta_text: str, seq_type: str) -> FastaAnalysisResponse:
    """Internal helper to parse and compute sequence metrics."""
    raw_records, warnings = parse_fasta_string(fasta_text)
    if not raw_records and not warnings:
        warnings.append("No valid FASTA records found in input.")

    records = []
    for r in raw_records:
        seq = r["sequence"]
        mw = None
        comp = None
        gc = None
        pi = None

        if seq_type.lower() in ("nucleotide", "dna", "rna"):
            nuc_stats = analyze_nucleotide_sequence(seq)
            gc = nuc_stats["gc_content"]
        else:
            prot_stats = analyze_protein_sequence(seq)
            mw = prot_stats["molecular_weight"]
            comp = prot_stats["amino_acid_composition"]
            pi = prot_stats["isoelectric_point"]

        records.append(
            SequenceRecord(
                id=r["id"],
                description=r.get("description"),
                sequence=seq,
                length=r["length"],
                molecular_weight=mw,
                amino_acid_composition=comp,
                gc_content=gc,
                isoelectric_point=pi,
            )
        )

    return FastaAnalysisResponse(
        success=len(records) > 0,
        total_sequences=len(records),
        sequences=records,
        warnings=warnings,
    )


@router.post("/sequences/compare", response_model=SequenceComparisonResponse)
async def compare_sequences(request: SequenceComparisonRequest):
    """Execute global or local pairwise sequence alignment."""
    if not request.seq1.strip() or not request.seq2.strip():
        raise HTTPException(status_code=400, detail="Both sequences must be provided.")

    result = align_sequences(request.seq1, request.seq2, mode=request.comparison_type)
    return SequenceComparisonResponse(**result)


@router.post("/structures/analyze", response_model=StructureAnalysisResponse)
async def analyze_structure(
    file: Optional[UploadFile] = File(None),
    format: str = Form("pdb"),
):
    """Parse an uploaded 3D macromolecular structure (PDB or mmCIF) and summarize metrics."""
    if not file:
        raise HTTPException(status_code=400, detail="Please upload a structure file.")

    content_bytes = await file.read()
    content_str = content_bytes.decode("utf-8", errors="replace")

    res = parse_structure_content(content_str, file_format=format)
    return StructureAnalysisResponse(**res)
