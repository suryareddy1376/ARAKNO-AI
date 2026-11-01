"""
FASTA sequence parser and validator.
Supports multi-sequence FASTA files, format validation, and conversion.
"""

import io
from typing import List, Dict, Any, Tuple
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


def parse_fasta_string(fasta_text: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Parse a FASTA string into structured sequence records.
    Returns (records_list, warnings_list).
    """
    records = []
    warnings = []
    
    if not fasta_text or not fasta_text.strip():
        return records, ["Empty FASTA input provided"]

    # If user provided a raw sequence without a header, add a default header
    clean_text = fasta_text.strip()
    if not clean_text.startswith(">"):
        clean_text = ">seq_1 Input Sequence\n" + clean_text

    handle = io.StringIO(clean_text)
    try:
        for record in SeqIO.parse(handle, "fasta"):
            seq_str = str(record.seq).strip().upper()
            if not seq_str:
                warnings.append(f"Sequence '{record.id}' is empty.")
                continue

            records.append({
                "id": record.id,
                "description": record.description,
                "sequence": seq_str,
                "length": len(seq_str),
            })
    except Exception as e:
        warnings.append(f"Parsing error: {str(e)}")

    return records, warnings


def format_as_fasta(records: List[Dict[str, Any]]) -> str:
    """Export sequence records back to standard FASTA format."""
    out = io.StringIO()
    seq_records = []
    for r in records:
        rec = SeqRecord(
            Seq(r["sequence"]),
            id=r.get("id", "seq"),
            description=r.get("description", ""),
        )
        seq_records.append(rec)
    SeqIO.write(seq_records, out, "fasta")
    return out.getvalue()
