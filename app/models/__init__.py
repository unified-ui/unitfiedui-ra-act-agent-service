"""Request models for the agent service."""

from pydantic import BaseModel, Field


class AIModelConfig(BaseModel):
    """AI model configuration from the platform service."""

    provider: str
    model_name: str = ""
    api_key: str = ""
    endpoint: str = ""
    api_version: str = ""
    deployment_name: str = ""
    base_url: str = ""
    organization: str = ""


class ToolCredential(BaseModel):
    """Credential for a tool."""

    id: str = ""
    type: str = ""
    secret: str = ""


class ToolDefinition(BaseModel):
    """Tool definition from the platform service."""

    id: str
    name: str
    description: str = ""
    type: str
    config: dict[str, object] = Field(default_factory=dict)
    is_active: bool = True
    credential: ToolCredential | None = None


class ChatHistoryEntry(BaseModel):
    """Single chat history entry."""

    role: str
    content: str


class AgentConfig(BaseModel):
    """Full agent configuration passed from the agent service."""

    react_agent_id: str = ""
    version: int = 1
    system_prompt: str | None = None
    security_prompt: str | None = None
    tool_use_prompt: str | None = None
    response_prompt: str | None = None
    greeting_messages: list[str] = Field(default_factory=list)
    config: dict[str, object] = Field(default_factory=dict)
    ai_models: list[AIModelConfig] = Field(default_factory=list)
    tools: list[ToolDefinition] = Field(default_factory=list)
    multi_agent_enabled: bool = False


class AgentInvokeRequest(BaseModel):
    """Request body for agent invocation."""

    tenant_id: str
    chat_agent_id: str = ""
    conversation_id: str = ""
    message: str
    history: list[ChatHistoryEntry] = Field(default_factory=list)
    agent_config: AgentConfig
