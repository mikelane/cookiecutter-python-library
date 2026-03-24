{%- if cookiecutter.project_type == 'tui-app' -%}
"""Terminal user interface for {{cookiecutter.project_name}}."""
from __future__ import annotations

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static


class {{cookiecutter.__package_name | replace('_', ' ') | title | replace(' ', '')}}App(App[None]):
    """A Textual app for {{cookiecutter.project_name}}."""

    TITLE = '{{cookiecutter.project_name}}'
    BINDINGS = [
        ('q', 'quit', 'Quit'),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Static('Welcome to {{cookiecutter.project_name}}!')
        yield Footer()


def run() -> None:
    """Run the TUI application."""
    app = {{cookiecutter.__package_name | replace('_', ' ') | title | replace(' ', '')}}App()
    app.run()


if __name__ == '__main__':
    run()
{%- endif %}
