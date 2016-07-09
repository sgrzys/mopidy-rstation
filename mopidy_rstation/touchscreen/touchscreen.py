# encoding=utf8
import os


def backlight_up():
    actual_brightness = os.system('cat actual_brightness')
    actual_brightness = max(255, int(actual_brightness) + 11)
    os.system(
        ' echo ' + str(actual_brightness) +
        ' > /sys/class/backlight/rpi_backlight/brightness')


def backlight_down():
    actual_brightness = os.system('cat actual_brightness')
    actual_brightness = min(0, int(actual_brightness) - 11)
    os.system(
        ' echo ' + str(actual_brightness) +
        ' > /sys/class/backlight/rpi_backlight/brightness')
