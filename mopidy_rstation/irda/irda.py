# This Python file uses the following encoding: utf-8
import pylirc
import logging
import threading
import select
import pygame
from ..tts import tts

logger = logging.getLogger('mopidy_Rstation')

LIRC_PROG_NAME = "mopidyRstation"


class Event(list):
    """Event subscription.

    A list of callable objects. Calling an i_playPlaylistnstance of this will cause a
    call to each item in the list in ascending order by index."""
    def __call__(self, *args, **kwargs):
        for f in self:
            f(*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % list.__repr__(self)


class CommandDispatcher(object):
    def __init__(self, core, config, buttonPressEvent):
        self.core = core
        self.config = config
        self._handlers = {}

        self.registerHandler('ch_minus', self._chmHandler)
        self.registerHandler('ch', self._chHandler)
        self.registerHandler('ch_plus', self._chpHandler)
        self.registerHandler('prev', self._prevHandler)
        self.registerHandler('next', self._nextHandler)
        self.registerHandler('play_pause', self._playpauseHandler)
        self.registerHandler('vol_down',
                             self._volumeFunction(lambda vol: vol - 5))
        self.registerHandler('vol_up',
                             self._volumeFunction(lambda vol: vol + 5))
        self.registerHandler('eq', self._eqHandler)
        self.registerHandler('fl_minus', self._flmHandler)
        self.registerHandler('fl_plus', self._flpHandler)

        # 0 1 2 and 3 buttons are connected to playlists
        for i in range(3):
            self.registerHandler('num{0}'.format(i), self._playlistFunction(i))
        self.registerHandler('num4', self._num4Handler)
        self.registerHandler('num5', self._num5Handler)
        self.registerHandler('num6', self._num6Handler)
        self.registerHandler('num7', self._num7Handler)
        self.registerHandler('num8', self._num8Handler)
        self.registerHandler('num9', self._num9Handler)
        self.registerHandler('mute', self._muteHandler)
        self.registerHandler('stop', lambda: self.core.playback.stop().get())

        buttonPressEvent.append(self.handleCommand)

    def handleCommand(self, cmd):

        if cmd in self._handlers:
            logger.debug("Command {0} was handled".format(cmd))
            self._handlers[cmd]()
        else:
            logger.debug("Command {0} was not handled".format(cmd))

    def registerHandler(self, cmd, handler):
        self._handlers[cmd] = handler

    def _playpauseHandler(self):
        # state = self.core.playback.get_state().get()
        # if(state == PlaybackState.PAUSED):
        #     tts.speak("PLAY")
        #     # self.core.playback.resume().get()
        # elif (state == PlaybackState.PLAYING):
        #     tts.speak("PAUSE")
        #     # self.core.playback.pause().get()
        # elif (state == PlaybackState.STOPPED):
        #     tts.speak("PLAY")
        #     # self.core.playback.play().get()
        # self._screenEvent("PLAY_PAUSE")
        #
        # we are going to simulate the return key up and down
        dict = {}
        type = pygame.KEYDOWN
        dict['unicode'] = None
        dict['key'] = pygame.K_RETURN
        event = pygame.event.Event(type, dict)
        pygame.event.post(event)
        # and up
        type = pygame.KEYUP
        event = pygame.event.Event(type, dict)
        pygame.event.post(event)

    def _nextHandler(self):
        tts.speak("NEXT")
        # self._screenEvent("NEXT")
        # lambda: self.core.playback.next().get()
        dict = {}
        type = pygame.KEYDOWN
        dict['unicode'] = None
        dict['key'] = pygame.K_DOWN
        event = pygame.event.Event(type, dict)
        pygame.event.post(event)
        # and up
        type = pygame.KEYUP
        event = pygame.event.Event(type, dict)
        pygame.event.post(event)

    def _prevHandler(self):
        tts.speak("PREV")
        # self._screenEvent("PREV")
        # lambda: self.core.playback.prev().get()
        dict = {}
        type = pygame.KEYDOWN
        dict['unicode'] = None
        dict['key'] = pygame.K_UP
        event = pygame.event.Event(type, dict)
        pygame.event.post(event)
        # and up
        type = pygame.KEYUP
        event = pygame.event.Event(type, dict)
        pygame.event.post(event)

    def _chmHandler(self):
        tts.speak("CHM")
        self._screenEvent("CHM")

    def _chHandler(self):
        tts.speak("CH")
        self._screenEvent("CH")

    def _chpHandler(self):
        tts.speak("CHP")
        self._screenEvent("CHP")

    def _num4Handler(self):
        tts.speak("NUM4")
        self._screenEvent("NUM4")

    def _num5Handler(self):
        tts.speak("NUM5")
        self._screenEvent("NUM5")

    def _num6Handler(self):
        tts.speak("NUM6")
        self._screenEvent("NUM6")

    def _num7Handler(self):
        tts.speak("NUM7")
        self._screenEvent("NUM7")

    def _num8Handler(self):
        tts.speak("NUM8")
        self._screenEvent("NUM8")

    def _num9Handler(self):
        tts.speak("NUM9")
        self._screenEvent("NUM9")

    def _flmHandler(self):
        tts.speak("FLM")
        self._screenEvent("FLM")

    def _flpHandler(self):
        tts.speak("FLP")
        self._screenEvent("FLP")

    def _eqHandler(self):
        if tts.speak_on is True:
            if tts.lang == 'en':
                tts.lang = 'pl'
                tts.speak('SPEAK_ON')
            elif tts.lang == 'pl':
                tts.speak("SPEAK_OFF")
                tts.speak_on = False
        else:
            tts.speak_on = True
            tts.lang = 'en'
            tts.speak("SPEAK_ON")

    def _muteHandler(self):
        tts.speak('MUTE')
        self.core.mixer.set_mute(not self.core.mixer.get_mute().get())

    def _volumeFunction(self, changeFct):
        def volumeChange():
            vol = self.core.mixer.get_volume().get()
            self.core.mixer.set_volume(min(max(0, changeFct(vol)), 100))
            tts.speak(
                'VOL', val=str(min(max(0, changeFct(vol)), 100)))
        return volumeChange

    def _playPlaylist(self, uri):
        refs = self.core.playlists.get_items(uri).get()
        if not refs:
            logger.warn("Playlist '%s' does not exist", uri)
            return
        self.core.tracklist.clear()
        uris = map(lambda ref: ref.uri, refs)
        self.core.tracklist.add(uris=uris)
        self.core.tracklist.set_consume(False)
        self.core.tracklist.set_repeat(True)
        self.core.playback.play()

    def _playlistFunction(self, num):
        return lambda: self._playPlaylist(
            self.config['playlist_uri_template'].format(num)
        )

    def _screenEvent(self, key):
        dict = {}
        type = pygame.USEREVENT
        dict['key'] = key
        event = pygame.event.Event(type, dict)
        pygame.event.post(event)


class LircThread(threading.Thread):
    def __init__(self, configFile):
        threading.Thread.__init__(self)
        self.name = 'Lirc worker thread'
        self.configFile = configFile
        self.frontendActive = True
        self.ButtonPressed = Event()

    def run(self):
        try:
            self.run_inside_try()
        except Exception as e:
            logger.warning('Rstation has problems starting pylirc: ' + str(e))

    def run_inside_try(self):
        self.startPyLirc()

    def startPyLirc(self):
        logger.debug('Rstation start pylirc')
        lircHandle = pylirc.init(LIRC_PROG_NAME, self.configFile, 0)
        if(lircHandle != 0):
            while(self.frontendActive):
                self.consumePylirc(lircHandle)
            pylirc.exit()

    def consumePylirc(self, lircHandle):
        try:
            if(select.select([lircHandle], [], [], 1) == ([], [], [])):
                pass
            else:
                s = pylirc.nextcode(1)
                self.handleNextCode(s)
        except Exception as e:
            logger.warning('Exception during handling a command: ' + str(e))

    def handleNextCode(self, s):
        if s:
            self.handleLircCode(s)

    def handleLircCode(self, s):
        for code in s:
            self.handleCommand(code['config'])

    def handleCommand(self, cmd):
        logger.debug('Command: {0}'.format(cmd))
        self.ButtonPressed(cmd)
