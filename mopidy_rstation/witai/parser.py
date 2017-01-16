# encoding=utf8
from mopidy_rstation.utils import Utils
from mopidy_rstation.player import control
from mopidy_rstation.audio import voices
import traceback


def parse_wit(result):
    intent = u' '

    if result is not None:
        try:
            intent = result['entities']['intent'][0]['value']
        except Exception:
            traceback.print_exc()
            intent = None
        if result['_text'] is not None:
            if intent is not None:
                if intent == 'play_item':
                    play_item(result)
                elif intent == 'set_volume':
                    set_volume(result)
                elif intent == 'get_weather':
                    get_weather(result)
                elif intent == 'search_wikipedia':
                    search_wikipedia(result)
                elif intent == 'get_time':
                    Utils.get_time()
            else:
                voices.speak(
                    'WIT_HEAR_BUT_NOT_UNDERSTAND', val=result['_text'])
        else:
            voices.speak('WIT_HEAR_NOTHING')


def play_item(result):
    item_type = u' '
    item = None
    try:
        item_type = result['entities']['type'][0]['value']
    except Exception:
        print('we do not have item type')
        item_type = ''
    try:
        item = result['entities']['item'][0]['value']
    except Exception:
        print('we do not have item!')
    control.play_item(item, item_type)


def set_volume(result):
    try:
        vol = int(result['entities']['value'][0]['value'])
    except Exception:
        traceback.print_exc()
        vol = 50
    try:
        Utils.set_volume(vol)
    except Exception:
        traceback.print_exc()


def get_weather(result):
    location = None
    try:
        location = result['entities']['location'][0]['value']
    except Exception:
        traceback.print_exc()
    Utils.forecast_weather(location)


def search_wikipedia(result):
    query = None
    try:
        query = result['entities'][
            'wikipedia_search_query'][0]['value']
    except Exception:
        traceback.print_exc()
    Utils.search_wikipedia(query)
