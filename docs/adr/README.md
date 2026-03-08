# docs/adr/

This directory contains Architecture Decision Records (ADRs) for the unified-ui ReACT Agent Service.

## What is an ADR?

An Architecture Decision Record captures an important architectural decision made along with its context and consequences.

## ADR Index

| ADR | Title | Status |
|-----|-------|--------|
| [001](001_SERVICE_AUTHENTICATION.md) | Service-to-Service Authentication | Accepted |
| [002](002_VAULT_ABSTRACTION.md) | Vault Abstraction Pattern | Accepted |
| [003](003_LLM_PROVIDER_FACTORY.md) | LLM Provider Factory | Accepted |
| [004](004_SSE_STREAMING_PROTOCOL.md) | SSE Streaming Protocol | Accepted |

## ADR Template

When creating a new ADR, use this template:

```markdown
# ADR-XXX: Title

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** YYYY-MM-DD
**Author:** Name

---

## Context

What is the issue that we're seeing that is motivating this decision?

## Decision

What is the change that we're proposing and/or doing?

## Alternatives Considered

| Alternative | Pros | Cons |
|-------------|------|------|
| Option A | ... | ... |
| Option B ✅ | ... | ... |

## Consequences

### Positive
- ...

### Negative
- ...

---

## References

- Links to relevant documentation
```

## Naming Convention

ADRs are numbered sequentially: `001_`, `002_`, etc.

Use SCREAMING_SNAKE_CASE for the filename: `001_SERVICE_AUTHENTICATION.md`
