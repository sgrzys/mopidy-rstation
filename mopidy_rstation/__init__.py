from __future__ import unicode_literals

import logging
import os
from mopidy import config, ext

__version__ = '0.1.0'


logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = 'Mopidy-Rstation'
    ext_name = 'rstation'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['debug_irda_simulate'] = config.Boolean()
        schema['mute'] = config.String()
        schema['next'] = config.String()
        schema['previous'] = config.String()
        schema['playpause'] = config.String()
        schema['stop'] = config.String()
        schema['volumeup'] = config.String()
        schema['volumedown'] = config.String()
        schema['power'] = config.String()
        schema['menu'] = config.String()
        schema['favorites'] = config.String()
        schema['search'] = config.String()
        schema['playlist_uri_template'] = config.String()
        schema['num0'] = config.String()
        schema['num1'] = config.String()
        schema['num2'] = config.String()
        schema['num3'] = config.String()
        schema['num4'] = config.String()
        schema['num5'] = config.String()
        schema['num6'] = config.String()
        schema['num7'] = config.String()
        schema['num8'] = config.String()
        schema['num9'] = config.String()
        return schema

    def setup(self, registry):

        from .frontend import RstationFrontend
        registry.add('frontend', RstationFrontend)
