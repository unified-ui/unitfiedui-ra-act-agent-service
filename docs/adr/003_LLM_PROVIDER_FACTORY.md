# ADR-003: LLM Provider Factory

**Status:** Accepted
**Date:** 2026-03-08
**Author:** Enrico Goerlitz

---

## Context

The Agent Service passes AI model configuration to the ReACT Service. We need to instantiate the correct LangChain chat model based on the provider specified in the configuration.

Supported providers:
- Azure OpenAI
- OpenAI
- Anthropic
- Google GenAI
- Ollama
- Mistral
- Groq

## Decision

We implement a **Factory Function** pattern in `services/llm_factory.py`:

```python
def create_llm(config: AIModelConfig) -> BaseChatModel:
    provider = config.provider.upper()

    if provider == "AZURE_OPENAI":
        return _create_azure_openai(config)
    if provider == "OPENAI":
        return _create_openai(config)
    if provider == "ANTHROPIC":
        return _create_anthropic(config)
    # ... etc

    raise ValueError(f"Unsupported LLM provider: {config.provider}")
```

### Design Principles

1. **Lazy imports**: LangChain provider packages are imported inside functions to avoid loading unused dependencies
2. **Unified interface**: All providers return `BaseChatModel`
3. **Configuration-driven**: Provider-specific settings come from `AIModelConfig`
4. **No provider leakage**: Callers only interact with the abstract `BaseChatModel`

## Alternatives Considered

| Alternative | Pros | Cons |
|-------------|------|------|
| **Direct instantiation** | Simple | Provider logic scattered |
| **Class-based factory** | Extensible | Overengineered for this use case |
| **Function factory** ✅ | Simple, centralized | Less extensible than registry |
| **Plugin registry** | Highly extensible | Complex for 7 providers |

## Consequences

### Positive
- Centralized provider logic
- Easy to add new providers
- Lazy loading reduces startup time
- Consistent error handling

### Negative
- Adding a provider requires code changes (not config-only)
- Large switch statement (manageable with 7 providers)

### Future Considerations
- Consider a registry pattern if provider count grows significantly
- Add provider-specific validation (e.g., Azure requires `endpoint` + `deployment_name`)

---

## References

- [LangChain Chat Models](https://python.langchain.com/docs/integrations/chat/)
- [Factory Pattern](https://refactoring.guru/design-patterns/factory-method)
