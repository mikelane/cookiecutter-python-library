"""Tests for rust-backed project type generation."""
from __future__ import annotations

import json
from pathlib import Path

from cookiecutter.main import cookiecutter


def it_generates_cargo_toml_for_rust_backed_project(template_dir: Path, temp_project_dir: Path) -> None:
    """It generates a Cargo.toml with correct maturin configuration."""
    context = {
        'project_name': 'Rust Test Library',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'A rust-backed test library',
        'long_description': 'A longer description',
        'license': 'MIT',
        'project_type': 'rust-backed',
        'python_version_min': '3.11',
    }

    project_dir = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(temp_project_dir),
    )

    cargo_toml = Path(project_dir) / 'Cargo.toml'
    assert cargo_toml.exists(), 'Cargo.toml must exist for rust-backed projects'

    cargo_content = cargo_toml.read_text()
    assert '[package]' in cargo_content
    assert 'name = "rust-test-library"' in cargo_content
    assert '[lib]' in cargo_content
    assert 'crate-type = ["cdylib"]' in cargo_content
    assert 'path = "rust/src/lib.rs"' in cargo_content


def it_generates_rust_source_directory_structure(template_dir: Path, temp_project_dir: Path) -> None:
    """It generates rust/src/lib.rs with PyO3 bindings."""
    context = {
        'project_name': 'Rust Test Library',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'A rust-backed test library',
        'license': 'MIT',
        'project_type': 'rust-backed',
        'python_version_min': '3.11',
    }

    project_dir = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(temp_project_dir),
    )

    rust_lib = Path(project_dir) / 'rust' / 'src' / 'lib.rs'
    assert rust_lib.exists(), 'rust/src/lib.rs must exist'

    rust_content = rust_lib.read_text()
    assert 'use pyo3::prelude::*;' in rust_content
    assert '#[pymodule]' in rust_content
    assert 'PyResult' in rust_content


def it_uses_maturin_build_backend_for_rust_backed_projects(template_dir: Path, temp_project_dir: Path) -> None:
    """It configures pyproject.toml to use maturin as build backend."""
    context = {
        'project_name': 'Rust Test Library',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'A rust-backed test library',
        'license': 'MIT',
        'project_type': 'rust-backed',
        'python_version_min': '3.11',
    }

    project_dir = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(temp_project_dir),
    )

    pyproject_toml = Path(project_dir) / 'pyproject.toml'
    content = pyproject_toml.read_text()

    assert 'build-backend = "maturin"' in content
    assert 'requires = ["maturin>=1.0,<2.0"]' in content
    assert '[tool.maturin]' in content
    assert 'python-source = "src"' in content


def it_excludes_rust_directory_for_non_rust_backed_projects(template_dir: Path, temp_project_dir: Path) -> None:
    """It does not create rust directory for simple projects."""
    context = {
        'project_name': 'Simple Test Library',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'A simple test library',
        'license': 'MIT',
        'project_type': 'simple',
        'python_version_min': '3.11',
    }

    project_dir = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(temp_project_dir),
    )

    rust_dir = Path(project_dir) / 'rust'
    assert not rust_dir.exists(), 'rust directory should not exist for non-rust-backed projects'

    cargo_toml = Path(project_dir) / 'Cargo.toml'
    assert not cargo_toml.exists(), 'Cargo.toml should not exist for non-rust-backed projects'


def it_includes_pyo3_dependency_in_cargo_toml(template_dir: Path, temp_project_dir: Path) -> None:
    """It includes PyO3 with appropriate features in Cargo.toml."""
    context = {
        'project_name': 'Rust Test Library',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'A rust-backed test library',
        'license': 'MIT',
        'project_type': 'rust-backed',
        'python_version_min': '3.11',
    }

    project_dir = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(temp_project_dir),
    )

    cargo_toml = Path(project_dir) / 'Cargo.toml'
    cargo_content = cargo_toml.read_text()

    assert '[dependencies]' in cargo_content
    assert 'pyo3' in cargo_content
    assert 'extension-module' in cargo_content
    assert 'abi3-py311' in cargo_content or 'abi3-py312' in cargo_content or 'abi3-py313' in cargo_content


def it_configures_release_profile_for_optimal_performance(template_dir: Path, temp_project_dir: Path) -> None:
    """It includes optimized release profile in Cargo.toml."""
    context = {
        'project_name': 'Rust Test Library',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'A rust-backed test library',
        'license': 'MIT',
        'project_type': 'rust-backed',
        'python_version_min': '3.11',
    }

    project_dir = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(temp_project_dir),
    )

    cargo_toml = Path(project_dir) / 'Cargo.toml'
    cargo_content = cargo_toml.read_text()

    assert '[profile.release]' in cargo_content
    assert 'opt-level = 3' in cargo_content
    assert 'lto' in cargo_content


def it_includes_maturin_in_dev_dependencies_for_rust_backed_projects(template_dir: Path, temp_project_dir: Path) -> None:
    """It includes maturin in dev dependencies for local development."""
    context = {
        'project_name': 'Rust Test Library',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'A rust-backed test library',
        'license': 'MIT',
        'project_type': 'rust-backed',
        'python_version_min': '3.11',
    }

    project_dir = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(temp_project_dir),
    )

    pyproject_toml = Path(project_dir) / 'pyproject.toml'
    content = pyproject_toml.read_text()

    # Maturin should be in dev dependencies
    assert 'maturin' in content
    # Should be in the dev optional dependencies section
    assert '[project.optional-dependencies]' in content


def it_adds_rust_target_to_gitignore_for_rust_backed_projects(template_dir: Path, temp_project_dir: Path) -> None:
    """It adds Rust build artifacts to .gitignore."""
    context = {
        'project_name': 'Rust Test Library',
        'author_name': 'Test Author',
        'author_email': 'test@example.com',
        'short_description': 'A rust-backed test library',
        'license': 'MIT',
        'project_type': 'rust-backed',
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
    assert 'target/' in gitignore_content or '/target/' in gitignore_content
    assert 'Cargo.lock' in gitignore_content
