export interface SystemSettings {
  app_name: string;
  app_version: string;
  host: string;
  port: number;
  data_dir: string;
  structures_dir: string;
  reports_dir: string;
  ncbi_email_configured: boolean;
  ncbi_api_key_configured: boolean;
  llm_provider: string;
  llm_model: string;
  privacy_mode: boolean;
  pubmed_rate_limit: number;
  europe_pmc_rate_limit: number;
}

export interface ProviderStatus {
  provider: string;
  is_available: boolean;
  is_configured: boolean;
  requires_api_key: boolean;
  message: string;
}
