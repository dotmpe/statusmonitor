#!/bin/sh
set -e

# Jolt JSON transform: Example getting table from Elastic Search results
# Src: http://stackoverflow.com/questions/34139209/jolt-recursive-transformation-how-to-flatten

jolt transform var/es-jolt-example.json var/es-data-example.json \
  | jsotk json2yaml --pretty - var/es-data-table.json
jsotk -I json -O table var/es-data-table.json > var/es-data-table.txt
test "$(md5sum var/es-data-table.txt | cut -f 1 -d ' ')" = "a047cd24916b163777cbb3916338ad6a"

