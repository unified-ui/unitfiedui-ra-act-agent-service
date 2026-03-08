# ADR-002: Vault Abstraction Pattern

**Status:** Accepted
**Date:** 2026-03-08
**Author:** Enrico Goerlitz

---

## Context

The service needs to retrieve secrets (API keys, credentials) from various sources depending on the deployment environment:

- **Local development**: `.env` file
- **Production (Azure)**: Azure Key Vault
- **Production (Self-hosted)**: HashiCorp Vault

We need a consistent interface that abstracts away the underlying secret store.

## Decision

We implement the **Factory Pattern with Abstract Base Class**:

```
core/vault/
├── base.py           # BaseVault ABC
├── factory.py        # create_vault() factory function
├── dotenv_vault.py   # DotEnvVault implementation
├── azure_keyvault.py # AzureKeyVault implementation
├── hashicorp_vault.py# HashiCorpVault implementation
└── dependencies.py   # FastAPI Depends() helpers
```

### Interface

```python
class BaseVault(ABC):
    @abstractmethod
    def get_secret(self, key: str) -> str | None: ...

    @abstractmethod
    def store_secret(self, key: str, value: str) -> str: ...

    @abstractmethod
    def ping(self) -> bool: ...

    @abstractmethod
    def close(self) -> None: ...
```

### Factory

```python
def create_vault(vault_type: str, **kwargs) -> BaseVault:
    if vault_type == "dotenv":
        return DotEnvVault()
    if vault_type == "azure_keyvault":
        return AzureKeyVault(vault_url=kwargs["vault_url"])
    if vault_type == "hashicorp_vault":
        return HashiCorpVault(...)
    raise ValueError(f"Unsupported vault type: {vault_type}")
```

## Alternatives Considered

| Alternative | Pros | Cons |
|-------------|------|------|
| **Direct SDK calls** | Simple for single vault | Tight coupling, hard to test |
| **Dependency injection** | Flexible | More complex setup |
| **Factory + ABC** ✅ | Clean abstraction, testable | Slight overhead |
| **Unified Secrets Manager** | Cloud-agnostic | External dependency |

## Consequences

### Positive
- Environment-agnostic code
- Easy to test with mock vault
- New vault backends can be added without changing consumers
- Configuration-driven via `VAULT_TYPE` environment variable

### Negative
- Additional abstraction layer
- Each vault implementation must conform to the interface

---

## References

- [Factory Pattern](https://refactoring.guru/design-patterns/factory-method)
- [Azure Key Vault SDK](https://docs.microsoft.com/en-us/azure/key-vault/)
- [HashiCorp Vault API](https://developer.hashicorp.com/vault/api-docs)
