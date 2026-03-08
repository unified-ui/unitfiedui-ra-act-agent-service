# Testing Guide

## Framework & Tools

| Tool | Purpose |
|------|---------|
| pytest | Test runner |
| pytest-cov | Coverage measurement |
| pytest-xdist | Parallel test execution |
| pytest-asyncio | Async test support |

## Running Tests

> **IMPORTANT**: Always run pytest with `-n auto` to enable parallel test execution via pytest-xdist.

```bash
# All tests (parallel, quiet)
uv run pytest tests/ -n auto --no-header -q

# With coverage report
uv run pytest tests/ -n auto --cov=app --cov-report=html --cov-fail-under=80

# Specific module
uv run pytest tests/test_agent_executor.py -n auto -v

# By marker
uv run pytest tests/ -n auto -m unit
uv run pytest tests/ -n auto -m "not slow"

# Single test function
uv run pytest tests/test_llm_factory.py::test_create_azure_openai -v
```

## Directory Structure

Tests are in a flat structure in `tests/`:

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_health.py           # Health endpoint tests
├── test_agent_executor.py   # Agent executor service tests
├── test_llm_factory.py      # LLM factory tests
├── test_vault.py            # Vault implementation tests
├── test_auth.py             # Authentication tests
├── test_config.py           # Configuration tests
└── test_models.py           # Pydantic model tests
```

## Conventions

- **File naming**: `test_<module>.py`
- **Function naming**: `test_<behavior_under_test>` — be descriptive
- **Markers**: use `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.slow`
- **Fixtures**: place shared fixtures in `conftest.py`
- **Coverage**: minimum **80%** — CI will fail below this threshold

## Patterns

### Unit Tests

```python
def test_create_llm_azure_openai() -> None:
    """Azure OpenAI LLM should be created with correct parameters."""
    config = AIModelConfig(
        provider="AZURE_OPENAI",
        endpoint="https://example.openai.azure.com",
        deployment_name="gpt-4o",
        api_version="2024-02-15-preview",
        api_key="test-key",
    )
    llm = create_llm(config)
    assert isinstance(llm, BaseChatModel)
```

### Async Tests

```python
import pytest

@pytest.mark.asyncio
async def test_agent_execution_streams_events() -> None:
    """Agent execution should yield SSE events."""
    executor = AgentExecutorService()
    events = [e async for e in executor.execute(request)]
    assert len(events) > 0
```

### Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("provider,expected_class", [
    ("AZURE_OPENAI", "AzureChatOpenAI"),
    ("OPENAI", "ChatOpenAI"),
    ("ANTHROPIC", "ChatAnthropic"),
])
def test_create_llm_provider(provider: str, expected_class: str) -> None:
    config = AIModelConfig(provider=provider, ...)
    llm = create_llm(config)
    assert type(llm).__name__ == expected_class
```

### Mocking External Services

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_vault_get_secret() -> None:
    """Vault should return secret from underlying provider."""
    with patch.object(AzureKeyVault, "_client") as mock_client:
        mock_client.get_secret.return_value = Mock(value="secret-value")
        vault = AzureKeyVault(vault_url="https://example.vault.azure.net")
        result = vault.get_secret("my-key")
        assert result == "secret-value"
```

## Fixtures

Common fixtures in `conftest.py`:

```python
import pytest
from app.models import AgentInvokeRequest, AgentConfig

@pytest.fixture
def sample_agent_config() -> AgentConfig:
    """Sample agent configuration for testing."""
    return AgentConfig(
        react_agent_id="test-agent",
        system_prompt="You are a helpful assistant.",
        ai_models=[...],
    )

@pytest.fixture
def sample_invoke_request(sample_agent_config: AgentConfig) -> AgentInvokeRequest:
    """Sample invoke request for testing."""
    return AgentInvokeRequest(
        tenant_id="test-tenant",
        message="Hello",
        agent_config=sample_agent_config,
    )
```
