# encoding=utf8
from ConfigParser import ConfigParser
from ConfigParser import RawConfigParser
import time


class Config:
    config = None
    config_file = '/etc/mopidy/mopidy.conf'

    @staticmethod
    def change_config(key, value, section="rstation"):
        Config.config[key] = value
        conf = RawConfigParser()
        conf.read(Config.config_file)
        conf.set(section, key, value)
        with open(Config.config_file, 'wb') as configfile:
            conf.write(configfile)

    @staticmethod
    def get_config():
        if Config.config is None:
            conf = ConfigParser()
            conf.read(Config.config_file)
            the_dict = {}
            for section in conf.sections():
                the_dict[section] = {}
                for key, val in conf.items(section):
                    the_dict[section][key] = val
            Config.config = the_dict['rstation']
        return Config.config

    @staticmethod
    def get_current_lang(short=None):
        if short:
            return Config.get_config()['language'][:2]
        return Config.get_config()['language']

    @staticmethod
    def switch_current_lang(lang=None):
        new_lang = ''
        cur_lang = Config.get_current_lang()
        if lang is not None:
            new_lang = lang
        else:
            if cur_lang == 'pl-PL':
                new_lang = 'en-US'
                Config.switch_current_voice('Joey')
            elif cur_lang == 'en-US':
                new_lang = 'ru-RU'
                Config.switch_current_voice('Maxim')
            elif cur_lang == 'ru-RU':
                new_lang = 'fr-FR'
                Config.switch_current_voice('Celine')
            elif cur_lang == 'fr-FR':
                new_lang = 'pl-PL'
                Config.switch_current_voice('Ewa')

        Config.change_config('language', new_lang)
        from mopidy_rstation.audio import voices
        voices.voice = None
        voices.speak("LANGUAGE")
        print('languate changed to ' + str(new_lang))

    @staticmethod
    def switch_current_voice(voice=None):
        if voice is not None:
            new_voice = voice
            Config.change_config('voice_name', new_voice)
        else:
            cur_lang = Config.get_current_lang()
            cur_voice = Config.get_config()['voice_name']
            if cur_lang == 'pl-PL':
                if cur_voice == 'Ewa':
                    new_voice = 'Agnieszka'
                elif cur_voice == 'Agnieszka':
                    new_voice = 'Maja'
                elif cur_voice == 'Maja':
                    new_voice = 'Jacek'
                elif cur_voice == 'Jacek':
                    new_voice = 'Jan'
                elif cur_voice == 'Jan':
                    new_voice = 'Ewa'
                t = 'Cześć, mam na imię ' + new_voice + '.' \
                    + ' Jestem jednym z głosów Twojego radia.'
            elif cur_lang == 'en-US':
                if cur_voice == 'Joey':
                    new_voice = 'Justin'
                elif cur_voice == 'Justin':
                    new_voice = 'Salli'
                elif cur_voice == 'Salli':
                    new_voice = 'Kimberly'
                elif cur_voice == 'Kimberly':
                    new_voice = 'Kendra'
                elif cur_voice == 'Kendra':
                    new_voice = 'Eric'
                elif cur_voice == 'Eric':
                    new_voice = 'Jennifer'
                elif cur_voice == 'Jennifer':
                    new_voice = 'Ivy'
                elif cur_voice == 'Ivy':
                    new_voice = 'Chipmunk'
                elif cur_voice == 'Chipmunk':
                    new_voice = 'Joey'
                t = 'Hello there, my name is ' + new_voice + '.' \
                    + ' I am one of the redio voices.'
            elif cur_lang == 'ru-RU':
                if cur_voice == 'Maxim':
                    new_voice = 'Tatyana'
                elif cur_voice == 'Tatyana':
                    new_voice = 'Maxim'
                t = 'Привет, меня зовут ' + new_voice + '.' \
                    + ' Я один из голосов программы преобразования' \
                    + ' текста в речь Radio.'
            elif cur_lang == 'fr-FR':
                if cur_voice == 'Celine':
                    new_voice = 'Mathieu'
                elif cur_voice == 'Mathieu':
                    new_voice = 'Celine'
                t = 'Bonjour, mon nom est ' + new_voice + '.' \
                    + ' Je suis une des voix radio.'
            Config.change_config('voice_name', new_voice)
            from mopidy_rstation.audio import voices
            voices.voice = None
            voices.speak_text(t)

        print('voice changed to ' + str(new_voice))

    @staticmethod
    def switch_current_audio_in():
        new_audio_in_name = ''
        cur_audio_in_name = Config.get_config()['audio_in_name']
        audio_in_speak_code = ''
        if cur_audio_in_name == 'sysdefault':
            new_audio_in_name = 'Airmouse: USB Audio'
            audio_in_speak_code = "AUDIO_IN_AIRMOUSE"
        elif cur_audio_in_name == 'Airmouse: USB Audio':
            new_audio_in_name = 'USB Camera'
            audio_in_speak_code = "AUDIO_IN_ARRAY"
        elif cur_audio_in_name == 'USB Camera':
            new_audio_in_name = 'sysdefault'
            audio_in_speak_code = "AUDIO_IN_ONBOARD"
        else:
            cur_audio_in_name = 'sysdefault'
            audio_in_speak_code = "AUDIO_IN_ONBOARD"

        Config.change_config('audio_in_name', new_audio_in_name)
        from mopidy_rstation.audio import voices
        voices.voice = None
        voices.speak(audio_in_speak_code)
        print('audio in changed to ' + audio_in_speak_code)

    @staticmethod
    def switch_current_audio_out():
        new_audio_out_name = ''
        cur_audio_out_name = Config.get_config()['audio_out_name']
        audio_out_speak_code = ''
        if cur_audio_out_name == 'jack':
            new_audio_out_name = 'hdmi'
            audio_out_speak_code = "AUDIO_OUT_HDMI"
        if cur_audio_out_name == 'hdmi':
            new_audio_out_name = 'speaker'
            audio_out_speak_code = "AUDIO_OUT_SPEAKER"
        if cur_audio_out_name == 'speaker':
            new_audio_out_name = 'spdif'
            audio_out_speak_code = "AUDIO_OUT_SPDIF"
        if cur_audio_out_name == 'spdif':
            new_audio_out_name = 'jack'
            audio_out_speak_code = "AUDIO_OUT_JACK"

        Config.change_config('audio_out_name', new_audio_out_name)
        from mopidy_rstation.audio import voices
        voices.voice = None
        voices.speak(audio_out_speak_code)
        print('audio out changed to ' + audio_out_speak_code)


