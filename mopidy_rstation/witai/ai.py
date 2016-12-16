# encoding=utf8
from pprint import pprint
# from StringIO import StringIO
import wit
from mopidy_rstation.utils import Utils
from mopidy_rstation.player import control
from mopidy_rstation.config.settings import Config
import pyaudio
import wave
from StringIO import StringIO
import traceback
from struct import pack
from ..audio import sounds
from ..audio import voices


RECORDING = False
CHUNK = 256
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
INPUT_DEVICE_INDEX = None
if pack('@h', 1) == pack('<h', 1):
    ENDIAN = 'little'
else:
    ENDIAN = 'big'
CONTENT_TYPE = \
    'raw;encoding=signed-integer;bits=16;rate={0};endian={1}' \
    .format(RATE, ENDIAN)


def set_audio_in(audio_in_name):
    if INPUT_DEVICE_INDEX is not None:
        return
    global CHANNELS
    global RATE
    global INPUT_DEVICE_INDEX
    global CONTENT_TYPE
    p = pyaudio.PyAudio()
    for x in range(p.get_device_count()):
        try:
            info = p.get_device_info_by_index(x)
            if info['maxInputChannels'] > 0:
                # USB Audio Device or Airmouse: USB Audio
                if info['name'].startswith(audio_in_name):
                    INPUT_DEVICE_INDEX = info['index']
                    RATE = int(info['defaultSampleRate'])
                    CHANNELS = int(info['maxInputChannels'])
                    CONTENT_TYPE = \
                        'raw;encoding=signed-integer;bits=16;' + \
                        'rate={0};endian={1}' \
                        .format(RATE, ENDIAN)
                    print('*********************************************')
                    print('Selected device index: ' + str(INPUT_DEVICE_INDEX))
                    print('Selected device rate: ' + str(RATE))
                    print('Content type: ' + str(CONTENT_TYPE))
                    print('*********************************************')
        except Exception as e:
            print(x + '. Error: ' + e)
    p.terminate()


def record_only():
    global RECORDING
    p = pyaudio.PyAudio()
    output_file = StringIO()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=INPUT_DEVICE_INDEX)
    all = []
    sounds.play_file(sounds.C_SOUND_REC_START)
    RECORDING = True
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        all.append(data)
        # stop recording after RECORD_SECONDS or when the button is up
        if RECORDING is False:
            break
    sounds.play_file(sounds.C_SOUND_REC_END)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(output_file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(all))
    wf.close()
    return output_file


def record_and_stream():
    global RECORDING
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=INPUT_DEVICE_INDEX)
    RECORDING = True
    sounds.play_file(sounds.C_SOUND_REC_START)
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        yield stream.read(CHUNK, exception_on_overflow=False)
        if RECORDING is False:
            break
    sounds.play_file(sounds.C_SOUND_REC_END)
    stream.stop_stream()
    stream.close()
    p.terminate()


def ask_bot():
    try:
        config = Config.get_config()
        w = wit.Wit(config['wit_token'])
        audio_in_name = config['audio_in_name']
        set_audio_in(audio_in_name)
        # TODO this is a faster version but the qualitty have to be improved
        result = w.post_speech(
            record_and_stream(), content_type=CONTENT_TYPE)
        # slow version
        # output_file = StringIO()
        # output_file = record_only()
        # result = w.post_speech(output_file.getvalue())
    except Exception:
        traceback.print_exc()
        return
    pprint(result)
    intent = u' '
    item_type = u' '
    item = None
    pprint('result')
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
                    # voices.speak('PLAY_URI', val=item_type + ' ' + item)
                    # v.speak(u'OK, już włączam ' + item_type + ' ' + item)

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
    ask_bot()
