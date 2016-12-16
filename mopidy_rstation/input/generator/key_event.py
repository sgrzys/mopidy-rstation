# This Python file uses the following encoding: utf-8
from evdev import UInput, ecodes as e
import time


def pressMicButton():
    ui = UInput(name="micbutton")
    ui.write(e.EV_KEY, e.KEY_HOME, 1)  # down
    ui.write(e.EV_KEY, e.KEY_HOME, 0)  # up
    ui.syn()
    time.sleep(0.8)
    ui.close()


# TODO
def main():
    pressMicButton()


if __name__ == '__main__':
    main()
