# ADR-004: SSE Streaming Protocol

**Status:** Accepted
**Date:** 2026-03-08
**Author:** Enrico Goerlitz

---

## Context

The ReACT Agent Service executes agents that may take several seconds to complete. Users expect real-time feedback during execution, including:

- Token-by-token text streaming
- Reasoning steps (for models like o1/o3/Claude)
- Tool call visualization
- Multi-agent orchestration progress

## Decision

We use **Server-Sent Events (SSE)** with SSE-Starlette, forwarding the 22 event types from `unifiedui-sdk.streaming`:

### Event Types

| Category | Events |
|----------|--------|
| **Core** | `STREAM_START`, `TEXT_STREAM`, `STREAM_NEW_MESSAGE`, `STREAM_END`, `MESSAGE_COMPLETE`, `ERROR` |
| **Reasoning** | `REASONING_START`, `REASONING_STREAM`, `REASONING_END` |
| **Tool Calls** | `TOOL_CALL_START`, `TOOL_CALL_STREAM`, `TOOL_CALL_END` |
| **Multi-Agent** | `PLAN_START`, `PLAN_STREAM`, `PLAN_COMPLETE`, `SUB_AGENT_START`, `SUB_AGENT_STREAM`, `SUB_AGENT_END`, `SYNTHESIS_START`, `SYNTHESIS_STREAM`, `SYNTHESIS_END` |
| **Metadata** | `TITLE_GENERATION`, `TRACE` |

### Wire Format

```
event: message
data: {"type":"TEXT_STREAM","content":"Hello","config":{}}

event: message
data: {"type":"TOOL_CALL_START","content":"","config":{"tool_call_id":"tc_1","tool_name":"search","tool_input":{"query":"test"}}}
```

### Implementation

```python
@router.post("/agent/invoke")
async def invoke_agent(request: Request, body: AgentInvokeRequest):
    executor = AgentExecutorService()

    async def event_generator():
        async for event in executor.execute(body, request):
            yield {"event": "message", "data": event}

    return EventSourceResponse(event_generator())
```

## Alternatives Considered

| Alternative | Pros | Cons |
|-------------|------|------|
| **WebSockets** | Bidirectional | Overkill for unidirectional stream |
| **HTTP/2 Server Push** | Native | Limited browser support |
| **Long Polling** | Simple | Inefficient, high latency |
| **SSE** ✅ | Simple, well-supported, unidirectional | No binary support |

## Consequences

### Positive
- Native browser support via `EventSource`
- Automatic reconnection handling
- Simple implementation with SSE-Starlette
- Compatible with existing agent-service protocol

### Negative
- Unidirectional (client cannot send mid-stream)
- Text-only (no binary data)

---

## References

- [SSE Specification](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [SSE-Starlette](https://github.com/sysid/sse-starlette)
- [unifiedui-sdk Streaming Module](https://github.com/unified-ui/unifiedui-sdk)
