import os
import socket

from .on_off_configuration import OnOffConfiguration
from .playlist_menu import PlaylistMenu


class MainMenu():
    def __init__(self, frontend):
        self.current = 0
        self.fronted = frontend
        self.main_menu = False
        self.elements = [PlaylistMenu(frontend), 'zamknij program']
        self.elements.append(OnOffConfiguration('odtwarzaj losowo'))
        self.elements.append('wyłącz radio')
        self.elements.append('urucho ponownie')
        self.elements.append('sprawdz adres IP')

    def reset(self):
        self.current = 0
        self.say_current_element()
        self.main_menu = True

    def input(self, input_event):
        if self.main_menu:
            if input_event['key'] == 'next':
                self.change_current(1)
            elif input_event['key'] == 'previous':
                self.change_current(-1)
            elif input_event['key'] == 'main':
                if isinstance(self.elements[self.current], str):
                    self.item_selected(self.elements[self.current])
                else:
                    self.main_menu = False
                    self.elements[self.current].reset()
        else:
            self.elements[self.current].input(input_event)

    def item_selected(self, item):
        if item == 'zamknij program':
            os.system("pkill mopidy")
        elif item == 'wyłącz radio':
            os.system("shutdown now -h")
        elif item == 'urucho ponownie':
            os.system("shutdown -r now")
        elif item == 'sprawdz adres IP':
            self.check_ip()

    def change_current(self, move):
        self.current += move
        if self.current < 0:
            self.current = len(self.elements) - 1
        elif self.current >= len(self.elements):
            self.current = 0
        self.say_current_element()

    def say_current_element(self):
        self.fronted.tts.speak_text(str(self.elements[self.current]))

    def repeat(self):
        if self.main_menu:
            self.say_current_element()
        else:
            self.elements[self.current].repeat()

    def check_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            self.fronted.tts.speak_text("Twoje IP to: " + ip)
        except socket.error:
            s.close()
            self.fronted.tts.speak_text("Brak połączenia internetowego")
