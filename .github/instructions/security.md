# Security Guidelines — ReACT Agent Service (Python/FastAPI)

## CRITICAL: Read This First

These rules are **mandatory** for all code generation. Violations cause SAST/CodeQL failures in CI.

---

## 1. Prompt Injection Prevention

**Threat**: User-supplied text embedded in LLM prompts can manipulate agent behavior, bypass instructions, or exfiltrate data.

### Rules

- **ALWAYS** clearly separate system prompts from user content using distinct message roles.
- **NEVER** embed raw user input into system prompt strings via f-strings or `.format()`.
- **ALWAYS** use the structured message format (system/user/assistant roles) from the SDK.
- **ALWAYS** treat all user content as untrusted — even content from the platform service.

### Correct Pattern

```python
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_input},
]
```

### Wrong Pattern

```python
# WRONG — user input in system prompt
prompt = f"You are an assistant. Context: {user_input}. Respond helpfully."
```

---

## 2. SSRF Prevention (Server-Side Request Forgery)

**Threat**: User-controlled URLs (from agent config, tool definitions) redirect server to internal services or cloud metadata endpoints.

### Rules

- **ALWAYS** validate URLs before making HTTP requests:
  - Parse with `urllib.parse.urlparse()`
  - Verify scheme is `http` or `https`
  - Verify host is not empty
  - Reject private/internal IP ranges (`127.0.0.1`, `169.254.169.254`, `10.x.x.x`, `192.168.x.x`, `172.16-31.x.x`, `localhost`)
- **ALWAYS** set timeouts on HTTP clients (30s default).
- **NEVER** trust tool endpoint URLs from external configuration without validation.

### Correct Pattern

```python
from urllib.parse import urlparse

def validate_url(raw_url: str) -> str:
    """Validate and return a safe HTTP(S) URL."""
    parsed = urlparse(raw_url.rstrip("/"))
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")
    if not parsed.hostname:
        raise ValueError("URL missing host")
    return parsed.geturl()
```

---

## 3. Input Validation

### Rules

- **ALWAYS** use Pydantic models with constraints for request validation.
- **ALWAYS** add `max_length`, `min_length`, `pattern` constraints on user-controlled string fields.
- **NEVER** trust client-supplied IDs without validating format.
- **ALWAYS** validate tool configurations (URLs, parameter schemas) before execution.

### Correct Pattern

```python
from pydantic import BaseModel, Field, constr

class AgentRequest(BaseModel):
    tenant_id: constr(pattern=r"^[a-f0-9\-]{36}$")
    agent_id: constr(min_length=1, max_length=255, pattern=r"^[A-Za-z0-9_\-]+$")
    message: str = Field(max_length=50000)
```

---

## 4. Secret Management

### Rules

- **NEVER** hardcode secrets, API keys, or tokens in source code.
- **ALWAYS** use the vault abstraction (`core/vault/`) to retrieve secrets at runtime.
- **NEVER** log secrets — not even at debug level.
- **NEVER** include secrets in error messages or exception details.
- **NEVER** pass secrets through URL query parameters.

---

## 5. Tool Execution Safety

**Threat**: ReACT agents execute tools (functions, API calls) based on LLM decisions — a compromised prompt can trigger unintended tool calls.

### Rules

- **ALWAYS** validate tool inputs against their defined parameter schemas before execution.
- **ALWAYS** enforce tool allow-lists — only execute tools that are explicitly registered for the agent.
- **NEVER** allow dynamic tool loading from user-supplied code or URLs.
- **ALWAYS** sanitize tool outputs before including them in subsequent LLM prompts.
- **ALWAYS** set resource limits (timeouts, max iterations) on agent execution loops to prevent infinite loops.

---

## 6. Data Exposure Prevention

### Rules

- **ALWAYS** use separate response models (Pydantic) — never return internal data structures.
- **NEVER** expose stack traces or internal error details in production responses.
- **NEVER** include LLM API keys or internal configuration in streamed SSE responses.
- **ALWAYS** sanitize trace/log data before returning to the client.

---

## Quick Checklist Before Committing

- [ ] User content separated from system prompts (distinct roles)
- [ ] All outbound URLs validated (scheme, host, no internal IPs)
- [ ] All user input validated via Pydantic with constraints
- [ ] No hardcoded secrets
- [ ] No secrets logged at any level
- [ ] Tool inputs validated against schemas
- [ ] Agent execution has timeout/iteration limits
- [ ] No sensitive data in API responses or SSE streams
- [ ] HTTP clients have timeouts
