# encoding=utf8
import pyaudio
import wave
import logging
C_SOUNDS_DIR = '/home/pi/mopidy-rstation/audio/'
C_SOUND_REC_START = C_SOUNDS_DIR + 'start_rec.wav'
C_SOUND_REC_END = C_SOUNDS_DIR + 'stop_rec.wav'
C_SOUND_START_UP = C_SOUNDS_DIR + 'newbuntu.wav'
C_SOUND_BEEP = C_SOUNDS_DIR + 'alert.wav'
logger = logging.getLogger('mopidy_Rstation')
logger = logging.getLogger(__name__)


def play(sound):
    play_wav(sound)


def play_wav(file):
    wf = wave.open(file, 'rb')
    # create an audio object
    p = pyaudio.PyAudio()

    # open stream based on the wave object which has been input.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data (based on the chunk size)
    data = wf.readframes(1024)

    # play stream (looping from beginning of file to the end)
    while data != '':
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(1024)

    # cleanup stuff.
    stream.close()
    p.terminate()
