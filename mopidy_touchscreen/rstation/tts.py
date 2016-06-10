import os
speak_on = True
lang = 'pl'


def speak_text(text):
    # t = Thread(target=speak_text_thread, args=(text,))
    # t.start()
    os.system(' echo "' + text + '" | espeak -v ' + lang)


def speak(code, *param, **key):

    if speak_on is False:
        return 0

    if ('val' in key):
        val = key['val']

    if code == 'PLAY':
        if lang == 'pl':
            speak_text("Graj")
        elif lang == 'en':
            speak_text("Play")
    if code == 'PAUSE':
        if lang == 'pl':
            speak_text("Pauza")
        elif lang == 'en':
            speak_text("Pause")
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
            speak_text("Następny")
        elif lang == 'en':
            speak_text("Next")
    if code == 'PREV':
        if lang == 'pl':
            speak_text("Poprzedni")
        elif lang == 'en':
            speak_text("Previous")
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
        if lang == 'pl':
            speak_text(val)
        elif lang == 'en':
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
