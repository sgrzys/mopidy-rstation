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
        schema['wit_token'] = config.String()
        schema['ivona_access_key'] = config.String()
        schema['ivona_secret_key'] = config.String()
        schema['language'] = config.String(optional=True)
        # optional
        schema['enable_irda'] = config.Boolean(optional=True)
        schema['enable_keypad'] = config.Boolean(optional=True)
        schema['debug_irda_simulate'] = config.Boolean(optional=True)
        schema['track_list_prev'] = config.String(optional=True)
        schema['track_list_enter'] = config.String(optional=True)
        schema['track_list_next'] = config.String(optional=True)
        schema['player_prev'] = config.String(optional=True)
        schema['player_next'] = config.String(optional=True)
        schema['player_play_pause'] = config.String(optional=True)
        schema['vol_up'] = config.String(optional=True)
        schema['vol_down'] = config.String(optional=True)
        schema['change_lang'] = config.String(optional=True)
        schema['ask_bot'] = config.String(optional=True)
        schema['backlight_down'] = config.String(optional=True)
        schema['backlight_up'] = config.String(optional=True)
        schema['num1'] = config.String(optional=True)
        schema['lib_root_dir'] = config.String(optional=True)
        schema['num3'] = config.String(optional=True)
        schema['lib_prev'] = config.String(optional=True)
        schema['lib_enter'] = config.String(optional=True)
        schema['lib_next'] = config.String(optional=True)
        schema['lib_audiobook'] = config.String(optional=True)
        schema['lib_radio'] = config.String(optional=True)
        schema['lib_music'] = config.String(optional=True)
        schema['mute'] = config.String(optional=True)
        schema['stop'] = config.String(optional=True)
        schema['power'] = config.String(optional=True)
        schema['menu'] = config.String(optional=True)
        schema['favorites'] = config.String(optional=True)
        schema['search'] = config.String(optional=True)
        schema['playlist_uri_template'] = config.String(optional=True)
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
