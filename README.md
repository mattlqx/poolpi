
# poolpi
A collection of scripts that I'm using to monitor my pool's temperature via a Raspberry Pi and a 1-wire temperature probe. Specifically, a DS18B20 waterproof probe wired to a Pi-EzConnect GPIO hat.

## Prerequisites

* `rrdtool` - I'm just shelling out to rrdtool for now to do the actual data store work.
* python 2.7 - Most of the scripts are Python.
* OS packages for Raspian/Debian, in order to compile the pypi `python-rrdtool` module:
  * `libpango1.0-dev`
  * `libxml2-dev`
  * `libcairo2-dev`
  * `libglib2.0-dev`
  * `python-dev`
  * `librrd-dev`
* python modules - Run `pip install -r requirements.txt`
* php 5.x - The web frontend is hastily written in PHP. You'll need apache or another web server too.

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
webpath = 'https://mywebserver.com/poolpi'
```

Weather station is an identifier from wunderground.com.

### RRD

Create an rrd at `temperature.rrd` with the `tools/create_rrd.py` script.

### Cron

Just add a crontab to take the temperature every minute and store it in rrd:
```
* * * * *   poolpi/update_rrd.py
```

### Web

Symlink or document root the `web` directory. Then you can access `temps.php` for a rudimentary display of
hourly, daily, weekly and yearly graphs. One graph for each time period will have ambient and probe
temperature overlaid and another graph will have just the probe temperature so it's easier to see
its fluctuation without the scale of the ambient temperature zooming out the graph.

### Alexa

The Alexa Skill is in the `alexa` directory. Run the `build_lambda_zip.sh` script to install python
dependencies within the directory and zip it up. You can then place that zip in a Lambda function and
configure an Alexa Skill to use its ARN. The `location.py` config is copied into the zip for configuration
of the timezone and location of the web server that is hosting the `web` contents.
