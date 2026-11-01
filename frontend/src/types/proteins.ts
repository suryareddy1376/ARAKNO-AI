export interface Protein {
  id: number;
  accession: string;
  entry_name?: string;
  protein_name: string;
  gene_name?: string;
  organism: string;
  organism_id?: number;
  sequence?: string;
  sequence_length?: number;
  molecular_weight?: number;
  function_description?: string;
  subcellular_location?: string;
  go_terms?: string[];
  ec_number?: string;
  pdb_ids?: string[];
  alphafold_id?: string;
  division?: string;
  has_structure?: boolean;
  created_at: string;
  updated_at?: string;
}

export interface ProteinStructure {
  accession: string;
  pdb_id?: string;
  source: 'alphafold' | 'pdb' | 'uploaded';
  format: 'pdb' | 'mmcif' | 'cif';
  structure_data?: string;
  structure_url?: string;
  confidence_data?: ConfidenceData;
  resolution?: number;
}

export interface ConfidenceData {
  plddt_scores?: number[];
  pae_matrix?: number[][];
  mean_plddt?: number;
}

export interface AlphaFoldPrediction {
  accession: string;
  model_url: string;
  pae_image_url?: string;
  plddt_url?: string;
  mean_plddt?: number;
  coverage?: number;
}

export interface ProteinSearchParams {
  query: string;
  organism?: string;
  gene_name?: string;
  has_structure?: boolean;
}

export interface SequenceAnalysis {
  length: number;
  molecular_weight: number;
  amino_acid_composition: Record<string, number>;
  isoelectric_point?: number;
  charge_at_ph7?: number;
  instability_index?: number;
  gravy?: number;
}

export interface AlignmentResult {
  score: number;
  identity: number;
  gaps: number;
  aligned_seq1: string;
  aligned_seq2: string;
  alignment_string: string;
}
