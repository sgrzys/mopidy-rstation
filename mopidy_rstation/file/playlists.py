from __future__ import unicode_literals
import logging
from mopidy import backend
from mopidy.models import Ref

logger = logging.getLogger(__name__)


class FilePlaylistsProvider(backend.PlaylistsProvider):

    def __init__(self, backend):
        super(FilePlaylistsProvider, self).__init__(backend)
        logger.debug('FilePlaylistsProvider __init__')
        self._playlists = {}

    def as_list(self):
        logger.error('FilePlaylistsProvider as_list')
        refs = [
            Ref.playlist(uri=pl.uri, name=pl.name)
            for pl in self._playlists.values()]
        return refs

    def get_items(self, uri):
        logger.debug('FilePlaylistsProvider get_items')
        playlist = self._playlists.get(uri)
        if playlist is None:
            return None
        return [Ref.track(uri=t.uri, name=t.name) for t in playlist.tracks]

    def create(self, name):
        logger.debug('FilePlaylistsProvider create')
        pass  # TODO

    def delete(self, uri):
        logger.debug('FilePlaylistsProvider delete')
        pass  # TODO

    def lookup(self, uri):
        logger.debug('FilePlaylistsProvider lookup')
        for playlist in self._playlists:
            if playlist.uri == uri:
                tracks = self.backend.library.lookup(uri)
                return playlist.copy(tracks=tracks)

    def refresh(self):
        logger.debug('FilePlaylistsProvider refresh')
        playlists = {}
        self._playlists = playlists
        backend.BackendListener.send('playlists_loaded')

    def save(self, playlist):
        logger.debug('FilePlaylistsProvider save')
        pass  # TODO
