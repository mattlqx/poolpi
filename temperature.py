#!/usr/bin/python

# Adapted from http://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/

temperature_probe_serial = '28-011620f667ee'

# Open temperature probe device
with open("/sys/bus/w1/devices/{serial}/w1_slave".format(serial=temperature_probe_serial)) as tfile:
    text = tfile.read()

# Parse the data
secondline = text.split("\n")[1]
temperaturedata = secondline.split(" ")[9]
# The first two characters are "t=", so get rid of those and convert the temperature from a string to a number.
temperature = float(temperaturedata[2:]) / 1000

# celsius
#print temperature

# fahrenheit
print temperature * 9 / 5 + 32
