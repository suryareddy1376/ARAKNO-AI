"""
Test health and system diagnostic endpoints.
"""

import pytest


@pytest.mark.asyncio
async def test_health_endpoint(client):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "ARAKNO-AI" in data["service"]


@pytest.mark.asyncio
async def test_system_status(client):
    response = await client.get("/api/v1/system/status")
    assert response.status_code == 200
    data = response.json()
    assert data["database_connected"] is True
    assert data["privacy_mode"] is True


@pytest.mark.asyncio
async def test_system_storage(client):
    response = await client.get("/api/v1/system/storage")
    assert response.status_code == 200
    data = response.json()
    assert "disk_total_gb" in data
    assert "disk_free_gb" in data
