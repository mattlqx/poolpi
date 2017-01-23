#!/usr/bin/python

# Export solar information as JSON

from datetime import date
from solartime import SolarTime
from location import longitude, latitude, localtz

import json
import sys

class SolarDetails:

    def __init__(self, day_timestamp=None):
        if day_timestamp is None:
            self.target_day = date.today()
        else:
            self.target_day = date.fromtimestamp(day_timestamp)

        self.solar_utc = SolarTime().sun_utc(self.target_day, latitude, longitude)

    def dict(self):
        solar_utc = self.solar_utc
        daylight = solar_utc['sunset'] - solar_utc['sunrise']
        return {
          'sunrise':  int(solar_utc['sunrise'].astimezone(localtz).strftime('%s')),
          'sunset':   int(solar_utc['sunset'].astimezone(localtz).strftime('%s')),
          'peak':     int(solar_utc['noon'].astimezone(localtz).strftime('%s')),
          'daylight': daylight.seconds,
        }

    def __unicode__(self):
        return self.target_day

if __name__ == '__main__':
    target_timestamp = float(sys.argv[1]) if len(sys.argv) > 1 else None
    print json.dumps(SolarDetails(target_timestamp).dict())
