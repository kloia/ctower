# ctower

ctower is a CLI application for managing GuardRail Controls across Organizational Units on AWS Control Tower. 


## Installation
```bash
pip3 install ctower
```

## Basic Usage
```bash

# export your aws cli profile and region
export AWS_REGION=eu-west-1
export AWS_PROFILE=default

# list organizational units in your AWS Organization
ctower ls organizational-units

# List all available GuardRail Controls
ctower ls controls all

# List enabled controls for an organizational unit
ctower ls enabled-controls -ou <organizational-unit-name>

# Apply a singular GuardRail Control to an organizational unit
ctower apply control --to-organizational-unit <ou-name> --control-id <control-id>

# Apply `Strongly Recommended` GuardRail Controls to specified Organizational Unit  
ctower apply strongly-recommended -ou <organizational-unit-name>


# Remove a GuardRail Control from an organizational unit
ctower remove control --to-organizational-unit <ou-name> --control-id <control-id>

# Sync(mirror) `--from-organizational-unit` controls to `--to-organizational-unit`
 ctower sync --from-organizational-unit <ou-from> --to-organizational-unit <ou-to>
```


###  Package Management with Poetry

#### Publishing to PyPI
```bash
# get and set the PYPI_USERNAME, PYPI_PASSWORD
poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD
```

#### Generating CLI Documentation
```bash
# generate CLI application documentation
poetry shell
typer ctower.main utils docs --name ctower --output CLI-README.md
```

## CLI Documentation

## `ctower`

**Usage**:

```console
$ ctower [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `apply`
* `ls`
* `remove`
* `sync`

### `ctower apply`

**Usage**:

```console
$ ctower apply [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `control`
* `strongly-recommended`

#### `ctower apply control`

**Usage**:

```console
$ ctower apply control [OPTIONS]
```

**Options**:

* `-ou, --organizational-unit TEXT`: ID or Name of Organizational Unit to get the controls from.  [required]
* `-cid, --control-id TEXT`: Control Identifier. Try: `ls controls all` command  [required]
* `--help`: Show this message and exit.

#### `ctower apply strongly-recommended`

**Usage**:

```console
$ ctower apply strongly-recommended [OPTIONS]
```

**Options**:

* `-ou, --organizational-unit TEXT`: ID or Name of Organizational Unit to apply GuardRail controls. Try: `ls organizational-units` command  [required]
* `--help`: Show this message and exit.

### `ctower ls`

**Usage**:

```console
$ ctower ls [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `controls`
* `enabled-controls`
* `organizational-units`

#### `ctower ls controls`

**Usage**:

```console
$ ctower ls controls [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `all`
* `data-residency`
* `elective`
* `strongly-recommended`

##### `ctower ls controls all`

**Usage**:

```console
$ ctower ls controls all [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

##### `ctower ls controls data-residency`

**Usage**:

```console
$ ctower ls controls data-residency [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

##### `ctower ls controls elective`

**Usage**:

```console
$ ctower ls controls elective [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

##### `ctower ls controls strongly-recommended`

**Usage**:

```console
$ ctower ls controls strongly-recommended [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

#### `ctower ls enabled-controls`

**Usage**:

```console
$ ctower ls enabled-controls [OPTIONS]
```

**Options**:

* `-ou, --organizational-unit TEXT`: ID or Name of Organizational Unit to list its enabled controls. Try: `ls organizational-units` command  [required]
* `--help`: Show this message and exit.

#### `ctower ls organizational-units`

**Usage**:

```console
$ ctower ls organizational-units [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `ctower remove`

**Usage**:

```console
$ ctower remove [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

### `ctower sync`

**Usage**:

```console
$ ctower sync [OPTIONS]
```

**Options**:

* `-fou, --from-organizational-unit TEXT`: ID or Name of Organizational Unit to get the controls from.  [required]
* `-tou, --to-organizational-unit TEXT`: ID or Name of Organizational Unit to apply GuardRail controls to.  [required]
* `--help`: Show this message and exit.

**Screenshots**:
* List Organizational Units for current Organization
<img width="711" alt="image" src="https://user-images.githubusercontent.com/8745804/198024275-d161267b-77e6-4423-9331-5c9623580006.png">
* List available GuardRails Controls
<img width="807" alt="image" src="https://user-images.githubusercontent.com/8745804/198024342-315494be-41b8-4554-bf29-067cbd0d9504.png">
* List enabled GuardRails for Organizational Unit
<img width="557" alt="image" src="https://user-images.githubusercontent.com/8745804/198024674-b5a684b3-a4b8-494c-8382-1f710b053083.png">
* Apply a GuardRail Control to Organizational Unit
<img width="780" alt="image" src="https://user-images.githubusercontent.com/8745804/198024762-5d515c3e-2530-4986-9170-66231793e597.png">
* Remove a GuardRail Control from Organizational Unit
<img width="808" alt="image" src="https://user-images.githubusercontent.com/8745804/198024853-03af540d-96a6-487f-8dbc-2982b99d06f2.png">
* Mirror Controls from OU to another OU
<img width="824" alt="image" src="https://user-images.githubusercontent.com/8745804/198024941-cd30fa95-d3b2-491e-9299-b9a930a4e597.png">



