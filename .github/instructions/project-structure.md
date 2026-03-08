# Project Structure

## Package Layout

```
unified-ui-re-act-agent-service/
├── app/                         # Main application package
│   ├── __init__.py
│   ├── main.py                  # FastAPI app factory
│   ├── config.py                # Pydantic Settings
│   ├── api/                     # API layer (thin wrappers only)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── health.py        # Health endpoints (/health, /ready)
│   │       └── agent.py         # Agent invoke endpoint (SSE stream)
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   ├── agent_executor.py    # ReActAgentEngine orchestration
│   │   └── llm_factory.py       # LLM provider factory
│   ├── models/                  # Pydantic request/response schemas
│   │   ├── __init__.py          # Re-exports all models
│   │   ├── requests.py          # Request schemas
│   │   └── responses.py         # Response schemas (if any)
│   ├── middleware/              # FastAPI middleware & dependencies
│   │   ├── __init__.py
│   │   └── service_auth.py      # S2S key validation
│   └── core/                    # Core infrastructure
│       ├── __init__.py
│       └── vault/               # Secret vault abstraction
│           ├── __init__.py
│           ├── base.py          # BaseVault ABC
│           ├── factory.py       # create_vault() factory
│           ├── dependencies.py  # FastAPI Depends() helpers
│           ├── dotenv_vault.py  # DotEnv implementation
│           ├── azure_keyvault.py # Azure Key Vault implementation
│           └── hashicorp_vault.py # HashiCorp Vault implementation
├── tests/                       # Test suite (mirrors app structure)
│   ├── __init__.py
│   ├── conftest.py              # Shared fixtures
│   ├── test_health.py
│   ├── test_agent_executor.py
│   ├── test_llm_factory.py
│   ├── test_vault.py
│   ├── test_auth.py
│   └── test_config.py
├── docs/                        # Documentation
│   ├── README.md
│   └── adr/                     # Architecture Decision Records
├── docker/                      # Docker configuration
│   └── Dockerfile
└── .github/                     # CI workflows & instructions
    ├── workflows/
    ├── instructions/
    └── copilot-instructions.md
```

## Naming Conventions

| What | Pattern | Example |
|------|---------|---------|
| **Route file** | `{resource}.py` in `api/v1/` | `agent.py`, `health.py` |
| **Service file** | `{name}.py` in `services/` | `agent_executor.py`, `llm_factory.py` |
| **Model file** | `{purpose}.py` in `models/` | `requests.py`, `responses.py` |
| **Vault impl** | `{type}_vault.py` in `core/vault/` | `dotenv_vault.py` |
| **Test file** | `test_{module}.py` in `tests/` | `test_agent_executor.py` |

## Module Responsibilities

### `api/v1/`
Thin wrappers around services. **No business logic**. Routes should:
- Parse and validate request with Pydantic
- Call service methods
- Return response

### `services/`
All business logic lives here. Services:
- Orchestrate operations
- Handle errors with proper logging
- Return typed results

### `models/`
Pydantic models for API contracts:
- `requests.py` — Incoming request bodies
- `responses.py` — Outgoing response bodies

### `core/vault/`
Secret management abstraction:
- `base.py` — Abstract base class defining interface
- `factory.py` — Factory function to create vault instances
- Implementations for each vault provider

### `middleware/`
FastAPI middleware and dependencies:
- Authentication middleware
- Request/response logging
- Error handling

## Dependency Flow

```
api/ → services/ → core/
  ↓         ↓         ↓
models/   models/   vault/
```

- API layer depends on services and models
- Services depend on core infrastructure and models
- Core infrastructure has no internal dependencies
