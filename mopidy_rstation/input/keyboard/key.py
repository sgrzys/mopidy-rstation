# This Python file uses the following encoding: utf-8
from ..command_dispatcher import Event
from threading import Thread
from evdev import InputDevice, ecodes, list_devices
import logging
import sys

logger = logging.getLogger('mopidy_Rstation')


class KeyPad(Thread):
    def __init__(self, config):
        Thread.__init__(self)
        self.name = 'KeyPad worker thread'
        self.frontendActive = True
        self.config = config
        self.ButtonPressed = Event()
        self.dev = None

    def run(self):
        try:
            self.run_inside_try()
        except Exception as e:
            logger.warning('Rstation has problems starting KeyPad: ' + str(e))

    def run_inside_try(self):
        self.startKeyPad()

    def stop(self):
        logger.info('Stoping KeyPad')
        # self.dev.ungrab()
        self.frontendActive = False
        sys.exit(0)

    def startKeyPad(self):
        self.frontendActive = True

        devices = map(InputDevice, list_devices())
        for device in devices:
            if "Microsoft" in device.name and self.dev is None:
                print(device.fn, device.name, device.phys)
                self.dev = InputDevice(device.fn)
                self.dev.grab()

        # devices = [InputDevice(fn) for fn in list_devices()]
        # for device in devices:
        #     print(device.fn, device.name, device.phys)
        # self.dev = InputDevice('/dev/input/event4')
        # self.dev.capabilities()
        # self.dev.capabilities(verbose=True)

        while self.frontendActive:
            for event in self.dev.read_loop():
                if event.type == ecodes.EV_KEY & event.value == 1:
                    # event.value == 1 key down
                    # event.value == 0 key up
                    # event.value == 2 key hold
                    self.handle_event(ecodes.KEY[event.code])

    def handle_event(self, code):
        if code == 'KEY_LEFT':
            self.ButtonPressed('player_prev')
        if code == 'KEY_SPACE':
            self.ButtonPressed('player_play_pause')
        if code == 'KEY_RIGHT':
            self.ButtonPressed('player_next')
        if code == 'KEY_DOWN':
            self.ButtonPressed('track_list_prev')
        if code == 'KEY_ENTER':
            self.ButtonPressed('track_list_enter')
        if code == 'KEY_UP':
            self.ButtonPressed('track_list_next')
        if code == 'KEY_2':
            self.ButtonPressed('lib_root_dir')
        if code == 'KEY_4':
            self.ButtonPressed('lib_prev')
        if code == 'KEY_5':
            self.ButtonPressed('lib_enter')
        if code == 'KEY_6':
            self.ButtonPressed('lib_next')
        if code == 'KEY_7':
            self.ButtonPressed('lib_audiobook')
        if code == 'KEY_8':
            self.ButtonPressed('lib_radio')
        if code == 'KEY_9':
            self.ButtonPressed('lib_music')
        if code == 'KEY_MINUS':
            self.ButtonPressed('vol_down')
        if code == 'KEY_EQUAL':
            self.ButtonPressed('vol_up')
        if code == 'KEY_L':
            self.ButtonPressed('change_lang')
