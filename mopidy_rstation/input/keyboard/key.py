# This Python file uses the following encoding: utf-8
from ..command_dispatcher import Event
import threading
import logging
import pyudev
import evdev
import select
import functools
import errno

logger = logging.getLogger('mopidy_Rstation')
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='input')
monitor.start()


class KeyPad(threading.Thread):
    def __init__(self, config):
        super(KeyPad, self).__init__()
        self.name = 'KeyPad worker thread'
        self.frontendActive = True
        self.config = config
        self.ButtonPressed = Event()
        self.devices = {}
        self._stop = threading.Event()

    def checkIfDevIsKeyboard(self, d):
        d.capabilities()
        return "keyboard" in d.name.lower() or "microsoft" in d.name.lower()

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
        self._stop.set()

    def startKeyPad(self):
        self.frontendActive = True
        for d in map(evdev.InputDevice, evdev.list_devices()):
            if self.checkIfDevIsKeyboard(d):
                print('We have keyboard device ' + str(d))
                self.devices[d.fn] = d

        self.devices['monitor'] = monitor

        while self.frontendActive:
            rs, _, _ = select.select(self.devices.values(), [], [])
            # Unconditionally ping monitor; if this is spurious this
            # will no-op because we pass a zero timeout.  Note that
            # it takes some time for udev events to get to us.
            for udev in iter(functools.partial(monitor.poll, 0), None):
                if not udev.device_node:
                    break
                if udev.action == 'add':
                    if udev.device_node not in self.devices:
                        print("Device added: %s" % udev)
                        try:
                            self.devices[udev.device_node] = evdev.InputDevice(
                                udev.device_node)
                        except IOError as e:
                            # udev reports MORE devices than are accessible
                            # evdev; a simple way to check is see if devinfo
                            # ioctl fails
                            if e.errno != errno.ENOTTY:
                                    raise
                            pass
                elif udev.action == 'remove':
                    # NB: This code path isn't exercised very frequently,
                    # because select() will trigger a read immediately when fil
                    # descriptor goes away, whereas the udev event takes some
                    # time to propagate to us.
                    if udev.device_node in self.devices:
                        print(
                            "Device removed (udev): %s" %
                            self.devices[udev.device_node])
                        del self.devices[udev.device_node]
            for r in rs:
                # You can't read from a monitor
                if r.fileno() == monitor.fileno():
                    continue
                if r.fn not in self.devices:
                    continue
                # Select will immediately return an fd for read if it will
                # ENODEV.  So be sure to handle that.
                try:
                    for event in r.read():
                        if event.type == evdev.ecodes.EV_KEY & \
                           event.value == 1:
                            self.handle_event(evdev.ecodes.KEY[event.code])
                except IOError as e:
                    if e.errno != errno.ENODEV:
                        raise
                    print("Device removed: %s" % r)
                    del self.devices[r.fn]

        # for device in devices:
        #     if "Microsoft" in device.name and self.dev is None:
        #         print(device.fn, device.name, device.phys)
        #         self.dev = InputDevice(device.fn)
        #         self.dev.grab()

        # devices = [InputDevice(fn) for fn in list_devices()]
        # for device in devices:
        #     print(device.fn, device.name, device.phys)
        # self.dev = InputDevice('/dev/input/event4')
        # self.dev.capabilities()
        # self.dev.capabilities(verbose=True)

        # while self.frontendActive:
        #     for event in self.dev.read_loop():
        #         if event.type == ecodes.EV_KEY & event.value == 1:
        #             # event.value == 1 key down
        #             # event.value == 0 key up
        #             # event.value == 2 key hold
        #             self.handle_event(ecodes.KEY[event.code])

    def handle_event(self, code):
        logger.debug('KeyPad -> handle_event -> ' + code)
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
