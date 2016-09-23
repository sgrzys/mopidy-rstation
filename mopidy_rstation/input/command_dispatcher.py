from ..utils import Utils
from mopidy.core import PlaybackState
from .wit import ai
import traceback

LIRC_PROG_NAME = "mopidyRstation"
C_MODE_PLAYER = 'PLAYER'
C_MODE_LIBRARY = 'LIBRARY'
C_MODE_TRACKLIST = 'TRACKLIST'
url = u'rstation:/home/pi/mopidy-rstation/media'


class Event(list):
    """Event subscription.

    A list of callable objects. Calling an
    i_playPlaylistnstance of this will cause a
    call to each item in the list in ascending order by index."""
    def __call__(self, *args, **kwargs):
        for f in self:
            f(*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % list.__repr__(self)


class CommandDispatcher(object):
    def __init__(self, core, config, buttonPressEvent):
        self.core = core
        self.config = config
        self.current_mode = C_MODE_PLAYER
        buttonPressEvent.append(self.handleCommand)

    def handleCommand(self, cmd):
        Utils.beep()
        # send the command to all the
        # CoreListener.send("handleRemoteCommand", cmd=cmd)
        self.onCommand(cmd)

    def track_list_prev(self):
        # prev on track list
        tracks = self.core.tracklist.tl_tracks.get()
        if len(tracks) == 0:
            pass
        else:
            if Utils.curr_track_id == 0:
                Utils.curr_track_id = len(tracks) - 1
            else:
                Utils.curr_track_id -= 1
            try:
                item = tracks[Utils.curr_track_id]
                Utils.speak_text(Utils.convert_text(item.track.name))
            except Exception as e:
                print(str(e))

    def track_list_enter(self):
        # enter on track list
        tracks = self.core.tracklist.tl_tracks.get()
        if len(tracks) == 0:
            pass
        else:
            item = tracks[Utils.curr_track_id]
            Utils.speak('PLAY_URI', val=item.track.name)
            self.core.playback.play(tlid=item.tlid)

    def track_list_next(self):
        # next on track list
        tracks = self.core.tracklist.tl_tracks.get()
        if len(tracks) == 0:
            pass
        else:
            if len(tracks) == Utils.curr_track_id + 1:
                Utils.curr_track_id = 0
            else:
                Utils.curr_track_id += 1
            try:
                item = tracks[Utils.curr_track_id]
                Utils.speak_text(Utils.convert_text(item.track.name))

            except Exception as e:
                print(str(e))

    def player_play_pause(self):
        if self.core.playback.state.get() == PlaybackState.PLAYING:
            self.core.playback.pause()
            Utils.speak('PAUSE')
        else:
            Utils.speak('PLAY')
            self.core.playback.play()

    def go_to_library(self):
        # go up in library
        Utils.speak('LIBRARY')
        self.core.library.browse(url)
        self.current_mode = C_MODE_LIBRARY

    def go_to_player(self):
        # go to player mode
        Utils.speak('PLAYER')
        self.current_mode = C_MODE_PLAYER

    def change_lang(self):
        if Utils.lang == 'pl':
            Utils.lang = 'en'
            Utils.speak_text('English')
        else:
            Utils.lang = 'pl'
            Utils.speak_text('Polski')

    def lib_prev(self):
        # prev in library
        if len(Utils.lib_items) == 0:
            pass
        else:
            if Utils.curr_lib_item_id == 0:
                Utils.curr_lib_item_id = len(Utils.lib_items) - 1
            else:
                Utils.curr_lib_item_id -= 1
            try:
                item = Utils.lib_items[Utils.curr_lib_item_id]
                Utils.speak_text(Utils.convert_text(item.name))
            except Exception as e:
                print(str(e))

    def lib_enter(self):
        # enter in library
        if len(Utils.lib_items) > 0:
            current_item = Utils.lib_items[Utils.curr_lib_item_id]
            if current_item.type == 'track':
                self.core.tracklist.clear()
                self.core.tracklist.add(uri=current_item.uri)
                self.core.playback.play()
                Utils.speak('PLAY_URI', val=current_item.name)
                # get info about tracklist
                Utils.curr_track_id = 0
                Utils.track_items = self.core.tracklist.get_tracks()
            else:
                self.core.library.browse(current_item.uri)
                Utils.speak('ENTER_DIR', val=current_item.name)

    def lib_next():
        # next in library
        if len(Utils.lib_items) == 0:
            pass
        else:
            if len(Utils.lib_items) == Utils.curr_lib_item_id + 1:
                Utils.curr_lib_item_id = 0
            else:
                Utils.curr_lib_item_id += 1
            try:
                item = Utils.lib_items[Utils.curr_lib_item_id]
                Utils.speak_text(Utils.convert_text(item.name))

            except Exception as e:
                print(str(e))

    def onCommand(self, cmd):
        if cmd == 'track_list_prev':
            self.track_list_prev()

        if cmd == 'track_list_enter':
            self.track_list_enter()

        if cmd == 'track_list_next':
            self.track_list_next()

        if cmd == 'player_prev':
            # prev in player
            self.core.playback.previous()

        if cmd == 'player_next':
            # next in player
            self.core.playback.next()

        if cmd == 'player_play_pause':
            self.player_play_pause()

        if cmd == 'vol_down':
            vol = max(int(self.core.playback.volume.get()) - 10, 0)
            self.core.playback.volume = vol

        if cmd == 'vol_up':
            vol = min(int(self.core.playback.volume.get()) + 10, 100)
            self.core.playback.volume = vol

        if cmd == 'change_lang':
            self.change_lang()

        if cmd == 'ask_bot':
            try:
                ai.ask_bot(self.config)
            except Exception:
                str("Error in ai.ask_bot")
                traceback.print_exc()

        if cmd == 'backlight_up':
            Utils.backlight_up()

        if cmd == 'backlight_down':
            Utils.backlight_down()

        if cmd == 'lib_root_dir':
            self.go_to_library()

        if cmd == 'lib_prev':
            self.lib_prev()

        if cmd == 'lib_enter':
            self.lib_enter()

        if cmd == 'lib_next':
            self.lib_next()

        if cmd == 'lib_audiobook':
            Utils.speak('AUDIOBOOKS_DIR')
            uri = url + '/Audiobuki'
            self.core.library.browse(uri)

        if cmd == 'lib_radio':
            Utils.speak('RADIO_DIR')
            uri = url + '/Radia'
            self.core.library.browse(uri)

        if cmd == 'lib_music':
            Utils.speak('MUSIC_DIR')
            uri = url + '/Muzyka'
            self.core.library.browse(uri)
