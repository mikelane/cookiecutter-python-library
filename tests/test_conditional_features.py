"""Tests for conditional features based on cookiecutter configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from pytest_cookies.plugin import Cookies


@pytest.fixture
def base_context() -> dict[str, Any]:
    """Return base context for template generation."""
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
    }


def test_documentation_directory_created_when_enabled(cookies: Cookies, base_context: dict[str, Any]) -> None:
    """When include_documentation is enabled, a docs/ directory is created."""
    context = base_context | {'include_documentation': 'y'}
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    docs_dir = result.project_path / 'docs'
    assert docs_dir.is_dir()


def test_documentation_directory_not_created_when_disabled(cookies: Cookies, base_context: dict[str, Any]) -> None:
    """When include_documentation is disabled, no docs/ directory is created."""
    context = base_context | {'include_documentation': 'n'}
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    docs_dir = result.project_path / 'docs'
    assert not docs_dir.exists()
    mkdocs_yml = result.project_path / 'mkdocs.yml'
    assert not mkdocs_yml.exists()


def test_bdd_directory_created_when_enabled(cookies: Cookies, base_context: dict[str, Any]) -> None:
    """When include_bdd_testing is enabled, a tests/bdd/ directory is created."""
    context = base_context | {'include_bdd_testing': 'y'}
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    bdd_dir = result.project_path / 'tests' / 'bdd'
    assert bdd_dir.is_dir()


def test_bdd_directory_not_created_when_disabled(cookies: Cookies, base_context: dict[str, Any]) -> None:
    """When include_bdd_testing is disabled, no tests/bdd/ directory is created."""
    context = base_context | {'include_bdd_testing': 'n'}
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    bdd_dir = result.project_path / 'tests' / 'bdd'
    assert not bdd_dir.exists()


def test_benchmarks_directory_created_when_enabled(cookies: Cookies, base_context: dict[str, Any]) -> None:
    """When include_benchmarks is enabled, a benchmarks/ directory is created."""
    context = base_context | {'include_benchmarks': 'y'}
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    benchmarks_dir = result.project_path / 'benchmarks'
    assert benchmarks_dir.is_dir()


def test_benchmarks_directory_not_created_when_disabled(cookies: Cookies, base_context: dict[str, Any]) -> None:
    """When include_benchmarks is disabled, no benchmarks/ directory is created."""
    context = base_context | {'include_benchmarks': 'n'}
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    benchmarks_dir = result.project_path / 'benchmarks'
    assert not benchmarks_dir.exists()


def test_unit_and_integration_test_directories_always_created(cookies: Cookies, base_context: dict[str, Any]) -> None:
    """Unit and integration test directories are always created regardless of options."""
    result = cookies.bake(extra_context=base_context)

    assert result.exit_code == 0
    unit_dir = result.project_path / 'tests' / 'unit'
    integration_dir = result.project_path / 'tests' / 'integration'

    assert unit_dir.is_dir()
    assert integration_dir.is_dir()


def test_version_file_created_when_semantic_release_enabled(cookies: Cookies, base_context: dict[str, Any]) -> None:
    """When use_semantic_release is enabled, _version.py is created."""
    context = base_context | {'use_semantic_release': 'y'}
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    version_file = result.project_path / 'src' / 'test_library' / '_version.py'
    assert version_file.exists()


def test_version_file_not_created_when_semantic_release_disabled(
    cookies: Cookies, base_context: dict[str, Any]
) -> None:
    """When use_semantic_release is disabled, no _version.py is created."""
    context = base_context | {'use_semantic_release': 'n'}
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    version_file = result.project_path / 'src' / 'test_library' / '_version.py'
    assert not version_file.exists()


def test_multiple_features_can_be_combined(cookies: Cookies, base_context: dict[str, Any]) -> None:
    """Multiple optional features can be enabled together."""
    context = base_context | {
        'include_documentation': 'y',
        'include_bdd_testing': 'y',
        'include_benchmarks': 'y',
        'use_semantic_release': 'y',
    }
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0

    # All optional features should be present
    assert (result.project_path / 'docs').is_dir()
    assert (result.project_path / 'tests' / 'bdd').is_dir()
    assert (result.project_path / 'benchmarks').is_dir()
    assert (result.project_path / 'src' / 'test_library' / '_version.py').exists()

    # Core structure should still be present
    assert (result.project_path / 'tests' / 'unit').is_dir()
    assert (result.project_path / 'tests' / 'integration').is_dir()
    assert (result.project_path / 'src' / 'test_library').is_dir()


def test_bdd_dependencies_added_when_bdd_enabled(cookies: Cookies, base_context: dict[str, Any]) -> None:
    """When BDD is enabled, pytest-bdd is added to dependencies."""
    import tomllib

    context = base_context | {'include_bdd_testing': 'y'}
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0

    pyproject_path = result.project_path / 'pyproject.toml'
    config = tomllib.loads(pyproject_path.read_text())

    # Check test dependencies include pytest-bdd
    test_deps = config['project']['optional-dependencies']['test']
    assert any('pytest-bdd' in dep for dep in test_deps)


def test_bdd_dependencies_not_added_when_bdd_disabled(cookies: Cookies, base_context: dict[str, Any]) -> None:
    """When BDD is disabled, pytest-bdd is not in dependencies."""
    import tomllib

    context = base_context | {'include_bdd_testing': 'n'}
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0

    pyproject_path = result.project_path / 'pyproject.toml'
    config = tomllib.loads(pyproject_path.read_text())

    # Check test dependencies do not include pytest-bdd
    test_deps = config['project']['optional-dependencies']['test']
    assert not any('pytest-bdd' in dep for dep in test_deps)


def test_mkdocs_dependencies_added_when_docs_enabled(cookies: Cookies, base_context: dict[str, Any]) -> None:
    """When documentation is enabled, MkDocs Material dependencies are added."""
    import tomllib

    context = base_context | {'include_documentation': 'y'}
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0

    pyproject_path = result.project_path / 'pyproject.toml'
    config = tomllib.loads(pyproject_path.read_text())

    # Check for docs optional dependency group
    assert 'docs' in config['project']['optional-dependencies']
    docs_deps = config['project']['optional-dependencies']['docs']
    assert any('mkdocs-material' in dep.lower() for dep in docs_deps)


def test_mkdocs_dependencies_not_added_when_docs_disabled(cookies: Cookies, base_context: dict[str, Any]) -> None:
    """When documentation is disabled, no MkDocs dependencies are added."""
    import tomllib

    context = base_context | {'include_documentation': 'n'}
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0

    pyproject_path = result.project_path / 'pyproject.toml'
    config = tomllib.loads(pyproject_path.read_text())

    # Check docs optional dependency group doesn't exist
    assert 'docs' not in config['project']['optional-dependencies']


def test_pytest_benchmark_added_when_benchmarks_enabled(cookies: Cookies, base_context: dict[str, Any]) -> None:
    """When benchmarks are enabled, pytest-benchmark is added."""
    import tomllib

    context = base_context | {'include_benchmarks': 'y'}
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0

    pyproject_path = result.project_path / 'pyproject.toml'
    config = tomllib.loads(pyproject_path.read_text())

    # Check test dependencies include pytest-benchmark
    test_deps = config['project']['optional-dependencies']['test']
    assert any('pytest-benchmark' in dep for dep in test_deps)


def test_pytest_benchmark_not_added_when_benchmarks_disabled(cookies: Cookies, base_context: dict[str, Any]) -> None:
    """When benchmarks are disabled, pytest-benchmark is not added."""
    import tomllib

    context = base_context | {'include_benchmarks': 'n'}
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0

    pyproject_path = result.project_path / 'pyproject.toml'
    config = tomllib.loads(pyproject_path.read_text())

    # Check test dependencies do not include pytest-benchmark
    test_deps = config['project']['optional-dependencies']['test']
    assert not any('pytest-benchmark' in dep for dep in test_deps)
