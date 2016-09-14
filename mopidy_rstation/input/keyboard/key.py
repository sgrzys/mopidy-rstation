# This Python file uses the following encoding: utf-8
from ..command_dispatcher import Event
from showkey import ShowKey
from threading import Thread


class KeyPad():
    def __init__(self, config):
        self.config = config
        # self.hm = HookManager()
        # self.hm.HookKeyboard()
        # self.hm.KeyUp = self.handle_event
        # self.hm.start()
        self.ButtonPressed = Event()

        t = Thread(target=self.show_key)
        t.start()

    def show_key(self):
        sk = ShowKey()
        sk.addKeyAction("*p", self.key_pressed)
        sk.addKeyAction("*r", self.key_released)
        sk.run()

    def key_pressed(self, kc):
        print("Key pressed - keycode: %d" % kc)

    def key_released(self, kc):
        print("Key released - keycode: %d" % kc)

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
