# This Python file uses the following encoding: utf-8
from ..command_dispatcher import Event
import threading
import logging
import pyudev
import evdev
import select
import functools
import errno
import traceback
from threading import Thread
from mopidy_rstation.audio import sounds
from mopidy_rstation.audio import voices
from mopidy_rstation.witai import ai

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

    def checkIfDevIsKeyboard(self, d):
        d.capabilities()
        return "microsoft" not in d.name.lower() \
            and "AT Translated Set 2 keyboard" not in d.name \
            and "AlpsPS/2" not in d.name
        # return "airmouse" in d.name.lower() or "wireless" in d.name.lower()
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
            if self.checkIfDevIsKeyboard(d):
                print('We have keyboard device ' + str(d))
                self.devices[d.fn] = d
                d.grab()

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
                            if self.checkIfDevIsKeyboard(new_d):
                                self.devices[udev.device_node] = new_d
                                new_d.grab()
                                # sounds.play_file(sounds.C_SOUND_PLUG_IN)
                        except Exception:
                            print('Error during add device ')
                            traceback.print_exc()
                elif udev.action == 'remove':
                    if udev.device_node in self.devices:
                        print(
                            "Device removed (udev): %s" %
                            self.devices[udev.device_node])
                        del self.devices[udev.device_node]
                        # sounds.play_file(sounds.C_SOUND_PLUG_OUT)

            for r in rs:
                # You can't read from a monitor
                if r.fileno() == self.monitor.fileno():
                    continue
                if r.fn not in self.devices:
                    continue
                # Select will immediately return an fd for read if it will
                # ENODEV.  So be sure to handle that.
                try:
                    for event in r.read():
                        # event.value == 1 key down
                        # event.value == 0 key up
                        # event.value == 2 key hold
                        if event.type == evdev.ecodes.EV_KEY and \
                           event.value == 1:
                            # enter with mouse mode on airmouse
                            if event.code == 272:
                                self.handle_event('KEY_ENTER')
                            # esc with mouse mode on airmouse
                            elif event.code == 273:
                                self.handle_event('KEY_ESC')
                            # key on device
                            elif r.name == 'sunxi-gpiokey':
                                self.handle_event('KEY_MIC_ON_DEVICE')
                            else:
                                self.handle_event(evdev.ecodes.KEY[event.code])
                        if event.type == evdev.ecodes.EV_KEY and \
                           (event.value == 0 or event.value == 00):
                            if r.name == 'sunxi-gpiokey' or \
                             evdev.ecodes.KEY[event.code] == 'KEY_COMPOSE':
                                print('key up on sunxi-gpiokey or KEY_COMPOSE')
                                print('this action is ignored')
                            else:
                                ai.RECORDING = False

                except Exception as e:
                    if hasattr(e, 'errno'):
                        if e.errno == errno.ENODEV:
                            print("Device removed: %s" % r)
                            del self.devices[r.fn]
                    logger.error('KeyPad: ' + str(e))
                    traceback.print_exc()

    def handle_event_thread(self, code):
            # main keys
            if code == 'KEY_POWER':
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
            if code in ['KEY_F24', 'KEY_COMPOSE', 'KEY_HOMEPAGE']:
                self.ButtonPressed('ask_bot')
            if code in ['KEY_MIC_ON_DEVICE']:
                self.ButtonPressed('ask_bot_2')
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

    def handle_event(self, code):
        print('KeyPad -> handle_event -> ' + code)
        # workeround - kill the ivona - to stop the forecast
        if code != 'KEY_VOLUMEDOWN' and code != 'KEY_VOLUMEUP':
            try:
                if sounds.channel.get_busy():
                    sounds.channel.stop()
                    voices.stop_speak_long_text = True
            except Exception:
                traceback.print_exc()

        t = Thread(target=self.handle_event_thread, args=(code,))
        t.start()
        return
