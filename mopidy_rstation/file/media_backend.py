from __future__ import absolute_import, unicode_literals

import logging

import pykka

from mopidy import backend
from . import medialib
# ,playlists ,playback
from mopidy.m3u import playlists
logger = logging.getLogger(__name__)


class MediaBackend(pykka.ThreadingActor, backend.Backend):
    uri_schemes = ['rstation']

    def __init__(self, config, audio):
        super(MediaBackend, self).__init__()
        self.library = medialib.FileLibraryProvider(
            backend=self, config=config)
        # self.playlists = playlists.FilePlaylistsProvider(
        #     config=config, backend=self)
        # self.playlists = backend.PlaylistsProvider(backend=self)
        self.playlists = playlists.M3UPlaylistsProvider(
            backend=self, config=config)
        # self.playback = playback.FilePlaybackProvider(
        #     audio=audio, backend=self)

    def on_start(self):
        logger.info("Rstation backend start...")
