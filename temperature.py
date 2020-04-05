#!/usr/bin/python

# Adapted from http://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/
# Run with 'cpu' argument for cpu temp, otherwise read from probe

import sys

class TemperatureProbe:
    cpu_device = '/sys/class/thermal/thermal_zone0/temp'

    @classmethod
    def device_for_serial(cls, serial):
        return '/sys/bus/w1/devices/{serial}/w1_slave'.format(serial=serial)

    @classmethod
    def from_serial(cls, serial):
        return TemperatureProbe(device=cls.device_for_serial(serial))

    def __init__(self, device=None):
	if device is None:
            device = TemperatureProbe.cpu_device

        # Open temperature probe device
        with open(device) as tfile:
            text = tfile.read()

        # Parse the data
        if device == self.cpu_device:
            temperature_data = text
        else:
            secondline = text.split('\n')[1]
            # The first two characters are "t="
            temperature_data = secondline.split(' ')[9][2:]
        self.temperature_data = temperature_data

    def fahrenheit(self):
        return self.celsius() * 9 / 5 + 32

    def celsius(self):
        return float(self.temperature_data) / 1000

    def __str__(self):
        return '{0:.2f} degrees F'.format(self.fahrenheit())

if __name__ == '__main__':
    if sys.argv[1] == 'cpu':
        device = TemperatureProbe.cpu_device
    else:
        device = TemperatureProbe.device_for_serial(sys.argv[1])
    print TemperatureProbe(device=device)
