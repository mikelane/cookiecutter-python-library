{%- if cookiecutter.project_type in ['cli-app', 'tui-app'] -%}
"""Command-line interface for {{cookiecutter.project_name}}."""
from __future__ import annotations

import typer
from loguru import logger

app = typer.Typer(
    name='{{cookiecutter.__package_name}}',
    help='{{cookiecutter.short_description}}',
    add_completion=False,
)


@app.command()
def hello(name: str = typer.Argument(default='world', help='Name to greet.')) -> None:
    """Greet someone by name."""
    logger.info(f'Hello, {name}!')
    typer.echo(f'Hello, {name}!')


if __name__ == '__main__':
    app()
{%- endif %}
