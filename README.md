# esphome-projects

Projects related to home automation with ESPHome.

# Python Virtual Environment

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

# ESPHome

See [ESPHome: Getting Started](https://esphome.io/guides/getting_started_command_line.html) for details on how to create a new node.

Create a `config/secrets.yaml` file, copying from the example then edit:
```
$ cp config/secrets-example.yaml playground/secrets.yaml
```

To verify config:
```
$ esphome playground/nook.yaml config
```

To upload config:
```
$ esphome playground/nook.yaml run
```
