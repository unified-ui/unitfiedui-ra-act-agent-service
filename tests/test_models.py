"""Tests for request and response models."""

import pytest
from app.models import AgentConfig, AgentInvokeRequest, AIModelConfig, ChatHistoryEntry, ToolDefinition
from app.models.responses import ErrorResponse


@pytest.mark.unit
class TestRequestModels:
    """Tests for request model validation."""

    def test_agent_invoke_request_minimal(self) -> None:
        """Test creating a minimal AgentInvokeRequest."""
        req = AgentInvokeRequest(
            tenant_id="t1",
            message="Hello",
            agent_config=AgentConfig(react_agent_id="r1"),
        )
        assert req.tenant_id == "t1"
        assert req.message == "Hello"
        assert req.history == []

    def test_agent_invoke_request_with_history(self) -> None:
        """Test creating AgentInvokeRequest with history."""
        req = AgentInvokeRequest(
            tenant_id="t1",
            message="Hello",
            history=[
                ChatHistoryEntry(role="user", content="Hi"),
                ChatHistoryEntry(role="assistant", content="Hello!"),
            ],
            agent_config=AgentConfig(react_agent_id="r1"),
        )
        assert len(req.history) == 2
        assert req.history[0].role == "user"

    def test_agent_config_defaults(self) -> None:
        """Test AgentConfig default values."""
        config = AgentConfig(react_agent_id="r1")
        assert config.version == 1
        assert config.system_prompt is None
        assert config.ai_models == []
        assert config.tools == []
        assert config.multi_agent_enabled is False

    def test_ai_model_config(self) -> None:
        """Test AIModelConfig creation."""
        model = AIModelConfig(provider="OPENAI", model_name="gpt-4o", api_key="key123")
        assert model.provider == "OPENAI"
        assert model.model_name == "gpt-4o"

    def test_tool_definition(self) -> None:
        """Test ToolDefinition creation."""
        tool = ToolDefinition(
            id="tool-1",
            name="search",
            type="MCP_SERVER",
            config={"url": "http://localhost:3000"},
        )
        assert tool.id == "tool-1"
        assert tool.is_active is True


@pytest.mark.unit
class TestResponseModels:
    """Tests for response model validation."""

    def test_error_response(self) -> None:
        """Test ErrorResponse creation."""
        err = ErrorResponse(code="AGENT_ERROR", message="Failed", details="Stack trace")
        assert err.code == "AGENT_ERROR"
        assert err.details == "Stack trace"

    def test_error_response_defaults(self) -> None:
        """Test ErrorResponse default values."""
        err = ErrorResponse(code="ERR", message="fail")
        assert err.details == ""
