# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A **cookiecutter template** that generates Python library projects. The `{{ cookiecutter.__project_name }}/` directory contains **Jinja2 templates**, not runnable Python code. Do not try to execute, import, or lint files inside that directory directly.

## Commands

```bash
uv run pytest tests/ -v                    # Test template generation
uv run pytest tests/ -v --cov              # With coverage (90% threshold)
uv run ruff check .                        # Lint
uv run ruff format --check .               # Format check
uv run mypy hooks tests                    # Type check (strict mode)
```

## Template Architecture

- **cookiecutter.json**: All template variables and choices (5 project types, feature toggles)
- **hooks/pre_gen_project.py**: Validates project_name before generation
- **hooks/post_gen_project.py**: Removes conditional dirs/files based on choices, runs `git init` + `uv sync` + `pre-commit install`
- **tests/**: Uses `pytest-cookies` to test template generation for each project type and feature combination

## When Adding or Modifying Project Types

1. Update `cookiecutter.json` with new variables/choices
2. Add conditional Jinja2 blocks in template files (use `{% if cookiecutter.project_type == 'new-type' %}`)
3. Update `hooks/post_gen_project.py` to clean up files not needed for the new type
4. Add tests in `tests/` covering the new type's generation and file structure

## Code Style

- Ruff with ALL rules selected, single quotes, 120 char line length
- mypy strict mode
- Generated projects enforce 100% test coverage

## Known Debt

- Template `README.md` still references poetry commands instead of uv
- `include_security_scanning` option exists but has no CI implementation yet
- AWS CDK project type has minimal infrastructure scaffolding
- Two pre-existing test failures: `ci_platforms` and `python_versions_test` are CSV strings in cookiecutter.json but tests expect lists
