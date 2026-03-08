# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation overhaul (README, CONTRIBUTING, TOOLING)
- ADR documentation in `docs/adr/`
- Open source files (LICENSE, SECURITY.md, SPONSORS.md)
- Enhanced CI workflows with branch validation

### Changed
- Updated branching strategy documentation

---

## [0.1.0] - 2026-03-08

### Added
- Initial project setup with FastAPI
- ReACT Agent execution via `unifiedui-sdk` `ReActAgentEngine`
- SSE streaming with all 22 event types
- Service-to-service authentication via `X-Service-Key`
- Vault integration:
  - Azure Key Vault
  - HashiCorp Vault
  - DotEnv (local development)
- Health and readiness endpoints (`/health`, `/ready`)
- LLM provider factory supporting:
  - Azure OpenAI
  - OpenAI
  - Anthropic
  - Google GenAI
  - Ollama
  - Mistral
  - Groq
- Pre-commit hooks (ruff, commitlint)
- CI/CD workflows (tests, lint, branch checks)
- Test suite with pytest and 80%+ coverage
