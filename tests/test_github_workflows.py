"""Tests for GitHub Actions workflow generation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml
from pytest_cookies.plugin import Cookies, Result


@pytest.fixture
def context_simple_ci() -> dict[str, Any]:
    """Return context for a simple project with basic CI."""
    return {
        'project_name': 'Test Library',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'github_username': 'testauthor',
        'short_description': 'A test library',
        'long_description': 'A longer description',
        'license': 'MIT',
        'project_intent': 'prototype',
        'project_type': 'pure-python',
        'python_version_min': '3.11',
        'include_runtime_contracts': 'n',
        'include_property_testing': 'n',
        'include_mutation_testing': 'n',
        'include_dependency_injection': 'n',
        'use_semantic_release': 'n',
        'include_documentation': 'n',
        'include_bdd_testing': 'n',
        'include_benchmarks': 'n',
        'include_security_scanning': 'n',
        'use_codecov': 'y',
        'publish_to_pypi': 'y',
        'ci_platforms': 'ubuntu',
        'python_versions_test': '3.11,3.12',
    }


@pytest.fixture
def context_full_featured() -> dict[str, Any]:
    """Return context for a package project with all bells and whistles."""
    return {
        'project_name': 'Full Featured Library',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'github_username': 'testauthor',
        'short_description': 'A full-featured library',
        'long_description': 'A comprehensive description',
        'license': 'MIT',
        'project_intent': 'package',
        'project_type': 'pure-python',
        'python_version_min': '3.11',
        'include_runtime_contracts': 'y',
        'include_property_testing': 'y',
        'include_mutation_testing': 'y',
        'include_dependency_injection': 'n',
        'use_semantic_release': 'y',
        'include_documentation': 'y',
        'include_bdd_testing': 'y',
        'include_benchmarks': 'y',
        'include_security_scanning': 'y',
        'use_codecov': 'y',
        'publish_to_pypi': 'y',
        'ci_platforms': 'ubuntu,macos,windows',
        'python_versions_test': '3.11,3.12,3.13',
    }


def _load_workflow(project_path: Path, workflow_name: str) -> dict[str, Any]:
    """Load and parse a workflow YAML file."""
    workflow_path = project_path / '.github' / 'workflows' / workflow_name
    assert workflow_path.exists(), f'Workflow {workflow_name} does not exist'

    with workflow_path.open() as f:
        return yaml.safe_load(f)


class TestCIWorkflowGeneration:
    """Tests for CI workflow generation."""

    def test_ci_workflow_exists(self, cookies: Cookies, context_simple_ci: dict[str, Any]) -> None:
        """The CI workflow file is generated."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        ci_workflow = result.project_path / '.github' / 'workflows' / 'ci.yml'
        assert ci_workflow.exists()

    def test_ci_workflow_is_valid_yaml(self, cookies: Cookies, context_simple_ci: dict[str, Any]) -> None:
        """The CI workflow is valid YAML."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        workflow = _load_workflow(result.project_path, 'ci.yml')
        assert isinstance(workflow, dict)
        assert 'name' in workflow
        assert 'jobs' in workflow

    def test_ci_workflow_has_lint_job(self, cookies: Cookies, context_simple_ci: dict[str, Any]) -> None:
        """The CI workflow has a lint job using ruff."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        workflow = _load_workflow(result.project_path, 'ci.yml')
        assert 'lint' in workflow['jobs']

        lint_job = workflow['jobs']['lint']
        assert 'steps' in lint_job

        # Check that ruff is used in the lint job
        steps_text = str(lint_job['steps'])
        assert 'ruff' in steps_text.lower()

    def test_ci_workflow_has_type_check_job(self, cookies: Cookies, context_simple_ci: dict[str, Any]) -> None:
        """The CI workflow has a type-check job using mypy."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        workflow = _load_workflow(result.project_path, 'ci.yml')
        assert 'type-check' in workflow['jobs']

        type_check_job = workflow['jobs']['type-check']
        assert 'steps' in type_check_job

        # Check that mypy is used
        steps_text = str(type_check_job['steps'])
        assert 'mypy' in steps_text.lower()

    def test_ci_workflow_has_test_job_with_matrix(self, cookies: Cookies, context_simple_ci: dict[str, Any]) -> None:
        """The CI workflow has a test job with matrix strategy."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        workflow = _load_workflow(result.project_path, 'ci.yml')
        assert 'test' in workflow['jobs']

        test_job = workflow['jobs']['test']
        assert 'strategy' in test_job
        assert 'matrix' in test_job['strategy']

        matrix = test_job['strategy']['matrix']
        assert 'python-version' in matrix
        assert 'os' in matrix

    def test_ci_workflow_test_matrix_uses_correct_python_versions(
        self, cookies: Cookies, context_simple_ci: dict[str, Any]
    ) -> None:
        """The test matrix includes the correct Python versions from context."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        workflow = _load_workflow(result.project_path, 'ci.yml')
        test_job = workflow['jobs']['test']
        python_versions = test_job['strategy']['matrix']['python-version']

        # Context specified '3.11,3.12'
        assert '3.11' in python_versions
        assert '3.12' in python_versions

    def test_ci_workflow_test_matrix_uses_correct_platforms(
        self, cookies: Cookies, context_simple_ci: dict[str, Any]
    ) -> None:
        """The test matrix includes the correct platforms from context."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        workflow = _load_workflow(result.project_path, 'ci.yml')
        test_job = workflow['jobs']['test']
        platforms = test_job['strategy']['matrix']['os']

        # Context specified 'ubuntu'
        assert any('ubuntu' in str(p).lower() for p in platforms)

    def test_ci_workflow_test_matrix_multi_platform(
        self, cookies: Cookies, context_full_featured: dict[str, Any]
    ) -> None:
        """The test matrix includes multiple platforms for full-featured projects."""
        result = cookies.bake(extra_context=context_full_featured)
        assert result.exit_code == 0

        workflow = _load_workflow(result.project_path, 'ci.yml')
        test_job = workflow['jobs']['test']
        platforms = test_job['strategy']['matrix']['os']

        # Context specified 'ubuntu,macos,windows'
        platforms_str = str(platforms).lower()
        assert 'ubuntu' in platforms_str
        assert 'macos' in platforms_str
        assert 'windows' in platforms_str

    def test_ci_workflow_has_all_checks_gate_job(self, cookies: Cookies, context_simple_ci: dict[str, Any]) -> None:
        """The CI workflow has an all-checks gate job that depends on other jobs."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        workflow = _load_workflow(result.project_path, 'ci.yml')
        assert 'all-checks' in workflow['jobs']

        all_checks_job = workflow['jobs']['all-checks']
        assert 'needs' in all_checks_job

        # Should depend on lint, type-check, and test
        needs = all_checks_job['needs']
        assert 'lint' in needs
        assert 'type-check' in needs
        assert 'test' in needs

    def test_ci_workflow_uses_setup_uv_action(self, cookies: Cookies, context_simple_ci: dict[str, Any]) -> None:
        """The CI workflow uses the setup-uv composite action."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        workflow = _load_workflow(result.project_path, 'ci.yml')

        # Convert workflow to string to search for setup-uv action reference
        workflow_str = str(workflow)
        assert '.github/actions/setup-uv' in workflow_str

    def test_ci_workflow_includes_codecov_when_enabled(
        self, cookies: Cookies, context_simple_ci: dict[str, Any]
    ) -> None:
        """The CI workflow includes Codecov upload when use_codecov is y."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        workflow = _load_workflow(result.project_path, 'ci.yml')
        workflow_str = str(workflow)

        # Should reference codecov
        assert 'codecov' in workflow_str.lower()

    def test_ci_workflow_no_codecov_when_disabled(self, cookies: Cookies) -> None:
        """The CI workflow does not include Codecov when use_codecov is n."""
        context = {
            'project_name': 'No Codecov Library',
            'author_name': 'Test Author',
            'author_email': 'test@example.com',
            'github_username': 'testauthor',
            'short_description': 'A test library',
            'long_description': 'A longer description',
            'license': 'MIT',
            'project_intent': 'prototype',
            'project_type': 'pure-python',
            'python_version_min': '3.11',
            'include_runtime_contracts': 'n',
            'include_property_testing': 'n',
            'include_mutation_testing': 'n',
            'include_dependency_injection': 'n',
            'use_semantic_release': 'n',
            'include_documentation': 'n',
            'include_bdd_testing': 'n',
            'include_benchmarks': 'n',
            'include_security_scanning': 'n',
            'use_codecov': 'n',
            'publish_to_pypi': 'n',
            'ci_platforms': 'ubuntu',
            'python_versions_test': '3.11',
        }

        result = cookies.bake(extra_context=context)
        assert result.exit_code == 0

        workflow = _load_workflow(result.project_path, 'ci.yml')
        workflow_str = str(workflow)

        # Should NOT reference codecov
        assert 'codecov' not in workflow_str.lower()

    def test_ci_workflow_includes_docs_job_when_enabled(
        self, cookies: Cookies, context_full_featured: dict[str, Any]
    ) -> None:
        """The CI workflow includes a docs job when include_documentation is y."""
        result = cookies.bake(extra_context=context_full_featured)
        assert result.exit_code == 0

        workflow = _load_workflow(result.project_path, 'ci.yml')
        assert 'docs' in workflow['jobs']

        # all-checks should also depend on docs
        all_checks_needs = workflow['jobs']['all-checks']['needs']
        assert 'docs' in all_checks_needs

    def test_ci_workflow_no_docs_job_when_disabled(self, cookies: Cookies, context_simple_ci: dict[str, Any]) -> None:
        """The CI workflow does not include a docs job when include_documentation is n."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        workflow = _load_workflow(result.project_path, 'ci.yml')
        assert 'docs' not in workflow['jobs']


