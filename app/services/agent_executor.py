"""Agent executor service — orchestrates ReActAgentEngine execution."""

import logging
from collections.abc import AsyncGenerator

from fastapi import Request
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from unifiedui_sdk.agents import ReActAgentConfig, ReActAgentEngine, ToolConfig, ToolType
from unifiedui_sdk.streaming import StreamWriter
from unifiedui_sdk.tracing import ReActAgentTracer, Trace, TraceContextType

from app.models import AgentConfig, AgentInvokeRequest, AIModelConfig, ToolDefinition
from app.services.llm_factory import create_llm

logger = logging.getLogger(__name__)


class AgentExecutorService:
    """Service for executing ReACT agents via the unifiedui-sdk."""

    async def execute(self, request: AgentInvokeRequest, http_request: Request) -> AsyncGenerator[str]:
        """Execute a ReACT agent and yield SSE event strings.

        Args:
            request: The agent invocation request.
            http_request: The HTTP request for disconnect detection.

        Yields:
            JSON-serialized StreamMessage strings.
        """
        config = request.agent_config
        writer = StreamWriter()

        try:
            llm = self._create_llm(config.ai_models)
            tools = self._create_tools(config.tools)
            agent_config = self._create_agent_config(config)
            trace = self._create_trace(request)
            tracer = ReActAgentTracer(trace=trace, stream_writer=writer)

            engine = ReActAgentEngine(
                config=agent_config,
                llm=llm,
                tools=tools,
                tracer=tracer,
            )

            history = [{"role": entry.role, "content": entry.content} for entry in request.history]

            async for msg in engine.invoke_stream(request.message, history=history):
                if await http_request.is_disconnected():
                    logger.info("Client disconnected, stopping agent execution")
                    break
                yield msg.model_dump_json()

        except Exception:
            logger.exception("Agent execution failed")
            error_msg = writer.error("Agent execution failed")
            yield error_msg.model_dump_json()

    def _create_llm(self, ai_models: list[AIModelConfig]) -> BaseChatModel:
        """Create an LLM instance from the first available AI model config.

        Args:
            ai_models: List of AI model configurations.

        Returns:
            A BaseChatModel instance.

        Raises:
            ValueError: If no AI models are configured.
        """
        if not ai_models:
            msg = "No AI models configured"
            raise ValueError(msg)

        return create_llm(ai_models[0])

    def _create_tools(self, tool_definitions: list[ToolDefinition]) -> list[BaseTool]:
        """Create BaseTool instances from tool definitions.

        The SDK's ReActAgentEngine handles tool instantiation from ToolConfig,
        so we pass them as ToolConfig objects and let the engine resolve them.

        Args:
            tool_definitions: List of tool definitions from the platform.

        Returns:
            Empty list — tools are passed via agent config.
        """
        return []

    def _create_tool_configs(self, tool_definitions: list[ToolDefinition]) -> list[ToolConfig]:
        """Create ToolConfig instances from tool definitions.

        Args:
            tool_definitions: List of tool definitions.

        Returns:
            List of ToolConfig objects for the SDK engine.
        """
        tool_configs: list[ToolConfig] = []
        for tool_def in tool_definitions:
            if not tool_def.is_active:
                continue
            credential = tool_def.credential.secret if tool_def.credential else None
            tool_configs.append(
                ToolConfig(
                    name=tool_def.name,
                    type=ToolType(tool_def.type),
                    config=tool_def.config,
                    credential=credential,
                )
            )
        return tool_configs

    def _create_agent_config(self, config: AgentConfig) -> ReActAgentConfig:
        """Create a ReActAgentConfig from the agent configuration.

        Args:
            config: Agent configuration from the request.

        Returns:
            SDK ReActAgentConfig instance.
        """
        tool_configs = self._create_tool_configs(config.tools)

        extra_config: dict[str, object] = config.config or {}
        max_iterations = int(str(extra_config.get("max_iterations", 15)))
        max_execution_time = int(str(extra_config.get("max_execution_time_seconds", 120)))
        temperature = float(str(extra_config.get("temperature", 0.1)))

        return ReActAgentConfig(
            system_prompt=config.system_prompt,
            security_prompt=config.security_prompt,
            tool_use_prompt=config.tool_use_prompt,
            response_prompt=config.response_prompt,
            max_iterations=max_iterations,
            max_execution_time_seconds=max_execution_time,
            temperature=temperature,
            multi_agent_enabled=config.multi_agent_enabled,
            tool_configs=tool_configs,
        )

    def _create_trace(self, request: AgentInvokeRequest) -> Trace:
        """Create a Trace object for the agent execution.

        Args:
            request: The agent invocation request.

        Returns:
            A Trace instance for tracking the execution.
        """
        return Trace(
            tenant_id=request.tenant_id,
            chat_agent_id=request.chat_agent_id,
            conversation_id=request.conversation_id,
            context_type=TraceContextType.CONVERSATION,
        )
