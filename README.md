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

To verify config:
```
$ esphome nook.yaml config
```

To upload config:
```
$ esphome nook.yaml run
```
