"""
Tests for LLM integration and provider settings.
"""

import pytest
from app.core.config import get_settings
from app.llm.client import LLMClient


def test_llm_settings_nvidia_validation():
    """Verify that 'nvidia' is an accepted llm_provider."""
    settings = get_settings()
    original_provider = settings.llm_provider
    try:
        settings.llm_provider = "nvidia"
        assert settings.llm_provider == "nvidia"
    finally:
        settings.llm_provider = original_provider


def test_llm_client_disabled_by_default():
    """Verify that by default LLM client is disabled."""
    client = LLMClient()
    assert client.is_enabled is False


@pytest.mark.asyncio
async def test_llm_client_fallback_when_disabled():
    """Verify that client returns empty strings when disabled."""
    client = LLMClient()
    content, reasoning = await client.generate_completion("Test prompt")
    assert content == ""
    assert reasoning == ""
