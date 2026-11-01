export interface DashboardStatistics {
  total_publications: number;
  total_proteins: number;
  total_structures: number;
  total_evidence_records: number;
  total_projects: number;
  total_reports: number;
  active_jobs: number;
}

export interface ActivityItem {
  id: number;
  activity_type: string;
  description: string;
  entity_type?: string;
  entity_id?: string;
  created_at: string;
}

export interface PublicationsByMonthItem {
  month: string;
  count: number;
}

export interface DivisionStatsItem {
  division_name: string;
  division_slug: string;
  color: string;
  project_count: number;
  publication_count: number;
}

export interface EvidenceDistributionItem {
  strength: string;
  count: number;
}

export interface DashboardOverviewResponse {
  statistics: DashboardStatistics;
  recent_activities: ActivityItem[];
  publications_by_month: PublicationsByMonthItem[];
  division_distribution: DivisionStatsItem[];
  evidence_distribution: EvidenceDistributionItem[];
  backend_status: string;
}
