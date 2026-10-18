#!/bin/bash
#
# Find ESPHome configuration files and output JSON for use in the CI matrix.

set -e

find camera displays sensors -maxdepth 1 -type f \( -name "*.yaml" ! -name "secrets*.yaml" \) \
    | sort \
    | jq -Rs -c 'rtrimstr("\n") | split("\n")'
