# Tooling

## Development Commands

| Command | Description |
|---------|-------------|
| `uv sync --all-extras` | Install all dependencies |
| `uv run uvicorn app.main:app --reload --port 8086` | Run dev server |
| `uv run pytest tests/ -n auto --no-header -q` | Run tests |
| `uv run pytest tests/ -n auto --cov=app --cov-report=html` | Run tests with coverage |
| `uv run ruff check .` | Lint |
| `uv run ruff format .` | Format |
| `uv run ruff check . && uv run ruff format --check .` | Lint + format check (CI) |
| `uv run mypy app/` | Type check |
| `pre-commit run --all-files` | Run pre-commit hooks |

## Quality Gates

- **Coverage**: minimum 80%
- **Linting**: ruff (E, W, F, I, N, UP, B, SIM, TC, RUF, D)
- **Type checking**: mypy strict mode
- **Docstrings**: Google style (mandatory on public APIs)
- **Commits**: Conventional Commits enforced via commitlint
