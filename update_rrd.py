#!/usr/bin/python

from temperature import TemperatureProbe
from location import temperature_probes

import os
import rrdtool

# Update rrd with weather station and temperature probe data
args = [
    '{rrd_dir}/temperature.rrd'.format(rrd_dir=os.path.dirname(__file__)),
    '-t', ':'.join(temperature_probes.keys()),
    'N:{temps}'.format(
        temps=':'.join(map(
            lambda serial: str(TemperatureProbe.from_serial(serial).fahrenheit()),
            temperature_probes.values()
        ))
    )
]
print 'rrdtool update {args}'.format(args=' '.join(args))
rrdtool.update(*args)
