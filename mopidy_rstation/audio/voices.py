# encoding=utf8
from ..utils import Utils
import os
import sys
from threading import Thread
import time
import pyvona

speak_time = None
voice = None
# to avoid the UnicodeDecodeError: 'ascii' codec can't decode byte
reload(sys)
sys.setdefaultencoding("utf-8")


def set_voice():
    global voice
    voice = pyvona.create_voice(Utils.config)
    print("set_voice")


def convert_text(text):
    t = u''
    t = t + text
    t = t.replace('_', ' ')
    t = t.replace('-', ' ')
    # remove the file extension
    t = os.path.splitext(t)[0]
    return t


def speak_text(text, thread=True):
    global speak_time
    global voice
    if voice is None:
        set_voice()
    t = convert_text(text)

    if thread:
        speak_time = time.time()
        t = Thread(target=speak_text_thread, args=(t,))
        t.start()
    else:
        voice.speak(t)


def speak_text_thread(text):
    global speak_time
    global voice
    if voice is None:
        set_voice()
    # wait a little
    time.sleep(0.4)
    # check if no next button was pressed
    if time.time() - speak_time > 0.4:
        voice.speak(text)
    else:
        pass


def speak(code, *param, **key):
    language = Utils.config['language']
    val = ''
    if ('val' in key):
        val = key['val']
        if isinstance(val, int):
            val = str(val)
        val = convert_text(val)
    if code == 'PROCESSING':
        if language == 'pl-PL':
            speak_text(u"Przetwarzam", False)
        elif language == 'en-US':
            speak_text(u"Processing", False)
    if code == 'PLAY':
        if language == 'pl-PL':
            speak_text(u"Graj", False)
        elif language == 'en-US':
            speak_text(u"Play", False)
    if code == 'PLAYING':
        if language == 'pl-PL':
            speak_text(u"Gramy " + val)
        elif language == 'en-US':
            speak_text(u"Now playing " + val)
    if code == 'PAUSE':
        if language == 'pl-PL':
            speak_text(u"Pauza", False)
        elif language == 'en-US':
            speak_text(u"Pause", False)
    if code == 'SPEAK_ON':
        if language == 'pl-PL':
            speak_text(u"Podpowiedzi")
        elif language == 'en-US':
            speak_text(u"Hints on")
    if code == 'SPEAK_OFF':
        if language == 'pl-PL':
            speak_text(u"Bez podpowiedzi")
        elif language == 'en-US':
            speak_text(u"Hints off")
    if code == 'VOL':
        if language == 'pl-PL':
            speak_text(u"Głośność " + val)
        elif language == 'en-US':
            speak_text(u"Volume " + val)
    if code == 'MUTE':
        if language == 'pl-PL':
            speak_text(u"Wycisz")
        elif language == 'en-US':
            speak_text(u"Mute")
    if code == 'NEXT':
        if language == 'pl-PL':
            speak_text(u"Następny", False)
        elif language == 'en-US':
            speak_text(u"Next", False)
    if code == 'PREV':
        if language == 'pl-PL':
            speak_text(u"Poprzedni", False)
        elif language == 'en-US':
            speak_text(u"Previous", False)
    if code == 'LIBRARY':
        if language == 'pl-PL':
            speak_text(u"Biblioteka")
        elif language == 'en-US':
            speak_text(u"library")
    if code == 'PLAYER':
        if language == 'pl-PL':
            speak_text(u"Odtwarzacz")
        elif language == 'en-US':
            speak_text(u"Player")
    if code == 'CHM':
        if language == 'pl-PL':
            speak_text(u"Listy")
        elif language == 'en-US':
            speak_text(u"Play lists")
    if code == 'NUM0':
        if language == 'pl-PL':
            speak_text(u"Numer 0")
        elif language == 'en-US':
            speak_text(u"Number 0")
    if code == 'FLM':
        if language == 'pl-PL':
            speak_text(u"Fl minus")
        elif language == 'en-US':
            speak_text(u"Fl minus")
    if code == 'FLP':
        if language == 'pl-PL':
            speak_text(u"Fl plus")
        elif language == 'en-US':
            speak_text(u"Fl plus")
    if code == 'lib_music':
        if language == 'pl-PL':
            speak_text(u"Informacja")
        elif language == 'en-US':
            speak_text(u"Information")
    if code == 'LIST_ITEM':
            speak_text(val)
    if code == 'ENTER_DIR':
        if language == 'pl-PL':
            speak_text(u"Wybieram " + val)
        elif language == 'en-US':
            speak_text(u"Going to " + val)
    if code == 'PLAY_URI':
        if language == 'pl-PL':
            speak_text(u"Włączam " + val)
        elif language == 'en-US':
            speak_text(u"Playing " + val)
    if code == 'UP_DIR':
        if language == 'pl-PL':
            speak_text(u"Do góry")
        elif language == 'en-US':
            speak_text(u"Go up")
    if code == 'NO_TRACK':
        if language == 'pl-PL':
            speak_text(u"Aktualnie nie jest odtwarzany żaden utwór")
        elif language == 'en-US':
            speak_text(u"Currently we do not play any song")
    if code == 'NO_PLAYLISTS':
        if language == 'pl-PL':
            speak_text(u"Brak list odtwarzania")
        elif language == 'en-US':
            speak_text(u"We do not have any playlist")
    if code == 'AUDIOBOOKS_DIR':
        if language == 'pl-PL':
            speak_text(u"Audiobuki")
        elif language == 'en-US':
            speak_text(u"Audiobooks")
    if code == 'INFO_DIR':
        if language == 'pl-PL':
            speak_text(u"Informacje")
        elif language == 'en-US':
            speak_text(u"Information")
    if code == 'MUSIC_DIR':
        if language == 'pl-PL':
            speak_text(u"Muzyka")
        elif language == 'en-US':
            speak_text(u"Music")
    if code == 'PODCAST_DIR':
        if language == 'pl-PL':
            speak_text(u"Podkasty")
        elif language == 'en-US':
            speak_text(u"Podcasts")
    if code == 'RADIO_DIR':
        if language == 'pl-PL':
            speak_text(u"Radio")
        elif language == 'en-US':
            speak_text(u"Radio")
    if code == 'NO_LIBRARY':
        if language == 'pl-PL':
            speak_text(u"Brak pozycji w bibliotece")
        elif language == 'en-US':
            speak_text(u"There is nothing in the library")
    if code == 'LIB_SCREAN_INFO':
        if language == 'pl-PL':
            speak_text(u"Jesteś w bibliotece, mamy tu " + val)
        elif language == 'en-US':
            speak_text(u"You are in library, we have here " + val)
    if code == 'PL_SCREAN_INFO':
        if language == 'pl-PL':
            speak_text(u"Listy odtwarzania")
        elif language == 'en-US':
            speak_text(u"Playlists")
    if code == 'TR_SCREAN_INFO':
        if language == 'pl-PL':
            speak_text(u"Lista utworów ma " + val + ' pozycji')
        elif language == 'en-US':
            speak_text(u"Tracks list has " + val + ' entries')
    if code == 'BRIGHTNESS':
        if language == 'pl-PL':
            speak_text(u"jasność " + val)
        elif language == 'en-US':
            speak_text(u"brightness " + val)
