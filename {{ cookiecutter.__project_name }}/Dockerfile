{%- if cookiecutter.project_type in ['cli-app', 'tui-app'] -%}
FROM python:{{cookiecutter.python_version_min}}-slim

WORKDIR /app

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev --no-editable

# Copy application code
COPY src/ src/

# Run the application
ENTRYPOINT ["uv", "run", "{{cookiecutter.__package_name}}"]
{%- endif %}
