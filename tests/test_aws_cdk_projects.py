"""Tests for aws-cdk project type generation."""

from __future__ import annotations

import json
from pathlib import Path

from cookiecutter.main import cookiecutter


def it_generates_infrastructure_directory_for_aws_cdk_project(template_dir: Path, temp_project_dir: Path) -> None:
    """It generates infrastructure/ directory with CDK structure."""
    context = {
        'project_name': 'CDK Test Project',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'An AWS CDK test project',
        'long_description': 'A longer description',
        'license': 'MIT',
        'project_type': 'aws-cdk',
        'python_version_min': '3.11',
    }

    project_dir = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(temp_project_dir),
    )

    infra_dir = Path(project_dir) / 'infrastructure'
    assert infra_dir.exists(), 'infrastructure/ directory must exist for aws-cdk projects'

    # Check subdirectories
    assert (infra_dir / 'bin').exists()
    assert (infra_dir / 'lib').exists()
    assert (infra_dir / 'lambda').exists()


def it_generates_cdk_json_configuration(template_dir: Path, temp_project_dir: Path) -> None:
    """It generates cdk.json with correct configuration."""
    context = {
        'project_name': 'CDK Test Project',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'An AWS CDK test project',
        'license': 'MIT',
        'project_type': 'aws-cdk',
        'python_version_min': '3.11',
    }

    project_dir = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(temp_project_dir),
    )

    cdk_json = Path(project_dir) / 'infrastructure' / 'cdk.json'
    assert cdk_json.exists(), 'cdk.json must exist'

    cdk_config = json.loads(cdk_json.read_text())
    assert 'app' in cdk_config
    assert 'npx ts-node' in cdk_config['app'] or 'ts-node' in cdk_config['app']


def it_generates_package_json_with_cdk_dependencies(template_dir: Path, temp_project_dir: Path) -> None:
    """It generates package.json with CDK dependencies."""
    context = {
        'project_name': 'CDK Test Project',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'An AWS CDK test project',
        'license': 'MIT',
        'project_type': 'aws-cdk',
        'python_version_min': '3.11',
    }

    project_dir = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(temp_project_dir),
    )

    package_json = Path(project_dir) / 'infrastructure' / 'package.json'
    assert package_json.exists(), 'package.json must exist'

    package_data = json.loads(package_json.read_text())
    assert 'dependencies' in package_data or 'devDependencies' in package_data

    # Check for CDK dependencies
    all_deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
    assert 'aws-cdk' in all_deps or 'aws-cdk-lib' in all_deps


def it_generates_typescript_configuration(template_dir: Path, temp_project_dir: Path) -> None:
    """It generates tsconfig.json for TypeScript."""
    context = {
        'project_name': 'CDK Test Project',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'An AWS CDK test project',
        'license': 'MIT',
        'project_type': 'aws-cdk',
        'python_version_min': '3.11',
    }

    project_dir = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(temp_project_dir),
    )

    tsconfig = Path(project_dir) / 'infrastructure' / 'tsconfig.json'
    assert tsconfig.exists(), 'tsconfig.json must exist'

    tsconfig_data = json.loads(tsconfig.read_text())
    assert 'compilerOptions' in tsconfig_data


def it_generates_cdk_app_entry_point(template_dir: Path, temp_project_dir: Path) -> None:
    """It generates bin/app.ts as CDK app entry point."""
    context = {
        'project_name': 'CDK Test Project',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'An AWS CDK test project',
        'license': 'MIT',
        'project_type': 'aws-cdk',
        'python_version_min': '3.11',
    }

    project_dir = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(temp_project_dir),
    )

    app_ts = Path(project_dir) / 'infrastructure' / 'bin' / 'app.ts'
    assert app_ts.exists(), 'bin/app.ts must exist'

    app_content = app_ts.read_text()
    assert 'import' in app_content
    assert 'App' in app_content
    assert 'new App()' in app_content or 'new cdk.App()' in app_content


def it_generates_cdk_stack_definition(template_dir: Path, temp_project_dir: Path) -> None:
    """It generates lib/stack.ts with CDK stack definition."""
    context = {
        'project_name': 'CDK Test Project',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'An AWS CDK test project',
        'license': 'MIT',
        'project_type': 'aws-cdk',
        'python_version_min': '3.11',
    }

    project_dir = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(temp_project_dir),
    )

    stack_ts = Path(project_dir) / 'infrastructure' / 'lib' / 'stack.ts'
    assert stack_ts.exists(), 'lib/stack.ts must exist'

    stack_content = stack_ts.read_text()
    assert 'Stack' in stack_content
    assert 'export class' in stack_content


def it_generates_lambda_handler_template(template_dir: Path, temp_project_dir: Path) -> None:
    """It generates lambda/handler.py template."""
    context = {
        'project_name': 'CDK Test Project',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'An AWS CDK test project',
        'license': 'MIT',
        'project_type': 'aws-cdk',
        'python_version_min': '3.11',
    }

    project_dir = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(temp_project_dir),
    )

    handler_py = Path(project_dir) / 'infrastructure' / 'lambda' / 'handler.py'
    assert handler_py.exists(), 'lambda/handler.py must exist'

    handler_content = handler_py.read_text()
    assert 'def handler' in handler_content or 'def lambda_handler' in handler_content
    assert 'event' in handler_content
    assert 'context' in handler_content


def it_excludes_infrastructure_directory_for_non_cdk_projects(template_dir: Path, temp_project_dir: Path) -> None:
    """It does not create infrastructure directory for simple projects."""
    context = {
        'project_name': 'Simple Test Library',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'A simple test library',
        'license': 'MIT',
        'project_type': 'library',
        'python_version_min': '3.11',
    }

    project_dir = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(temp_project_dir),
    )

    infra_dir = Path(project_dir) / 'infrastructure'
    assert not infra_dir.exists(), 'infrastructure directory should not exist for non-aws-cdk projects'


def it_adds_node_modules_to_gitignore_for_cdk_projects(template_dir: Path, temp_project_dir: Path) -> None:
    """It adds Node.js artifacts to .gitignore for CDK projects."""
    context = {
        'project_name': 'CDK Test Project',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'An AWS CDK test project',
        'license': 'MIT',
        'project_type': 'aws-cdk',
        'python_version_min': '3.11',
    }

    project_dir = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(temp_project_dir),
    )

    gitignore = Path(project_dir) / '.gitignore'
    assert gitignore.exists()

    gitignore_content = gitignore.read_text()
    assert 'node_modules' in gitignore_content or 'node_modules/' in gitignore_content
    assert 'cdk.out' in gitignore_content or 'cdk.out/' in gitignore_content
