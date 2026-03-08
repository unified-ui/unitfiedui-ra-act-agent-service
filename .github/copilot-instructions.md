# Copilot Instructions — unified-ui ReACT Agent Service

## Project Overview

**unified-ui ReACT Agent Service** is a FastAPI microservice that executes ReACT (Reasoning + Acting) agents using the `unifiedui-sdk`. It receives agent configuration and message history from the Agent Service (Go) and streams all 22 SSE event types back.

## Tech Stack

- **Language**: Python 3.13+
- **Framework**: FastAPI + SSE-Starlette
- **Agent Engine**: `unifiedui-sdk` ReActAgentEngine
- **Package Manager**: [uv](https://docs.astral.sh/uv/)
- **Testing**: pytest + pytest-cov + pytest-xdist
- **Linting/Formatting**: Ruff
- **Type Checking**: mypy (strict mode)
- **CI/CD**: GitHub Actions

## Key Files & References

| Document | Description |
|----------|-------------|
| [TOOLING.md](../../TOOLING.md) | Development tooling, commands, and quality gates |
| [CONTRIBUTING.md](../../CONTRIBUTING.md) | Contribution guidelines and workflow |
| [CHANGELOG.md](../../CHANGELOG.md) | Version history |
| [pyproject.toml](../../pyproject.toml) | Project configuration (deps, ruff, pytest, mypy, coverage) |

## Detailed Instructions

Refer to the following files for domain-specific guidance:

| Instruction File | Topic |
|------------------|-------|
| [project-structure.md](instructions/project-structure.md) | Package layout and module organization |
| [coding-standards.md](instructions/coding-standards.md) | Code style, type hints, docstrings, naming conventions |
| [testing-guide.md](instructions/testing-guide.md) | Testing patterns, coverage requirements, fixtures |

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

## Conventions

- **Commit messages**: [Conventional Commits](https://www.conventionalcommits.org/) — `type(scope): subject`
- **Branch names**: `<type>/<description>` (e.g. `feat/multi-agent`, `fix/vault-timeout`)
- **Imports**: sorted by ruff/isort; `app` is first-party
- **Docstrings**: Google style
- **Type hints**: required on all public APIs
- **Coverage**: minimum 80%

## Quick Reference

| Command | Description |
|---------|-------------|
| `uv run uvicorn app.main:app --reload --port 8086` | Run dev server |
| `uv run pytest tests/ -n auto --no-header -q` | Run tests |
| `uv run ruff check . && uv run ruff format --check .` | Lint + format check |
| `uv run mypy app/` | Type check |
| `pre-commit run --all-files` | Run all pre-commit hooks |

## Naming Conventions

| What | Pattern | Example |
|------|---------|---------|
| Route file | `{resource}.py` in `api/v1/` | `agent.py`, `health.py` |
| Service file | `{name}.py` in `services/` | `agent_executor.py`, `llm_factory.py` |
| Model file | `{purpose}.py` in `models/` | `requests.py`, `responses.py` |
| Vault impl | `{type}_vault.py` in `core/vault/` | `dotenv_vault.py` |
| Test file | `test_{module}.py` in `tests/` | `test_agent.py`, `test_health.py` |