class Settings:
    G_MAIN_MENU_CURRENT = ''
    G_MAIN_MENU_FOCUS = ''
    G_MENU_CURRENT = ''
    G_MENU_FOCUS = ''

    @staticmethod
    def speak(keys_list, val=None):
        from mopidy_rstation.audio import voices
        v = ''
        if val is not None:
            v = val
        voices.speak(keys_list, val=v)

    @staticmethod
    def switch_current_info():
        if Settings.G_MENU_FOCUS == '':
            Settings.G_MENU_FOCUS = 'INFO_VERSION'
        elif Settings.G_MENU_FOCUS == 'INFO_VERSION':
            Settings.G_MENU_FOCUS = 'INFO_UPDATE'
        elif Settings.G_MENU_FOCUS == 'INFO_UPDATE':
            Settings.G_MENU_FOCUS = 'INFO_ANALYSIS'
        elif Settings.G_MENU_FOCUS == 'INFO_ANALYSIS':
            Settings.G_MENU_FOCUS = 'INFO_VERSION'
        Settings.speak(Settings.G_MENU_FOCUS)

    @staticmethod
    def main_menu_right():
        print(
            'main_menu_right G_MAIN_MENU_FOCUS ' + Settings.G_MAIN_MENU_FOCUS)
        if Settings.G_MAIN_MENU_FOCUS == '':
            Settings.G_MAIN_MENU_FOCUS = "MENU_LANGUAGE"
        elif Settings.G_MAIN_MENU_FOCUS == "MENU_LANGUAGE":
            Settings.G_MAIN_MENU_FOCUS = "MENU_VOICE"
        elif Settings.G_MAIN_MENU_FOCUS == "MENU_VOICE":
            Settings.G_MAIN_MENU_FOCUS = "MENU_AUDIO_IN"
        elif Settings.G_MAIN_MENU_FOCUS == "MENU_AUDIO_IN":
            Settings.G_MAIN_MENU_FOCUS = "MENU_AUDIO_OUT"
        elif Settings.G_MAIN_MENU_FOCUS == "MENU_AUDIO_OUT":
            Settings.G_MAIN_MENU_FOCUS = "MENU_HELP"
        elif Settings.G_MAIN_MENU_FOCUS == "MENU_HELP":
            Settings.G_MAIN_MENU_FOCUS = "MENU_LANGUAGE"
        Settings.speak(Settings.G_MAIN_MENU_FOCUS)

    @staticmethod
    def main_menu_left():
        if Settings.G_MAIN_MENU_FOCUS == '':
            Settings.G_MAIN_MENU_FOCUS = "MENU_HELP"
        elif Settings.G_MAIN_MENU_FOCUS == "MENU_HELP":
            Settings.G_MAIN_MENU_FOCUS = "MENU_AUDIO_OUT"
        elif Settings.G_MAIN_MENU_FOCUS == "MENU_AUDIO_OUT":
            Settings.G_MAIN_MENU_FOCUS = "MENU_AUDIO_IN"
        elif Settings.G_MAIN_MENU_FOCUS == "MENU_AUDIO_IN":
            Settings.G_MAIN_MENU_FOCUS = "MENU_VOICE"
        elif Settings.G_MAIN_MENU_FOCUS == "MENU_VOICE":
            Settings.G_MAIN_MENU_FOCUS = "MENU_LANGUAGE"
        elif Settings.G_MAIN_MENU_FOCUS == "MENU_LANGUAGE":
            Settings.G_MAIN_MENU_FOCUS = "MENU_HELP"
        Settings.speak(Settings.G_MAIN_MENU_FOCUS)

    @staticmethod
    def main_menu_enter():
        print("main_menu_enter")
        Settings.G_MAIN_MENU_CURRENT = Settings.G_MAIN_MENU_FOCUS
        Settings.speak(['ENTER_DIR', Settings.G_MAIN_MENU_CURRENT])

    @staticmethod
    def main_menu_up():
        Settings.G_MAIN_MENU_CURRENT = ''
        Settings.speak(['UP_DIR', 'SETTINGS'])

    @staticmethod
    def main_menu_switch():
        from mopidy_rstation.config.settings import Config
        if Settings.G_MAIN_MENU_FOCUS == "MENU_HELP":
            Settings.switch_current_info()
        elif Settings.G_MAIN_MENU_FOCUS == "MENU_VOICE":
            Config.switch_current_voice()
        elif Settings.G_MAIN_MENU_FOCUS == "MENU_LANGUAGE":
            Config.switch_current_lang()
        elif Settings.G_MAIN_MENU_FOCUS == "MENU_AUDIO_IN":
            Config.switch_current_audio_in()
        elif Settings.G_MAIN_MENU_FOCUS == "MENU_AUDIO_OUT":
            Config.switch_current_audio_out()

    @staticmethod
    def menu_enter():
        import update
        print("menu_enter")
        Settings.G_MENU_CURRENT = Settings.G_MENU_FOCUS
        if Settings.G_MENU_CURRENT == 'INFO_VERSION':
            ver = update.get_version_info(update.APP_SOURCE_DIR)
            Settings.speak(Settings.G_MENU_CURRENT, val=ver)
        elif Settings.G_MENU_CURRENT == 'INFO_UPDATE':
            Settings.speak('PROCESSING')
            # MEDIA
            if update.isUpToDate(update.MEDIA_DIR):
                Settings.speak('MEDIA_UP_TO_DATE')
            else:
                update.resetHard(update.MEDIA_DIR)
                Settings.speak('MEDIA_UPDATED')
            # APP
            if update.isUpToDate(update.APP_SOURCE_DIR):
                Settings.speak('APP_SOURCES_UP_TO_DATE')
            else:
                update.resetHard(update.APP_SOURCE_DIR)
                Settings.speak('APP_SOURCES_UPDATED')
                update.updateApp()
                Settings.speak('APP_UPDATED')
                time.sleep(2)
                Settings.speak('SERVICE_RESTART')
                time.sleep(4)
                update.restartService()

        elif Settings.G_MENU_CURRENT == 'INFO_ANALYSIS':
            Settings.speak(
                Settings.G_MENU_CURRENT,
                val='Właśnie wykonałam analiza systemu. Jest super!')

    @staticmethod
    def menu_up():
        Settings.G_MENU_CURRENT = ''
        Settings.speak(['UP_DIR', Settings.G_MAIN_MENU_CURRENT])

    @staticmethod
    def onCommand(cmd):
        print('Settings.onCommand ' + cmd)
        if cmd == 'left' or cmd == 'right':
            if Settings.G_MAIN_MENU_CURRENT == '':
                if cmd == 'left':
                    Settings.main_menu_left()
                else:
                    Settings.main_menu_right()
            else:
                Settings.main_menu_switch()
        elif cmd == 'enter' or cmd == 'down':
            print('cmd enter')
            if Settings.G_MAIN_MENU_FOCUS != '':
                if Settings.G_MAIN_MENU_CURRENT == '':
                    Settings.main_menu_enter()
                else:
                    Settings.menu_enter()

        elif cmd == 'up':
            if Settings.G_MAIN_MENU_CURRENT != '':
                Settings.main_menu_up()
            else:
                Settings.menu_up()


def main():
    print('TODO')

if __name__ == '__main__':
    main()
