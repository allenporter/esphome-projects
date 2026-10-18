# esphome-projects

This repository is used to manage configuration verification and testing for
all of my ESPHome devices. Each project has a config file which is verified
through continuous integration scripts. Renovate is used to automatically test
against new versions of ESPHome so I can find regressions early, well before
attempting to update.

The `scripts/` directory contains scripts for helping with pushing
configurations to devices, which is not currently automated.

## Python Virtual Environment

```shell
$ uv venv
$ source .venv/bin/activate
$ uv pip install -r requirements.txt
```

## Secrets Setup

Create a `secrets.yaml` file from the example and symlink it into each device directory (`camera/`, `displays/`, `sensors/`):

```shell
$ cp config/secrets-example.yaml secrets.yaml
$ ln -s ../secrets.yaml camera/secrets.yaml
$ ln -s ../secrets.yaml displays/secrets.yaml
$ ln -s ../secrets.yaml sensors/secrets.yaml
```

## ESPHome Projects

See [ESPHome: Getting Started](https://esphome.io/guides/getting_started_command_line.html) for details on how to create a new node.

Device configurations are organized by type:
- `displays/`: `eink-panel.yaml`, `eink-frame.yaml`, `frekvens.yaml` (with shared UI definitions in `displays/packages/`)
- `sensors/`: `driveway-gate.yaml`, `water-softener.yaml`
- `camera/`: `smart-glasses.yaml`

To verify a config:

```shell
$ esphome config displays/eink-frame.yaml
```

To run interactive (compile, upload, and stream logs):

```shell
$ esphome run displays/eink-frame.yaml
```

To compile and upload only:

```shell
$ esphome compile displays/eink-frame.yaml
$ esphome upload displays/eink-frame.yaml
```

## Display Snapshot Tests

Display layouts in `displays/packages/` are tested offline using ESPHome's `host` platform and `syrupy` golden PNG snapshots in `tests/`:

```shell
$ pytest
```

To update the golden PNG snapshots after intentionally changing a display layout:

```shell
$ pytest --snapshot-update
```

## Update all Devices

This will run the check and update command for a set of known devices:

```shell
$ scripts/update.sh
```
