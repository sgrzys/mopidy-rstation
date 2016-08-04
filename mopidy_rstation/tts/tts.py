# encoding=utf8
import os
from threading import Thread
import pykka
from mopidy import core
import logging

logger = logging.getLogger('mopidy_Rstation')


class TtsFrontend(pykka.ThreadingActor, core.CoreListener):

    def __init__(self, config, core):
        super(TtsFrontend, self).__init__()
        self.core = core
        self.config = config['rstation']
        # TODO add this to settings
        self.speak_on = False
        self.lang = 'pl'

    def on_start(self):
        try:
            logger.debug('TTS starting')
            # todo
            logger.debug('TTS started')
        except Exception as e:
            logger.warning('TTS has not started: ' + str(e))
            self.stop()

    def on_stop(self):
        logger.info('TTS stopped')

    def on_failure(self):
        logger.warning('TTS failing')

    def handleRemoteCommand(self, cmd):
        logger.debug('handleRemoteCommand in TTS ' + cmd)
        # self.speak_text(cmd)

    def handleRemoteTTS(self, text):
        logger.debug('handleRemoteTTS in TTS ' + text)
        self.speak_text(text)

    def convert_text(text):
        try:
            t = str(text).encode("utf8", "ignore")
        except Exception as e:
            print(str(e))
            t = 'Error ' + e.message

        t = t.replace('_', ' ')
        t = t.replace('-', ' ')
        # remove the file extension
        t = os.path.splitext(t)[0]
        return t

    def speak_text(self, text, thread=True):
        if thread:
            os.system('pkill espeak')
            t = Thread(target=self.speak_text_thread, args=(text,))
            t.start()
        else:
            os.system(
                ' echo "' + text + '" | espeak -v ' + self.lang + ' -a 200')

    def speak_text_thread(self, text):
            os.system(
                ' echo "' + text + '" | espeak -v ' + self.lang + ' -a 200')

    def speak(self, code, *param, **key):

        if self.speak_on is False:
            return 0

        if ('val' in key):
            val = self.convert_text(key['val'])

        if code == 'PLAY':
            if self.lang == 'pl':
                self.speak_text("Graj", False)
            elif self.lang == 'en':
                self.speak_text("Play", False)
        if code == 'PAUSE':
            if self.lang == 'pl':
                self.speak_text("Pauza", False)
            elif self.lang == 'en':
                self.speak_text("Pause", False)
        if code == 'SPEAK_ON':
            if self.lang == 'pl':
                self.speak_text("Podpowiedzi")
            elif self.lang == 'en':
                self.speak_text("Hints on")
        if code == 'SPEAK_OFF':
            if self.lang == 'pl':
                self.speak_text("Bez podpowiedzi")
            elif self.lang == 'en':
                self.speak_text("Hints off")
        if code == 'VOL':
            if self.lang == 'pl':
                self.speak_text("głośność " + val)
            elif self.lang == 'en':
                self.speak_text("Volume " + val)
        if code == 'MUTE':
            if self.lang == 'pl':
                self.speak_text("Wycisz")
            elif self.lang == 'en':
                self.speak_text("Mute")
        if code == 'NEXT':
            if self.lang == 'pl':
                self.speak_text("Następny", False)
            elif self.lang == 'en':
                self.speak_text("Next", False)
        if code == 'PREV':
            if self.lang == 'pl':
                self.speak_text("Poprzedni", False)
            elif self.lang == 'en':
                self.speak_text("Previous", False)
        if code == 'CHM':
            if self.lang == 'pl':
                self.speak_text("Biblioteka")
            elif self.lang == 'en':
                self.speak_text("library")
        if code == 'CH':
            if self.lang == 'pl':
                self.speak_text("Odtwarzacz")
            elif self.lang == 'en':
                self.speak_text("Player")
        if code == 'CHP':
            if self.lang == 'pl':
                self.speak_text("Listy")
            elif self.lang == 'en':
                self.speak_text("Play lists")
        if code == 'NUM0':
            if self.lang == 'pl':
                self.speak_text("Numer 0")
            elif self.lang == 'en':
                self.speak_text("Number 0")
        if code == 'FLM':
            if self.lang == 'pl':
                self.speak_text("Fl minus")
            elif self.lang == 'en':
                self.speak_text("Fl minus")
        if code == 'FLP':
            if self.lang == 'pl':
                self.speak_text("Fl plus")
            elif self.lang == 'en':
                self.speak_text("Fl plus")
        if code == 'NUM9':
            if self.lang == 'pl':
                self.speak_text("Informacja")
            elif self.lang == 'en':
                self.speak_text("Information")
        if code == 'LIST_ITEM':
                self.speak_text(val)
        if code == 'ENTER_DIR':
            if self.lang == 'pl':
                self.speak_text("Wybierz " + val)
            elif self.lang == 'en':
                self.speak_text("Go to " + val)
        if code == 'PLAY_URI':
            if self.lang == 'pl':
                self.speak_text("Graj " + val)
            elif self.lang == 'en':
                self.speak_text("Play " + val)
        if code == 'GO_UP_DIR':
            if self.lang == 'pl':
                self.speak_text("Idz do góry")
            elif self.lang == 'en':
                self.speak_text("Go up")
        if code == 'NO_TRACK':
            if self.lang == 'pl':
                self.speak_text("Aktualnie nie jest odtwarzany żaden utwór")
            elif self.lang == 'en':
                self.speak_text("Currently we do not play any song")
        if code == 'NO_PLAYLISTS':
            if self.lang == 'pl':
                self.speak_text("Brak list odtwarzania")
            elif self.lang == 'en':
                self.speak_text("We do not have any playlist")
        if code == 'AUDIOBOOKS_DIR':
            if self.lang == 'pl':
                self.speak_text("Audiobuki")
            elif self.lang == 'en':
                self.speak_text("Audiobooks")
        if code == 'INFO_DIR':
            if self.lang == 'pl':
                self.speak_text("Informacje")
            elif self.lang == 'en':
                self.speak_text("Information")
        if code == 'MUSIC_DIR':
            if self.lang == 'pl':
                self.speak_text("Muzyka")
            elif self.lang == 'en':
                self.speak_text("Music")
        if code == 'PODCAST_DIR':
            if self.lang == 'pl':
                self.speak_text("Podkasty")
            elif self.lang == 'en':
                self.speak_text("Podcasts")
        if code == 'RADIO_DIR':
            if self.lang == 'pl':
                self.speak_text("Radio")
            elif self.lang == 'en':
                self.speak_text("Radio")
        if code == 'NO_LIBRARY':
            if self.lang == 'pl':
                self.speak_text("Brak pozycji w bibliotece")
            elif self.lang == 'en':
                self.speak_text("There is nothing in the library")
        if code == 'LIB_SCREAN_INFO':
            if self.lang == 'pl':
                self.speak_text("Jesteś w bibliotece, mamy tu " + val)
            elif self.lang == 'en':
                self.speak_text("You are in library, we have here " + val)
        if code == 'PL_SCREAN_INFO':
            if self.lang == 'pl':
                self.speak_text("Listy odtwarzania")
            elif self.lang == 'en':
                self.speak_text("Playlists")
        if code == 'TR_SCREAN_INFO':
            if self.lang == 'pl':
                self.speak_text("Lista utworów ma " + val + ' pozycji')
            elif self.lang == 'en':
                self.speak_text("Tracks list has " + val + ' entries')
        if code == 'BRIGHTNESS':
            if self.lang == 'pl':
                self.speak_text("jasność " + val)
            elif self.lang == 'en':
                self.speak_text("brightness " + val)
