# Coding Standards

## Type Hints

- **Required** on all functions, methods, and class attributes
- Use `from __future__ import annotations` where beneficial
- Prefer `X | None` over `Optional[X]`
- Use `typing.Protocol` for structural subtyping
- **No `Any`** — always use specific types

## Docstrings

Follow **Google style**. Only class docstrings and function docstrings — **no inline comments**:

```python
class AgentExecutorService:
    """Service for executing ReACT agents via the unifiedui-sdk."""

    async def execute(self, request: AgentInvokeRequest) -> AsyncGenerator[str]:
        """Execute a ReACT agent and yield SSE event strings.

        Args:
            request: The agent invocation request.

        Yields:
            JSON-serialized StreamMessage strings.

        Raises:
            ValueError: If no AI models are configured.
        """
```

## Error Handling

- Define custom exceptions in dedicated exception files
- Never catch bare `Exception` unless re-raising
- Use `raise ... from err` for exception chaining
- Log exceptions with `logger.exception()` for stack traces

## Imports

- Sorted automatically by ruff (isort rules)
- `app` is configured as first-party
- Use `TYPE_CHECKING` blocks for import-only-at-type-check-time dependencies
- Prefer absolute imports within the package

## Architecture Rules

1. **No comments in code** — Code must be self-documenting
2. **ALL business logic in services** — API routes are thin wrappers
3. **Factory pattern for infrastructure** — See `core/vault/factory.py`
4. **Pydantic for all schemas** — Separate request and response models in `models/`
5. **Dependency injection** — Use `Depends()` or factories, never instantiate directly
6. **Keep files under 400 lines** — Split large services into helpers

## DRY (Don't Repeat Yourself)

- Extract shared logic into private helper methods
- Move reusable utility functions to appropriate modules
- If two methods share 3+ lines of identical logic, refactor into a shared helper
- Prefer composition and delegation over copy-paste

## File & Module Naming

- **Modules**: prefer short, descriptive names: `config.py`, `factory.py`, `base.py`
- **Classes**: `PascalCase` (e.g. `AgentExecutorService`, `BaseVault`)
- **Functions/Methods**: `snake_case` (e.g. `create_llm`, `get_secret`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g. `_PROVIDER_AZURE_OPENAI`)
- **Test files**: `test_<module>.py` (e.g. `test_agent_executor.py`)

## Pydantic Models

- Use `Field(alias="camelCase")` for JSON serialization if needed
- Set `model_config = {"populate_by_name": True}` for dual naming
- Use `Field(default_factory=...)` for mutable defaults
- Group models by purpose: `requests.py`, `responses.py`
