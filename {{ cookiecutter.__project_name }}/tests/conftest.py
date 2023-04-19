from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _pytest.config import Config
    from _pytest.config.argparsing import Parser


def pytest_addoption(parser: Parser) -> None:
    """Add a command line option to disable logger."""
    parser.addoption(
        '--log-disable',
        action='append',
        default=[],
        help='disable specific loggers',
    )


def pytest_configure(config: Config) -> None:
    """Disable the loggers."""
    for name in config.getoption('--log-disable', default=[]):
        logger = logging.getLogger(name)
        logger.propagate = False
