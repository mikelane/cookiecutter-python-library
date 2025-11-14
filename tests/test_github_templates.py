"""Tests for GitHub templates (issues, PR, CODEOWNERS, dependabot)."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml
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
        'python_versions_test': '3.11,3.12',
    }


class TestIssueTemplates:
    """Tests for GitHub issue templates."""

    def test_bug_report_template_exists(self, cookies: Cookies, context_simple: dict[str, Any]) -> None:
        """The bug report issue template is generated."""
        result = cookies.bake(extra_context=context_simple)
        assert result.exit_code == 0

        template_path = result.project_path / '.github' / 'ISSUE_TEMPLATE' / 'bug_report.md'
        assert template_path.exists()

    def test_feature_request_template_exists(
        self, cookies: Cookies, context_simple: dict[str, Any]
    ) -> None:
        """The feature request issue template is generated."""
        result = cookies.bake(extra_context=context_simple)
        assert result.exit_code == 0

        template_path = result.project_path / '.github' / 'ISSUE_TEMPLATE' / 'feature_request.md'
        assert template_path.exists()

    def test_security_template_exists(self, cookies: Cookies, context_simple: dict[str, Any]) -> None:
        """The security vulnerability issue template is generated."""
        result = cookies.bake(extra_context=context_simple)
        assert result.exit_code == 0

        template_path = (
            result.project_path / '.github' / 'ISSUE_TEMPLATE' / 'security_vulnerability.md'
        )
        assert template_path.exists()


class TestPullRequestTemplate:
    """Tests for GitHub PR template."""

    def test_pr_template_exists(self, cookies: Cookies, context_simple: dict[str, Any]) -> None:
        """The pull request template is generated."""
        result = cookies.bake(extra_context=context_simple)
        assert result.exit_code == 0

        template_path = result.project_path / '.github' / 'PULL_REQUEST_TEMPLATE.md'
        assert template_path.exists()

    def test_pr_template_has_checklist(self, cookies: Cookies, context_simple: dict[str, Any]) -> None:
        """The PR template contains a checklist."""
        result = cookies.bake(extra_context=context_simple)
        assert result.exit_code == 0

        template_path = result.project_path / '.github' / 'PULL_REQUEST_TEMPLATE.md'
        content = template_path.read_text()

        # Should have checkboxes
        assert '- [ ]' in content or '- []' in content


class TestCodeowners:
    """Tests for CODEOWNERS file."""

    def test_codeowners_exists(self, cookies: Cookies, context_simple: dict[str, Any]) -> None:
        """The CODEOWNERS file is generated."""
        result = cookies.bake(extra_context=context_simple)
        assert result.exit_code == 0

        codeowners_path = result.project_path / '.github' / 'CODEOWNERS'
        assert codeowners_path.exists()

    def test_codeowners_has_owner(self, cookies: Cookies, context_simple: dict[str, Any]) -> None:
        """The CODEOWNERS file includes the project owner."""
        result = cookies.bake(extra_context=context_simple)
        assert result.exit_code == 0

        codeowners_path = result.project_path / '.github' / 'CODEOWNERS'
        content = codeowners_path.read_text()

        # Should reference the github username
        assert '@testauthor' in content


class TestDependabot:
    """Tests for dependabot configuration."""

    def test_dependabot_exists(self, cookies: Cookies, context_simple: dict[str, Any]) -> None:
        """The dependabot.yml file is generated."""
        result = cookies.bake(extra_context=context_simple)
        assert result.exit_code == 0

        dependabot_path = result.project_path / '.github' / 'dependabot.yml'
        assert dependabot_path.exists()

    def test_dependabot_is_valid_yaml(self, cookies: Cookies, context_simple: dict[str, Any]) -> None:
        """The dependabot.yml is valid YAML."""
        result = cookies.bake(extra_context=context_simple)
        assert result.exit_code == 0

        dependabot_path = result.project_path / '.github' / 'dependabot.yml'
        with dependabot_path.open() as f:
            config = yaml.safe_load(f)

        assert isinstance(config, dict)
        assert 'version' in config
        assert 'updates' in config

    def test_dependabot_includes_github_actions(
        self, cookies: Cookies, context_simple: dict[str, Any]
    ) -> None:
        """The dependabot config includes GitHub Actions updates."""
        result = cookies.bake(extra_context=context_simple)
        assert result.exit_code == 0

        dependabot_path = result.project_path / '.github' / 'dependabot.yml'
        with dependabot_path.open() as f:
            config = yaml.safe_load(f)

        # Should have GitHub Actions ecosystem
        ecosystems = [update['package-ecosystem'] for update in config['updates']]
        assert 'github-actions' in ecosystems
