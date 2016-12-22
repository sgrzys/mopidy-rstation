# encoding=utf8
import json
import os
import subprocess
import time
from mopidy_rstation.audio import pyvona
import locale
import sys
# to avoid the UnicodeDecodeError: 'ascii' codec can't decode byte
reload(sys)
sys.setdefaultencoding("utf-8")


class Utils:
    lib_items = []
    curr_lib_item_id = 0
    core = None

    @staticmethod
    def save_core(core):
        Utils.core = core

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
    def search_wikipedia(query):
        print(query)
        from mopidy_rstation.wikipedia import search
        from mopidy_rstation.audio import voices
        from mopidy_rstation.config import settings
        voices.speak('ASKING_WIKIPEDIA')
        lang = settings.Config.get_current_lang(short=True)
        ret = ''
        try:
            ret = u'' + search.do(query, lang)
        except Exception:
            voices.speak_text('Wikipedia Error ' + query)
            return
        ret = ret.replace('=', '')
        voices.speak_long_text(ret)

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

        from mopidy_rstation.weather import forecast
        from mopidy_rstation.audio import voices
        from mopidy_rstation.config import settings
        if location is not None:
            from geopy.geocoders import Nominatim
            geolocator = Nominatim()
            loc = geolocator.geocode(location)
            gps = str(loc.latitude) + ',' + str(loc.longitude)
            weather = forecast.ForecastData(location_gps=gps)
        else:
            weather = forecast.ForecastData(location_gps=None)
        weather.verbose = True
        voices.speak(
            'WEATHER_INFO',
            val=weather.location_name + ', ' + weather.country_name)

        days = weather.read_txt_forecast()
        text = u""
        for day in days:
            text = text + u" " + day['title'] + ' ' + parse_text(day['text'])

        voices.speak_long_text(text)

    @staticmethod
    def get_time():
        from mopidy_rstation.config import settings
        if settings.Config.get_current_lang() == 'pl-PL':
            locale.setlocale(locale.LC_TIME, 'pl_PL.utf8')
        curr_time = time.localtime()
        t = time.strftime("%H:%M", curr_time)
        m = time.strftime("%m", curr_time)
        dm = time.strftime("%e_%B", curr_time)
        d = time.strftime("%e", curr_time)
        dd = time.strftime("%A %e %B %Y", curr_time)
        v = pyvona.create_voice()
        v.speak(u'Godzina ' + t + u'. Dzisiaj jest ' + dd + u' rok.')
        if settings.Config.get_current_lang() == 'pl-PL':
            mm = m
            if m == '01':
                mm = 'stycznia'
            elif m == '02':
                mm = 'lutego'
            elif m == '03':
                mm = 'marca'
            elif m == '04':
                mm = 'kwietnia'
            elif m == '05':
                mm = 'maja'
            elif m == '06':
                mm = 'czerwca'
            elif m == '07':
                mm = 'lipca'
            elif m == '08':
                mm = 'sierpnia'
            elif m == '09':
                mm = 'września'
            elif m == '10':
                mm = 'października'
            elif m == '11':
                mm = 'listopada'
            elif m == '12':
                mm = 'grudnia'
            Utils.search_wikipedia(d + '_' + mm)
        else:
            Utils.search_wikipedia(dm)


# TODO
def main():
    Utils.get_time()
    # Utils.forecast_weather()
    # item = sys.argv[1]
    # print('item to precess: ' + item)

if __name__ == '__main__':
    main()
