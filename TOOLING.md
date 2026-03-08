# Tooling

## Development Commands

| Command | Description |
|---------|-------------|
| `uv sync --all-extras` | Install all dependencies |
| `uv run uvicorn app.main:app --reload --port 8086` | Run dev server |
| `uv run pytest tests/ -n auto --no-header -q` | Run tests (parallel) |
| `uv run pytest tests/ -n auto --cov=app --cov-report=html` | Tests with coverage |
| `uv run ruff check .` | Lint |
| `uv run ruff format .` | Format |
| `uv run ruff check . && uv run ruff format --check .` | Lint + format check (CI) |
| `uv run mypy app/` | Type check |
| `pre-commit run --all-files` | Run all pre-commit hooks |

## Quality Gates

| Check | Tool | Threshold/Config |
|-------|------|------------------|
| Coverage | pytest-cov | minimum 80% |
| Linting | ruff | E, W, F, I, N, UP, B, SIM, TC, RUF, D |
| Type checking | mypy | strict mode |
| Docstrings | ruff (pydocstyle) | Google style |
| Commits | commitlint | Conventional Commits |

## Pre-commit Hooks

Configured hooks (see `.pre-commit-config.yaml`):

- `trailing-whitespace` — Remove trailing whitespace
- `end-of-file-fixer` — Ensure files end with newline
- `check-yaml` / `check-toml` — Validate config files
- `check-added-large-files` — Prevent large file commits (>500KB)
- `check-merge-conflict` — Detect merge conflict markers
- `debug-statements` — Detect debug statements
- `ruff` — Lint with auto-fix
- `ruff-format` — Format code
- `commitlint` — Enforce conventional commits

## CI/CD Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci-tests-and-lint.yml` | Push/PR to main, develop | Lint, type check, tests |
| `ci-pr-branch-check.yml` | PR opened/edited | Branch naming, target validation |
| `cd-release.yml` | Push to main / Manual | Create GitHub Release with changelog |

## Docker

```bash
# Build
docker build -f docker/Dockerfile -t unified-ui-re-act-agent-service .

# Run
docker run -p 8086:8086 --env-file .env unified-ui-re-act-agent-service
```

## IDE Configuration

Recommended VS Code extensions:

- `ms-python.python` — Python support
- `ms-python.vscode-pylance` — Type checking
- `charliermarsh.ruff` — Ruff integration
- `tamasfe.even-better-toml` — TOML support

Recommended settings (`.vscode/settings.json`):

```json
{
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll.ruff": "explicit",
            "source.organizeImports.ruff": "explicit"
        }
    }
}
```
