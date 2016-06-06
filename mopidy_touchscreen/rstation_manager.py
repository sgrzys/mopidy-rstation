import logging
from mopidy import core
import pykka
import tempfile
from rstation.irda import LircThread
from rstation.irda import CommandDispatcher


logger = logging.getLogger('mopidy_Rstation')

LIRC_PROG_NAME = "mopidyRstation"

logger = logging.getLogger(__name__)


class RstationFrontend(pykka.ThreadingActor, core.CoreListener):

    def __init__(self, config, core):
        super(RstationFrontend, self).__init__()
        self.core = core
        self.config = config['touchscreen']
        self.configFile = self.generateLircConfigFile(config['touchscreen'])
        logger.debug('lircrc file:{0}'.format(self.configFile))

        self.thread = LircThread(self.configFile)
        self.dispatcher = CommandDispatcher(
            self.core,
            self.config,
            self.thread.ButtonPressed)

        self.debug_irda_simulate = config['touchscreen']['debug_irda_simulate']
        if self.debug_irda_simulate:
            from rstation.irda_simulator import IrdaSimulator
            self.simulator = IrdaSimulator(self.dispatcher)
        # else:
        #     from .gpio_input_manager import GPIOManager
        #     self.gpio_manager = GPIOManager(self, config['ttsgpio'])

    def on_start(self):
        try:
            logger.debug('Rstation starting')
            self.thread.ButtonPressed.append(self.handleButtonPress)
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

    def handleButtonPress(self, cmd):
        pass
        # CoreListener.send("IRButtonPressed", button=cmd)

    def generateLircConfigFile(self, config):
        '''Returns file name of generate config file for pylirc'''
        f = tempfile.NamedTemporaryFile(delete=False)
        skeleton = 'begin\n   prog={2}\n   button={0}\n   config={1}\nend\n'
        for action in config:
            entry = skeleton.format(config[action], action, LIRC_PROG_NAME)
            f.write(entry)
        f.close()
        return f.name