class TestCDWorkflowGeneration:
    """Tests for CD/release workflow generation."""

    def test_cd_workflow_exists(self, cookies: Cookies, context_simple_ci: dict[str, Any]) -> None:
        """The CD workflow file is generated."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        cd_workflow = result.project_path / '.github' / 'workflows' / 'cd.yml'
        assert cd_workflow.exists()

    def test_cd_workflow_is_valid_yaml(self, cookies: Cookies, context_simple_ci: dict[str, Any]) -> None:
        """The CD workflow is valid YAML."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        workflow = _load_workflow(result.project_path, 'cd.yml')
        assert isinstance(workflow, dict)
        assert 'name' in workflow

    def test_cd_workflow_uses_pypi_trusted_publishing(
        self, cookies: Cookies, context_simple_ci: dict[str, Any]
    ) -> None:
        """The CD workflow uses PyPI Trusted Publishing (OIDC)."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        workflow = _load_workflow(result.project_path, 'cd.yml')
        workflow_str = str(workflow)

        # Should use OIDC permissions
        assert 'id-token' in workflow_str
        assert 'write' in workflow_str

        # Should NOT use api-token or password
        assert 'api-token' not in workflow_str.lower()
        assert 'password' not in workflow_str.lower()

    def test_cd_workflow_manual_trigger_when_no_semantic_release(
        self, cookies: Cookies, context_simple_ci: dict[str, Any]
    ) -> None:
        """The CD workflow has manual/tag trigger when semantic release is disabled."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        workflow = _load_workflow(result.project_path, 'cd.yml')

        # Should trigger on push tags or workflow_dispatch
        # Note: PyYAML parses 'on:' as boolean True, not string 'on'
        on_triggers = workflow.get('on') or workflow.get(True)
        assert on_triggers is not None

        # Convert to string for easier checking
        triggers_str = str(on_triggers)
        assert 'tags' in triggers_str.lower() or 'workflow_dispatch' in triggers_str.lower()

    def test_cd_workflow_semantic_release_trigger_when_enabled(
        self, cookies: Cookies, context_full_featured: dict[str, Any]
    ) -> None:
        """The CD workflow integrates with semantic-release when enabled."""
        result = cookies.bake(extra_context=context_full_featured)
        assert result.exit_code == 0

        workflow = _load_workflow(result.project_path, 'cd.yml')
        workflow_str = str(workflow)

        # Should reference semantic-release
        assert 'semantic' in workflow_str.lower()


