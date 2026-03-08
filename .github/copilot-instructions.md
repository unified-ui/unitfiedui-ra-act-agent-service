---
applyTo: '**'
---

# unified-ui ReACT Agent Service — Copilot Instructions

## Project Overview

**unified-ui ReACT Agent Service** is a FastAPI microservice that executes ReACT (Reasoning + Acting) agents using the `unifiedui-sdk`. It receives agent configuration and message history from the Agent Service and streams all 22 SSE event types back.

**Tech Stack**: Python 3.13+ · FastAPI · unifiedui-sdk · SSE-Starlette · Pydantic v2 · uv

---

## Golden Rules

1. **No comments in code** — Only class docstrings and function docstrings (those are **mandatory**). No inline comments. Code must be self-documenting.
2. **ALL business logic in services** — API routes are thin wrappers. Zero logic, zero data transformation.
3. **Factory pattern for infrastructure** — Vault uses factory pattern with ABC in `core/`.
4. **Type annotations everywhere** — All function parameters, return types. No `Any`.
5. **Pydantic for all schemas** — Separate request and response models.
6. **Dependency injection** — Never instantiate vault/LLM in handlers directly. Use `Depends()` or factory.
7. **Keep files under 400 lines** — Split large services into helpers.
8. **Google-style docstrings** — Mandatory on all public APIs.
9. **Run tests after changes** — `uv run pytest tests/ -n auto --no-header -q`
10. **Run pre-commit after EVERY task** — `pre-commit run --all-files`

---

## Naming Conventions

| What | Pattern | Example |
|------|---------|---------|
| Route file | `{resource}.py` in `api/v1/` | `agent.py`, `health.py` |
| Service file | `{name}.py` in `services/` | `agent_executor.py`, `llm_factory.py` |
| Model file | `{purpose}.py` in `models/` | `requests.py`, `responses.py` |
| Vault impl | `{type}_vault.py` in `core/vault/` | `dotenv_vault.py` |
| Test file | `test_{module}.py` in `tests/` | `test_agent.py`, `test_health.py` |

---

## Quick Reference

- **Run**: `uv run uvicorn app.main:app --reload --port 8086`
- **Test**: `uv run pytest tests/ -n auto --no-header -q`
- **Lint**: `uv run ruff check . && uv run ruff format --check .`
- **Pre-commit**: `pre-commit run --all-files`
- **Entry point**: `app/main.py`
- **Config**: `app/config.py`
