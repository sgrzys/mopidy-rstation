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
RECORD_SECONDS = 3
# Change this based on your OSes settings. This should work for OSX, though.
ENDIAN = 'little'
CONTENT_TYPE = \
    'raw;encoding=signed-integer;bits=16;rate={0};endian={1}'.format(
        RATE, ENDIAN)


def record_and_stream():
    p = pyaudio.PyAudio()
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


def ask_bot(wit_token, ivona_access_key, ivona_secret_key):
    # output_file = StringIO()

    w = wit.Wit(wit_token)
    result = w.post_speech(record_and_stream(), content_type=CONTENT_TYPE)
    pprint(result)

    try:
        intent = u'Zrozumiałam, że intencją jest ' + \
            result['entities']['intent'][0]['value']
    except Exception:
        intent = "Niestety, nie zrozumiałam twojej intencji"

    try:
        item_type = "typ " + result['entities']['type'][0]['value']
    except Exception:
        item_type = "typ nie został rozpoznany"

    try:
        item = "pozycja" + result['entities']['item'][0]['value']
    except Exception:
        item = "pozycja nie znana"

    v = pyvona.create_voice(ivona_access_key, ivona_secret_key)
    v.speak(u'Cześć! Usłyszałam ' + result['_text'])
    v.speak(intent + ". " + item_type + ". " + item)

if __name__ == '__main__':
    ask_bot(1, 1, 1)
