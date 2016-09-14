from __future__ import unicode_literals
import os
from mopidy import config, ext

__version__ = '1.0.0'


class Extension(ext.Extension):
    dist_name = 'Mopidy-Rstation'
    ext_name = 'rstation'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__),
                                 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['enable_irda'] = config.Boolean()
        schema['enable_keypad'] = config.Boolean()
        schema['debug_irda_simulate'] = config.Boolean()
        schema['track_list_prev'] = config.String()
        schema['track_list_enter'] = config.String()
        schema['track_list_next'] = config.String()
        schema['player_prev'] = config.String()
        schema['player_next'] = config.String()
        schema['player_play_pause'] = config.String()
        schema['vol_up'] = config.String()
        schema['vol_down'] = config.String()
        schema['change_lang'] = config.String()
        schema['num0'] = config.String()
        schema['backlight_down'] = config.String()
        schema['backlight_up'] = config.String()
        schema['num1'] = config.String()
        schema['lib_root_dir'] = config.String()
        schema['num3'] = config.String()
        schema['lib_prev'] = config.String()
        schema['lib_enter'] = config.String()
        schema['lib_next'] = config.String()
        schema['lib_audiobook'] = config.String()
        schema['lib_radio'] = config.String()
        schema['lib_music'] = config.String()
        schema['mute'] = config.String()
        schema['stop'] = config.String()
        schema['power'] = config.String()
        schema['menu'] = config.String()
        schema['favorites'] = config.String()
        schema['search'] = config.String()
        schema['playlist_uri_template'] = config.String()
        schema['media_dir'] = config.List(optional=True)
        schema['show_dotfiles'] = config.Boolean(optional=True)
        schema['follow_symlinks'] = config.Boolean(optional=True)
        schema['metadata_timeout'] = config.Integer(optional=True)
        return schema

    def setup(self, registry):
        from .rstation_manager import RstationFrontend
        registry.add('frontend', RstationFrontend)
        from .file.media_backend import MediaBackend
        registry.add('backend', MediaBackend)
