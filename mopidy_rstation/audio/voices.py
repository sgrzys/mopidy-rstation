# encoding=utf8
from mopidy_rstation.config.settings import Config
import os
import sys
from threading import Thread
import time
import i18n
# import sounds

speak_time = None
voice = None
stop_speak_long_text = False

# to avoid the UnicodeDecodeError: 'ascii' codec can't decode byte
reload(sys)
sys.setdefaultencoding("utf-8")


def set_voice():
    global voice
    import pyvona
    voice = pyvona.create_voice()


def convert_text(text, remove_file_extension=False):
    t = u''
    t = t + text
    t = t.replace('_', ' ')
    t = t.replace('-', ' ')
    if remove_file_extension:
        # remove the file extension
        t = os.path.splitext(t)[0]
    return t


def tokenizer(text):
    result = text
    result = result.strip()
    result = result.split('.')
    return result


def speak_long_text(text):
    global speak_time
    global voice
    global stop_speak_long_text
    if voice is None:
        set_voice()
    # IVONA limit is 8192
    # if sounds.channel.get_busy():
    # text = text[0:8192]
    parts = tokenizer(text)
    stop_speak_long_text = False
    for t in parts:
        if stop_speak_long_text:
            break
        voice.speak(t)
    # t = Thread(
    #     target=voice.speak,
    #     kwargs={
    #         'text_to_speak': text,
    #         'use_cache': False,
    #         'async': True})
    # t.start()


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
    lang = Config.get_current_lang(short=True)
    i18n.config.set(
        'load_path', ['/home/pi/mopidy-rstation/mopidy_rstation/audio/i18n'])
    i18n.config.set('locale', lang)
    i18n.config.set("encoding", "utf-8")
    val = ''
    if ('val' in key):
        val = key['val']
        if isinstance(val, int):
            val = str(val)
        val = convert_text(val)
    speak_text(i18n.t('voice.' + code) + ' ' + val)
