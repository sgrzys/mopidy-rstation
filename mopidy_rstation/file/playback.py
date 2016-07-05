from __future__ import unicode_literals

import logging

from mopidy import backend, models
logger = logging.getLogger(__name__)


class FilePlaybackProvider(backend.PlaybackProvider):

    def __init__(self, audio, backend):
        super(FilePlaybackProvider, self).__init__(audio, backend)
        self.backend = backend
        logger.debug('FilePlaybackProvider __init__')

    def translate_uri(self, uri):
        tracks = []
        logger.debug('FilePlaybackProvider Translating...')
        if uri.endswith(('.m3u', '.m3u8')):
            logger.debug('Rstation playback... we have playlist: %s', uri)
            logger.warn(str(self.backend.playlists))
            items = self.backend.playlists.get_items(uri)
            logger.debug(str(items))
            if not items:
                logger.warn("Playlist '%s' does not exist", str(uri))
                return None
            for i in items:
                logger.debug('we will add to tracklist: ' + str(i))
                if i.type == models.Ref.TRACK:
                    tracks.append(
                        models.Track(uri=i.uri, name=i.name)
                    )
            # uris = map(lambda ref: ref.uri, items)
            # logger.debug('uris: ' + str(uris))
            # core.tracklist.add(uris=uris)
            # self.backend.tracklist.add(tracks)

            return uri
            # tracks[0].uri
        else:
            return uri
