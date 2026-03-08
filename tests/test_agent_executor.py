"""Tests for the agent executor service."""

import pytest
from app.models import AgentConfig, AIModelConfig
from app.services.agent_executor import AgentExecutorService


@pytest.mark.unit
class TestAgentExecutorService:
    """Tests for AgentExecutorService."""

    def test_create_agent_config(self) -> None:
        """Test creating a ReActAgentConfig from AgentConfig."""
        service = AgentExecutorService()
        config = AgentConfig(
            react_agent_id="react-001",
            system_prompt="You are helpful.",
            security_prompt="Be safe.",
            tool_use_prompt="Use tools wisely.",
            response_prompt="Be concise.",
            config={"max_iterations": 10, "temperature": 0.5},
        )
        result = service._create_agent_config(config)
        assert result.system_prompt == "You are helpful."
        assert result.security_prompt == "Be safe."
        assert result.max_iterations == 10
        assert result.temperature == 0.5

    def test_create_agent_config_defaults(self) -> None:
        """Test default values in agent config creation."""
        service = AgentExecutorService()
        config = AgentConfig(react_agent_id="react-001")
        result = service._create_agent_config(config)
        assert result.max_iterations == 15
        assert result.temperature == 0.1
        assert result.multi_agent_enabled is False

    def test_create_llm_raises_on_empty_models(self) -> None:
        """Test that _create_llm raises when no models configured."""
        service = AgentExecutorService()
        with pytest.raises(ValueError, match="No AI models configured"):
            service._create_llm([])

    def test_create_llm_with_valid_config(self) -> None:
        """Test creating LLM with valid config."""
        service = AgentExecutorService()
        models = [AIModelConfig(provider="OPENAI", model_name="gpt-4o", api_key="test")]
        llm = service._create_llm(models)
        assert llm is not None
