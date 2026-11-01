"""
Protein structure and UniProt exploration API router.
Supports accession resolution, UniProt metadata, AlphaFold DB models, and structure downloads.
"""

from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_db
from app.db.models.models import Protein, ProteinStructure, ResearchActivity
from app.db.repositories.proteins import ProteinRepository
from app.integrations.uniprot.client import UniProtClient
from app.integrations.alphafold.client import AlphaFoldClient
from app.schemas.proteins import (
    ProteinRead,
    ProteinCreate,
    ProteinResolveRequest,
    AlphaFoldPredictionInfo,
    ProteinStructureRead,
)

router = APIRouter(prefix="/proteins", tags=["Proteins"])


@router.post("/resolve-accession")
async def resolve_accession(req: ProteinResolveRequest):
    """Resolve a gene symbol, protein name, or keyword to verified UniProt accessions."""
    client = UniProtClient()
    results = await client.search(req.query, limit=10)
    return results


@router.get("/search")
async def search_proteins(
    query: str,
    organism: Optional[str] = "Homo sapiens",
    db: AsyncSession = Depends(get_db),
):
    """Search UniProt and local database for proteins matching query."""
    client = UniProtClient()
    uniprot_results = await client.search(query, organism=organism, limit=10)
    return uniprot_results


@router.get("/{accession}")
async def get_protein(
    accession: str,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve verified protein details from local database or UniProt. Supports accession or gene symbol."""
    clean_acc = accession.strip().upper()
    repo = ProteinRepository(db)

    # Check local database first by accession
    local = await repo.get_by_accession(clean_acc)
    if local:
        return ProteinRead.model_validate(local)

    # Query UniProt API directly
    client = UniProtClient()
    entry = await client.get_entry(clean_acc)

    # If direct accession lookup returned 404, clean_acc may be a gene symbol (e.g. ACTB, GAPDH, BMP2)
    if not entry:
        candidates = await client.search(clean_acc, limit=1)
        if candidates:
            entry = candidates[0]

    if not entry:
        raise HTTPException(
            status_code=404,
            detail=f"Protein '{clean_acc}' not found in UniProt by accession or gene symbol",
        )

    return entry


@router.get("/{accession}/structures")
async def get_protein_structures(
    accession: str,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve AlphaFold prediction metadata for a protein by accession or gene symbol."""
    clean_acc = accession.strip().upper()
    client = AlphaFoldClient()
    predictions = await client.get_prediction(clean_acc)

    # If not found directly, clean_acc may be a gene symbol; resolve accession first
    if not predictions:
        uniprot_client = UniProtClient()
        candidates = await uniprot_client.search(clean_acc, limit=1)
        if candidates and candidates[0].get("accession"):
            resolved_acc = candidates[0]["accession"]
            predictions = await client.get_prediction(resolved_acc)

    if not predictions:
        return []
    return predictions


@router.post("/{accession}/download")
async def download_structure(
    accession: str,
    format: str = Query(default="pdb", pattern="^(pdb|cif)$"),
    db: AsyncSession = Depends(get_db),
):
    """Download AlphaFold structure file to local disk and record in database."""
    clean_acc = accession.strip().upper()
    af_client = AlphaFoldClient()
    predictions = await af_client.get_prediction(clean_acc)

    # Resolve gene symbol to accession if needed
    if not predictions:
        uniprot_client = UniProtClient()
        candidates = await uniprot_client.search(clean_acc, limit=1)
        if candidates and candidates[0].get("accession"):
            clean_acc = candidates[0]["accession"]
            predictions = await af_client.get_prediction(clean_acc)

    if not predictions:
        raise HTTPException(status_code=404, detail="No AlphaFold model found for this protein")

    pred = predictions[0]
    download_url = pred.get("pdbUrl") if format == "pdb" else pred.get("cifUrl")
    if not download_url:
        raise HTTPException(status_code=404, detail=f"No {format.upper()} file URL provided by AlphaFold")

    filename = f"{clean_acc}_{pred.get('entryId', 'model')}.{format}"
    local_path = await af_client.download_structure_file(download_url, filename)

    if not local_path:
        raise HTTPException(status_code=500, detail="Failed to download structure file")

    # Persist or update in database
    repo = ProteinRepository(db)
    protein = await repo.get_by_accession(clean_acc)
    if not protein:
        # Fetch from UniProt to populate protein entry
        uniprot_client = UniProtClient()
        u_entry = await uniprot_client.get_entry(clean_acc)
        protein = Protein(
            accession=clean_acc,
            protein_name=u_entry.get("protein_name") if u_entry else clean_acc,
            gene_name=u_entry.get("gene_name") if u_entry else None,
            organism=u_entry.get("organism") if u_entry else "Homo sapiens",
            sequence=u_entry.get("sequence") if u_entry else None,
            sequence_length=u_entry.get("sequence_length") if u_entry else None,
        )
        protein = await repo.create_or_update(protein)

    structure = ProteinStructure(
        protein_id=protein.id,
        source="alphafold",
        structure_id=pred.get("entryId"),
        file_path=local_path,
        file_format=format,
        confidence_score=pred.get("globalPlddt"),
    )
    await repo.add_structure(structure)

    activity = ResearchActivity(
        activity_type="download",
        description=f"Downloaded AlphaFold model for {clean_acc} (pLDDT: {pred.get('globalPlddt')})",
        entity_type="protein",
        entity_id=protein.id,
    )
    db.add(activity)
    await db.commit()

    return {
        "success": True,
        "local_path": local_path,
        "filename": filename,
        "confidence_score": pred.get("globalPlddt"),
    }


@router.get("/{accession}/structure-content")
async def get_structure_content(
    accession: str,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve raw text content of downloaded structure file for 3Dmol viewer."""
    clean_acc = accession.strip().upper()
    repo = ProteinRepository(db)
    protein = await repo.get_by_accession(clean_acc)

    # Resolve gene symbol to accession if needed
    if not protein:
        uniprot_client = UniProtClient()
        candidates = await uniprot_client.search(clean_acc, limit=1)
        if candidates and candidates[0].get("accession"):
            clean_acc = candidates[0]["accession"]
            protein = await repo.get_by_accession(clean_acc)

    # First check if locally saved
    if protein and protein.structures:
        for s in protein.structures:
            if s.file_path and Path(s.file_path).exists():
                content = Path(s.file_path).read_text(encoding="utf-8", errors="replace")
                return PlainTextResponse(content)

    # If not saved locally yet, fetch directly from AlphaFold PDB URL
    af_client = AlphaFoldClient()
    preds = await af_client.get_prediction(clean_acc)
    if preds and preds[0].get("pdbUrl"):
        pdb_url = preds[0]["pdbUrl"]
        filename = f"{clean_acc}_model.pdb"
        local_path = await af_client.download_structure_file(pdb_url, filename)
        if local_path and Path(local_path).exists():
            content = Path(local_path).read_text(encoding="utf-8", errors="replace")
            return PlainTextResponse(content)

    raise HTTPException(status_code=404, detail="Structure file content not available")


@router.post("/save", response_model=ProteinRead)
async def save_protein(
    protein_in: ProteinCreate,
    db: AsyncSession = Depends(get_db),
):
    """Save protein entry into local database."""
    repo = ProteinRepository(db)
    protein = Protein(**protein_in.model_dump())
    saved = await repo.create_or_update(protein)
    await db.commit()
    return ProteinRead.model_validate(saved)
