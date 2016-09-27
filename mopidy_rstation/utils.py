# encoding=utf8
import json
import os
import subprocess
from threading import Thread
import time
from mopidy_rstation.output import pyvona
import traceback


class Utils:
    lib_items = []
    curr_lib_item_id = 0
    curr_track_id = 0
    speak_on = True
    speak_time = None
    config = {}

    @staticmethod
    def save_config(config):
        for k, v in config.iteritems():
            Utils.config[k] = v

    @staticmethod
    def change_lang(language):
        Utils.config['language'] = language
        if language == 'en-US':
            Utils.speak_text('English')
        elif language == 'pl-PL':
            Utils.speak_text('Polski')

    @staticmethod
    def format_time_to_string(seconds_total):
        duration_text = str(seconds_total / 60) + ':'
        seconds = seconds_total % 60
        if seconds < 10:
            duration_text += '0' + str(seconds)
        else:
            duration_text += str(seconds)
        return duration_text

    @staticmethod
    def get_title_string(tl_track):
        name = u''
        try:
            if 'track' in tl_track:
                name = tl_track['track']['name']
            else:
                name = tl_track['name']
        except Exception:
            pass
        return name

    @staticmethod
    def get_album_string(tl_track):
        name = u''
        try:
            name = tl_track['track']['album']['name']
        except Exception:
            pass
        return name

    @staticmethod
    def get_artist_string(tl_track):
        name = u''
        try:
            if len(tl_track['track']['artists']) > 0:
                name = ""
                for artist in tl_track['track']['artists']:
                    name += artist['name'] + " "
        except Exception:
            pass
        return name

    @staticmethod
    def get_message(id, method, params=None):
        message = {}
        message['jsonrpc'] = '2.0'
        message['id'] = id
        message['method'] = method
        if params is not None:
            message['params'] = params
        return json.dumps(message)

    @staticmethod
    def convert_text(text):
        t = u''
        t = t + text
        # try:
        #     t = text.decode("utf8", "ignore")
        # except Exception as e:
        #     print('Error in convert_text ' + str(e))
        #     # t = 'Error ' + e.message
        #     traceback.print_exc()

        t = t.replace('_', ' ')
        t = t.replace('-', ' ')
        # remove the file extension
        t = os.path.splitext(t)[0]
        return t

    @staticmethod
    def speak_text(text, thread=True):
        t = Utils.convert_text(text)
        if thread:
            Utils.speak_time = time.time()
            t = Thread(target=Utils.speak_text_thread, args=(t,))
            t.start()
        else:
            # os.system(
            #     ' echo "' + t + '" | espeak -v ' +
            #     Utils.config['language'] + ' -a 160 > /dev/null 2>&1')
            v = pyvona.create_voice(Utils.config)
            v.speak(t, use_cache=False)

    @staticmethod
    def speak_text_thread(text):
            # wait a little
            time.sleep(0.6)
            # check if no next button was pressed
            if time.time() - Utils.speak_time > 0.6:
                # os.system('pkill espeak')
                # os.system(
                #     ' echo "' + text + '" | espeak -v ' +
                #     Utils.config['language'] + ' -a 160 > /dev/null 2>&1')
                v = pyvona.create_voice(Utils.config)
                v.speak(text, use_cache=False)
            else:
                pass

    @staticmethod
    def speak(code, *param, **key):
        if Utils.speak_on is False:
            return 0

        if ('val' in key):
            val = key['val']
            print(val)
            # if not isinstance(val, str) and not isinstance(val, unicode):
            #     val = str(val)
            val = Utils.convert_text(val)

        if code == 'PLAY':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Graj", False)
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Play", False)
        if code == 'PLAYING':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Gramy " + val)
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Now playing " + val)
        if code == 'PAUSE':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Pauza", False)
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Pause", False)
        if code == 'SPEAK_ON':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Podpowiedzi")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Hints on")
        if code == 'SPEAK_OFF':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Bez podpowiedzi")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Hints off")
        if code == 'VOL':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"głośność " + val)
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Volume " + val)
        if code == 'MUTE':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Wycisz")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Mute")
        if code == 'NEXT':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Następny", False)
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Next", False)
        if code == 'PREV':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Poprzedni", False)
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Previous", False)
        if code == 'LIBRARY':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Biblioteka")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"library")
        if code == 'PLAYER':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Odtwarzacz")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Player")
        if code == 'CHM':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Listy")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Play lists")
        if code == 'NUM0':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Numer 0")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Number 0")
        if code == 'FLM':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Fl minus")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Fl minus")
        if code == 'FLP':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Fl plus")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Fl plus")
        if code == 'lib_music':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Informacja")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Information")
        if code == 'LIST_ITEM':
                Utils.speak_text(val)
        if code == 'ENTER_DIR':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Wybieram " + val)
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Going to " + val)
        if code == 'PLAY_URI':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Włączam " + val)
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Playing " + val)
        if code == 'GO_UP_DIR':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Idz do góry")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Go up")
        if code == 'UP_DIR':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Do góry")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Up")
        if code == 'NO_TRACK':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Aktualnie nie jest odtwarzany żaden utwór")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Currently we do not play any song")
        if code == 'NO_PLAYLISTS':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Brak list odtwarzania")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"We do not have any playlist")
        if code == 'AUDIOBOOKS_DIR':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Audiobuki")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Audiobooks")
        if code == 'INFO_DIR':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Informacje")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Information")
        if code == 'MUSIC_DIR':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Muzyka")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Music")
        if code == 'PODCAST_DIR':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Podkasty")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Podcasts")
        if code == 'RADIO_DIR':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Radio")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Radio")
        if code == 'NO_LIBRARY':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Brak pozycji w bibliotece")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"There is nothing in the library")
        if code == 'LIB_SCREAN_INFO':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Jesteś w bibliotece, mamy tu " + val)
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"You are in library, we have here " + val)
        if code == 'PL_SCREAN_INFO':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Listy odtwarzania")
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Playlists")
        if code == 'TR_SCREAN_INFO':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"Lista utworów ma " + val + ' pozycji')
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"Tracks list has " + val + ' entries')
        if code == 'BRIGHTNESS':
            if Utils.config['language'] == 'pl-PL':
                Utils.speak_text(u"jasność " + val)
            elif Utils.config['language'] == 'en-US':
                Utils.speak_text(u"brightness " + val)

    @staticmethod
    def get_actual_brightness():
        ab = subprocess.check_output(
            'cat /sys/class/backlight/rpi_backlight/actual_brightness',
            shell=True)
        return ab

    @staticmethod
    def set_actual_brightness(ab):
        # Utils.speak('BRIGHTNESS', val=str(ab))
        os.system(
            'echo ' + str(ab) +
            ' > /sys/class/backlight/rpi_backlight/brightness')
        if ab == 0:
            # turn off the display
            os.system(
                'echo 1 > /sys/class/backlight/rpi_backlight/bl_power')
        else:
            # turn on the display
            os.system(
                'echo 0 > /sys/class/backlight/rpi_backlight/bl_power')
            os.system('echo -ne "\033[13]" > /dev/tty1')

    @staticmethod
    def backlight_up():
        try:
            ab = Utils.get_actual_brightness()
            ab = min(255, int(ab) + 30)
            ab = max(0, ab)
            Utils.set_actual_brightness(ab)
        except Exception as e:
            print(str(e))

    @staticmethod
    def backlight_down():
        try:
            ab = Utils.get_actual_brightness()
            ab = min(255, int(ab) - 30)
            ab = max(0, ab)
            Utils.set_actual_brightness(ab)
        except Exception as e:
            print(str(e))

    @staticmethod
    def aplay_thread(wav):
        cmd = "aplay /home/pi/mopidy-rstation/audio/"
        cmd += wav + ".wav > /dev/null 2>&1"
        os.system(cmd)

    @staticmethod
    def beep():
        t = Thread(target=Utils.aplay_thread, args=("alert",))
        t.start()

    @staticmethod
    def start_rec_wav():
        t = Thread(target=Utils.aplay_thread, args=("start_rec",))
        t.start()

    @staticmethod
    def stop_rec_wav():
        t = Thread(target=Utils.aplay_thread, args=("stop_rec",))
        t.start()
