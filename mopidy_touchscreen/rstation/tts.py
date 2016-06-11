# encoding=utf8
import os

speak_on = True
lang = 'pl'


def convert_text(text):
    try:
        t = text.encode("utf8", "ignore")
    except Exception as e:
        print(str(e))
        t = 'Error ' + e.message

    return t


def speak_text(text):
    # t = Thread(target=speak_text_thread, args=(text,))
    # t.start()
    os.system(' echo "' + text + '" | espeak -v ' + lang)


def speak(code, *param, **key):

    if speak_on is False:
        return 0

    if ('val' in key):
        val = convert_text(key['val'])

    if code == 'PLAY':
        if lang == 'pl':
            speak_text(u"Graj")
        elif lang == 'en':
            speak_text(u"Play")
    if code == 'PAUSE':
        if lang == 'pl':
            speak_text(u"Pauza")
        elif lang == 'en':
            speak_text(u"Pause")
    if code == 'SPEAK_ON':
        if lang == 'pl':
            speak_text(u"Podpowiedzi")
        elif lang == 'en':
            speak_text(u"Hints on")
    if code == 'SPEAK_OFF':
        if lang == 'pl':
            speak_text(u"Bez podpowiedzi")
        elif lang == 'en':
            speak_text(u"Hints off")
    if code == 'VOL':
        if lang == 'pl':
            speak_text(u"głośność " + val)
        elif lang == 'en':
            speak_text(u"Volume " + val)
    if code == 'MUTE':
        if lang == 'pl':
            speak_text(u"Wycisz")
        elif lang == 'en':
            speak_text(u"Mute")
    if code == 'NEXT':
        if lang == 'pl':
            speak_text(u"Następny")
        elif lang == 'en':
            speak_text(u"Next")
    if code == 'PREV':
        if lang == 'pl':
            speak_text(u"Poprzedni")
        elif lang == 'en':
            speak_text(u"Previous")
    if code == 'CHM':
        if lang == 'pl':
            speak_text(u"Biblioteka")
        elif lang == 'en':
            speak_text(u"library")
    if code == 'CH':
        if lang == 'pl':
            speak_text(u"Odtwarzacz")
        elif lang == 'en':
            speak_text(u"Player")
    if code == 'CHP':
        if lang == 'pl':
            speak_text(u"Listy")
        elif lang == 'en':
            speak_text(u"Play lists")
    if code == 'NUM0':
        if lang == 'pl':
            speak_text(u"Numer 0")
        elif lang == 'en':
            speak_text(u"Number 0")
    if code == 'FLM':
        if lang == 'pl':
            speak_text(u"Fl minus")
        elif lang == 'en':
            speak_text(u"Fl minus")
    if code == 'FLP':
        if lang == 'pl':
            speak_text(u"Fl plus")
        elif lang == 'en':
            speak_text(u"Fl plus")
    if code == 'NUM9':
        if lang == 'pl':
            speak_text(u"Informacja")
        elif lang == 'en':
            speak_text(u"Information")
    if code == 'LIST_ITEM':
            speak_text(val)
    if code == 'ENTER_DIR':
        if lang == 'pl':
            speak_text(u"Wybierz " + val)
        elif lang == 'en':
            speak_text("Go to " + val)
    if code == 'PLAY_URI':
        if lang == 'pl':
            speak_text(u"Graj " + val)
        elif lang == 'en':
            speak_text(u"Play " + val)
    if code == 'GO_UP_DIR':
        if lang == 'pl':
            speak_text(u"Idz do góry")
        elif lang == 'en':
            speak_text(u"Go up")
