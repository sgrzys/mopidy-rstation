from __future__ import unicode_literals
import logging
from mopidy import backend

logger = logging.getLogger(__name__)


class FilePlaylistsProvider(backend.PlaylistsProvider):

    def as_list(self):
        refs = []
        logger.debug('FilePlaylistsProvider as_list')
        return refs

    def get_items(self, uri):
        logger.debug('FilePlaylistsProvider get_items')
        playlist = self._playlists.get(uri)
        if playlist is None:
            return None
        return []

    def create(self, name):
        logger.debug('FilePlaylistsProvider create')
        pass  # TODO

    def delete(self, uri):
        logger.debug('FilePlaylistsProvider delete')
        pass  # TODO

    def lookup(self, uri):
        logger.debug('FilePlaylistsProvider lookup')
        for playlist in self.playlists:
            if playlist.uri == uri:
                tracks = self.backend.library.lookup(uri)
                return playlist.copy(tracks=tracks)

    def refresh(self):
        logger.debug('FilePlaylistsProvider refresh')

        backend.BackendListener.send('playlists_loaded')

    def save(self, playlist):
        logger.debug('FilePlaylistsProvider save')
        pass  # TODO
