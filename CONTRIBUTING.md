# Contributing to unified-ui ReACT Agent Service

Thank you for your interest in contributing! 🎉

## Development Setup

```bash
# Clone the repository
git clone https://github.com/unified-ui/unified-ui-re-act-agent-service.git
cd unified-ui-re-act-agent-service

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --all-extras

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg

# Copy environment
cp .env.example .env
```

## Development Workflow

1. **Fork** the repository
2. **Create a branch** following the naming convention: `<type>/<description>`
   - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`, `hotfix`
   - Example: `feat/multi-agent-support`
3. **Make your changes** and write tests
4. **Run quality checks** locally:
   ```bash
   uv run ruff check .               # Lint
   uv run ruff format .              # Format
   uv run mypy app/                  # Type check
   uv run pytest tests/ -n auto --cov=app --cov-fail-under=80  # Tests + coverage
   pre-commit run --all-files        # All pre-commit hooks
   ```
5. **Commit** using [Conventional Commits](https://www.conventionalcommits.org/):
   ```
   feat(agent): add multi-agent orchestration
   fix(vault): handle connection timeout gracefully
   ```
6. **Push** and open a Pull Request to `develop`

## Code Standards

- **Type hints** on all functions and methods
- **Docstrings** in Google style on all public APIs (class docstrings and function docstrings only — no inline comments)
- **Test coverage** must stay above **80%**
- **Ruff** must pass with zero warnings
- All business logic in `services/` — API routes are thin wrappers

## Architecture Rules

1. **No comments in code** — Only docstrings. Code must be self-documenting.
2. **ALL business logic in services** — API routes are thin wrappers. Zero logic.
3. **Factory pattern for infrastructure** — Vault uses factory pattern with ABC.
4. **Type annotations everywhere** — All parameters and return types. No `Any`.
5. **Pydantic for all schemas** — Separate request and response models.
6. **Dependency injection** — Use `Depends()` or factories, never instantiate directly.
7. **Keep files under 400 lines** — Split large services into helpers.

## Reporting Issues

- Use GitHub Issues
- Include: Python version, service version, steps to reproduce, expected vs. actual behavior

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
