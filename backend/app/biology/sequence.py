"""
Sequence analysis utilities: composition, molecular weight, pairwise alignment.
"""

from typing import Dict, Any, Tuple
from collections import Counter
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from Bio.SeqUtils import gc_fraction
from Bio.Align import PairwiseAligner


# Standard amino acid molecular weights (Da)
AA_WEIGHTS = {
    'A': 89.09, 'R': 174.20, 'N': 132.12, 'D': 133.10, 'C': 121.16,
    'E': 147.13, 'Q': 146.15, 'G': 75.07, 'H': 155.16, 'I': 131.17,
    'L': 131.17, 'K': 146.19, 'M': 149.21, 'F': 165.19, 'P': 115.13,
    'S': 105.09, 'T': 119.12, 'W': 204.23, 'Y': 181.19, 'V': 117.15
}


def analyze_protein_sequence(sequence: str) -> Dict[str, Any]:
    """Calculate amino acid composition, molecular weight, and pI."""
    clean_seq = sequence.strip().upper()
    valid_aas = set(AA_WEIGHTS.keys())

    # Count amino acids
    counts = Counter(clean_seq)
    total_len = len(clean_seq)
    composition = {}
    for aa in sorted(valid_aas):
        composition[aa] = round((counts.get(aa, 0) / max(total_len, 1)) * 100, 2)

    # Use Biopython ProtParam if sequence has only standard amino acids
    mw = None
    pi = None
    try:
        # Filter only standard amino acids for ProtParam
        filtered_seq = "".join([c for c in clean_seq if c in valid_aas])
        if filtered_seq:
            analysed = ProteinAnalysis(filtered_seq)
            mw = round(analysed.molecular_weight(), 2)
            pi = round(analysed.isoelectric_point(), 2)
    except Exception:
        # Fallback simple MW estimate
        raw_weight = sum(AA_WEIGHTS.get(aa, 110.0) for aa in clean_seq) - max(0, total_len - 1) * 18.015
        mw = round(raw_weight, 2)

    return {
        "length": total_len,
        "molecular_weight": mw,
        "isoelectric_point": pi,
        "amino_acid_composition": composition,
    }


def analyze_nucleotide_sequence(sequence: str) -> Dict[str, Any]:
    """Calculate GC content and length for DNA/RNA sequences."""
    clean_seq = sequence.strip().upper()
    total_len = len(clean_seq)
    gc = round(gc_fraction(clean_seq) * 100, 2) if total_len > 0 else 0.0

    return {
        "length": total_len,
        "gc_content": gc,
    }


def align_sequences(seq1: str, seq2: str, mode: str = "global") -> Dict[str, Any]:
    """
    Perform pairwise sequence alignment using Biopython PairwiseAligner.
    mode: 'global' or 'local'.
    """
    s1 = seq1.strip().upper()
    s2 = seq2.strip().upper()

    aligner = PairwiseAligner()
    aligner.mode = mode.lower() if mode.lower() in ("global", "local") else "global"

    score = aligner.score(s1, s2)
    alignments = aligner.align(s1, s2)

    try:
        best = next(iter(alignments))
        al_seq1 = str(best[0])
        al_seq2 = str(best[1])
        al_len = len(al_seq1)
        matches = sum(1 for a, b in zip(al_seq1, al_seq2) if a == b and a != "-")
        gaps = sum(1 for a, b in zip(al_seq1, al_seq2) if a == "-" or b == "-")
        identity = round((matches / max(al_len, 1)) * 100, 2)
    except Exception:
        al_seq1 = s1
        al_seq2 = s2
        al_len = max(len(s1), len(s2))
        matches = sum(1 for a, b in zip(s1, s2) if a == b)
        gaps = abs(len(s1) - len(s2))
        identity = round((matches / max(al_len, 1)) * 100, 2)

    return {
        "alignment_score": float(score),
        "identity_percentage": identity,
        "similarity_percentage": identity,
        "aligned_seq1": al_seq1,
        "aligned_seq2": al_seq2,
        "alignment_length": al_len,
        "matches": matches,
        "gaps": gaps,
    }
