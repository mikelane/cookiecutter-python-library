"""Pre-Generate Project Hook."""
from __future__ import annotations

import shlex
import subprocess


# TODO: If cookiecutter allows you to import from the local hooks directory,
#  then move this function to a shared module.
# Related: https://github.com/cookiecutter/cookiecutter/issues/824
def stream_shell_output(command: str) -> None:
    """Stream the output of a shell command to stdout."""
    with subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        for line in iter(proc.stdout.readline, b''):
            print(line.decode('utf-8').rstrip())


print(f'{" Post Gen Project Hook ":=^80}')
print(f'{" Initializing git repo ":-^50}')
stream_shell_output('git init')
