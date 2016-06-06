from __future__ import unicode_literals

import os

from mopidy import config, ext

from .touch_screen import TouchScreen


__version__ = '1.0.0'


class Extension(ext.Extension):
    dist_name = 'Mopidy-Touchscreen'
    ext_name = 'touchscreen'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__),
                                 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['screen_width'] = config.Integer(minimum=1)
        schema['screen_height'] = config.Integer(minimum=1)
        schema['resolution_factor'] = config.Integer(minimum=6)
        schema['cursor'] = config.Boolean()
        schema['fullscreen'] = config.Boolean()
        schema['cache_dir'] = config.Path()
        schema['gpio'] = config.Boolean()
        schema['gpio_left'] = config.Integer()
        schema['gpio_right'] = config.Integer()
        schema['gpio_up'] = config.Integer()
        schema['gpio_down'] = config.Integer()
        schema['gpio_enter'] = config.Integer()
        schema['sdl_fbdev'] = config.String()
        schema['sdl_mousdrv'] = config.String()
        schema['sdl_mousedev'] = config.String()
        schema['sdl_audiodriver'] = config.String()
        schema['sdl_path_dsp'] = config.String()
        schema['debug_irda_simulate'] = config.Boolean()
        schema['ch_minus'] = config.String()
        schema['ch'] = config.String()
        schema['ch_plus'] = config.String()
        schema['prev'] = config.String()
        schema['next'] = config.String()
        schema['play_pause'] = config.String()
        schema['vol_up'] = config.String()
        schema['vol_down'] = config.String()
        schema['eq'] = config.String()
        schema['num0'] = config.String()
        schema['fl_minus'] = config.String()
        schema['fl_plus'] = config.String()
        schema['num1'] = config.String()
        schema['num2'] = config.String()
        schema['num3'] = config.String()
        schema['num4'] = config.String()
        schema['num5'] = config.String()
        schema['num6'] = config.String()
        schema['num7'] = config.String()
        schema['num8'] = config.String()
        schema['num9'] = config.String()
        schema['mute'] = config.String()
        schema['stop'] = config.String()
        schema['power'] = config.String()
        schema['menu'] = config.String()
        schema['favorites'] = config.String()
        schema['search'] = config.String()
        schema['playlist_uri_template'] = config.String()
        return schema

    def setup(self, registry):
        registry.add('frontend', TouchScreen)
        from .rstation_manager import RstationFrontend
        registry.add('frontend', RstationFrontend)
