# esphome-projects

This repository is used to manage configuration verification and testing for
all of my ESPHome devices. Each project has a config file which is verified
through continuous integration scripts. Renovate is used to automatically test
against new versions of ESPHome so I can find regressions early, well before
attempting to update.

The `scripts/` directory contains scripts for helping with pushing
configurations to devies, which is not currently automated.

## Python Virtual Environment

```shell
$ uv venv --python=3.13
$ source .venv/bin/activate
$ uv pip install -r requirements.txt
```

## ESPHome Projects

See [ESPHome: Getting Started](https://esphome.io/guides/getting_started_command_line.html) for details on how to create a new node.

Create a `config/secrets.yaml` file, copying from the example then edit:

```shell
$ cp config/secrets-example.yaml playground/secrets.yaml
```

To verify config:

```shell
$ esphome config playground/nook.yaml
```

To run interactive:

```shell
$ esphome run playground/nook.yaml
```

To complie and upload only:

```shell
$ esphome compile playground/nook.yaml
$ esphome upload playground/nook.yaml
```

## Update all Devices

This will run the check and update command for a set of known devices:

```shell
$ scripts/update.sh
```
