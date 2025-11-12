"""Integration tests for template generation using pytest-cookies."""
from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

import pytest
from pytest_cookies.plugin import Cookies


@pytest.fixture
def context_simple() -> dict[str, Any]:
    """Return context for a simple project."""
    return {
        'project_name': 'Test Library',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'github_username': 'testauthor',
        'short_description': 'A test library',
        'long_description': 'A longer description',
        'license': 'MIT',
        'project_type': 'simple',
        'python_version_min': '3.11',
        'use_semantic_release': 'n',
        'include_documentation': 'n',
        'include_bdd_testing': 'n',
        'include_benchmarks': 'n',
        'include_security_scanning': 'n',
        'use_codecov': 'y',
        'ci_platforms': 'ubuntu',
        'python_versions_test': '3.11',
    }


def test_template_generates_successfully(cookies: Cookies, context_simple: dict[str, Any]) -> None:
    """The template generates a project successfully with valid context."""
    # Skip hooks to make tests fast
    from cookiecutter.main import cookiecutter

    template_dir = Path(__file__).parent.parent
    result = cookies.bake(extra_context=context_simple)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.is_dir()


def test_generated_project_has_expected_structure(cookies: Cookies, context_simple: dict[str, Any]) -> None:
    """The generated project has the expected directory structure."""
    result = cookies.bake(extra_context=context_simple)
    assert result.exit_code == 0

    project_dir = result.project_path

    # Check for essential files
    assert (project_dir / 'pyproject.toml').exists()
    assert (project_dir / 'README.md').exists()
    assert (project_dir / 'LICENSE.txt').exists()
    assert (project_dir / '.gitignore').exists()
    assert (project_dir / '.pre-commit-config.yaml').exists()

    # Check for src directory and package
    src_dir = project_dir / 'src'
    assert src_dir.is_dir()

    package_dir = src_dir / 'test_library'
    assert package_dir.is_dir()
    assert (package_dir / '__init__.py').exists()

    # Check for tests directory
    tests_dir = project_dir / 'tests'
    assert tests_dir.is_dir()


def test_generated_pyproject_toml_is_valid(cookies: Cookies, context_simple: dict[str, Any]) -> None:
    """The generated pyproject.toml is valid TOML."""
    result = cookies.bake(extra_context=context_simple)
    assert result.exit_code == 0

    pyproject_path = result.project_path / 'pyproject.toml'
    pyproject_content = pyproject_path.read_text()

    # Should be valid TOML
    config = tomllib.loads(pyproject_content)
    assert isinstance(config, dict)


def test_generated_project_has_ruff_config(cookies: Cookies, context_simple: dict[str, Any]) -> None:
    """The generated pyproject.toml contains Ruff configuration."""
    result = cookies.bake(extra_context=context_simple)
    assert result.exit_code == 0

    pyproject_path = result.project_path / 'pyproject.toml'
    pyproject_content = pyproject_path.read_text()
    config = tomllib.loads(pyproject_content)

    # Check for Ruff configuration
    assert 'tool' in config
    assert 'ruff' in config['tool']


def test_generated_project_has_mypy_config(cookies: Cookies, context_simple: dict[str, Any]) -> None:
    """The generated pyproject.toml contains mypy configuration."""
    result = cookies.bake(extra_context=context_simple)
    assert result.exit_code == 0

    pyproject_path = result.project_path / 'pyproject.toml'
    pyproject_content = pyproject_path.read_text()
    config = tomllib.loads(pyproject_content)

    # Check for mypy configuration
    assert 'tool' in config
    assert 'mypy' in config['tool']
    assert config['tool']['mypy']['strict'] is True


def test_generated_project_has_pytest_config(cookies: Cookies, context_simple: dict[str, Any]) -> None:
    """The generated pyproject.toml contains pytest configuration."""
    result = cookies.bake(extra_context=context_simple)
    assert result.exit_code == 0

    pyproject_path = result.project_path / 'pyproject.toml'
    pyproject_content = pyproject_path.read_text()
    config = tomllib.loads(pyproject_content)

    # Check for pytest configuration
    assert 'tool' in config
    assert 'pytest' in config['tool']


def test_precommit_config_exists_and_valid(cookies: Cookies, context_simple: dict[str, Any]) -> None:
    """The generated .pre-commit-config.yaml exists and is valid."""
    result = cookies.bake(extra_context=context_simple)
    assert result.exit_code == 0

    precommit_path = result.project_path / '.pre-commit-config.yaml'
    assert precommit_path.exists()

    import yaml

    with precommit_path.open() as f:
        config = yaml.safe_load(f)

    assert 'repos' in config
    assert isinstance(config['repos'], list)
    assert len(config['repos']) > 0
