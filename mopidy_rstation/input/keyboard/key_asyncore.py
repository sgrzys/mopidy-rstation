# This Python file uses the following encoding: utf-8
from ..command_dispatcher import Event
import threading
import logging
import pyudev
import evdev
import select
import functools
import traceback
from mopidy_rstation.utils import Utils
from asyncore import file_dispatcher, loop

logger = logging.getLogger('mopidy_Rstation')


class KeyPad(threading.Thread):
    def __init__(self, config):
        super(KeyPad, self).__init__()
        self.name = 'KeyPad worker thread'
        self.frontendActive = True
        self.config = config
        self.ButtonPressed = Event()
        self.devices = {}
        self._stop = threading.Event()
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='input')
        self.monitor.start()

    def checkIfDevIsAirmouse(self, d):
        d.capabilities()
        return "airmouse" in d.name.lower()
        # return "keyboard" in d.name.lower() \
        #     or "microsoft" in d.name.lower() \
        #     or "airmouse" in d.name.lower()

    def run(self):
        try:
            self.run_inside_try()
        except Exception as e:
            logger.error('KeyPad: ' + str(e))
            traceback.print_exc()

    def run_inside_try(self):
        self.startKeyPad()

    def stop(self):
        logger.info('Stoping KeyPad start')
        # for device in self.devices:
        #     self.dev = evdev.InputDevice(device.fn)
        #     self.dev.ungrab()
        self.frontendActive = False
        self._stop.set()
        logger.info('Stoping KeyPad end')
        try:
            self.monitor.stop()
        except Exception:
            print('Error in monitor.stop()')
            traceback.print_exc()

    def startKeyPad(self):
        self.frontendActive = True
        for d in map(evdev.InputDevice, evdev.list_devices()):
            if self.checkIfDevIsAirmouse(d):
                print('We have airmouse device ' + str(d))
                InputDeviceDispatcher(d, self)
                d.grab()
            # self.devices[d.fn] = d
        loop()

        self.devices['monitor'] = self.monitor

        while self.frontendActive:
            rs, _, _ = select.select(self.devices.values(), [], [])
            # Unconditionally ping monitor; if this is spurious this
            # will no-op because we pass a zero timeout.  Note that
            # it takes some time for udev events to get to us.
            for udev in iter(functools.partial(self.monitor.poll, 0), None):
                if not udev.device_node:
                    break
                if udev.action == 'add':
                    if udev.device_node not in self.devices:
                        print("Device added: %s" % udev)
                        try:
                            new_d = evdev.InputDevice(udev.device_node)
                            if self.checkIfDevIsAirmouse(new_d):
                                self.devices[udev.device_node] = new_d
                                new_d.grab()
                                Utils.aplay_thread("plugin")
                        except Exception:
                            print('Error during add device ')
                            traceback.print_exc()
                elif udev.action == 'remove':
                    if udev.device_node in self.devices:
                        print(
                            "Device removed (udev): %s" %
                            self.devices[udev.device_node])
                        del self.devices[udev.device_node]
                        Utils.aplay_thread("plugout")

    def handle_event(self, code):
        print('KeyPad -> handle_event -> ' + code)
        # workeround - kill the ivona - to stop the forecast
        try:
            if Utils.channel is not None:
                Utils.channel.stop()
                Utils.channel = None
                Utils.core.playback.volume = Utils.prev_volume
        except Exception:
            traceback.print_exc()
        # main keys
        if code == 'KEY_COMPOSE':
            self.ButtonPressed('mode')
        if code == 'KEY_LEFT':
            self.ButtonPressed('left')
        if code == 'KEY_RIGHT':
            self.ButtonPressed('right')
        if code == 'KEY_DOWN':
            self.ButtonPressed('down')
        if code == 'KEY_UP':
            self.ButtonPressed('up')
        if code == 'KEY_ENTER':
            self.ButtonPressed('enter')
        if code == 'KEY_ESC' or code == 'KEY_BACK':
            self.ButtonPressed('change_lang')
        if code == 'KEY_MINUS' or code == 'KEY_VOLUMEDOWN':
            self.ButtonPressed('vol_down')
        if code == 'KEY_PLUS' or code == 'KEY_VOLUMEUP':
            self.ButtonPressed('vol_up')
        if code == 'KEY_POWER' or code == 'KEY_F24':
            # Utils.recording = True
            self.ButtonPressed('ask_bot')
        #
        if code == 'KEY_PREVIOUSSONG':
            self.ButtonPressed('player_prev')
        if code == 'KEY_SPACE' or code == 'KEY_PLAYPAUSE':
            self.ButtonPressed('player_play_pause')
        if code == 'KEY_NEXTSONG':
            self.ButtonPressed('player_next')
        if code == 'KEY_L':
            self.ButtonPressed('change_lang')
        if code == 'KEY_0':
            self.ButtonPressed('ask_bot')
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


class InputDeviceDispatcher(file_dispatcher, KeyPad):
    def __init__(self, device, keypad):
        self.device = device
        self.keypad = keypad
        file_dispatcher.__init__(self, device)

    def recv(self, ign=None):
        return self.device.read()

    def handle_read(self):
        for event in self.recv():
            # event.value == 1 key down
            # event.value == 0 key up
            # event.value == 2 key hold
            if event.type == evdev.ecodes.EV_KEY & event.value == 1:
                # enter with mouse mode on airmouse
                if event.code == 272:
                    self.keypad.handle_event('KEY_ENTER')
                # esc with mouse mode on airmouse
                elif event.code == 273:
                    self.keypad.handle_event('KEY_ESC')
                else:
                    self.keypad.handle_event(evdev.ecodes.KEY[event.code])
            elif event.type == evdev.ecodes.EV_KEY & event.value == 0:
                # key up on microphone
                print('Key UP: ' + evdev.ecodes.KEY[event.code])
                if evdev.ecodes.KEY[event.code] == 'KEY_F24' or \
                   evdev.ecodes.KEY[event.code] == 'KEY_POWER':
                        print('!!!Stop recording!!!')
                        Utils.recording = False