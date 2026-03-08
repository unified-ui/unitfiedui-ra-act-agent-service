# Contributing

## Branch Naming

```
<type>/<description>
```

Examples: `feat/agent-streaming`, `fix/vault-timeout`, `docs/readme-update`

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): subject
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`

## Development Workflow

1. Create feature branch from `develop`
2. Implement changes
3. Run `pre-commit run --all-files`
4. Run `uv run pytest tests/ -n auto --no-header -q`
5. Open PR to `develop`

## Code Quality

- Type hints on all functions
- Google-style docstrings on all public APIs
- 80% minimum test coverage
- All pre-commit hooks must pass
