"""
Test computational biology endpoints: FASTA, alignment, structure parsing.
"""

import pytest


@pytest.mark.asyncio
async def test_fasta_analysis(client):
    fasta_payload = {
        "fasta_text": ">sp|P02452|CO1A1_HUMAN Collagen alpha-1(I) chain\nMFSFVDLRLLLLLAATALLTHGQEEGQVEGQDEDIPPVT",
        "sequence_type": "protein"
    }
    response = await client.post("/api/v1/biology/fasta/analyze", json=fasta_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["total_sequences"] == 1
    seq = data["sequences"][0]
    assert seq["length"] == 39
    assert seq["molecular_weight"] is not None
    assert "G" in seq["amino_acid_composition"]


@pytest.mark.asyncio
async def test_sequence_comparison(client):
    cmp_payload = {
        "seq1": "MKWVTFISLL",
        "seq2": "MKWVTFISLL",
        "comparison_type": "global"
    }
    response = await client.post("/api/v1/biology/sequences/compare", json=cmp_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["identity_percentage"] == 100.0
    assert data["alignment_score"] > 0


@pytest.mark.asyncio
async def test_protein_gene_symbol_resolution(client):
    """Verify that gene symbol 'ACTB' resolves to human beta-actin entry P60709."""
    response = await client.get("/api/v1/proteins/ACTB")
    assert response.status_code == 200
    data = response.json()
    assert data["gene_name"] == "ACTB"
    assert data["accession"] == "P60709"
    assert data["sequence_length"] == 375
