"""Post generation hook for cookiecutter-pypackage-minimal."""
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


# TODO: If cookiecutter allows you to import from the local hooks directory,
#  then move this function to a shared module.
# Related: https://github.com/cookiecutter/cookiecutter/issues/824
def stream_shell_output(command: str) -> None:
    """Stream the output of a shell command to stdout."""
    with subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        for line in iter(proc.stdout.readline, b''):
            logger.debug(line.decode('utf-8').rstrip())


logger.debug('Initializing git repo')
stream_shell_output('git init')

logger.debug(' Installing dependencies')
stream_shell_output('poetry install')

logger.debug('Installing pre-commit hooks')
stream_shell_output('poetry run pre-commit install')
