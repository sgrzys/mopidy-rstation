# encoding=utf8
import os


def get_actual_brightness():
    actual_brightness = os.popen(
        'cat /sys/class/backlight/rpi_backlight/actual_brightness')
    return actual_brightness


def set_actual_brightness(ab):
    os.system(
        'echo ' + str(ab) +
        ' > /sys/class/backlight/rpi_backlight/brightness')


def backlight_up():
    ab = get_actual_brightness()
    ab = max(255, int(ab) + 11)
    set_actual_brightness(ab)


def backlight_down():
    ab = get_actual_brightness()
    ab = max(255, int(ab) - 11)
    set_actual_brightness(ab)
