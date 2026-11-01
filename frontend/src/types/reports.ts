export interface ResearchReport {
  id: string;
  project_id?: string;
  title: string;
  report_type: string;
  content?: string;
  format: string;
  file_path?: string;
  status: string;
  word_count: number;
  created_at: string;
  updated_at: string;
}

export interface ResearchReportCreate {
  title: string;
  project_id?: string;
  report_type?: string;
  format?: string;
  content?: string;
}
