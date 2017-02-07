# -*- coding: UTF-8 -*-

from ask import alexa
import requests
import pytz
from datetime import datetime
from location import localtz, webpath

def lambda_handler(request_obj, context=None):
    metadata = {}
    return alexa.route_request(request_obj, metadata)

@alexa.default_handler()
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request type """
    return alexa.respond(get_pool_weather_handler(request))

@alexa.intent_handler(intent='GetPoolWeather')
def get_pool_weather_handler(request):
    pool_data = requests.get('{}/json.php'.format(webpath)).json()
    card = alexa.create_card(
        title="The pool is {}".format(adjective_for_temp(pool_data['probe_temp_f'])[1]),
        subtitle=None,
        content="Pool water temperature is {}°F at {}.\n\nYesterday's peak water temperature was {}°F at {}.".format(
            pool_data['probe_temp_f'],
            datetime.strftime(datetime.now(pytz.UTC).astimezone(localtz), "%I:%M %p"),
            pool_data['peak_temp_f'],
            timestamp_to_local(pool_data['peak_temp_time'])),
        large_image='{}/temperature.php?start={}&lookback={}'.format(
            webpath,
            int(datetime.strftime(datetime.now(), "%s")),
            60 * 60 * 12))
    return alexa.create_response(
        message=get_pool_weather(pool_data),
        end_session=True,
        card_obj=card)

def timestamp_to_local(ts):
    return datetime.strftime(datetime.fromtimestamp(ts, pytz.UTC).astimezone(localtz), "%I:%M %p")

def get_pool_weather(pool_data):
    return ' '.join([
        message_for_temp(pool_data['probe_temp_f']),
        message_for_peak(pool_data['peak_temp_f'], pool_data['peak_temp_time']),
    ])

def message_for_temp(temp_f):
    return 'The pool is presently {} {} degrees.'.format(' '.join(adjective_for_temp(temp_f)), round(temp_f, 1))

def message_for_peak(peak_temp_f, peak_ts):
    peak_time = timestamp_to_local(peak_ts)
    return 'Yesterday the pool made it up to {} degrees at {}.'.format(round(peak_temp_f, 1), peak_time)

def adjective_for_temp(temp_f):
    temp_f = round(temp_f, 1)
    if temp_f <= 60:
        adj = 'icy'
    elif temp_f <= 65:
        adj = 'frigid'
    elif temp_f <= 68:
        adj = 'chilly'
    elif temp_f <= 71:
        adj = 'cool'
    elif temp_f <= 75:
        adj = 'pleasant'
    elif temp_f <= 80:
        adj = 'perfect'
    elif temp_f <= 82:
        adj = 'warm'
    elif temp_f <= 85:
        adj = 'hot'
    else:
        adj = 'swampy'

    indef_art = 'an' if adj == 'icy' else 'a'
    return (indef_art, adj)
