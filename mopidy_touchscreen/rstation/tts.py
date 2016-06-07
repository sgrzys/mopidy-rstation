import os
from threading import Thread

music_level = 30


class TTS():

    def __init__(self, frontend, config):
        self.frontend = frontend
        self.speak_on = True

    def speak_text(self, text, language='pl'):
        # t = Thread(target=self.speak_text_thread, args=(text,))
        # t.start()
        os.system(' echo "' + text + '" | espeak -v' + language)

    def speak_text_thread(self, text):
        os.system(' echo "' + text + '" | espeak -v pl')

    def speak(self, code, *param, **key):

        if self.speak_on is False:
            return 0

        if ('val' in key):
            val = key['val']

        if code == 'PLAY':
            self.speak_text("Graj")
        if code == 'PAUSE':
            self.speak_text("Pauza")
        if code == 'SPEAK_ON':
            self.speak_text("Podpowiedzi")
        if code == 'SPEAK_OFF':
            self.speak_text("Bez podpowiedzi")
        if code == 'VOL':
            self.speak_text("głośność " + val)
        if code == 'MUTE':
            self.speak_text("Wycisz")
        if code == 'NEXT':
            self.speak_text("Następny")
        if code == 'PREV':
            self.speak_text("Poprzedni")
        if code == 'CHM':
            self.speak_text("Biblioteka")
        if code == 'CH':
            self.speak_text("Odtwarzacz")
        if code == 'CHP':
            self.speak_text("Listy")
        if code == 'NUM0':
            self.speak_text("Numer 0")
        if code == 'FLM':
            self.speak_text("Fl minus")
        if code == 'FLP':
            self.speak_text("Fl plus")
        if code == 'NUM9':
            self.speak_text("Informacja")
