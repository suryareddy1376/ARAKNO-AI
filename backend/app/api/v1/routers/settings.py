"""
Settings and LLM provider configuration API router.
Enforces privacy rules: API keys are masked and never exposed in responses.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
import httpx

from app.core.config import get_settings
from app.schemas.settings import (
    SystemSettingsRead,
    SystemSettingsUpdate,
    ProviderStatusResponse,
)

router = APIRouter(prefix="/settings", tags=["Settings"])


@router.get("", response_model=SystemSettingsRead)
async def get_system_settings():
    """Retrieve system configuration without exposing raw API secrets."""
    settings = get_settings()

    return SystemSettingsRead(
        app_name=settings.app_name,
        app_version=settings.app_version,
        host=settings.host,
        port=settings.port,
        data_dir=settings.data_dir,
        structures_dir=settings.structures_dir,
        reports_dir=settings.reports_dir,
        ncbi_email_configured=bool(settings.ncbi_email),
        ncbi_api_key_configured=bool(settings.ncbi_api_key),
        llm_provider=settings.llm_provider,
        llm_model=settings.llm_model or "none",
        privacy_mode=settings.privacy_mode,
        pubmed_rate_limit=settings.pubmed_rate_limit,
        europe_pmc_rate_limit=settings.europe_pmc_rate_limit,
    )


@router.patch("", response_model=SystemSettingsRead)
async def update_settings(update_data: SystemSettingsUpdate):
    """Update settings in memory. Raw secrets are accepted but never returned."""
    settings = get_settings()

    if update_data.ncbi_email is not None:
        settings.ncbi_email = update_data.ncbi_email
    if update_data.ncbi_api_key is not None:
        settings.ncbi_api_key = update_data.ncbi_api_key
    if update_data.llm_provider is not None:
        settings.llm_provider = update_data.llm_provider
    if update_data.llm_model is not None:
        settings.llm_model = update_data.llm_model
    if update_data.llm_api_key is not None:
        settings.llm_api_key = update_data.llm_api_key
    if update_data.privacy_mode is not None:
        settings.privacy_mode = update_data.privacy_mode

    return await get_system_settings()


@router.get("/provider-status", response_model=List[ProviderStatusResponse])
async def get_provider_status():
    """Check availability and configuration status for each supported provider."""
    settings = get_settings()
    providers = []

    # 1. None (Default)
    providers.append(
        ProviderStatusResponse(
            provider="none",
            is_available=True,
            is_configured=settings.llm_provider == "none",
            requires_api_key=False,
            message="Zero-budget mode active. Uses deterministic literature retrieval and extraction without remote LLMs.",
        )
    )

    # 2. Ollama (Local)
    ollama_online = False
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get("http://localhost:11434/api/tags")
            ollama_online = resp.status_code == 200
    except Exception:
        ollama_online = False

    providers.append(
        ProviderStatusResponse(
            provider="ollama",
            is_available=ollama_online,
            is_configured=settings.llm_provider == "ollama",
            requires_api_key=False,
            message="Local Ollama service reachable" if ollama_online else "Ollama not running locally on port 11434",
        )
    )

    # 3. OpenRouter
    openrouter_configured = bool(settings.llm_api_key and settings.llm_provider == "openrouter")
    providers.append(
        ProviderStatusResponse(
            provider="openrouter",
            is_available=openrouter_configured,
            is_configured=openrouter_configured,
            requires_api_key=True,
            message="OpenRouter configured with API key" if openrouter_configured else "OpenRouter requires API key. Paid routes blocked by default.",
        )
    )

    # 4. Google Gemini
    gemini_configured = bool(settings.llm_api_key and settings.llm_provider == "gemini")
    providers.append(
        ProviderStatusResponse(
            provider="gemini",
            is_available=gemini_configured,
            is_configured=gemini_configured,
            requires_api_key=True,
            message="Gemini API configured" if gemini_configured else "Gemini requires API key.",
        )
    )

    # 5. NVIDIA NIM / Nemotron
    nvidia_configured = bool(settings.llm_api_key and settings.llm_provider == "nvidia")
    providers.append(
        ProviderStatusResponse(
            provider="nvidia",
            is_available=nvidia_configured,
            is_configured=nvidia_configured,
            requires_api_key=True,
            message="NVIDIA Nemotron API configured" if nvidia_configured else "NVIDIA API requires API key (https://integrate.api.nvidia.com/v1).",
        )
    )

    return providers
