from __future__ import absolute_import, unicode_literals
import logging
import pykka
from mopidy import backend
from . import medialib
from mopidy.m3u import playlists

logger = logging.getLogger(__name__)


class MediaBackend(pykka.ThreadingActor, backend.Backend):
    uri_schemes = ['rstation']

    def __init__(self, config, audio):
        super(MediaBackend, self).__init__()
        self.library = medialib.FileLibraryProvider(
            backend=self, config=config)
        self.playlists = playlists.M3UPlaylistsProvider(
            backend=self, config=config)
        # config is type 'tuple'
        url = 'rstation:' + config['rstation']['media_dir'][0]
        self.library.browse(url)

    def on_start(self):
        logger.info("Rstation backend start...")

    def handle_remote_command(self, cmd):
        pass

    def on_event(self, event, **kwargs):
        logger.debug("------------------------- ")
        logger.debug("Event: " + str(event))
        logger.debug("Button pressed: " + str(kwargs))
        logger.debug("------------------------- ")
        if event == "handleRemoteCommand":
            self.handle_remote_command(kwargs['cmd'])
        pass
