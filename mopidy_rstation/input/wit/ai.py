# encoding=utf8
from pprint import pprint
# from StringIO import StringIO
import wit
from mopidy_rstation.utils import Utils
from mopidy_rstation.output import pyvona
import pyaudio


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
# Change this based on your OSes settings. This should work for OSX, though.
ENDIAN = 'little'
CONTENT_TYPE = \
    'raw;encoding=signed-integer;bits=16;rate={0};endian={1}'.format(
        RATE, ENDIAN)


def record_and_stream():
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16, channels=1, rate=44100,
        input=True, frames_per_buffer=1024)

    stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE,
        input=True, frames_per_buffer=CHUNK)

    print("* recording and streaming")
    Utils.start_rec_wav()

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        yield stream.read(CHUNK)

    Utils.stop_rec_wav()
    print("* done recording and streaming")

    stream.stop_stream()
    stream.close()
    p.terminate()


def ask_bot(config):

    # output_file = StringIO()

    w = wit.Wit(config['wit_token'])
    result = w.post_speech(record_and_stream(), content_type=CONTENT_TYPE)
    pprint(result)
    intent = u' '
    item_type = u' '
    item = u' '
    t = u' '
    if result is not None:
        try:
            intent = result['entities']['intent'][0]['value']
            t = u'. Zrozumiałam, że intencją jest ' + intent

        except Exception:
            t = u'. Niestety, nie zrozumiałam twojej intencji'

        if intent == 'play_item':
            try:
                item_type = "typ " + result['entities']['type'][0]['value']
            except Exception:
                item_type = "typ nie został rozpoznany"

            try:
                item = u'pozycja ' + result['entities']['item'][0]['value']
            except Exception:
                item = 'pozycja nie znana'

        if intent == 'set_volume':
            try:
                item = u'wartość ' + result['entities']['value'][0]['value']
            except Exception:
                item = u'wartość nie znana'

        v = pyvona.create_voice(config)
        if result['_text'] is not None:
            v.speak(u'Cześć! Usłyszałam ')
            # s = u'Cześć! Usłyszałam ' + result[u'_text'] + \
            #     t + '. ' + item_type + '. ' + item + '.'
            s = result[u'_text']
            v.speak(s)
        else:
            v.speak(
                u'Przepraszam, ale nic nie słyszałam. Czy możesz powtórzyć?')

if __name__ == '__main__':
    ask_bot(1, 1, 1)
