# encoding=utf8
from pprint import pprint
# from StringIO import StringIO
import wit
from mopidy_rstation.utils import Utils
from mopidy_rstation.output import pyvona
import pyaudio
import wave
from StringIO import StringIO
import traceback


CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
INPUT_DEVICE_INDEX = 0
# Change this based on your OSes settings. This should work for OSX, though.
ENDIAN = 'little'
CONTENT_TYPE = \
    'raw;encoding=signed-integer;bits=16;rate={0};endian={1}'.format(
        RATE, ENDIAN)


def record_only():
    output_file = StringIO()
    p = pyaudio.PyAudio()
    for x in range(p.get_device_count()):
        info = p.get_device_info_by_index(x)
        if info['maxInputChannels'] > 0:
            print(str(x) + str(info))
            INPUT_DEVICE_INDEX = info['index']
            RATE = int(info['defaultSampleRate'])

    print('*********************************************')
    print('Selected device index: ' + str(INPUT_DEVICE_INDEX))
    print('device sample rate: ' + str(RATE))
    print('*********************************************')
    print("* recording")
    Utils.start_rec_wav()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=INPUT_DEVICE_INDEX)
    all = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        all.append(data)

    Utils.stop_rec_wav()
    print("* done recording")

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
    p = pyaudio.PyAudio()
    for x in range(p.get_device_count()):
        info = p.get_device_info_by_index(x)
        if info['maxInputChannels'] > 0:
            print(str(x) + str(info))
            INPUT_DEVICE_INDEX = info['index']
            RATE = int(info['defaultSampleRate'])
    print('*********************************************')
    print('Selected device index: ' + str(INPUT_DEVICE_INDEX))
    print('device sample rate: ' + str(RATE))
    print('*********************************************')
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=INPUT_DEVICE_INDEX)

    print("* recording and streaming")
    Utils.start_rec_wav()

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        yield stream.read(CHUNK, exception_on_overflow=False)

    Utils.stop_rec_wav()
    print("* done recording and streaming")

    stream.stop_stream()
    stream.close()
    p.terminate()


def ask_bot(config):

    v = pyvona.create_voice(config)

    try:
        w = wit.Wit(config['wit_token'])
        # TODO switch to record_and_stream!!!
        # record_and_stream works fine on my laptop but not on raspberry pi
        # record_and_stream
        # result = w.post_speech(record_and_stream(),content_type=CONTENT_TYPE)
        #
        # record_only
        output_file = StringIO()
        output_file = record_only()
        Utils.speak('PROCESSING')
        result = w.post_speech(output_file.getvalue())
    except Exception:
        str("Error in ai.ask_bot")
        traceback.print_exc()
        return
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
                        traceback.print_exc()
                        # v.speak(u'Usłyszałam ' + result['_text'] + u' \
                        #     . Zrozumiałam, że intencją jest dtwarzanie. \
                        #     Niestety nie zrozumiałam co mam włączyć.')
                        # return
                        # continue without item type
                        item_type = ''

                    try:
                        item = result['entities']['item'][0]['value']
                    except Exception:
                        traceback.print_exc()
                        v.speak(u'Usłyszałam ' + result['_text'] + u' \
                            . Zrozumiałam, że intencją jest \
                            odtwarzanie ' + item_type + u'. Niestety \
                            nie zrozumiałam co konkretnie mam włączyć.')
                        return
                    v.speak(u'OK, już włączam ' + item_type + ' ' + item)
                    Utils.play_item(item, item_type)

                elif intent == 'set_volume':
                    try:
                        vol = int(result['entities']['value'][0]['value'])
                    except Exception:
                        traceback.print_exc()
                        v.speak(u'Usłyszałam ' + result['_text'] + u' \
                            . Zrozumiałam, że intencją jest ustawienie \
                            głośności. Niestety nie zrozumiałam jaką głośność \
                            mam ustawić.')
                        return
                    try:
                        Utils.set_volume(vol)
                    except Exception:
                        traceback.print_exc()
                        v.speak(u'Mam problem z ustawieniem głośności, \
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
                        v.speak(u'Usłyszałam ' + result['_text'] + u' \
                            . Zrozumiałam, że intencją jest \
                            szukanie informacji na Wikipedii ' + u'. Niestety \
                            nie zrozumiałam co konkretnie mam szukać.')
                        return
                    Utils.search_wikipedia(query)

            else:
                v.speak(u'Usłyszałam ' + result['_text'] + u' Niestety nie \
                zrozumiałam twojej intencji.')
        else:
            v.speak(u'Przepraszam, ale nic nie słyszałam.')


if __name__ == '__main__':
    conf = Utils.get_config()
    Utils.config = conf['rstation']
    ask_bot(conf['rstation'])
