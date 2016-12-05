from ..utils import Utils
from mopidy.core import PlaybackState
from ..witai import ai
import traceback
import time
from ..audio import sounds
from ..audio import voices

LIRC_PROG_NAME = "mopidyRstation"
C_MODE_PLAYER = 'PLAYER'
C_MODE_LIBRARY = 'LIBRARY'
C_MODE_TRACKLIST = 'TRACKLIST'
current_tl_track = None
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
        self.current_mode = None
        self.change_mode_time = None
        buttonPressEvent.append(self.handleCommand)

    def handleCommand(self, cmd):
        sounds.beep()
        # send the command to all the
        # CoreListener.send("handleRemoteCommand", cmd=cmd)
        self.onCommand(cmd)

    def track_list_prev(self):
        print('track_list_prev')
        global current_tl_track
        # prev on track list
        self.change_mode(C_MODE_TRACKLIST)
        try:
            if current_tl_track is None:
                current_tl_track = \
                    self.core.playback.get_current_tl_track().get()
            current_tl_track = self.core.tracklist.previous_track(
                current_tl_track).get()
            track = current_tl_track.track
            if track is not None:
                voices.speak_text(voices.convert_text(track.name))
        except Exception:
            current_tl_track = Utils.core.tracklist.tl_tracks.get()[-1]

    def track_list_next(self):
        global current_tl_track
        print('track_list_next')
        # next on track list
        self.change_mode(C_MODE_TRACKLIST)
        try:
            if current_tl_track is None:
                current_tl_track = \
                    self.core.playback.get_current_tl_track().get()
            current_tl_track = self.core.tracklist.next_track(
                current_tl_track).get()
            track = current_tl_track.track
            if track is not None:
                voices.speak_text(voices.convert_text(track.name))
        except Exception:
            current_tl_track = Utils.core.tracklist.tl_tracks.get()[0]

    def track_list_enter(self):
        global current_tl_track
        print('track_list_enter')
        # enter on track list
        # switch to player mode
        if current_tl_track is None:
            current_tl_track = \
                self.core.playback.get_current_tl_track().get()
        track = current_tl_track.track
        voices.speak('PLAY_URI', val=track.name)
        self.core.playback.play(tlid=current_tl_track.tlid)
        self.change_mode(C_MODE_PLAYER)

    def player_play_pause(self):
        print('player_play_pause')
        if self.core.playback.state.get() == PlaybackState.PLAYING:
            self.core.playback.pause()
            voices.speak('PAUSE')
        else:
            voices.speak('PLAY')
            self.core.playback.play()

    def go_to_library(self):
        print('go_to_library')
        # go up in library
        voices.speak('LIBRARY')
        self.core.library.browse(url)
        self.change_mode()

    def go_to_player(self):
        print('go_to_player')
        # go to player mode
        voices.speak('PLAYER')
        self.change_mode(C_MODE_PLAYER)

    def change_lang(self):
        print('change_lang from: ' + Utils.config['language'])
        if Utils.config['language'] == 'pl-PL':
            Utils.config['language'] = 'en-US'
            voices.speak_text('English')
        elif Utils.config['language'] == 'en-US':
            Utils.config['language'] = 'pl-PL'
            voices.speak_text('Polski')
        print('change_lang to: ' + Utils.config['language'])

    def lib_enter(self):
        print('lib_enter')
        # enter in library
        if len(Utils.lib_items) > 0:
            current_item = Utils.lib_items[Utils.curr_lib_item_id]
            if current_item.type == 'track':
                # switch to player mode
                self.change_mode(C_MODE_PLAYER)
                self.core.tracklist.clear()
                self.core.tracklist.add(uri=current_item.uri)
                self.core.playback.play()
                voices.speak('PLAY_URI', val=current_item.name)
            else:
                self.core.library.browse(current_item.uri)
                voices.speak('ENTER_DIR', val=current_item.name)

    def lib_next(self):
        print('lib_next')
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
                voices.speak_text(voices.convert_text(item.name))

            except Exception as e:
                print(str(e))

    def lib_prev(self):
        print('lib_prev')
        # prev in library
        if len(Utils.lib_items) == 0:
            return
        if Utils.curr_lib_item_id == 0:
            Utils.curr_lib_item_id = len(Utils.lib_items) - 1
        else:
            Utils.curr_lib_item_id -= 1
        try:
            item = Utils.lib_items[Utils.curr_lib_item_id]
            voices.speak_text(voices.convert_text(item.name))
        except Exception as e:
            print(str(e))

    def lib_up(self):
        print('lib_up')
        if len(Utils.lib_items) == 0:
            pass
        item = Utils.lib_items[Utils.curr_lib_item_id]
        uri = item.uri.rsplit('/', 2)[0]
        name = item.uri.rsplit('/', 2)[1]
        self.core.library.browse(uri)
        voices.speak('UP_DIR', val=name)

    def lib_down(self):
        print('lib_down')
        self.lib_enter()

    def lib_next_dir(self):
        print('lib_next_dir')
        # next dir in library
        u = Utils.lib_items[Utils.curr_lib_item_id].uri
        if u.startswith(url + '/Radia'):
            self.lib_audiobook()
        elif u.startswith(url + '/Audiobuki'):
            self.lib_music()
        elif u.startswith(url + '/Muzyka'):
            self.lib_radio()
        else:
            self.lib_radio()

    def lib_prev_dir(self):
        print('lib_prev_dir')
        # prev dir in library
        u = Utils.lib_items[Utils.curr_lib_item_id].uri
        if u.startswith(url + url + '/Radia'):
            self.lib_music()
        elif u.startswith(url + '/Audiobuki'):
            self.lib_radio()
        elif u.startswith(url + '/Muzyka'):
            self.lib_audiobook()
        else:
            self.lib_music()

    def lib_audiobook(self):
        voices.speak('AUDIOBOOKS_DIR')
        uri = url + '/Audiobuki'
        self.core.library.browse(uri)

    def lib_radio(self):
        voices.speak('RADIO_DIR')
        uri = url + '/Radia'
        self.core.library.browse(uri)

    def lib_music(self):
        voices.speak('MUSIC_DIR')
        uri = url + '/Muzyka'
        self.core.library.browse(uri)

    def change_mode(self, mode):
        global current_tl_track
        print('change_mode to ' + mode)
        self.change_mode_time = time.time()
        self.current_mode = mode
        if mode != C_MODE_TRACKLIST:
            current_tl_track = None

    def check_mode(self):
        # after start switch to PLAYER mode
        if self.current_mode is None:
            self.change_mode(C_MODE_PLAYER)

        # if nothing to play switch to LIBRARY mode
        tracks = self.core.tracklist.tl_tracks.get()
        if self.current_mode != C_MODE_LIBRARY and len(tracks) == 0:
            self.change_mode(C_MODE_LIBRARY)
        # if nothing was pressed after 10 seconds in mode TRACKLIST
        # switch back to PLAYER mode
        if self.current_mode == C_MODE_TRACKLIST:
            sec_left = time.time() - self.change_mode_time
            print('check_mode sec_left: ' + str(sec_left))
            if sec_left > 10:
                self.change_mode(C_MODE_PLAYER)

    def onCommand(self, cmd):
        print(cmd + ': on Command started, mode: ' + str(self.current_mode))
        self.check_mode()
        print('mode after check_mode: ' + self.current_mode)
        # main commands - avalible on each remote
        if cmd == 'mode':
            if len(self.core.tracklist.tl_tracks.get()) == 0:
                self.go_to_library()
            else:
                if self.current_mode == C_MODE_PLAYER:
                    self.go_to_library()
                else:
                    self.go_to_player()

        if cmd == 'left':
            if self.current_mode != C_MODE_LIBRARY:
                self.track_list_prev()
                self.track_list_enter()
            elif self.current_mode == C_MODE_LIBRARY:
                self.lib_prev()

        if cmd == 'right':
            if self.current_mode != C_MODE_LIBRARY:
                self.track_list_next()
                self.track_list_enter()
            elif self.current_mode == C_MODE_LIBRARY:
                self.lib_next()

        if cmd == 'up':
            if self.current_mode != C_MODE_LIBRARY:
                self.track_list_prev()
            elif self.current_mode == C_MODE_LIBRARY:
                self.lib_up()

        if cmd == 'down':
            if self.current_mode != C_MODE_LIBRARY:
                self.track_list_next()
            elif self.current_mode == C_MODE_LIBRARY:
                self.lib_down()

        if cmd == 'enter':
            if self.current_mode == C_MODE_PLAYER:
                self.player_play_pause()
            elif self.current_mode == C_MODE_TRACKLIST:
                self.track_list_enter()
            elif self.current_mode == C_MODE_LIBRARY:
                self.lib_enter()

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
            self.change_mode(C_MODE_PLAYER)
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

        if cmd == 'lib_up':
            self.lib_up()

        if cmd == 'lib_down':
            self.lib_down()

        if cmd == 'lib_enter':
            self.lib_enter()

        if cmd == 'lib_next':
            self.lib_next()

        if cmd == 'lib_audiobook':
            self.lib_audiobook()

        if cmd == 'lib_radio':
            self.lib_radio()

        if cmd == 'lib_music':
            self.lib_music()

        print(cmd + ': on Command ended, mode: ' + self.current_mode)
