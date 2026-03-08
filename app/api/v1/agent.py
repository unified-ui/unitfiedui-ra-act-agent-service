"""Agent invocation endpoint with SSE streaming."""

import logging
from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends, Request
from sse_starlette.sse import EventSourceResponse

from app.middleware.service_auth import validate_service_key
from app.models.requests import AgentInvokeRequest
from app.services.agent_executor import AgentExecutorService

router = APIRouter(tags=["agent"])
logger = logging.getLogger(__name__)


@router.post("/agent/invoke", dependencies=[Depends(validate_service_key)])
async def invoke_agent(request: Request, body: AgentInvokeRequest) -> EventSourceResponse:
    """Execute a ReACT agent and stream results via SSE.

    Args:
        request: The incoming HTTP request.
        body: Agent invocation request with config, history, and message.

    Returns:
        SSE event stream with all agent events.
    """
    executor = AgentExecutorService()

    async def event_generator() -> AsyncGenerator[dict[str, str]]:
        async for event in executor.execute(body, request):
            yield {"event": "message", "data": event}

    return EventSourceResponse(event_generator())
