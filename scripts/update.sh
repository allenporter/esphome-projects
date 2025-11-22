#!/bin/bash

set -e

esphome compile displays/eink-panel.yaml
esphome upload displays/eink-panel.yaml

esphome compile displays/eink-frame.yaml
esphome upload displays/eink-frame.yaml

esphome compile displays/frekvens.yaml
esphome upload displays/frekvens.yaml

esphome compile sensors/driveway-gate.yaml
esphome upload sensors/driveway-gate.yaml

esphome compile sensors/water-softener.yaml
esphome upload sensors/water-softener.yaml
