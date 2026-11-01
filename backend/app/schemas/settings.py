"""
Pydantic schemas for system settings and provider diagnostics.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class SystemSettingsRead(BaseModel):
    app_name: str
    app_version: str
    host: str
    port: int
    data_dir: str
    structures_dir: str
    reports_dir: str
    ncbi_email_configured: bool
    ncbi_api_key_configured: bool
    llm_provider: str
    llm_model: str
    privacy_mode: bool
    pubmed_rate_limit: float
    europe_pmc_rate_limit: float


class SystemSettingsUpdate(BaseModel):
    ncbi_email: Optional[str] = None
    ncbi_api_key: Optional[str] = None
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None
    llm_api_key: Optional[str] = None
    llm_base_url: Optional[str] = None
    privacy_mode: Optional[bool] = None


class ProviderStatusResponse(BaseModel):
    provider: str
    is_available: bool
    is_configured: bool
    requires_api_key: bool
    message: str
