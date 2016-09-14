# This Python file uses the following encoding: utf-8
from ..command_dispatcher import Event
from threading import Thread
from evdev import InputDevice, categorize, ecodes, list_devices
from select import select


class KeyPad():
    def __init__(self, config):
        self.config = config
        self.ButtonPressed = Event()

        t = Thread(target=self.keyboard)
        t.start()

    def keyboard(self):
        devices = [InputDevice(fn) for fn in list_devices()]
        for device in devices:
            print(device.fn, device.name, device.phys)

        # TODO check the capabilities and add all the keyboards
        dev = InputDevice('/dev/input/event2')
        dev.capabilities()
        dev.capabilities(verbose=True)
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY:
                print(categorize(event))

    def handle_event(self, event):
        # if event.Key in watched_keys:
        # print(str(event.Key))
        if event.Key == 'Left':
            self.ButtonPressed('player_prev')
        if event.Key == 'space':
            self.ButtonPressed('player_play_pause')
        if event.Key == 'Right':
            self.ButtonPressed('player_next')
        if event.Key == 'Up':
            self.ButtonPressed('track_list_prev')
        if event.Key == 'Return':
            self.ButtonPressed('track_list_enter')
        if event.Key == 'Down':
            self.ButtonPressed('track_list_next')
        if event.Key == '2':
            self.ButtonPressed('lib_root_dir')
        if event.Key == '4':
            self.ButtonPressed('lib_prev')
        if event.Key == '5':
            self.ButtonPressed('lib_enter')
        if event.Key == '6':
            self.ButtonPressed('lib_next')
        if event.Key == '7':
            self.ButtonPressed('lib_audiobook')
        if event.Key == '8':
            self.ButtonPressed('lib_radio')
        if event.Key == '9':
            self.ButtonPressed('lib_music')
        if event.Key == 'minus':
            self.ButtonPressed('vol_down')
        if event.Key == 'plus':
            self.ButtonPressed('vol_up')
        if event.Key == 'l':
            self.ButtonPressed('change_lang')
