
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
import collections

# Location information
longitude = -5;
latitude = 22;
localtz = timezone('UTC')
webpath = 'https://mywebserver.com/poolpi'
color_start = 0xff0000
color_offset = 12
temperature_probes = collections.OrderedDict()
temperature_probes['outdoor'] = '28-011620f667ff'
temperature_probes['probe'] = '28-011620f667ee'
```

**NOTE**: Weather Underground has shutdown. As a result, I've removed outdoor temperature scraping. Instead of
having to deal with an external service, I've decided to just go with another temperature probe. So I've added
that to the config above. It's an ordered dictionary with the key being the name of the rrd gauge and value being
the serial number of the probe. The ordering is important for exporting the structure between Python and PHP.

`color_start` and `color_offset` are used to override the stock colors. The first gauge starts at red and then
each gauge after that shifts 12 bits.

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
