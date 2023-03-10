# Cookiecutter Modern Python Library Template

## Overview
This is a cookiecutter template for a modern Python library. It is intended to 
be used as a starting point for new Python libraries rather than for back end 
services (though, you can certainly use this template as a base for a backend
service). It comes with dependencies for testing, linting, and packaging.

## Usage
### Pre-Requisites
- Install [git](https://git-scm.com/)
- Install [poetry](https://python-poetry.org/)
- Install [cookiecutter](https://cookiecutter.readthedocs.io/)

### Setup a new project
```shell
cookiecutter gh:mikelane/cookiecutter-python-library
```

Answer the questions that cookiecutter asks you. You can accept the defaults by
pressing enter.

Cookiecutter will create a new project as a subdirectory of the current working
directory with the name you specified. It will also create a git repository and
it will install some basic dependencies. Additionally, it will set up pre-
commit hooks for linting and formatting.
