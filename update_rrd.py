#!/usr/bin/python

# Nearest weather station for ambient temps
from location import weather_station
from temperature import TemperatureProbe

from stat import ST_MTIME
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import os
import urllib2
import rrdtool

# Pull weather station data every 5 minutes and get cached value
use_cache = False
now = datetime.now()
try:
    weather_mod = os.stat('weather.xml')[ST_MTIME]
    if datetime.fromtimestamp(weather_mod) > (now - timedelta(minutes=5)):
        use_cache = True
except OSError as e:
    pass

# Load from file or URL
if use_cache:
    with open('weather.xml') as f:
        weather_data = f.read()
else:
    weather_data = urllib2.urlopen("http://api.wunderground.com/weatherstation/WXCurrentObXML.asp?ID={wx}".format(wx=weather_station)).read()

# Read data and verify correctness
root = ET.fromstring(weather_data)
temp_f = root.find('./temp_f').text
# Write to cache file if seems valid
if temp_f != 0 and not use_cache:
    with open('weather.xml', 'w') as f:
        f.write(weather_data)

# Update rrd with weather station and temperature probe data
args = [
    '{rrd_dir}/temperature.rrd'.format(rrd_dir=os.path.dirname(__file__)),
    '-t', 'probe:outdoor',
    'N:{probe_temp}:{outside_temp}'.format(
        probe_temp=TemperatureProbe().fahrenheit(),
        outside_temp=temp_f)
]
print 'rrdtool update {args}'.format(args=' '.join(args))
rrdtool.update(*args)
