#!/bin/sh
set -e
test -n "$1" || set -- ~/.projects.yaml
test -n "$2" || set -- "$1" "states.yml"

pd_json="$(dirname $1)/$(basename $1).json"
states_json="$(dirname $2)/$(basename $2).json"
jsotk.py yaml2json $1 $pd_json
jolt transform var/pd-states.jolt.json $pd_json > $states_json
jsotk.py json2yaml --pretty $states_json $2
#./bin/pd-to-states.py $1 $2

wc -l "$@"
echo ./bin/bstat $2
