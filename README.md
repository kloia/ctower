# ctower

Control Tower CLI application.


## Installation
```bash
# Make sure you have python:^3.7
python3 --version

# Install the PyPI package w/
pip3 install ctower

# or

python3 -m pip install ctower
```
## Poetry

```bash

poetry init
poetry install
poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD

# generate CLI application documentation
poetry shell
typer ctower.main utils docs --name ctower --output CLI-README.md
```

```bash
pip install ctower
ctower apply strongly-recommended
```

## Tasks

- logic for enabling controls
  - enable singular control to ou
  - sync one account to other
    - --strict to mirror the controls
    - nothing to just merge apply
- ? maybe prompting
- show accounts under ous
-
