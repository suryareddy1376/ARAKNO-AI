export interface SequenceRecord {
  id: string;
  description?: string;
  sequence: string;
  length: number;
  molecular_weight?: number;
  amino_acid_composition?: Record<string, number>;
  gc_content?: number;
  isoelectric_point?: number;
}

export interface FastaAnalysisResponse {
  success: boolean;
  total_sequences: number;
  sequences: SequenceRecord[];
  warnings: string[];
}

export interface SequenceComparisonResponse {
  alignment_score: number;
  identity_percentage: number;
  similarity_percentage: number;
  aligned_seq1: string;
  aligned_seq2: string;
  alignment_length: number;
  matches: number;
  gaps: number;
}

export interface StructureAnalysisResponse {
  format: string;
  chains: string[];
  total_residues: number;
  total_atoms: number;
  residue_counts: Record<string, number>;
  mean_b_factor_or_plddt?: number;
  missing_residues: string[];
}
