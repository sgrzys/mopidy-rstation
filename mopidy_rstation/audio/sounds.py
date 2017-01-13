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

# The problem is that in some soundcards/configurations
# pygame takes exclusive use of the soundcard at init
# and mopidy is not able to use the soundcard.
# os.environ["SDL_AUDIODRIVER"] = "none"


def beep():
    # print('\a')
    play_file(C_SOUND_BEEP)


def play_file(f, async=False):
    pygame.init()
    pygame.mixer.music.load(f)
    pygame.mixer.music.play()
    if async is False:
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
