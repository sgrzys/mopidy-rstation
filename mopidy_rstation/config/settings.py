# encoding=utf8
from ConfigParser import ConfigParser
from ConfigParser import RawConfigParser


class Config:
    config = None
    # config_file = '/home/pi/mopidy.conf'
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
            elif cur_lang == 'en-US':
                new_lang = 'ru-RU'
            elif cur_lang == 'ru-RU':
                new_lang = 'fr-FR'
            elif cur_lang == 'fr-FR':
                new_lang = 'pl-PL'

        Config.change_config('language', new_lang)
        print('languate changed to ' + str(new_lang))


class Settings:
    current_main_menu = None
    current_menu = None

    @staticmethod
    def speak(text):
        from mopidy_rstation.audio import voices
        voices.speak(text)

    @staticmethod
    def main_menu_right ():
        if Settings.current_menu is None:
            Settings.current_menu = "MENU_LANGUAGE"
        if Settings.current_menu == "MENU_LANGUAGE":
            Settings.current_menu = "MENU_VOICE"
        if Settings.current_menu == "MENU_VOICE":
            Settings.current_menu = "MENU_HELP"
        if Settings.current_menu == "MENU_HELP":
            Settings.current_menu = "MENU_LANGUAGE"
        Settings.speak(Settings.current_menu)

    @staticmethod
    def main_menu_left():
        if Settings.current_menu is None:
            Settings.current_menu = "MENU_HELP"
        if Settings.current_menu == "MENU_HELP":
            Settings.current_menu = "MENU_VOICE"
        if Settings.current_menu == "MENU_VOICE":
            Settings.current_menu = "MENU_LANGUAGE"
        if Settings.current_menu == "MENU_LANGUAGE":
            Settings.current_menu = "MENU_HELP"
        Settings.speak(Settings.current_menu)

    @staticmethod
    def menu_left():
        print('menu_left TODO')

    @staticmethod
    def menu_right():
        print('menu_right TODO')

    @staticmethod
    def onCommand(cmd):
        if cmd == 'left':
            if Settings.current_main_menu is None:
                Settings.main_menu_left()
            else:
                Settings.menu_left()
        elif cmd == 'right':
            if Settings.current_main_menu is None:
                Settings.main_menu_right()
            else:
                Settings.menu_right()


def main():
    print('TODO')

if __name__ == '__main__':
    main()
