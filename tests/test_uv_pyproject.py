"""Tests for uv-based pyproject.toml generation."""

from __future__ import annotations

import tomllib
from typing import Any

from pytest_cookies.plugin import Cookies


def test_generated_pyproject_does_not_use_poetry(cookies: Cookies) -> None:
    """The generated pyproject.toml uses uv, not Poetry."""
    context = {
        'project_name': 'Test Library',
        'project_type': 'library',
        'python_version_min': '3.11',
    }
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0

    pyproject_path = result.project_path / 'pyproject.toml'
    config = tomllib.loads(pyproject_path.read_text())

    # Should NOT have Poetry configuration
    assert 'tool' in config
    assert 'poetry' not in config.get('tool', {})


def test_generated_pyproject_uses_hatchling(cookies: Cookies) -> None:
    """The generated pyproject.toml uses hatchling as build backend."""
    context = {
        'project_name': 'Test Library',
        'project_type': 'library',
        'python_version_min': '3.11',
    }
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0

    pyproject_path = result.project_path / 'pyproject.toml'
    config = tomllib.loads(pyproject_path.read_text())

    # Check build system
    assert 'build-system' in config
    assert config['build-system']['requires'] == ['hatchling']
    assert config['build-system']['build-backend'] == 'hatchling.build'


def test_generated_pyproject_uses_pep621_metadata(cookies: Cookies) -> None:
    """The generated pyproject.toml uses PEP 621 [project] metadata."""
    context = {
        'project_name': 'Test Library',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'A test library',
        'python_version_min': '3.11',
        'project_type': 'library',
    }
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0

    pyproject_path = result.project_path / 'pyproject.toml'
    config = tomllib.loads(pyproject_path.read_text())

    # Check PEP 621 metadata
    assert 'project' in config
    project = config['project']
    assert project['name'] == 'test-library'
    assert project['description'] == 'A test library'
    assert 'requires-python' in project
    assert project['requires-python'].startswith('>=3.11')


def test_generated_pyproject_has_optional_dependencies(cookies: Cookies) -> None:
    """The generated pyproject.toml has optional dependency groups."""
    context = {
        'project_name': 'Test Library',
        'project_type': 'library',
        'python_version_min': '3.11',
    }
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0

    pyproject_path = result.project_path / 'pyproject.toml'
    config = tomllib.loads(pyproject_path.read_text())

    # Check optional dependencies
    assert 'project' in config
    assert 'optional-dependencies' in config['project']
    optional_deps = config['project']['optional-dependencies']

    # Should have test and dev groups
    assert 'test' in optional_deps
    assert 'dev' in optional_deps

    # Test group should have pytest
    assert any('pytest' in dep for dep in optional_deps['test'])

    # Dev group should have ruff and mypy
    assert any('ruff' in dep for dep in optional_deps['dev'])
    assert any('mypy' in dep for dep in optional_deps['dev'])


def test_generated_pyproject_only_uses_ruff_not_black(cookies: Cookies) -> None:
    """The generated pyproject.toml only has Ruff config, not Black or isort."""
    context = {
        'project_name': 'Test Library',
        'project_type': 'library',
        'python_version_min': '3.11',
    }
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0

    pyproject_path = result.project_path / 'pyproject.toml'
    config = tomllib.loads(pyproject_path.read_text())

    # Should have Ruff
    assert 'tool' in config
    assert 'ruff' in config['tool']

    # Should NOT have Black or isort
    assert 'black' not in config.get('tool', {})
    assert 'isort' not in config.get('tool', {})


def test_generated_ruff_config_has_format_section(cookies: Cookies) -> None:
    """The generated Ruff config includes format section."""
    context = {
        'project_name': 'Test Library',
        'project_type': 'library',
        'python_version_min': '3.11',
    }
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0

    pyproject_path = result.project_path / 'pyproject.toml'
    config = tomllib.loads(pyproject_path.read_text())

    # Check Ruff format configuration
    assert 'tool' in config
    assert 'ruff' in config['tool']
    ruff_config = config['tool']['ruff']

    # Should have format settings
    assert 'format' in ruff_config
    assert 'quote-style' in ruff_config['format']


def test_generated_ruff_config_selects_all_rules(cookies: Cookies) -> None:
    """The generated Ruff config selects ALL rules as baseline."""
    context = {
        'project_name': 'Test Library',
        'project_type': 'library',
        'python_version_min': '3.11',
    }
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0

    pyproject_path = result.project_path / 'pyproject.toml'
    config = tomllib.loads(pyproject_path.read_text())

    # Check Ruff lint configuration
    ruff_config = config['tool']['ruff']
    assert 'lint' in ruff_config
    assert 'select' in ruff_config['lint']
    assert 'ALL' in ruff_config['lint']['select']
