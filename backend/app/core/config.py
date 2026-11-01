"""
Application configuration using Pydantic Settings.

Loads configuration from environment variables and .env file.
All settings are centralized here for the entire application.
"""

import os
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _find_env_file() -> str:
    """Locate the .env file relative to project root."""
    # Look for .env in the project root (parent of backend/)
    backend_dir = Path(__file__).resolve().parent.parent.parent
    project_root = backend_dir.parent
    env_file = project_root / ".env"
    if env_file.exists():
        return str(env_file)
    # Fallback: look in backend dir
    env_in_backend = backend_dir / ".env"
    if env_in_backend.exists():
        return str(env_in_backend)
    return str(env_file)  # Return default path even if not found


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=_find_env_file(),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "ARAKNO-AI"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "development"

    # Server
    host: str = "127.0.0.1"
    port: int = 8000

    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///./data/arakno.db",
        description="SQLAlchemy database URL",
    )

    # Data directories
    data_dir: str = Field(default="./data", description="Data directory path")
    downloads_dir: str = Field(
        default="./data/downloads", description="Downloads directory"
    )
    structures_dir: str = Field(
        default="./data/structures", description="Protein structures directory"
    )
    reports_dir: str = Field(
        default="./data/reports", description="Generated reports directory"
    )

    # API Keys (all optional, privacy-first)
    ncbi_api_key: Optional[str] = Field(
        default=None, description="NCBI API key for PubMed (increases rate limit)"
    )
    ncbi_email: Optional[str] = Field(
        default=None, description="Email for NCBI E-utilities"
    )

    # LLM Settings (disabled by default)
    llm_provider: str = Field(
        default="none",
        description="LLM provider: none, openrouter, gemini, ollama, nvidia",
    )
    llm_api_key: Optional[str] = Field(
        default=None, description="API key for LLM provider"
    )
    llm_model: str = Field(
        default="", description="Model name for LLM provider"
    )
    llm_base_url: Optional[str] = Field(
        default=None, description="Base URL for LLM provider"
    )

    # Rate Limiting
    pubmed_rate_limit: float = Field(
        default=3.0,
        description="PubMed requests per second (3 without key, 10 with key)",
    )
    europe_pmc_rate_limit: float = Field(
        default=5.0, description="Europe PMC requests per second"
    )

    # Timeouts (seconds)
    default_timeout: int = Field(default=30, description="Default HTTP timeout")
    download_timeout: int = Field(
        default=120, description="File download timeout"
    )

    # File validation
    max_download_size_mb: int = Field(
        default=100, description="Maximum download file size in MB"
    )
    allowed_structure_extensions: list[str] = Field(
        default=[".pdb", ".cif", ".mmcif", ".bcif"],
        description="Allowed structure file extensions",
    )

    # Privacy
    privacy_mode: bool = Field(
        default=True, description="Enable privacy mode (no external LLM calls)"
    )
    telemetry_enabled: bool = Field(
        default=False, description="Enable telemetry collection"
    )

    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000",
                 "http://localhost:5173", "http://127.0.0.1:5173"],
        description="Allowed CORS origins (localhost only)",
    )

    @field_validator("llm_provider")
    @classmethod
    def validate_llm_provider(cls, v: str) -> str:
        """Validate LLM provider value."""
        allowed = {"none", "openrouter", "gemini", "ollama", "nvidia"}
        if v.lower() not in allowed:
            raise ValueError(f"llm_provider must be one of {allowed}")
        return v.lower()

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Ensure SQLite URL uses aiosqlite for async engine."""
        if v.startswith("sqlite:///") and not v.startswith("sqlite+aiosqlite:///"):
            return v.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
        return v

    @field_validator("pubmed_rate_limit")
    @classmethod
    def validate_pubmed_rate_limit(cls, v: float) -> float:
        """Ensure rate limit is reasonable."""
        if v <= 0 or v > 10:
            raise ValueError("pubmed_rate_limit must be between 0 and 10")
        return v

    def ensure_directories(self) -> None:
        """Create required data directories if they don't exist."""
        for dir_path in [
            self.data_dir,
            self.downloads_dir,
            self.structures_dir,
            self.reports_dir,
        ]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)

    @property
    def effective_pubmed_rate_limit(self) -> float:
        """Return effective PubMed rate limit based on API key availability."""
        if self.ncbi_api_key:
            return min(self.pubmed_rate_limit, 10.0)
        return min(self.pubmed_rate_limit, 3.0)

    @property
    def max_download_size_bytes(self) -> int:
        """Return max download size in bytes."""
        return self.max_download_size_mb * 1024 * 1024


# Singleton settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the application settings singleton."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
