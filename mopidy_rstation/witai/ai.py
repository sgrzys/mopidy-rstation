# encoding=utf8
from pprint import pprint
from mopidy_rstation.utils import Utils
from mopidy_rstation.player import control
from mopidy_rstation.config.settings import Config
from mopidy_rstation.audio import sounds
from mopidy_rstation.audio import voices
import requests
import json
import pyaudio
import traceback

RECORDING = False
CHUNK = 512
RATE = 8000
RECORD_SECONDS = 5
INPUT_DEVICE_INDEX = None


def set_audio_in(audio_in_name):
    global INPUT_DEVICE_INDEX
    p = pyaudio.PyAudio()
    for x in range(p.get_device_count()):
        try:
            info = p.get_device_info_by_index(x)
            if info['maxInputChannels'] > 0:
                print('----------------------')
                print('MIC: ' + str(info))
                print('----------------------')
                if info['name'].startswith(audio_in_name):
                    INPUT_DEVICE_INDEX = info['index']
                    print('**************************************************')
                    print('Selected device index: ' + str(INPUT_DEVICE_INDEX))
                    print('**************************************************')
        except Exception as e:
            print(str(x) + '. Error: ' + str(e))
    p.terminate()


def record_and_stream(stream):
    global RECORDING
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        yield stream.read(CHUNK, exception_on_overflow=False)
        if RECORDING is False:
            break


def ask_bot(mic=None):
    result = None
    global RECORDING
    try:
        config = Config.get_config()
        if mic is not None:
            audio_in_name = mic
        else:
            audio_in_name = config['audio_in_name']
        print('set_audio_in -> ' + audio_in_name)
        set_audio_in(audio_in_name)

        headers = {'Authorization': 'Bearer ' + config['wit_token'],
                   'Content-Type': 'audio/raw; encoding=signed-integer; ' +
                   'bits=16; rate=8000; endian=little',
                   'Transfer-Encoding': 'chunked'}
        url = 'https://api.wit.ai/speech'

        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK,
            input_device_index=INPUT_DEVICE_INDEX)
        RECORDING = True
        sounds.play_file(sounds.C_SOUND_REC_START)

        result = requests.post(
            url, headers=headers, data=record_and_stream(stream))

        sounds.play_file(sounds.C_SOUND_REC_END)
        stream.stop_stream()
        stream.close()
        p.terminate()

        if result is not None:
            RECORDING = False
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
    ask_bot('default')
