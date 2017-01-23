#!/usr/bin/python

# Adapted from http://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/
# Run with 'cpu' argument for cpu temp, otherwise read from probe

import sys

temperature_probe_serial = '28-011620f667ee'
device = "/sys/bus/w1/devices/{serial}/w1_slave".format(serial=temperature_probe_serial)
do_cpu = False

if len(sys.argv) > 1 and sys.argv[1] == 'cpu':
    do_cpu = True
    device = "/sys/class/thermal/thermal_zone0/temp"

# Open temperature probe device
with open(device) as tfile:
    text = tfile.read()

# Parse the data
if do_cpu:
    temperaturedata = text
else:
    secondline = text.split("\n")[1]
    # The first two characters are "t="
    temperaturedata = secondline.split(" ")[9][2:]

temperature = float(temperaturedata) / 1000

# celsius
#print temperature

# fahrenheit
print temperature * 9 / 5 + 32
