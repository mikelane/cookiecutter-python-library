"""
Example Main File

This is an example main file for your library and there is a corresponding test
at `tests/test_main.py`. You should edit or remove both of these files as re-
quired for your project.
"""
from __future__ import annotations

from beartype import beartype
from loguru import logger

@beartype
def get_hello(name: str) -> str:
    """Get A Hello String.

    >>> get_hello('world')
    'Hello, world!'
    >>> get_hello('Mike')
    'Hello, Mike!'
    >>> get_hello(42)
    Traceback (most recent call last):
      ...
    beartype.roar.BeartypeCallHintParamViolation: ...

    >>> get_hello()
    Traceback (most recent call last):
      ...
    TypeError: get_hello() missing 1 required positional argument: 'name'
    """
    return f'Hello, {name}!'


if __name__ == '__main__':
    logger.info(get_hello('{{ cookiecutter.author_name }}'))

