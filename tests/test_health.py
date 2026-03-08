"""Tests for health endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.unit
async def test_health_returns_ok(async_client: AsyncClient) -> None:
    """Test that /health returns ok status."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.unit
async def test_ready_returns_ready(async_client: AsyncClient) -> None:
    """Test that /ready returns ready status with dotenv vault."""
    response = await async_client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
