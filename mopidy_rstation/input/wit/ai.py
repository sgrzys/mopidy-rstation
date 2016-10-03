# encoding=utf8
from pprint import pprint
# from StringIO import StringIO
import wit
from mopidy_rstation.utils import Utils
from mopidy_rstation.output import pyvona
from ConfigParser import ConfigParser
import pyaudio
import wave
from StringIO import StringIO


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


p = pyaudio.PyAudio()
for x in range(p.get_device_count()):
    info = p.get_device_info_by_index(x)
    if info['maxInputChannels'] > 0:
        print(str(x) + str(info))
        INPUT_DEVICE_INDEX = info['index']


def record_only():
    output_file = StringIO()
    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=INPUT_DEVICE_INDEX)

    print("* recording")
    Utils.start_rec_wav()

    all = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
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
        yield stream.read(CHUNK)

    Utils.stop_rec_wav()
    print("* done recording and streaming")

    stream.stop_stream()
    stream.close()
    p.terminate()


def play_item(item_type, item):
    print('*************** play_item ***************')
    print('***************' + item_type + '***************')
    print('***************' + item + '***************')


def ask_bot(config):
    output_file = StringIO()
    w = wit.Wit(config['wit_token'])
    # TODO
    # record_and_stream works fine on my laptop but not on raspberry pi with
    # result = w.post_speech(record_and_stream(), content_type=CONTENT_TYPE)

    output_file = record_only()
    result = w.post_speech(output_file.getvalue())
    pprint(result)
    intent = u' '
    item_type = u' '
    item = None
    if result is not None:
        try:
            intent = result['entities']['intent'][0]['value']
        except Exception:
            intent = None

        if intent == 'set_volume':
            try:
                item = u'wartość ' + result['entities']['value'][0]['value']
            except Exception:
                item = u'wartość nie znana'

        v = pyvona.create_voice(config)
        if result['_text'] is not None:
            if intent is not None:
                if intent == 'play_item':
                    try:
                        item_type = result['entities']['type'][0]['value']
                    except Exception:
                        v.speak(u'Usłyszałam ' + result['_text'] + ' \
                            . Zrozumiałam, że intencją jest dtwarzanie. \
                            Niestety nie zrozumiałam co mam włączyć.')
                        return

                    try:
                        item = result['entities']['item'][0]['value']
                    except Exception:
                        v.speak(u'Usłyszałam ' + result['_text'] + ' \
                            . Zrozumiałam, że intencją jest \
                            odtwarzanie ' + item_type + '. Niestety \
                            nie zrozumiałam co konkretnie mam włączyć.')
                        return
                    play_item(item_type, item)

            else:
                v.speak(u'Usłyszałam ' + result['_text'] + ' Niestety nie \
                zrozumiałam intencji.')
        else:
            v.speak(u'Przepraszam, ale nic nie słyszałam.')


# to test from cmd
def get_config():
    conf = ConfigParser()
    conf.read('/home/pi/mopidy.conf')
    the_dict = {}
    for section in conf.sections():
        the_dict[section] = {}
        for key, val in conf.items(section):
            the_dict[section][key] = val
    return the_dict

if __name__ == '__main__':
    conf = get_config()
    print(str(conf['rstation']))
    ask_bot(conf['rstation'])
