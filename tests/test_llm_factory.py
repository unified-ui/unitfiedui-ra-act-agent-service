"""Tests for the LLM factory."""

import pytest
from app.models import AIModelConfig
from app.services.llm_factory import create_llm


@pytest.mark.unit
class TestLLMFactory:
    """Tests for LLM factory functions."""

    def test_unsupported_provider_raises_error(self) -> None:
        """Test that unsupported provider raises ValueError."""
        config = AIModelConfig(provider="UNSUPPORTED", model_name="test")
        with pytest.raises(ValueError, match="Unsupported LLM provider"):
            create_llm(config)

    def test_create_openai_llm(self) -> None:
        """Test creating an OpenAI LLM."""
        config = AIModelConfig(provider="OPENAI", model_name="gpt-4o", api_key="test-key")
        llm = create_llm(config)
        assert llm is not None

    def test_create_azure_openai_llm(self) -> None:
        """Test creating an Azure OpenAI LLM."""
        config = AIModelConfig(
            provider="AZURE_OPENAI",
            endpoint="https://test.openai.azure.com",
            deployment_name="gpt-4o",
            api_version="2024-02-01",
            api_key="test-key",
        )
        llm = create_llm(config)
        assert llm is not None
