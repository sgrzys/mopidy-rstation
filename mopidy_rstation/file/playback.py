from __future__ import unicode_literals

import logging

from mopidy import backend, models, core
from mopidy.models import Track
logger = logging.getLogger(__name__)


class FilePlaybackProvider(backend.PlaybackProvider):
    def translate_uri(self, uri):
        tracks = []
        ppl = ''
        logger.debug('FilePlaybackProvider Translating...')
        if uri.endswith(('.m3u', '.m3u8')):
            logger.debug('Rstation playback... we have playlist: %s', uri)
            # return Ref.playlist(uri=uri, name='test')
            ppl = backend.api.parse_playlist(uri)
            if ppl:
                return [Track(uri=ppl.uri, name='name')]
        #
        return uri

        try:
            uri = uri.replace('rstation', 'm3u', 1)
            items = core.playlists.get_items(uri).get()
            if not items:
                logger.warn("Playlist '%s' does not exist", str(uri))
                return None

            logger.warn(str(items))

            for i in items:
                logger.debug('we will add to tracklist: ' + str(i))
                if i.type == models.Ref.TRACK:
                        tracks.append(
                            models.Track(uri=i.uri, name=i.name)
                        )
                core.tracklist.add(tracks)

        except Exception as e:
            logger.debug('we have a problem ' + str(e))

        # core.tracklist.set_consume(False)
        # core.tracklist.set_repeat(True)
        # core.playback.play()
        return None
