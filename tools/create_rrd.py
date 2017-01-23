#!/usr/bin/python

import rrdtool

rrdtool.create('temperature.rrd',
    '--step=60',
    'DS:probe:GAUGE:180:-32:150',
    'DS:outdoor:GAUGE:600:-32:150',
    'RRA:AVERAGE:0.5:1:4320',
    'RRA:MIN:0.5:60:525600',
    'RRA:MAX:0.5:60:525600',
    'RRA:AVERAGE:0.5:60:525600',
)
