# encoding=utf8
from fuzzywuzzy import process
from mopidy_rstation.finder import m3uparser
# from mopidy.models import Track
from mopidy_rstation.utils import Utils
from mopidy_rstation.audio import voices
import sys


def load_best_playlist(albums, names, item):
    name = process.extractOne(item, names)
    for album in albums:
        if album.title == name[0]:
            if Utils.core is None:
                return
            Utils.core.tracklist.clear()
            Utils.core.tracklist.add(uri=album.path)
            Utils.core.playback.play()
            voices.speak('PLAY_URI', val=album.title)


def load_best_track(tracks, titles, item):
    title = process.extractOne(item, titles)
    for track in tracks:
        if track.title == title[0]:
            if Utils.core is None:
                return
            Utils.core.tracklist.clear()
            Utils.core.tracklist.add(uri=track.file)
            tl_tracks = Utils.core.tracklist.tl_tracks.get()
            for tl_track in tl_tracks:
                if tl_track.track.name == title[0]:
                    voices.speak('PLAY_URI', val=tl_track.track.name)
                    Utils.core.playback.play(tlid=tl_track.tlid)


def start_player():
    if Utils.core is None:
        return
    Utils.core.playback.play()
    # TODO
    # voices.speak('PLAY_URI', val=album.title)


def play_item(item, item_type=None):

    if item_type == 'muzyka':
        albums, names = m3uparser.parseFolderForPlaylists(
            '/home/pi/mopidy-rstation/media/Music')
        load_best_playlist(albums, names, item)
    elif item_type == 'audiobook':
        albums, names = m3uparser.parseFolderForPlaylists(
            '/home/pi/mopidy-rstation/media/Audiobooks')
        load_best_playlist(albums, names, item)
    elif item_type == 'podcast':
        albums, names = m3uparser.parseFolderForPlaylists(
            '/home/pi/mopidy-rstation/media/Podcasts')
        load_best_playlist(albums, names, item)
    elif item_type == 'radio':
        tracks, titles = m3uparser.parseFolderForTracks(
            '/home/pi/mopidy-rstation/media/Radio')
        load_best_track(tracks, titles, item)
    else:
        # try to play without a type
        tracks, titles = m3uparser.parseFolderForTracks(
            '/home/pi/mopidy-rstation/media')
        albums, names = m3uparser.parseFolderForPlaylists(
            '/home/pi/mopidy-rstation/media')
        title = process.extractOne(item, titles)
        print(str(title))
        name = process.extractOne(item, names)
        print(str(name))
        if title[1] > name[1]:
            load_best_track(tracks, titles, item)
        else:
            load_best_playlist(albums, names, item)


# TODO
def turn_vol_down():
    pass


def main():
    item = sys.argv[1]
    print('item to precess: ' + item)
    play_item(item, 'radio')

if __name__ == '__main__':
    main()
