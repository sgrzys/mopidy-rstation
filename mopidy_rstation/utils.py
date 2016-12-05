# encoding=utf8
import json
import os
import subprocess
from threading import Thread
import time
from mopidy_rstation.audio import pyvona
from ConfigParser import ConfigParser
import locale
import sys
# to avoid the UnicodeDecodeError: 'ascii' codec can't decode byte
reload(sys)
sys.setdefaultencoding("utf-8")


class Utils:
    lib_items = []
    curr_lib_item_id = 0
    curr_track_id = 0
    core = None
    config = {}

    @staticmethod
    def save_config(config, core):
        Utils.core = core
        for k, v in config.iteritems():
            Utils.config[k] = v

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
    def get_actual_brightness():
        ab = subprocess.check_output(
            'cat /sys/class/backlight/rpi_backlight/actual_brightness',
            shell=True)
        return ab

    @staticmethod
    def set_actual_brightness(ab):
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
    def set_volume(volume):
        from mopidy_rstation.audio import voices
        voices.speak('VOL', val=volume)
        Utils.core.playback.volume = volume

    @staticmethod
    def get_config():
        conf = ConfigParser()
        conf.read('/etc/mopidy/mopidy.conf')
        the_dict = {}
        for section in conf.sections():
            the_dict[section] = {}
            for key, val in conf.items(section):
                the_dict[section][key] = val
        return the_dict

    @staticmethod
    def search_wikipedia(query):
        from mopidy_rstation.wikipedia import search
        from mopidy_rstation.audio import voices
        if Utils.config['language'] == 'pl-PL':
            voices.speak_text(u'Pytamy wikipedie ')
            lang = 'pl'
        else:
            voices.speak_text(u'According to Wikipedia ')
            lang = 'en'
        try:
            ret = u'' + search.do(query, lang)
        except Exception:
            voices.speak_text('Błąd podczas pytania Wikipedii o ' + query)
            return

        v = pyvona.create_voice(Utils.config)
        ret = ret.replace('=', '')
        ret = ret[0:8192]
        t = Thread(
            target=v.speak,
            kwargs={
                'text_to_speak': ret,
                'use_cache': False,
                'async': True})
        t.start()

    @staticmethod
    def forecast_weather(location=None):
        def parse_text(text):
            text = u' ' + text
            text = text.replace("Min. temp.", u"Minimalna temperatura")
            text = text.replace("Maks. temp.", u"Maksymalna temperatura")
            text = text.replace("pd.pd.-wsch.", u"południowo-wschodni")
            text = text.replace("pd.-wsch.", u"południowo-wschodni")
            text = text.replace("pd.pd.-zach.", u"południowo-zachodni")
            text = text.replace("pd.-zach.", u"południowo-zachodni")
            text = text.replace("pn.-zach.", u"północno-zachodni")
            text = text.replace("pn.-wsch.", u"północno-wschodni")
            text = text.replace("pn.", u"północny")
            text = text.replace("pd.", u"południowy")
            text = text.replace("zach.", u"zachodni")
            text = text.replace("wsch.", u"wschodni")
            text = text.replace("op.", u"opady")
            text = text.replace("100%", u"99%")
            return text

        # to test from cmd
        # conf = Utils.get_config()
        # Utils.config = conf['rstation']
        # language = 'en-US'
        from mopidy_rstation.weather import forecast
        from mopidy_rstation.audio import voices
        if location is not None:
            from geopy.geocoders import Nominatim
            geolocator = Nominatim()
            location = geolocator.geocode(location)
            Utils.config['location_gps'] = str(location.latitude) + \
                ',' + str(location.longitude)

        weather = forecast.ForecastData(Utils.config)
        weather.verbose = True

        if Utils.config['language'] == 'pl-PL':

            voices.speak_text(
                'Trzydniowa prognoza pogody dla ' + weather.country_name +
                ', ' + weather.location_name, False)
        else:
            voices.speak_text(
                'Weather forecast for ' + weather.country_name +
                ', ' + weather.location_name, False)
        days = weather.read_txt_forecast()
        text = u""
        for day in days:
            text = text + u" " + day['title'] + ' ' + parse_text(day['text'])

        v = pyvona.create_voice(Utils.config)
        t = Thread(
            target=v.speak,
            kwargs={
                'text_to_speak': text,
                'use_cache': False,
                'async': True})
        t.start()

    @staticmethod
    def get_time():
        if Utils.config['language'] == 'pl-PL':
            locale.setlocale(locale.LC_TIME, 'pl_PL.utf8')
        curr_time = time.localtime()
        t = time.strftime("%H:%M", curr_time)
        m = time.strftime("%m", curr_time)
        dm = time.strftime("%e_%B", curr_time)
        d = time.strftime("%e", curr_time)
        dd = time.strftime("%A %e %B %Y", curr_time)
        v = pyvona.create_voice(Utils.config)
        v.speak(u'Godzina ' + t + u' dzisiaj jest ' + dd + u' rok')
        if Utils.config['language'] == 'pl-PL':
            mm = m
            if m == '01':
                mm = 'Stycznia'
            elif m == '02':
                mm = 'Lutego'
            elif m == '03':
                mm = 'Marca'
            elif m == '04':
                mm = 'Kwietnia'
            elif m == '05':
                mm = 'Maja'
            elif m == '06':
                mm = 'Czerwca'
            elif m == '07':
                mm = 'Lipca'
            elif m == '08':
                mm = 'Sierpnia'
            elif m == '09':
                mm = 'Września'
            elif m == '10':
                mm = 'Października'
            elif m == '11':
                mm = 'Listopada'
            elif m == '12':
                mm = 'Grudnia'
            Utils.search_wikipedia(d + ' ' + mm)
        else:
            Utils.search_wikipedia(dm)


# for now, just pull the track info and print it onscreen
# get the M3U file path from the first command line argument
def main():
    conf = Utils.get_config()
    Utils.config = conf['rstation']
    Utils.forecast_weather()

    # item = sys.argv[1]
    # print('item to precess: ' + item)

if __name__ == '__main__':
    main()
