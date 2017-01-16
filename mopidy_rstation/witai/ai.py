# encoding=utf8
from pprint import pprint
from mopidy_rstation.config.settings import Config
from mopidy_rstation.audio import sounds
from mopidy_rstation.audio import voices
import parser
import requests
import json
import traceback
import alsaaudio
import pygame

RECORDING = False
CHUNK = 512
RATE = 8000
RECORD_SECONDS = 3
INPUT_DEVICE_INDEX = None


def set_mic(audio_in_name):
    global RATE
    if audio_in_name == 'audiocodec':
        # to fix the issue with the audio speed up
        RATE = 44100
    else:
        RATE = 8000
    mic = 'plughw:CARD=' + audio_in_name
    # plughw:CARD=audiocodec
    # plughw:CARD=Airmouse
    # plughw:CARD=CameraB409241
    #
    # TODO test is we have this hardware
    # for pd in alsaaudio.pcms(alsaaudio.PCM_CAPTURE):
    #         print(str(pd))
    # PCM_NONBLOCK
    try:
        inp = alsaaudio.PCM(
            type=alsaaudio.PCM_CAPTURE,
            mode=alsaaudio.PCM_NORMAL,
            device=mic)
        inp.setchannels(1)
        inp.setrate(RATE)
        inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        inp.setperiodsize(CHUNK)
        return inp
    except Exception:
        voices.speak_text('Problem z mikrofonem. Spróbuj zmienic port usb.')


def record_and_stream(inp):
    global RECORDING
    if pygame.mixer.music.get_busy:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.quit()
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
        lang = Config.get_current_lang(short=True)
        if mic is not None:
            audio_in_name = mic
        else:
            audio_in_name = config['audio_in_name']
        print('set_mic -> ' + audio_in_name)
        inp = set_mic(audio_in_name)

        headers = {'Authorization': 'Bearer ' + config['wit_token_' + lang],
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
    # HTTP code
    pprint(result)
    result = json.loads(result.text)
    # JSON message
    pprint(result)

    parser.parse_wit(result)
if __name__ == '__main__':
    ask_bot('PCH')
