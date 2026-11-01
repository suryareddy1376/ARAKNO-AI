export interface ResearchDivision {
  id: number;
  name: string;
  slug: string;
  description?: string;
  color: string;
  icon: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ResearchQuestion {
  id: string;
  project_id: string;
  question: string;
  hypothesis?: string;
  status: 'open' | 'investigating' | 'answered' | 'closed';
  priority: number;
  answer?: string;
  created_at: string;
  updated_at: string;
}

export interface ResearchProject {
  id: string;
  title: string;
  description?: string;
  division_id?: number;
  division?: ResearchDivision;
  status: 'active' | 'paused' | 'completed' | 'archived';
  tags?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
  questions: ResearchQuestion[];
}

export interface ResearchJob {
  id: string;
  job_type: string;
  query: string;
  parameters?: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
  progress: number;
  result?: string;
  error_message?: string;
  started_at?: string;
  completed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface ResearchRunRequest {
  query: string;
  project_id?: string;
  division_slug?: string;
  sources: string[];
  max_results: number;
  synthesize_ai: boolean;
}
