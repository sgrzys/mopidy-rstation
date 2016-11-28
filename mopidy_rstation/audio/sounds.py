# encoding=utf8
import logging
import pygame
C_SOUNDS_DIR = '/home/pi/mopidy-rstation/audio/'
C_SOUND_REC_START = C_SOUNDS_DIR + 'start_rec.wav'
C_SOUND_REC_END = C_SOUNDS_DIR + 'stop_rec.wav'
C_SOUND_START_UP = C_SOUNDS_DIR + 'newbuntu.wav'
C_SOUND_BEEP = C_SOUNDS_DIR + 'alert.wav'
C_SOUND_PLUG_IN = C_SOUNDS_DIR + 'plugin.wav'
C_SOUND_PLUG_OUT = C_SOUNDS_DIR + 'plugout.wav'

logger = logging.getLogger('mopidy_Rstation')
logger = logging.getLogger(__name__)
channel = None


def beep():
    # print('\a')
    play_file(C_SOUND_BEEP)


def start_up():
    play_file(C_SOUND_START_UP)


def play_file(f, async=False):
    global channel
    if not pygame.mixer.get_init():
        pygame.mixer.init()
        channel = pygame.mixer.Channel(5)
    else:
        channel = pygame.mixer.find_channel()
        if channel is None:
            pygame.mixer.set_num_channels(
                pygame.mixer.get_num_channels()+1)
            channel = pygame.mixer.find_channel()

    if type(f) is str:
        sound = pygame.mixer.Sound(file=f)
    else:
        sound = pygame.mixer.Sound(file=f.name)
    channel.play(sound)

    if async is False:
        while channel.get_busy():
            pass
