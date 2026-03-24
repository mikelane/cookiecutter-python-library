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
        'project_intent': 'prototype',
        'project_type': 'library',
        'include_runtime_contracts': 'n',
        'include_property_testing': 'n',
        'include_mutation_testing': 'n',
        'include_dependency_injection': 'n',
        'publish_to_pypi': 'n',
    }


@pytest.fixture(autouse=True)
def _mock_subprocess_for_tests(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock subprocess calls during tests to avoid running git, uv, etc."""
    import subprocess

    original_popen = subprocess.Popen

    def mock_popen(*args: Any, **kwargs: Any) -> Any:
        # Skip actual subprocess calls (git, uv, pre-commit) during tests
        # But allow the hook to run its file operations
        cmd_str = str(args[0]) if args else ''
        if any(x in cmd_str for x in ['git', 'uv', 'pre-commit']):
            return original_popen('true', **kwargs)
        return original_popen(*args, **kwargs)

    monkeypatch.setattr(subprocess, 'Popen', mock_popen)
