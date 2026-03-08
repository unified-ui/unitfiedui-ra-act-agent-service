# unified-ui ReACT Agent Service

High-performance FastAPI microservice that executes ReACT (Reasoning + Acting) agents for the [unified-ui](https://github.com/unified-ui) platform.

## Architecture

```
Agent Service (8085) → ReACT Service (8086) → unifiedui-sdk ReActAgentEngine
```

The Agent Service sends agent configuration, message history, and the user message to this service. This service instantiates a `ReActAgentEngine` from the `unifiedui-sdk`, executes it, and streams all 22 SSE event types back.

## Tech Stack

- **Language**: Python 3.13+
- **Framework**: FastAPI + SSE-Starlette
- **Agent Engine**: `unifiedui-sdk` ReActAgentEngine
- **Auth**: Service-to-Service key validation
- **Vault**: Azure Key Vault / HashiCorp Vault / DotEnv
- **Package Manager**: [uv](https://docs.astral.sh/uv/)

## Quick Start

```bash
# Install dependencies
uv sync --all-extras

# Copy environment
cp .env.example .env

# Run dev server
uv run uvicorn app.main:app --reload --port 8086

# Run tests
uv run pytest tests/ -n auto --no-header -q

# Lint
uv run ruff check . && uv run ruff format --check .

# Type check
uv run mypy app/
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/ready` | Readiness check |
| `POST` | `/api/v1/agent/invoke` | Execute agent (SSE stream) |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SERVER_HOST` | `0.0.0.0` | Server bind host |
| `SERVER_PORT` | `8086` | Server bind port |
| `VAULT_TYPE` | `dotenv` | Vault type (`dotenv`, `azure_keyvault`, `hashicorp_vault`) |
| `AGENT_TO_REACT_SERVICE_KEY` | — | S2S auth key (in vault) |
| `LOG_LEVEL` | `info` | Log level |

## Project Structure

```
app/
├── main.py              # FastAPI app factory
├── config.py            # Pydantic Settings
├── api/
│   └── v1/
│       ├── health.py    # Health endpoints
│       └── agent.py     # Agent invoke endpoint (SSE)
├── services/
│   └── agent_executor.py # ReActAgentEngine orchestration
├── models/
│   ├── requests.py      # Request schemas
│   └── responses.py     # Response schemas
├── middleware/
│   └── service_auth.py  # S2S key validation
└── core/
    └── vault/           # Vault ABC + implementations
```
