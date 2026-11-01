"""
Test privacy enforcement, LLM defaults, and API key masking.
"""

import pytest


@pytest.mark.asyncio
async def test_settings_privacy_defaults(client):
    response = await client.get("/api/v1/settings")
    assert response.status_code == 200
    data = response.json()
    assert data["llm_provider"] == "none"
    assert data["privacy_mode"] is True
    # Secrets should NEVER be exposed in settings response
    assert "api_key" not in data or data.get("api_key") is None
    assert "openrouter_api_key" not in data
    assert "gemini_api_key" not in data


@pytest.mark.asyncio
async def test_provider_status_defaults(client):
    response = await client.get("/api/v1/settings/provider-status")
    assert response.status_code == 200
    providers = response.json()
    none_prov = next((p for p in providers if p["provider"] == "none"), None)
    assert none_prov is not None
    assert none_prov["is_configured"] is True
    assert none_prov["is_available"] is True
