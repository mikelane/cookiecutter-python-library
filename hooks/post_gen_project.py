"""Post generation hook for cookiecutter-python-library."""
from __future__ import annotations

import logging
import os
import shlex
import shutil
import subprocess
from pathlib import Path

is_debug = os.getenv('DEBUG', '0') == '1'

logging.basicConfig(
    level=logging.DEBUG if is_debug else logging.INFO,
    format='%(asctime)s %(name)-12s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S',
)

logger = logging.getLogger('Post Gen Project Hook')


def stream_shell_output(command: str) -> None:
    """Stream the output of a shell command to stdout."""
    with subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        for line in iter(proc.stdout.readline, b''):
            logger.debug(line.decode('utf-8').rstrip())


def remove_conditional_files() -> None:
    """Remove files and directories based on cookiecutter options."""
    project_root = Path.cwd()

    # Remove docs directory if documentation is not included
    if '{{cookiecutter.include_documentation}}' != 'y':
        docs_dir = project_root / 'docs'
        if docs_dir.exists():
            logger.debug(f'Removing {docs_dir}')
            shutil.rmtree(docs_dir)

    # Remove BDD test directory if BDD testing is not included
    if '{{cookiecutter.include_bdd_testing}}' != 'y':
        bdd_dir = project_root / 'tests' / 'bdd'
        if bdd_dir.exists():
            logger.debug(f'Removing {bdd_dir}')
            shutil.rmtree(bdd_dir)

    # Remove benchmarks directory if benchmarks are not included
    if '{{cookiecutter.include_benchmarks}}' != 'y':
        benchmarks_dir = project_root / 'benchmarks'
        if benchmarks_dir.exists():
            logger.debug(f'Removing {benchmarks_dir}')
            shutil.rmtree(benchmarks_dir)

    # Remove _version.py if semantic release is not enabled
    if '{{cookiecutter.use_semantic_release}}' != 'y':
        version_file = project_root / 'src' / '{{cookiecutter.__package_name}}' / '_version.py'
        if version_file.exists():
            logger.debug(f'Removing {version_file}')
            version_file.unlink()

    # Remove Rust directory and Cargo.toml if not rust-backed
    if '{{cookiecutter.project_type}}' != 'rust-backed':
        rust_dir = project_root / 'rust'
        if rust_dir.exists():
            logger.debug(f'Removing {rust_dir}')
            shutil.rmtree(rust_dir)
        cargo_toml = project_root / 'Cargo.toml'
        if cargo_toml.exists():
            logger.debug(f'Removing {cargo_toml}')
            cargo_toml.unlink()

    # Remove infrastructure directory if not aws-cdk
    if '{{cookiecutter.project_type}}' != 'aws-cdk':
        infra_dir = project_root / 'infrastructure'
        if infra_dir.exists():
            logger.debug(f'Removing {infra_dir}')
            shutil.rmtree(infra_dir)


logger.debug('Removing conditional files and directories')
remove_conditional_files()

logger.debug('Initializing git repo')
stream_shell_output('git init')

logger.debug('Syncing dependencies with uv')
stream_shell_output('uv sync --all-extras')

logger.debug('Installing pre-commit hooks')
stream_shell_output('uv run pre-commit install')

logger.info('Project initialized successfully!')
logger.info('Next steps:')
logger.info('  1. cd {{cookiecutter.__project_name}}')
logger.info('  2. uv sync  # Install dependencies')
logger.info('  3. uv run pytest  # Run tests')
logger.info('  4. uv run pre-commit run --all-files  # Run code quality checks')
