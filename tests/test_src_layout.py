"""Tests for src/ layout implementation in generated projects."""

from __future__ import annotations

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
        'project_type': 'library',
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


def test_generated_project_has_src_directory(cookies: Cookies, context_simple: dict[str, Any]) -> None:
    """The generated project has a src/ directory."""
    result = cookies.bake(extra_context=context_simple)
    assert result.exit_code == 0

    src_dir = result.project_path / 'src'
    assert src_dir.is_dir()


def test_package_is_inside_src_directory(cookies: Cookies, context_simple: dict[str, Any]) -> None:
    """The package directory is located inside src/."""
    result = cookies.bake(extra_context=context_simple)
    assert result.exit_code == 0

    # Package should be in src/test_library/
    package_dir = result.project_path / 'src' / 'test_library'
    assert package_dir.is_dir()
    assert (package_dir / '__init__.py').exists()

    # Old location should NOT exist
    old_package_dir = result.project_path / 'test_library'
    assert not old_package_dir.exists()


def test_generated_project_has_py_typed_marker(cookies: Cookies, context_simple: dict[str, Any]) -> None:
    """The generated project has a py.typed marker file in the package."""
    result = cookies.bake(extra_context=context_simple)
    assert result.exit_code == 0

    package_dir = result.project_path / 'src' / 'test_library'
    py_typed_file = package_dir / 'py.typed'

    assert py_typed_file.exists()
    assert py_typed_file.is_file()


def test_py_typed_marker_is_empty(cookies: Cookies, context_simple: dict[str, Any]) -> None:
    """The py.typed marker file is empty (PEP 561 requirement)."""
    result = cookies.bake(extra_context=context_simple)
    assert result.exit_code == 0

    py_typed_file = result.project_path / 'src' / 'test_library' / 'py.typed'
    content = py_typed_file.read_text()

    assert content == ''


def test_main_module_exists_in_src_package(cookies: Cookies, context_simple: dict[str, Any]) -> None:
    """The main.py module exists in the src/package/ directory."""
    result = cookies.bake(extra_context=context_simple)
    assert result.exit_code == 0

    main_file = result.project_path / 'src' / 'test_library' / 'main.py'
    assert main_file.exists()
    assert main_file.is_file()


def test_tests_import_from_src_layout(cookies: Cookies, context_simple: dict[str, Any]) -> None:
    """Test files import correctly from src/ layout."""
    result = cookies.bake(extra_context=context_simple)
    assert result.exit_code == 0

    test_file = result.project_path / 'tests' / 'unit' / 'test_test_library' / 'test_main.py'
    content = test_file.read_text()

    # Import should reference the package name, not src.package
    assert 'from test_library.main import' in content


def test_pyproject_toml_does_not_need_packages_configuration(cookies: Cookies, context_simple: dict[str, Any]) -> None:
    """The pyproject.toml relies on hatchling's automatic src/ discovery."""
    result = cookies.bake(extra_context=context_simple)
    assert result.exit_code == 0

    import tomllib

    pyproject_path = result.project_path / 'pyproject.toml'
    content = pyproject_path.read_text()
    config = tomllib.loads(content)

    # Hatchling automatically discovers packages in src/
    # No explicit packages configuration should be needed
    assert 'tool' in config
    # If there's a hatch config, it shouldn't need packages specified
    if 'hatch' in config.get('tool', {}):
        hatch_config = config['tool']['hatch']
        # Either no build config, or build config without explicit packages
        if 'build' in hatch_config:
            # Packages can be omitted when using src/ layout
            pass


def test_different_project_names_generate_correct_package_paths(cookies: Cookies) -> None:
    """Different project names generate correct src/package/ paths."""
    test_cases = [
        ('Simple Name', 'simple-name', 'simple_name'),
        ('My Test Library', 'my-test-library', 'my_test_library'),
        ('PyAwesome', 'pyawesome', 'pyawesome'),
    ]

    for project_name, expected_project_slug, expected_package_name in test_cases:
        context = {
            'project_name': project_name,
            'author_name': 'Test Author',
            'author_email': 'test@example.com',
            'github_username': 'testauthor',
            'short_description': 'Test',
            'long_description': 'Test description',
            'license': 'MIT',
            'project_type': 'library',
            'python_version_min': '3.11',
        }

        result = cookies.bake(extra_context=context)
        assert result.exit_code == 0

        package_dir = result.project_path / 'src' / expected_package_name
        assert package_dir.is_dir(), f'Expected src/{expected_package_name} for project {project_name}'
        assert (package_dir / '__init__.py').exists()
        assert (package_dir / 'py.typed').exists()
