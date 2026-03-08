"""Tests for service-to-service authentication."""

import pytest
from httpx import AsyncClient


@pytest.mark.unit
async def test_invoke_without_service_key_returns_422(async_client: AsyncClient) -> None:
    """Test that missing X-Service-Key header returns 422."""
    response = await async_client.post("/api/v1/agent/invoke", json={})
    assert response.status_code == 422


@pytest.mark.unit
async def test_invoke_with_invalid_service_key_returns_403(
    async_client: AsyncClient,
    sample_agent_config: dict[str, object],
) -> None:
    """Test that invalid service key returns 403."""
    response = await async_client.post(
        "/api/v1/agent/invoke",
        json=sample_agent_config,
        headers={"X-Service-Key": "wrong-key"},
    )
    assert response.status_code == 403


@pytest.mark.unit
async def test_invoke_with_valid_service_key_is_accepted(
    async_client: AsyncClient,
    service_key_header: dict[str, str],
    sample_agent_config: dict[str, object],
) -> None:
    """Test that valid service key is accepted (may fail on execution, but auth passes)."""
    response = await async_client.post(
        "/api/v1/agent/invoke",
        json=sample_agent_config,
        headers=service_key_header,
    )
    assert response.status_code == 200