class TestSetupUVCompositeAction:
    """Tests for the setup-uv composite action."""

    def test_setup_uv_action_exists(self, cookies: Cookies, context_simple_ci: dict[str, Any]) -> None:
        """The setup-uv composite action file is generated."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        action_file = result.project_path / '.github' / 'actions' / 'setup-uv' / 'action.yml'
        assert action_file.exists()

    def test_setup_uv_action_is_valid_yaml(self, cookies: Cookies, context_simple_ci: dict[str, Any]) -> None:
        """The setup-uv action is valid YAML."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        action_file = result.project_path / '.github' / 'actions' / 'setup-uv' / 'action.yml'
        with action_file.open() as f:
            action = yaml.safe_load(f)

        assert isinstance(action, dict)
        assert 'name' in action
        assert 'runs' in action
        assert action['runs']['using'] == 'composite'

    def test_setup_uv_action_has_python_version_input(
        self, cookies: Cookies, context_simple_ci: dict[str, Any]
    ) -> None:
        """The setup-uv action has a python-version input parameter."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        action_file = result.project_path / '.github' / 'actions' / 'setup-uv' / 'action.yml'
        with action_file.open() as f:
            action = yaml.safe_load(f)

        assert 'inputs' in action
        assert 'python-version' in action['inputs']

    def test_setup_uv_action_installs_uv(self, cookies: Cookies, context_simple_ci: dict[str, Any]) -> None:
        """The setup-uv action installs uv."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        action_file = result.project_path / '.github' / 'actions' / 'setup-uv' / 'action.yml'
        with action_file.open() as f:
            action = yaml.safe_load(f)

        action_str = str(action)
        assert 'uv' in action_str.lower()

    def test_setup_uv_action_caches_dependencies(self, cookies: Cookies, context_simple_ci: dict[str, Any]) -> None:
        """The setup-uv action caches dependencies."""
        result = cookies.bake(extra_context=context_simple_ci)
        assert result.exit_code == 0

        action_file = result.project_path / '.github' / 'actions' / 'setup-uv' / 'action.yml'
        with action_file.open() as f:
            action = yaml.safe_load(f)

        action_str = str(action)
        assert 'cache' in action_str.lower()
