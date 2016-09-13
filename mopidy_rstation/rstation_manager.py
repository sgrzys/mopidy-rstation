import logging
from mopidy import core
import pykka
from input.irda.irda import LircThread
from input.keyboard.key import KeyPad
from input.command_dispatcher import CommandDispatcher
from utils import Utils

logger = logging.getLogger('mopidy_Rstation')
LIRC_PROG_NAME = "mopidyRstation"
logger = logging.getLogger(__name__)


class RstationFrontend(pykka.ThreadingActor, core.CoreListener):

    def __init__(self, config, core):
        super(RstationFrontend, self).__init__()
        self.core = core
        self.config = config['rstation']
        self.debug_irda_simulate = config['rstation']['debug_irda_simulate']
        self.enable_irda = config['rstation']['enable_irda']
        self.enable_keypad = config['rstation']['enable_keypad']
        # IRDA
        if self.enable_irda:
            logger.debug('Irda Input is ON')
            self.irda_thread = LircThread(self.config)
            self.irda_dispatcher = CommandDispatcher(
                self.core,
                self.config,
                self.irda_thread.ButtonPressed)
            if self.debug_irda_simulate:
                logger.debug('Irda Simulator is ON')
                from input.irda.irda_simulator import IrdaSimulator
                self.simulator = IrdaSimulator(self.irda_dispatcher)
            else:
                logger.debug('Irda Simulator is OFF')
        else:
            logger.debug('Irda Input is OFF')

        # Keyboard
        if self.enable_keypad:
            logger.debug('KeyPad Input is ON')
            self.keypad = KeyPad(self.config)
            self.keypad_dispatcher = CommandDispatcher(
                self.core,
                self.config,
                self.keypad.ButtonPressed)
        else:
            logger.debug('KeyPad Input is OFF')

    def playback_state_changed(self, old_state, new_state):
        pass

    def track_playback_started(self, tl_track):
        if tl_track is not None:
            try:
                Utils.speak('PLAYING', val=tl_track.track.name)
            except Exception as e:
                print(str(e))

    def on_start(self):
        try:
            logger.debug('Rstation starting')
            self.irda_thread.start()
            logger.debug('Rstation started')
        except Exception as e:
            logger.warning('Rstation has not started: ' + str(e))
            self.stop()

    def on_stop(self):
        logger.info('Rstation stopped')
        if self.enable_irda:
            self.irda_thread.frontendActive = False
            self.irda_thread.join()

    def on_failure(self):
        logger.warning('Rstation failing')
        if self.enable_irda:
            self.irda_thread.frontendActive = False
            self.irda_thread.join()
