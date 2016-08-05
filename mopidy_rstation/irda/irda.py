# This Python file uses the following encoding: utf-8
import pylirc
import logging
import threading
import select
from mopidy.core import CoreListener

logger = logging.getLogger('mopidy_Rstation')

LIRC_PROG_NAME = "mopidyRstation"


class Event(list):
    """Event subscription.

    A list of callable objects. Calling an
    i_playPlaylistnstance of this will cause a
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
        buttonPressEvent.append(self.handleCommand)

    def handleCommand(self, cmd):
        logger.debug("Start handleRemoteCommand: {0} ".format(cmd))
        CoreListener.send("handleRemoteCommand", cmd=cmd)
        logger.debug("Stop handleRemoteCommand: {0} ".format(cmd))

    def registerHandler(self, cmd, handler):
        self._handlers[cmd] = handler


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
        logger.error('handleLircCode')
        for code in s:
            self.handleCommand(code['config'])

    def handleCommand(self, cmd):
        self.ButtonPressed(cmd)
