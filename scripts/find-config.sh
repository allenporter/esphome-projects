#!/bin/bash
#
# Find ESPHome configuration files and output JSON for use in the CI matrix.

set -e

find . -maxdepth 2 -type f \( -name "*.yaml" ! -name "secrets*.yaml" \) \
    | jq -Rs -c 'rtrimstr("\n") | split("\n")' 
