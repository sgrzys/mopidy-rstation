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
        schema['media_dir'] = config.List(optional=True)
        schema['show_dotfiles'] = config.Boolean(optional=True)
        schema['follow_symlinks'] = config.Boolean(optional=True)
        schema['metadata_timeout'] = config.Integer(optional=True)
        return schema

    def setup(self, registry):
        from .rstation_manager import RstationFrontend
        registry.add('frontend', RstationFrontend)
        from .tts.tts import TtsFrontend
        registry.add('frontend', TtsFrontend)
        from .file.media_backend import MediaBackend
        registry.add('backend', MediaBackend)
