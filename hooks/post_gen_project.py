"""Post generation hook for cookiecutter-python-library."""
from __future__ import annotations

import logging
import os
import shlex
import subprocess

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
