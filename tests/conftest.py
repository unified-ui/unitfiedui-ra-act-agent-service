"""Shared test fixtures."""

import os
from collections.abc import AsyncGenerator

import pytest
from app.main import app
from httpx import ASGITransport, AsyncClient


@pytest.fixture(autouse=True)
def _set_test_env() -> None:
    """Set test environment variables."""
    os.environ["VAULT_TYPE"] = "dotenv"
    os.environ["APP_VAULT_TYPE"] = "dotenv"
    os.environ["AGENT_TO_REACT_SERVICE_KEY"] = "test-service-key"


@pytest.fixture
def service_key_header() -> dict[str, str]:
    """Return valid service key header."""
    return {"X-Service-Key": "test-service-key"}


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient]:
    """Create an async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def sample_agent_config() -> dict[str, object]:
    """Return a sample agent invoke request body."""
    return {
        "tenant_id": "tenant-123",
        "chat_agent_id": "agent-456",
        "conversation_id": "conv-789",
        "message": "Hello, agent!",
        "history": [
            {"role": "user", "content": "Previous message"},
            {"role": "assistant", "content": "Previous response"},
        ],
        "agent_config": {
            "react_agent_id": "react-001",
            "version": 1,
            "system_prompt": "You are a helpful assistant.",
            "ai_models": [
                {
                    "provider": "OPENAI",
                    "model_name": "gpt-4o",
                    "api_key": "test-key",
                }
            ],
            "tools": [],
            "multi_agent_enabled": False,
        },
    }
