
# poolpi
A collection of scripts that I'm using to monitor my pool's temperature.

## Config
### `location.py`

A simple config so I don't have to put my home location into the public repo. It should look something like this:

```
from pytz import timezone

# Location information
longitude = -5;
latitude = 22;
localtz = timezone('UTC')
weather_station = 'KNYNEWYO256'
```

Weather station is an identifier from wunderground.com.
