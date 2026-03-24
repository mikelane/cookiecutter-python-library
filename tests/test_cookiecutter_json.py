"""Tests for cookiecutter.json configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def test_cookiecutter_json_exists(template_dir: Path) -> None:
    """The cookiecutter.json file exists in the template root."""
    cookiecutter_file = template_dir / 'cookiecutter.json'
    assert cookiecutter_file.exists()


def test_cookiecutter_json_is_valid_json(cookiecutter_json: dict[str, Any]) -> None:
    """The cookiecutter.json contains valid JSON."""
    assert isinstance(cookiecutter_json, dict)


def test_has_required_basic_fields(cookiecutter_json: dict[str, Any]) -> None:
    """The cookiecutter.json contains all required basic fields."""
    required_fields = [
        'project_name',
        'author_name',
        'author_email',
        'short_description',
        'license',
    ]
    for field in required_fields:
        assert field in cookiecutter_json, f'Missing required field: {field}'


def test_has_project_intent_field(cookiecutter_json: dict[str, Any]) -> None:
    """The cookiecutter.json contains a project_intent field."""
    assert 'project_intent' in cookiecutter_json


def test_project_intent_has_valid_choices(cookiecutter_json: dict[str, Any]) -> None:
    """The project_intent field contains the expected choices."""
    expected_choices = ['prototype', 'project', 'package']
    project_intent = cookiecutter_json['project_intent']

    assert isinstance(project_intent, list), 'project_intent should be a list of choices'
    assert set(project_intent) == set(expected_choices), f'Expected choices {expected_choices}, got {project_intent}'


def test_has_project_type_field(cookiecutter_json: dict[str, Any]) -> None:
    """The cookiecutter.json contains a project_type field."""
    assert 'project_type' in cookiecutter_json


def test_project_type_has_valid_choices(cookiecutter_json: dict[str, Any]) -> None:
    """The project_type field contains the expected choices."""
    expected_choices = ['pure-python', 'rust-backed', 'aws-cdk']
    project_type = cookiecutter_json['project_type']

    assert isinstance(project_type, list), 'project_type should be a list of choices'
    assert set(project_type) == set(expected_choices), f'Expected choices {expected_choices}, got {project_type}'


def test_has_python_version_min_field(cookiecutter_json: dict[str, Any]) -> None:
    """The cookiecutter.json contains a python_version_min field."""
    assert 'python_version_min' in cookiecutter_json


def test_python_version_min_has_valid_choices(cookiecutter_json: dict[str, Any]) -> None:
    """The python_version_min field contains valid Python version choices."""
    python_versions = cookiecutter_json['python_version_min']
    assert isinstance(python_versions, list)
    assert '3.11' in python_versions
    assert '3.12' in python_versions
    assert '3.13' in python_versions


def test_has_feature_flags(cookiecutter_json: dict[str, Any]) -> None:
    """The cookiecutter.json contains feature flag fields."""
    feature_flags = [
        'include_runtime_contracts',
        'include_property_testing',
        'include_mutation_testing',
        'include_dependency_injection',
        'include_bdd_testing',
        'include_benchmarks',
        'include_documentation',
        'use_semantic_release',
        'include_security_scanning',
        'use_codecov',
        'publish_to_pypi',
    ]
    for flag in feature_flags:
        assert flag in cookiecutter_json, f'Missing feature flag: {flag}'


def test_has_ci_platforms_field(cookiecutter_json: dict[str, Any]) -> None:
    """The cookiecutter.json contains ci_platforms field."""
    assert 'ci_platforms' in cookiecutter_json


def test_ci_platforms_has_valid_choices(cookiecutter_json: dict[str, Any]) -> None:
    """The ci_platforms field contains valid platform choices."""
    ci_platforms = cookiecutter_json['ci_platforms']
    assert isinstance(ci_platforms, list)
    expected_platforms = {'ubuntu', 'macos', 'windows'}
    assert set(ci_platforms).issubset(expected_platforms)


def test_has_python_versions_test_field(cookiecutter_json: dict[str, Any]) -> None:
    """The cookiecutter.json contains python_versions_test field."""
    assert 'python_versions_test' in cookiecutter_json


def test_python_versions_test_has_valid_choices(cookiecutter_json: dict[str, Any]) -> None:
    """The python_versions_test field contains valid Python version choices."""
    python_versions = cookiecutter_json['python_versions_test']
    assert isinstance(python_versions, list)
    valid_versions = {'3.11', '3.12', '3.13', '3.14'}
    assert set(python_versions).issubset(valid_versions)


def test_has_computed_fields(cookiecutter_json: dict[str, Any]) -> None:
    """The cookiecutter.json contains computed fields using Jinja2 templates."""
    computed_fields = ['__project_name', '__package_name']
    for field in computed_fields:
        assert field in cookiecutter_json, f'Missing computed field: {field}'
