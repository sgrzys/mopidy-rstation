# This Python file uses the following encoding: utf-8
import pylirc
import logging
import threading
import select
from ..command_dispatcher import Event
import tempfile

logger = logging.getLogger('mopidy_Rstation')
LIRC_PROG_NAME = "mopidyRstation"
url = u'rstation:/home/pi/mopidy-rstation/media'


class LircThread(threading.Thread):
    def __init__(self, config):
        threading.Thread.__init__(self)
        self.name = 'Lirc worker thread'
        self.frontendActive = True
        self.configFile = self.generateLircConfigFile(config)
        logger.debug('lircrc file:{0}'.format(self.configFile))
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
        self.ButtonPressed(cmd)

    def generateLircConfigFile(self, config):
        '''Returns file name of generate config file for pylirc'''
        f = tempfile.NamedTemporaryFile(delete=False)
        skeleton = 'begin\n   prog={2}\n   button={0}\n   config={1}\nend\n'
        for action in config:
            entry = skeleton.format(config[action], action, LIRC_PROG_NAME)
            f.write(entry)
        f.close()
        return f.name
