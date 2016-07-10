# encoding=utf8
import os

from threading import Thread

# TODO add this to settings
speak_on = False
lang = 'pl'


def convert_text(text):
    try:
        t = text.encode("utf8", "ignore")
    except Exception as e:
        print(str(e))
        t = 'Error ' + e.message

    t = t.replace('_', ' ')
    t = t.replace('-', ' ')
    # remove the file extension
    t = os.path.splitext(t)[0]
    return t


def speak_text(text, thread=True):
    if thread:
        os.system('pkill espeak')
        t = Thread(target=speak_text_thread, args=(text,))
        t.start()
    else:
        os.system(' echo "' + text + '" | espeak -v ' + lang + ' -a 200')


def speak_text_thread(text):

        os.system(' echo "' + text + '" | espeak -v ' + lang + ' -a 200')


def speak(code, *param, **key):

    if speak_on is False:
        return 0

    if ('val' in key):
        val = convert_text(key['val'])

    if code == 'PLAY':
        if lang == 'pl':
            speak_text("Graj", False)
        elif lang == 'en':
            speak_text("Play", False)
    if code == 'PAUSE':
        if lang == 'pl':
            speak_text("Pauza", False)
        elif lang == 'en':
            speak_text("Pause", False)
    if code == 'SPEAK_ON':
        if lang == 'pl':
            speak_text("Podpowiedzi")
        elif lang == 'en':
            speak_text("Hints on")
    if code == 'SPEAK_OFF':
        if lang == 'pl':
            speak_text("Bez podpowiedzi")
        elif lang == 'en':
            speak_text("Hints off")
    if code == 'VOL':
        if lang == 'pl':
            speak_text("głośność " + val)
        elif lang == 'en':
            speak_text("Volume " + val)
    if code == 'MUTE':
        if lang == 'pl':
            speak_text("Wycisz")
        elif lang == 'en':
            speak_text("Mute")
    if code == 'NEXT':
        if lang == 'pl':
            speak_text("Następny", False)
        elif lang == 'en':
            speak_text("Next", False)
    if code == 'PREV':
        if lang == 'pl':
            speak_text("Poprzedni", False)
        elif lang == 'en':
            speak_text("Previous", False)
    if code == 'CHM':
        if lang == 'pl':
            speak_text("Biblioteka")
        elif lang == 'en':
            speak_text("library")
    if code == 'CH':
        if lang == 'pl':
            speak_text("Odtwarzacz")
        elif lang == 'en':
            speak_text("Player")
    if code == 'CHP':
        if lang == 'pl':
            speak_text("Listy")
        elif lang == 'en':
            speak_text("Play lists")
    if code == 'NUM0':
        if lang == 'pl':
            speak_text("Numer 0")
        elif lang == 'en':
            speak_text("Number 0")
    if code == 'FLM':
        if lang == 'pl':
            speak_text("Fl minus")
        elif lang == 'en':
            speak_text("Fl minus")
    if code == 'FLP':
        if lang == 'pl':
            speak_text("Fl plus")
        elif lang == 'en':
            speak_text("Fl plus")
    if code == 'NUM9':
        if lang == 'pl':
            speak_text("Informacja")
        elif lang == 'en':
            speak_text("Information")
    if code == 'LIST_ITEM':
            speak_text(val)
    if code == 'ENTER_DIR':
        if lang == 'pl':
            speak_text("Wybierz " + val)
        elif lang == 'en':
            speak_text("Go to " + val)
    if code == 'PLAY_URI':
        if lang == 'pl':
            speak_text("Graj " + val)
        elif lang == 'en':
            speak_text("Play " + val)
    if code == 'GO_UP_DIR':
        if lang == 'pl':
            speak_text("Idz do góry")
        elif lang == 'en':
            speak_text("Go up")
    if code == 'NO_TRACK':
        if lang == 'pl':
            speak_text("Aktualnie nie jest odtwarzany żaden utwór")
        elif lang == 'en':
            speak_text("Currently we do not play any song")
    if code == 'NO_PLAYLISTS':
        if lang == 'pl':
            speak_text("Brak list odtwarzania")
        elif lang == 'en':
            speak_text("We do not have any playlist")
    if code == 'AUDIOBOOKS_DIR':
        if lang == 'pl':
            speak_text("Audiobuki")
        elif lang == 'en':
            speak_text("Audiobooks")
    if code == 'INFO_DIR':
        if lang == 'pl':
            speak_text("Informacje")
        elif lang == 'en':
            speak_text("Information")
    if code == 'MUSIC_DIR':
        if lang == 'pl':
            speak_text("Muzyka")
        elif lang == 'en':
            speak_text("Music")
    if code == 'PODCAST_DIR':
        if lang == 'pl':
            speak_text("Podkasty")
        elif lang == 'en':
            speak_text("Podcasts")
    if code == 'RADIO_DIR':
        if lang == 'pl':
            speak_text("Radio")
        elif lang == 'en':
            speak_text("Radio")
    if code == 'NO_LIBRARY':
        if lang == 'pl':
            speak_text("Brak pozycji w bibliotece")
        elif lang == 'en':
            speak_text("There is nothing in the library")
    if code == 'LIB_SCREAN_INFO':
        if lang == 'pl':
            speak_text("Jesteś w bibliotece, mamy tu " + val)
        elif lang == 'en':
            speak_text("You are in library, we have here " + val)
    if code == 'PL_SCREAN_INFO':
        if lang == 'pl':
            speak_text("Listy odtwarzania")
        elif lang == 'en':
            speak_text("Playlists")
    if code == 'TR_SCREAN_INFO':
        if lang == 'pl':
            speak_text("Lista utworów ma " + val + ' pozycji')
        elif lang == 'en':
            speak_text("Tracks list has " + val + ' entries')
    if code == 'BRIGHTNESS':
        if lang == 'pl':
            speak_text("jasność " + val)
        elif lang == 'en':
            speak_text("brightness " + val)
