import logging
from mopidy import core
import pykka
import tempfile
from irda.irda import LircThread
from irda.irda import CommandDispatcher

logger = logging.getLogger('mopidy_Rstation')
LIRC_PROG_NAME = "mopidyRstation"
logger = logging.getLogger(__name__)


class RstationFrontend(pykka.ThreadingActor, core.CoreListener):

    def __init__(self, config, core):
        super(RstationFrontend, self).__init__()
        self.core = core
        self.config = config['rstation']
        self.configFile = self.generateLircConfigFile(config['rstation'])
        logger.debug('lircrc file:{0}'.format(self.configFile))

        self.thread = LircThread(self.configFile)
        self.dispatcher = CommandDispatcher(
            self.core,
            self.config,
            self.thread.ButtonPressed)

        self.debug_irda_simulate = config['rstation']['debug_irda_simulate']
        if self.debug_irda_simulate:
            logger.debug('IrdaSimulator is ON')
            from irda.irda_simulator import IrdaSimulator
            self.simulator = IrdaSimulator(self.dispatcher)
        else:
            logger.debug('IrdaSimulator is OFF')

    def on_start(self):
        try:
            logger.debug('Rstation starting')
            self.thread.start()
            logger.debug('Rstation started')
        except Exception as e:
            logger.warning('Rstation has not started: ' + str(e))
            self.stop()

    def on_stop(self):
        logger.info('Rstation stopped')
        self.thread.frontendActive = False
        self.thread.join()

    def on_failure(self):
        logger.warning('Rstation failing')
        self.thread.frontendActive = False
        self.thread.join()

    def generateLircConfigFile(self, config):
        '''Returns file name of generate config file for pylirc'''
        f = tempfile.NamedTemporaryFile(delete=False)
        skeleton = 'begin\n   prog={2}\n   button={0}\n   config={1}\nend\n'
        for action in config:
            entry = skeleton.format(config[action], action, LIRC_PROG_NAME)
            f.write(entry)
        f.close()
        return f.name
