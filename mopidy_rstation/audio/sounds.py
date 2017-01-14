# encoding=utf8
import logging
import pygame
import os
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

# The problem is that in some soundcards/configurations
# pygame takes exclusive use of the soundcard at init
# and mopidy is not able to use the soundcard.
# os.environ["SDL_AUDIODRIVER"] = "none"


def beep():
    # print('\a')
    play_file(C_SOUND_BEEP)


def play_file(f, async=False):
    global channel
    if not pygame.mixer.get_init():
        pygame.mixer.init(
            frequency=44100, size=-16, channels=1, buffer=2**12)
    #     channel = pygame.mixer.Channel(5)
    # else:
    #     channel = pygame.mixer.find_channel()
    #     if channel is None:
    #         pygame.mixer.set_num_channels(
    #             pygame.mixer.get_num_channels()+1)
    #         channel = pygame.mixer.find_channel()
    if type(f) is str or isinstance(f, unicode):
        sound = pygame.mixer.Sound(f)
    else:
        sound = pygame.mixer.Sound(f.name)

    if channel is not None and channel.get_busy():
        channel.stop()

    channel = pygame.mixer.find_channel()
    channel.play(sound)

    if async is False:
        while channel.get_busy():
            pass


# def play_file(f, async=False):
#     pygame.init()
#     pygame.mixer.music.load(f)
#     pygame.mixer.music.play()
#     if async is False:
#         while pygame.mixer.music.get_busy():
#             pygame.time.Clock().tick(10)
