export interface EvidenceRecord {
  id: string;
  claim: string;
  evidence_text?: string;
  evidence_type: string;
  strength: string;
  confidence_score?: number;
  verified: boolean;
  verification_notes?: string;
  source_section?: string;
  tags?: string;
  project_id?: string;
  publication_id?: string;
  created_at: string;
  updated_at?: string;
}

export interface EvidenceSearchParams {
  project_id?: string;
  publication_id?: string;
  evidence_type?: string;
  strength?: string;
  verified?: boolean;
  page?: number;
  page_size?: number;
}

export interface CitationVerificationResult {
  valid: boolean;
  source_found: boolean;
  title?: string;
  journal?: string;
  year?: number;
  pmid?: string;
  doi?: string;
  verification_message: string;
  matched_abstract_excerpt?: string;
}
