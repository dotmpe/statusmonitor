#!/bin/sh
set -e


# Jolt JSON transform: Example getting table from Elastic Search results
# Src: http://stackoverflow.com/questions/34139209/jolt-recursive-transformation-how-to-flatten

jolt transform var/es-jolt-example.json var/es-data-example.json \
  | jsotk json2yaml --pretty - var/es-data-table.json
jsotk -I json -O table var/es-data-table.json > var/es-data-table.txt
test "$(md5sum var/es-data-table.txt | cut -f 1 -d ' ')" = "a047cd24916b163777cbb3916338ad6a" \
  && echo "OK - Jolt JSON-to-table example" \
  || exit $?


# Work in progress

python test/py/pd_to_states.py \
  && echo "OK - Python pd-to-states unit tests" \
 || exit $?


jsotk yaml2json ~/.projects.yaml home.json
./bin/pd-to-states.py home.json statusmonitor.yaml
jsotk --pretty yaml2json statusmonitor.yaml statusmonitor.json

jsotk yaml2json ~/project/.projects.yaml projects.json
./bin/pd-to-states.py projects.json statusmonitor-2.yaml
jsotk --pretty yaml2json statusmonitor-2.yaml statusmonitor-2.json

#jsotk --pretty update statusmonitor.json statusmonitor-2.yaml

