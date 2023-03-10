"""Pre-Generate Project Hook."""
from __future__ import annotations

import logging
import os
import re
import sys

is_debug = os.getenv('DEBUG', '0') == '1'

logging.basicConfig(
    level=logging.DEBUG if is_debug else logging.INFO,
    format='%(asctime)s %(name)-12s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S',
)

logger = logging.getLogger('Pre Gen Project Hook')


def _has_valid_project_name(project_name: str) -> bool:
    regex = re.compile(r'^[a-zA-Z][-\w\s]*$')
    return bool(regex.match(project_name))


if not _has_valid_project_name('{{ cookiecutter.project_name }}'):
    logger.error('Invalid project name')
    sys.exit(1)
else:
    logger.debug('Project name is valid')
