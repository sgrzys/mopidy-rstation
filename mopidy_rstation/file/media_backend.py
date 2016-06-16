from __future__ import absolute_import, unicode_literals

import logging

import pykka

from mopidy import backend
from . import medialib


logger = logging.getLogger(__name__)


class MediaBackend(pykka.ThreadingActor, backend.Backend):
    uri_schemes = ['file']

    def __init__(self, config, audio):
        super(MediaBackend, self).__init__()
        self.library = medialib.FileLibraryProvider(
            backend=self, config=config)
        self.playback = backend.PlaybackProvider(audio=audio, backend=self)
        self.playlists = None
