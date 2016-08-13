#!/usr/bin/env python
"""
[2016-08-13] Started writing Py script, but abbandoned ifo JOLT transform spec
experiment first.

Source format::

    repositories:
      .conf:
        status:
          bats:
            result: 0
            specs: 0
          check: 0
          git:
            status:
              result: 0
          test: 0
      Applications:
        status: {}
      Desktop:
        enabled: true
        status:
          check: 0
          fs:
            clean:
              result: 0
      Documents:
        status: {}

Dest. format::

    label: .*
    status: [0-255]
    values:
    - label: .*
      value: abcd 123
    states:
    - label: .*
      status: [0-255]
      states:
      ...

Prefix path + state key are merged into one.
Then hierarchy for this label is created.

"""


import pprint

import yaml

def get_comp( data, label ):
    for state in data['states']:
        if state['label'] == label:
            return state

def new_state(label, states=[], status=None):
    return dict(states=states, label=label, status=status)

def init_state(data, key, status=None):
    sub = None
    if 'states' in data:
        sub = get_comp( data, key)
    if sub:
        sub['status'] = status
    else:
        sub = new_state(key, status=status)
        if data:
            data['states'].append(sub)
    return sub

def set_path( data, prefix, state, o ):

    assert data
    assert isinstance(data, dict) , ( data, prefix, state, o )

    c = data
    els = prefix.split('/')
    while els:
        el = els.pop(0)
        c = init_state( c, el )

    #init_state( c, state, o )

def set_states( tod, prefix, fromd ):
    for state, o in fromd.items():
        if isinstance( o, dict ):
            set_states( tod, prefix+'/'+state, o )
        else:
            set_path( tod, prefix, state, o )

def run(fromfp, tofp):

    out = new_state('~')
    home = init_state( out, '~' )
    assert out
    data = yaml.safe_load(fromfp)

    for prefix, record in data['repositories'].items():
        set_states(out, '~/'+prefix, record['status'])

    pprint.pprint(home)


if __name__ == '__main__':

    import sys
    assert len(sys.argv) == 3, "Usage: pd-to-states SRC DEST"
    if sys.argv[1] == '-': inf = sys.stdin
    else: inf = open(sys.argv[1])
    if sys.argv[2] == '-': outf = sys.stdout
    else: outf = open(sys.argv[2])
    sys.exit(run(inf, outf))

