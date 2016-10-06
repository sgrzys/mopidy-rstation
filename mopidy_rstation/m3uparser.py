# more info on the M3U file format available here:
# http://n4k3d.com/the-m3u-file-format/
import sys
import os


class track():
    def __init__(self, length, title, path):
        self.length = length
        self.title = title
        self.path = path

"""
    song info lines are formatted like:
    EXTINF:419,Alice In Chains - Rotten Apple
    length (seconds)
    Song title
    file name - relative or absolute path of file
    ..\Minus The Bear\Minus The Bear_Planet of Ice_01_Burying Luck.mp3
"""


def parseFolder(folder):
    if folder is None:
        return
    tracks = []
    titles = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".m3u8"):
                tracks = tracks + parsem3u(os.path.join(root, file))

    for track in tracks:
        titles.append(track.title)

    return tracks, titles


def parsem3u(infile):
    try:
        assert(type(infile) == '_io.TextIOWrapper')
    except AssertionError:
        infile = open(infile, 'r')

    """
        All M3U files start with #EXTM3U.
        If the first line doesn't start with this, we're either
        not working with an M3U or the file we got is corrupted.
    """

    line = infile.readline()
    if not line.startswith('#EXTM3U'):
        return

    # initialize playlist variables before reading file
    playlist = []
    song = track(None, None, None)

    for line in infile:
        line = line.strip()
        if line.startswith('#EXTINF:'):
            # pull length and title from #EXTINF line
            length, title = line.split('#EXTINF:')[1].split(',', 1)
            song = track(length, title, None)
        elif (len(line) != 0):
            # pull song path from all other, non-blank lines
            song.path = line
            playlist.append(song)
            # reset the song variable so it doesn't use the same EXTINF
            # more than once
            song = track(None, None, None)

    infile.close()

    return playlist


# for now, just pull the track info and print it onscreen
# get the M3U file path from the first command line argument
def main():
    folder = sys.argv[1]
    tracks, titles = parseFolder(folder)
    for title in titles:
        print(title)
    # m3ufile = sys.argv[1]
    # playlist = parsem3u(m3ufile)
    # for track in playlist:
    #     print(track.title, track.length, track.path)

if __name__ == '__main__':
    main()
