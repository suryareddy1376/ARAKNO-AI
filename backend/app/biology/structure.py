"""
3D macromolecular structure parser (PDB / mmCIF).
Extracts chains, residues, atom counts, and AlphaFold pLDDT confidence scores.
"""

import io
from typing import Dict, Any, List, Optional
from Bio.PDB import PDBParser, MMCIFParser


def parse_structure_content(content: str, file_format: str = "pdb") -> Dict[str, Any]:
    """
    Parse PDB or mmCIF string and extract structural metrics and pLDDT.
    In AlphaFold PDB/CIF files, the B-factor column stores per-residue pLDDT (0-100).
    """
    fmt = file_format.lower()
    string_handle = io.StringIO(content)

    parser = MMCIFParser(QUIET=True) if fmt in ("cif", "mmcif") else PDBParser(QUIET=True)
    
    try:
        structure = parser.get_structure("struc", string_handle)
    except Exception as e:
        # Fallback basic PDB line scanning if parser fails
        return _fallback_pdb_scanner(content)

    chains = []
    residue_counts: Dict[str, int] = {}
    total_atoms = 0
    total_residues = 0
    b_factors = []

    for model in structure:
        for chain in model:
            c_id = chain.get_id()
            if c_id not in chains:
                chains.append(c_id)

            for residue in chain:
                # Ignore heteroatoms (water, ligands) if needed or count them
                r_name = residue.get_resname().strip()
                residue_counts[r_name] = residue_counts.get(r_name, 0) + 1
                total_residues += 1

                for atom in residue:
                    total_atoms += 1
                    b_factors.append(atom.get_bfactor())

    mean_b_factor = round(sum(b_factors) / max(len(b_factors), 1), 2) if b_factors else None

    return {
        "format": fmt,
        "chains": chains,
        "total_residues": total_residues,
        "total_atoms": total_atoms,
        "residue_counts": residue_counts,
        "mean_b_factor_or_plddt": mean_b_factor,
        "missing_residues": [],
        "secondary_structure_summary": {},
    }


def _fallback_pdb_scanner(content: str) -> Dict[str, Any]:
    """Lightweight scanner for PDB format as fallback."""
    chains = set()
    residues = set()
    b_factors = []
    atom_count = 0

    for line in content.splitlines():
        if line.startswith("ATOM  "):
            atom_count += 1
            chain_id = line[21].strip() or "A"
            res_seq = line[22:26].strip()
            res_name = line[17:20].strip()
            chains.add(chain_id)
            residues.add((chain_id, res_seq, res_name))
            try:
                bfactor = float(line[60:66].strip())
                b_factors.append(bfactor)
            except (ValueError, IndexError):
                pass

    res_counts: Dict[str, int] = {}
    for _, _, r_name in residues:
        res_counts[r_name] = res_counts.get(r_name, 0) + 1

    mean_bf = round(sum(b_factors) / max(len(b_factors), 1), 2) if b_factors else None

    return {
        "format": "pdb",
        "chains": sorted(list(chains)),
        "total_residues": len(residues),
        "total_atoms": atom_count,
        "residue_counts": res_counts,
        "mean_b_factor_or_plddt": mean_bf,
        "missing_residues": [],
        "secondary_structure_summary": {},
    }
