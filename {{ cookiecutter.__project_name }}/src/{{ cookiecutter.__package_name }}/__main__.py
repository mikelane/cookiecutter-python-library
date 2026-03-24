{%- if cookiecutter.project_type in ['cli-app', 'tui-app'] -%}
"""Allow running the package as `python -m {{cookiecutter.__package_name}}`."""
from __future__ import annotations

from {{cookiecutter.__package_name}}.cli import app

app()
{%- endif %}
