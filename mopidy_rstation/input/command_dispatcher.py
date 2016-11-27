from ..utils import Utils
from mopidy.core import PlaybackState
from ..witai import ai
import traceback
import time
from ..audio import sounds

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
        self.current_mode = None
        self.change_mode_time = None
        buttonPressEvent.append(self.handleCommand)

    def handleCommand(self, cmd):
        # sounds.play(sounds.C_SOUND_BEEP)
        sounds.beep()
        # send the command to all the
        # CoreListener.send("handleRemoteCommand", cmd=cmd)
        self.onCommand(cmd)

    def track_list_prev(self):
        print('track_list_prev')
        # prev on track list
        self.change_mode(C_MODE_TRACKLIST)
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

    def track_list_next(self):
        print('track_list_next')
        # next on track list
        self.change_mode(C_MODE_TRACKLIST)
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

    def track_list_enter(self):
        print('track_list_enter')
        # enter on track list
        # switch to player mode
        self.change_mode(C_MODE_PLAYER)
        tracks = self.core.tracklist.tl_tracks.get()
        if len(tracks) == 0:
            pass
        else:
            item = tracks[Utils.curr_track_id]
            Utils.speak('PLAY_URI', val=item.track.name)
            self.core.playback.play(tlid=item.tlid)

    def player_play_pause(self):
        print('player_play_pause')
        if self.core.playback.state.get() == PlaybackState.PLAYING:
            self.core.playback.pause()
            Utils.speak('PAUSE')
        else:
            Utils.speak('PLAY')
            self.core.playback.play()

    def go_to_library(self):
        print('go_to_library')
        # go up in library
        Utils.speak('LIBRARY')
        self.core.library.browse(url)
        self.change_mode(C_MODE_LIBRARY)

    def go_to_player(self):
        print('go_to_player')
        # go to player mode
        Utils.speak('PLAYER')
        self.change_mode(C_MODE_PLAYER)

    def change_lang(self):
        print('change_lang from: ' + Utils.config['language'])
        if Utils.config['language'] == 'pl-PL':
            Utils.change_lang('en-US')
        else:
            Utils.change_lang('pl-PL')
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
                print('#########' + current_item.uri + '#########')
                self.core.tracklist.add(uri=current_item.uri)
                self.core.playback.play()
                Utils.speak('PLAY_URI', val=current_item.name)
                # get info about tracklist
                Utils.curr_track_id = 0
                Utils.track_items = self.core.tracklist.get_tracks()
            else:
                self.core.library.browse(current_item.uri)
                Utils.speak('ENTER_DIR', val=current_item.name)

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
                Utils.speak_text(Utils.convert_text(item.name))

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
            Utils.speak_text(Utils.convert_text(item.name))
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
        Utils.speak('UP_DIR', val=name)

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
        Utils.speak('AUDIOBOOKS_DIR')
        uri = url + '/Audiobuki'
        self.core.library.browse(uri)

    def lib_radio(self):
        Utils.speak('RADIO_DIR')
        uri = url + '/Radia'
        self.core.library.browse(uri)

    def lib_music(self):
        Utils.speak('MUSIC_DIR')
        uri = url + '/Muzyka'
        self.core.library.browse(uri)

    def change_mode(self, mode):
        print('change_mode to ' + mode)
        self.change_mode_time = time.time()
        self.current_mode = mode

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
                # revert Utils.curr_track_id
                try:
                    tl_track = self.core.playback.get_current_tl_track().get()
                    track = tl_track.track
                    print(track.name)

                    tracks = self.core.tracklist.tl_tracks.get()
                    if len(tracks) == 0:
                        Utils.curr_track_id = 0
                    else:
                        for i, val in enumerate(tracks):
                            if val.track.name == track.name:
                                print(
                                    'Utils.curr_track_id rested to ' + str(i))
                                Utils.curr_track_id = i
                except Exception as e:
                    print(e)

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
