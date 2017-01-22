#!/usr/bin/python

# Export solar information as JSON

from datetime import date
from solartime import SolarTime
from location import longitude, latitude, localtz

import json

today = date.today()
solar_utc = SolarTime().sun_utc(date.today(), latitude, longitude)
daylight = solar_utc['sunset'] - solar_utc['sunrise']

solar_local = {
  'sunrise':  int(solar_utc['sunrise'].astimezone(localtz).strftime('%s')),
  'sunset':   int(solar_utc['sunset'].astimezone(localtz).strftime('%s')),
  'peak':     int(solar_utc['noon'].astimezone(localtz).strftime('%s')),
  'daylight': daylight.seconds,
}

print json.dumps(solar_local)
