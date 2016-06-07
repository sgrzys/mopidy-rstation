import pylirc
import logging
import threading
import select

# from mopidy_touchscreen.screen_manager import ScreenManager
import pygame

from mopidy.core import PlaybackState
from .tts import TTS

logger = logging.getLogger('mopidy_Rstation')

LIRC_PROG_NAME = "mopidyRstation"


class Event(list):
    """Event subscription.

    A list of callable objects. Calling an instance of this will cause a
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
        self.tts = TTS(self, config)
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

        for i in range(10):
            self.registerHandler('num{0}'.format(i), self._playlistFunction(i))

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
        state = self.core.playback.get_state().get()
        if(state == PlaybackState.PAUSED):
            self.tts.speak("PLAY")
            self.core.playback.resume().get()
        elif (state == PlaybackState.PLAYING):
            self.tts.speak("PAUSE")
            self.core.playback.pause().get()
        elif (state == PlaybackState.STOPPED):
            self.tts.speak("PLAY")
            self.core.playback.play().get()

    def _nextHandler(self):
        self.tts.speak("NEXT")
        # self._screenEvent("NEXT")
        lambda: self.core.playback.next().get()

    def _prevHandler(self):
        self.tts.speak("PREV")
        # self._screenEvent("PREV")
        lambda: self.core.playback.prev().get()

    def _chmHandler(self):
        self.tts.speak("CHM")
        self._screenEvent("CHM")

    def _chHandler(self):
        self.tts.speak("CH")
        self._screenEvent("CH")

    def _chpHandler(self):
        self.tts.speak("CHP")
        self._screenEvent("CHP")

    def _flmHandler(self):
        self.tts.speak("FLM")
        self._screenEvent("FLM")

    def _flpHandler(self):
        self.tts.speak("FLP")
        self._screenEvent("FLP")

    def _eqHandler(self):
        if self.tts.speak_on is True:
            self.tts.speak("SPEAK_OFF")
            self.tts.speak_on = False
        else:
            self.tts.speak_on = True
            self.tts.speak("SPEAK_ON")

    def _muteHandler(self):
        self.tts.speak('MUTE')
        self.core.mixer.set_mute(not self.core.mixer.get_mute().get())

    def _volumeFunction(self, changeFct):
        def volumeChange():
            vol = self.core.mixer.get_volume().get()
            self.core.mixer.set_volume(min(max(0, changeFct(vol)), 100))
            self.tts.speak(
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
        if num == 1:
            return lambda: self._playPlaylist('m3u:muzyka.m3u')
        if num == 2:
            return lambda: self._playPlaylist('m3u:książki.m3u')
        if num == 3:
            return lambda: self._playPlaylist('m3u:podkasty.m3u')
        if num == 4:
            return lambda: self._playPlaylist('m3u:radia.m3u')
        if num == 5:
            return lambda: self._playPlaylist('m3u:wiadomości.m3u')
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
