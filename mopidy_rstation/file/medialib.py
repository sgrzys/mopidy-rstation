from __future__ import unicode_literals

import logging
import operator
import os
import sys
import urllib2

from mopidy import backend, exceptions, models
from mopidy.audio import scan, tags
import mpath


logger = logging.getLogger(__name__)
FS_ENCODING = sys.getfilesystemencoding()


class FileLibraryProvider(backend.LibraryProvider):
    """Library for browsing local files."""

    # TODO: get_images that can pull from metadata and/or .folder.png etc?
    # TODO: handle playlists?

    @property
    def root_directory(self):
        if not self._media_dir:
            return None
        # in rstation we have only one media directory
        elif len(self._media_dir) == 1:
            uri = mpath.path_to_uri(self._media_dir[0]['path'])
        else:
            uri = 'file:root'

        d = models.Ref.directory(name='Rstation', uri=uri)
        logger.debug('MEDIA DIR: %s', d)
        return d

    def __init__(self, backend, config):
        super(FileLibraryProvider, self).__init__(backend)
        self._media_dir = list(self._get_media_dir(config))
        logger.debug('Medialib fmedia dir: ' + str(self._media_dir))
        self._follow_symlinks = config['rstation']['follow_symlinks']
        self._show_dotfiles = config['rstation']['show_dotfiles']
        self._scanner = scan.Scanner(
            timeout=config['rstation']['metadata_timeout'])
        self.backend = backend
        logger.debug(
            'Medialib file system encoding: %s', sys.getfilesystemencoding())

    def browse(self, uri):
        logger.debug('Browsing files at: %s', uri)
        result = []
        local_path = mpath.uri_to_path(uri)

        if local_path == 'root':
            return list(self._get_media_dir_refs())

        if not self._is_in_basedir(os.path.realpath(local_path)):
            logger.warning(
                'Rejected attempt to browse path (%s) outside dirs defined '
                'in rstation/media_dir config.', uri)
            return []
        for dir_entry in os.listdir(local_path):
            child_path = os.path.join(local_path, dir_entry)
            uri = mpath.path_to_uri(child_path)

            if not self._show_dotfiles and dir_entry.startswith(b'.'):
                continue

            if os.path.islink(child_path) and not self._follow_symlinks:
                logger.debug('Ignoring symlink: %s', uri)
                continue

            if not self._is_in_basedir(os.path.realpath(child_path)):
                logger.debug('Ignoring symlink to outside base dir: %s', uri)
                continue

            name = dir_entry.decode(FS_ENCODING, 'replace')
            if os.path.isdir(child_path):
                result.append(models.Ref.directory(name=name, uri=uri))
            elif os.path.isfile(child_path):
                result.append(models.Ref.track(name=name, uri=uri))

        result.sort(key=operator.attrgetter('name'))
        return result

    def lookup(self, uri):
        logger.debug('Medialib... Looking up file URI: %s', uri)
        local_path = mpath.uri_to_path(uri)
        # check if it's playlist
        if uri.endswith(('.m3u', '.m3u8')):
            logger.debug('Medialib... we have playlist: %s', uri)
            track = models.Track(uri=uri)
        else:
            try:
                result = self._scanner.scan(uri)
                track = tags.convert_tags_to_track(result.tags).copy(
                    uri=uri, length=result.duration)
            except exceptions.ScannerError as e:
                logger.warning('Failed looking up %s: %s', uri, e)
                track = models.Track(uri=uri)

            if not track.name:
                filename = os.path.basename(local_path)
                name = urllib2.unquote(filename).decode(FS_ENCODING, 'replace')
                track = track.copy(name=name)

        return [track]

    def _get_media_dir(self, config):
        logger.debug('_get_media_dir ' + str(
            config['rstation']['media_dir']))
        for entry in config['rstation']['media_dir']:

            logger.debug('rstation/media_dir -> entry ' + entry)
            media_dir = {}
            media_dir_split = entry.split('|', 1)
            local_path = mpath.expand_path(
                media_dir_split[0].encode(FS_ENCODING))

            if not local_path:
                logger.debug(
                    'Failed expanding path (%s) from rstation/media_dir '
                    'config value.',
                    media_dir_split[0])
                continue
            elif not os.path.isdir(local_path):
                logger.warning(
                    '%s is not a directory. Please create the directory or '
                    'update the rstation/media_dir config value.', local_path)
                continue

            media_dir['path'] = local_path
            if len(media_dir_split) == 2:
                media_dir['name'] = media_dir_split[1]
            else:
                # TODO Mpd client should accept / in dir name
                media_dir['name'] = media_dir_split[0].replace(os.sep, '+')

            yield media_dir

    def _get_media_dir_refs(self):
        logger.debug('_get_media_dir_refs')
        for media_dir in self._media_dir:
            logger.debug('rstation/_get_media_dir_refs ' + media_dir)
            yield models.Ref.directory(
                name=media_dir['name'],
                uri=mpath.path_to_uri(media_dir['path']))

    def _is_in_basedir(self, local_path):
        return any(
            mpath.is_path_inside_base_dir(local_path, media_dir['path'])
            for media_dir in self._media_dir)
