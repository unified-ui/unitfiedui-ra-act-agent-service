# ADR-001: Service-to-Service Authentication

**Status:** Accepted
**Date:** 2026-03-08
**Author:** Enrico Goerlitz

---

## Context

The ReACT Agent Service is an internal microservice that should only be accessible by the Agent Service (Go). We need a simple, secure authentication mechanism for service-to-service communication.

## Decision

We use a **shared secret key** approach with the following characteristics:

1. **Header-based authentication**: Services pass a secret key in the `X-Service-Key` header
2. **Vault-stored secrets**: The key is stored in a secure vault (Azure Key Vault, HashiCorp Vault) or `.env` for local development
3. **Middleware validation**: A FastAPI dependency validates the key before any request is processed

### Implementation

```python
# middleware/service_auth.py
async def validate_service_key(x_service_key: str = Header(...)) -> None:
    vault = get_vault()
    expected_key = vault.get_secret("AGENT_TO_REACT_SERVICE_KEY")
    if not secrets.compare_digest(x_service_key, expected_key):
        raise HTTPException(status_code=401, detail="Invalid service key")
```

## Alternatives Considered

| Alternative | Pros | Cons |
|-------------|------|------|
| **mTLS** | Strong identity verification | Complex certificate management |
| **JWT tokens** | Standard, supports claims | Overhead for internal service |
| **API Gateway auth** | Centralized | Additional infrastructure |
| **Shared secret** ✅ | Simple, fast, sufficient | Key rotation requires coordination |

## Consequences

### Positive
- Simple implementation with minimal overhead
- No external dependencies for auth
- Works with all vault backends (Azure, HashiCorp, dotenv)

### Negative
- Key rotation requires coordinated deployment
- No fine-grained permissions (all-or-nothing access)

### Mitigations
- Use vault with automatic key rotation support
- Monitor for unauthorized access attempts
- Implement rate limiting at the network layer

---

## References

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [OWASP API Security](https://owasp.org/www-project-api-security/)
