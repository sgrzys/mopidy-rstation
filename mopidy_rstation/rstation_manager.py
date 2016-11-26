import logging
from mopidy import core
import pykka
from input.irda.irda import LircThread
from input.keyboard.key import KeyPad
from input.command_dispatcher import CommandDispatcher
from utils import Utils
from audio import sounds

logger = logging.getLogger('mopidy_Rstation')
LIRC_PROG_NAME = "mopidyRstation"
logger = logging.getLogger(__name__)


class RstationFrontend(pykka.ThreadingActor, core.CoreListener):

    def __init__(self, config, core):
        super(RstationFrontend, self).__init__()
        self.core = core
        self.config = config['rstation']
        Utils.save_config(self.config, self.core)
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
            self.keypad_thread = KeyPad(self.config)
            self.keypad_dispatcher = CommandDispatcher(
                self.core,
                self.config,
                self.keypad_thread.ButtonPressed)
        else:
            logger.debug('KeyPad Input is OFF')

    def playback_state_changed(self, old_state, new_state):
        pass

    def track_playback_started(self, tl_track):
        if tl_track is not None:
            # set current track id
            Utils.curr_track_id = tl_track.tlid - 1
            try:
                Utils.speak('PLAYING', val=tl_track.track.name)
            except Exception as e:
                print(str(e))

    def on_start(self):
        try:
            logger.debug('Rstation starting')
            if self.enable_irda:
                logger.debug('irda thread starting')
                self.irda_thread.start()
            if self.enable_keypad:
                logger.debug('keypad thread starting')
                self.keypad_thread.start()
            logger.debug('Rstation started')
            sounds.play(sounds.C_SOUND_START_UP)

        except Exception as e:
            logger.warning('Rstation has not started: ' + str(e))
            self.stop()

    def on_stop(self):
        logger.info('Rstation stopping')
        if self.enable_irda:
            logger.debug('irda thread stopping')
            self.irda_thread.frontendActive = False
            self.irda_thread.join()
            logger.debug('irda thread stopped')
        if self.enable_keypad:
            logger.debug('keypad thread stopping')
            self.keypad_thread.stop()
            logger.debug('keypad thread stopping 1')
            # self.keypad_thread.frontendActive = False
            # self.keypad_thread.join()
            logger.debug('keypad thread stopped')
        logger.info('Rstation stopped')

    def on_failure(self):
        logger.warning('Rstation failing')
        if self.enable_irda:
            self.irda_thread.frontendActive = False
            self.irda_thread.join()
        if self.enable_keypad:
            self.keypad_thread.stop()
            self.keypad_thread.join()
