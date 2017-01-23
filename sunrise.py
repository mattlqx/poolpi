#!/usr/bin/python

# Export solar information as JSON

from datetime import date
from solartime import SolarTime
from location import longitude, latitude, localtz

import json
import sys

target_day = date.fromtimestamp(float(sys.argv[1])) if len(sys.argv) > 1 else date.today()
solar_utc = SolarTime().sun_utc(target_day, latitude, longitude)
daylight = solar_utc['sunset'] - solar_utc['sunrise']

solar_local = {
  'sunrise':  int(solar_utc['sunrise'].astimezone(localtz).strftime('%s')),
  'sunset':   int(solar_utc['sunset'].astimezone(localtz).strftime('%s')),
  'peak':     int(solar_utc['noon'].astimezone(localtz).strftime('%s')),
  'daylight': daylight.seconds,
}

print json.dumps(solar_local)
