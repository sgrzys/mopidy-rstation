# encoding=utf8
from pprint import pprint
from mopidy_rstation.utils import Utils
from mopidy_rstation.player import control
from mopidy_rstation.config.settings import Config
from mopidy_rstation.audio import sounds
from mopidy_rstation.audio import voices
import requests
import json
import traceback
import alsaaudio

RECORDING = False
CHUNK = 512
RATE = 8000
RECORD_SECONDS = 5
INPUT_DEVICE_INDEX = None


def set_mic(audio_in_name):
    mic = 'plughw:CARD=' + audio_in_name + ',DEV=0'
    # plughw:CARD=audiocodec,DEV=0
    # plughw:CARD=Airmouse,DEV=0
    # plughw:CARD=CameraB409241,DEV=0
    #
    # TODO test is we have this hardware
    # for pd in alsaaudio.pcms(alsaaudio.PCM_CAPTURE):
    #         print(str(pd))
    # PCM_NONBLOCK
    inp = alsaaudio.PCM(
        type=alsaaudio.PCM_CAPTURE,
        mode=alsaaudio.PCM_NORMAL,
        device=mic)
    inp.setchannels(1)
    inp.setrate(RATE)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(CHUNK)
    return inp


def record_and_stream(inp):
    global RECORDING
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        print('i ' + str(i) + ' RECORDING is ' + str(RECORDING))
        if RECORDING is False:
            break
        _, data = inp.read()
        yield data
    print('record_and_stream done')


def ask_bot(mic=None):
    result = None
    global RECORDING
    try:
        config = Config.get_config()
        if mic is not None:
            audio_in_name = mic
        else:
            audio_in_name = config['audio_in_name']
        print('set_mic -> ' + audio_in_name)
        inp = set_mic(audio_in_name)

        headers = {'Authorization': 'Bearer ' + config['wit_token'],
                   'Content-Type': 'audio/raw; encoding=signed-integer; ' +
                   'bits=16; rate=8000; endian=little',
                   'Transfer-Encoding': 'chunked'}
        url = 'https://api.wit.ai/speech'

        print("\n[*]> Starting Recording\n")
        RECORDING = True
        sounds.play_file(sounds.C_SOUND_REC_START)
        result = requests.post(
            url, headers=headers, data=record_and_stream(inp))
        RECORDING = False
        print("[*]> Ready Recognize Voice\n")
        sounds.play_file(sounds.C_SOUND_REC_END)
    except Exception:
        traceback.print_exc()
        return
    pprint(result)
    result = json.loads(result.text)
    pprint(result)
    intent = u' '
    item_type = u' '
    item = None

    if result is not None:
        try:
            intent = result['entities']['intent'][0]['value']
        except Exception:
            traceback.print_exc()
            intent = None
        if result['_text'] is not None:
            if intent is not None:
                if intent == 'play_item':
                    try:
                        item_type = result['entities']['type'][0]['value']
                    except Exception:
                        print('we do not have item type')
                        item_type = ''
                    try:
                        item = result['entities']['item'][0]['value']
                    except Exception:
                        print('we do not have item!')
                        voices.speak_text(
                            u'Usłyszałam ' + result['_text'] + u' \
                            . Zrozumiałam, że intencją jest \
                            odtwarzanie ' + item_type + u'. Niestety \
                            nie zrozumiałam co konkretnie mam włączyć.')
                        return
                    control.play_item(item, item_type)

                elif intent == 'set_volume':
                    try:
                        vol = int(result['entities']['value'][0]['value'])
                    except Exception:
                        traceback.print_exc()
                        voices.speak_text(
                            u'Usłyszałam ' + result['_text'] + u' \
                            . Zrozumiałam, że intencją jest ustawienie \
                            głośności. Niestety nie zrozumiałam jaką głośność \
                            mam ustawić.')
                        return
                    try:
                        Utils.set_volume(vol)
                    except Exception:
                        traceback.print_exc()
                        voices.speak_text(
                            u'Mam problem z ustawieniem głośności, \
                            sprawdz kotku w logach.')

                elif intent == 'get_weather':
                    location = None
                    try:
                        location = result['entities']['location'][0]['value']
                    except Exception:
                        traceback.print_exc()
                    Utils.forecast_weather(location)
                elif intent == 'search_wikipedia':
                    query = None
                    try:
                        query = result['entities'][
                            'wikipedia_search_query'][0]['value']
                    except Exception:
                        traceback.print_exc()
                        voices.speak_text(
                            u'Usłyszałam ' + result['_text'] + u' \
                            . Zrozumiałam, że intencją jest \
                            szukanie informacji na Wikipedii ' + u'. Niestety \
                            nie zrozumiałam co konkretnie mam szukać.')
                        return
                    Utils.search_wikipedia(query)
                elif intent == 'get_time':
                    Utils.get_time()
            else:
                voices.speak_text(
                    u'Usłyszałam ' + result['_text'] + u' Niestety nie \
                    zrozumiałam twojej intencji.')
        else:
            voices.speak_text(u'Przepraszam, ale nic nie słyszałam.')


if __name__ == '__main__':
    ask_bot('PCH')
