# encoding=utf8
import os
import subprocess
import logging
from ..tts import tts

logger = logging.getLogger('mopidy_Rstation')


def get_actual_brightness():
    ab = subprocess.check_output(
        'cat /sys/class/backlight/rpi_backlight/actual_brightness', shell=True)

    logger.debug('touchscreen actual_brightness -> ' + str(ab))
    return ab


def set_actual_brightness(ab):
    logger.debug('touchscreen set_actual_brightness-> ' + str(ab))
    tts.speak('BRIGHTNESS', val=str(ab))
    os.system(
        'echo ' + str(ab) +
        ' > /sys/class/backlight/rpi_backlight/brightness')


def backlight_up():
    ab = get_actual_brightness()
    ab = min(255, int(ab) + 11)
    ab = max(0, ab)
    set_actual_brightness(ab)


def backlight_down():
    ab = get_actual_brightness()
    ab = min(255, int(ab) - 11)
    ab = max(0, ab)
    set_actual_brightness(ab)
