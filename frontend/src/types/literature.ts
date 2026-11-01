export interface Publication {
  id: string;
  pmid?: string;
  pmc_id?: string;
  doi?: string;
  title: string;
  abstract?: string;
  authors?: string;
  journal?: string;
  year?: number;
  source: string;
  publication_type?: string;
  url?: string;
  citation_count?: number;
  notes?: string;
  is_favorite?: boolean;
  project_id?: string;
  created_at: string;
  updated_at?: string;
}

export interface PublicationSearchParams {
  query: string;
  source?: string;
  max_results?: number;
  year_start?: number;
  year_end?: number;
  open_access_only?: boolean;
}

export interface PublicationSearchResult {
  title: string;
  pmid?: string;
  pmc_id?: string;
  doi?: string;
  authors: string[];
  journal?: string;
  year?: number;
  abstract?: string;
  publication_type?: string;
  source: string;
  url?: string;
  is_open_access: boolean;
  is_saved: boolean;
  saved_id?: string;
}
