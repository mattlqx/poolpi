#!/usr/bin/python

# Adapted from http://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/
# Run with 'cpu' argument for cpu temp, otherwise read from probe

import sys

class TemperatureProbe:
    temp_probe_serial = '28-011620f667ee'
    cpu_device = '/sys/class/thermal/thermal_zone0/temp'
    probe_device = '/sys/bus/w1/devices/{serial}/w1_slave'.format(serial=temp_probe_serial)

    def __init__(self, device=probe_device):
        self.device = device

        # Open temperature probe device
        with open(self.device) as tfile:
            text = tfile.read()

        # Parse the data
        if self.device == self.cpu_device:
            temperature_data = text
        else:
            secondline = text.split('\n')[1]
            # The first two characters are "t="
            temperature_data = secondline.split(' ')[9][2:]
        self.temperature_data = temperature_data

    def fahrenheit(self):
        temperature = float(self.temperature_data) / 1000
        return temperature * 9 / 5 + 32

    def celsius(self):
        return float(self.temperature_data) / 1000

    def __str__(self):
        return '{0:.2f} degrees F'.format(self.fahrenheit())

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'cpu':
        probe = TemperatureProbe(device=TemperatureProbe.cpu_device)
    else:
        probe = TemperatureProbe()
    print probe
