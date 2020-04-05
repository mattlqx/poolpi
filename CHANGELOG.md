## CHANGELOG

- 04/05/2020: Removed WeatherUnderground scraping. They've been shutdown for about 2 months now. The outdoor temperature can now be provided by a second temperature probe locally. The location.py config has changed to have a `temperature_probes` dictionary. See example in README. This dictionary is dynamic, you can have as many probes as you like now and they'll all be recorded and graphed (provided you create your RRD accordingly).

- 07/26/2019: Bump module versions in requirements.txt

- 2017: Initial Release
