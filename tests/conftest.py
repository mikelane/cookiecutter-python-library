"""Pytest configuration and fixtures for cookiecutter template tests."""
from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def template_dir() -> Path:
    """Return the path to the cookiecutter template directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def cookiecutter_json(template_dir: Path) -> dict[str, Any]:
    """Load and return the cookiecutter.json configuration."""
    with (template_dir / 'cookiecutter.json').open() as f:
        return json.load(f)


@pytest.fixture
def temp_project_dir() -> Path:
    """Create a temporary directory for generating test projects."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def default_context() -> dict[str, Any]:
    """Return default context for cookiecutter generation."""
    return {
        'project_name': 'Test Library',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'A test library',
        'long_description': 'A longer description of the test library',
        'license': 'MIT',
    }


@pytest.fixture(autouse=True)
def _skip_hooks_for_tests(monkeypatch: pytest.MonkeyPatch) -> None:
    """Skip post_gen_project hook execution during tests to make them fast."""
    import subprocess

    original_popen = subprocess.Popen

    def mock_popen(*args: Any, **kwargs: Any) -> Any:
        # Skip actual subprocess calls during tests
        return original_popen('true', **kwargs)

    monkeypatch.setattr(subprocess, 'Popen', mock_popen)
