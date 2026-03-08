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

    def test_create_anthropic_llm(self) -> None:
        """Test creating an Anthropic LLM."""
        config = AIModelConfig(
            provider="ANTHROPIC",
            model_name="claude-3-5-sonnet-20241022",
            api_key="test-key",
        )
        llm = create_llm(config)
        assert llm is not None

    def test_create_google_genai_llm(self) -> None:
        """Test creating a Google GenAI LLM."""
        config = AIModelConfig(
            provider="GOOGLE_GENAI",
            model_name="gemini-1.5-pro",
            api_key="test-key",
        )
        llm = create_llm(config)
        assert llm is not None

    def test_create_ollama_llm(self) -> None:
        """Test creating an Ollama LLM."""
        config = AIModelConfig(
            provider="OLLAMA",
            model_name="llama3.2",
        )
        llm = create_llm(config)
        assert llm is not None

    def test_create_ollama_llm_with_base_url(self) -> None:
        """Test creating an Ollama LLM with custom base URL."""
        config = AIModelConfig(
            provider="OLLAMA",
            model_name="llama3.2",
            base_url="http://localhost:11434",
        )
        llm = create_llm(config)
        assert llm is not None

    def test_create_mistral_llm(self) -> None:
        """Test creating a Mistral LLM."""
        config = AIModelConfig(
            provider="MISTRAL",
            model_name="mistral-large-latest",
            api_key="test-key",
        )
        llm = create_llm(config)
        assert llm is not None

    def test_create_groq_llm(self) -> None:
        """Test creating a Groq LLM."""
        config = AIModelConfig(
            provider="GROQ",
            model_name="llama-3.3-70b-versatile",
            api_key="test-key",
        )
        llm = create_llm(config)
        assert llm is not None

    def test_provider_is_case_insensitive(self) -> None:
        """Test that provider matching is case-insensitive."""
        config = AIModelConfig(provider="openai", model_name="gpt-4o", api_key="test-key")
        llm = create_llm(config)
        assert llm is not None

    def test_create_openai_with_organization(self) -> None:
        """Test creating OpenAI LLM with organization."""
        config = AIModelConfig(
            provider="OPENAI",
            model_name="gpt-4o",
            api_key="test-key",
            organization="org-123",
        )
        llm = create_llm(config)
        assert llm is not None

    def test_create_openai_with_base_url(self) -> None:
        """Test creating OpenAI LLM with custom base URL."""
        config = AIModelConfig(
            provider="OPENAI",
            model_name="gpt-4o",
            api_key="test-key",
            base_url="https://custom.openai.com",
        )
        llm = create_llm(config)
        assert llm is not None
