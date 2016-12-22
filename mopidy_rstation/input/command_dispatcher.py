from ..utils import Utils
from mopidy.core import PlaybackState
from ..witai import ai
import traceback
import time
from ..audio import sounds
from ..audio import voices
from mopidy_rstation.config.settings import Config
from mopidy_rstation.config.settings import Settings

LIRC_PROG_NAME = "mopidyRstation"
C_MODE_PLAYER = 'PLAYER'
C_MODE_LIBRARY = 'LIBRARY'
C_MODE_TRACKLIST = 'TRACKLIST'
C_MODE_SETTINGS = 'SETTINGS'
current_tl_track = None
url = u'rstation:' + Config.get_config()['media_dir']


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
        self.current_mode = C_MODE_LIBRARY
        self.change_mode_time = None
        buttonPressEvent.append(self.handleCommand)

    def handleCommand(self, cmd):
        if cmd == 'vol_down' or cmd == 'vol_up':
            None
        else:
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
            track = current_tl_track.track
            if track is not None:
                voices.speak_text(voices.convert_text(track.name))

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
            track = current_tl_track.track
            if track is not None:
                voices.speak_text(voices.convert_text(track.name))

    def track_list_enter(self):
        global current_tl_track
        print('track_list_enter')
        # enter on track list
        # switch to player mode
        if current_tl_track is None:
            current_tl_track = \
                self.core.playback.get_current_tl_track().get()
        # track = current_tl_track.trackvoices.speak
        # voices.speak('PLAY_URI', val=track.name)
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
        voices.speak('LIBRARY')
        # go up in library
        self.core.library.browse(url)
        self.change_mode(C_MODE_LIBRARY)

    def go_to_settings(self):
        print('go_to_settings')
        voices.speak('SETTINGS')
        self.change_mode(C_MODE_SETTINGS)
        Settings.G_MAIN_MENU_CURRENT = ''
        Settings.G_MAIN_MENU_FOCUS = ''
        Settings.G_MENU_CURRENT = ''
        Settings.G_MENU_FOCUS = ''

    def go_to_player(self):
        print('go_to_player')
        voices.speak('PLAYER')
        self.change_mode(C_MODE_PLAYER)

    def change_lang(self):
        Config.switch_current_lang()

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
                # voices.speak('PLAY_URI', val=current_item.name)
            else:
                self.core.library.browse(current_item.uri)
                t = voices.convert_text(
                    current_item.name, remove_file_extension=True)
                text = ''
                codes = 'ENTER_DIR'
                if t == 'Audiobooks':
                    codes = ['ENTER_DIR', 'AUDIOBOOKS_DIR']
                elif t == 'Music':
                    codes = ['ENTER_DIR', 'MUSIC_DIR']
                elif t == 'Podcasts':
                    codes = ['ENTER_DIR', 'PODCAST_DIR']
                elif t == 'Radio':
                    codes = ['ENTER_DIR', 'RADIO_DIR']
                else:
                    text = t
                voices.speak(codes, val=text)

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
                self.speak_lib_item(
                    voices.convert_text(item.name, remove_file_extension=True))

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
            self.speak_lib_item(
                voices.convert_text(item.name, remove_file_extension=True))
        except Exception as e:
            print(str(e))

    def speak_lib_item(self, name):
        if name == 'Audiobooks':
            voices.speak('AUDIOBOOKS_DIR')
        elif name == 'Music':
            voices.speak('MUSIC_DIR')
        elif name == 'Podcasts':
            voices.speak('PODCAST_DIR')
        elif name == 'Radio':
            voices.speak('RADIO_DIR')
        else:
            voices.speak_text(
                voices.convert_text(name, remove_file_extension=True))

    def lib_up(self):
        print('lib_up')
        item = Utils.lib_items[Utils.curr_lib_item_id]
        uri = item.uri.rsplit('/', 2)[0]
        name = item.uri.rsplit('/', 3)[1]
        self.core.library.browse(uri)
        if name == 'pi':
            voices.speak('LIBRARY')
            return
        text = ''
        codes = 'UP_DIR'
        if name == 'Audiobooks':
            codes = ['UP_DIR', 'AUDIOBOOKS_DIR']
        elif name == 'Music':
            codes = ['UP_DIR', 'MUSIC_DIR']
        elif name == 'Podcasts':
            codes = ['UP_DIR', 'PODCAST_DIR']
        elif name == 'Radio':
            codes = ['UP_DIR', 'RADIO_DIR']
        elif name == 'media':
            codes = ['UP_DIR', 'LIBRARY']
        else:
            text = name
        voices.speak(codes, val=text)

    def lib_down(self):
        print('lib_down')
        self.lib_enter()

    def lib_next_dir(self):
        print('lib_next_dir')
        # next dir in library
        u = Utils.lib_items[Utils.curr_lib_item_id].uri
        if u.startswith(url + '/Radio'):
            self.lib_audiobook()
        elif u.startswith(url + '/Audiobooks'):
            self.lib_music()
        elif u.startswith(url + '/Music'):
            self.lib_radio()
        else:
            self.lib_radio()

    def lib_prev_dir(self):
        print('lib_prev_dir')
        # prev dir in library
        u = Utils.lib_items[Utils.curr_lib_item_id].uri
        if u.startswith(url + url + '/Radio'):
            self.lib_music()
        elif u.startswith(url + '/Audiobooks'):
            self.lib_radio()
        elif u.startswith(url + '/Music'):
            self.lib_audiobook()
        else:
            self.lib_music()

    def lib_audiobook(self):
        voices.speak('AUDIOBOOKS_DIR')
        uri = url + '/Audiobooks'
        self.core.library.browse(uri)

    def lib_radio(self):
        voices.speak('RADIO_DIR')
        uri = url + '/Radio'
        self.core.library.browse(uri)

    def lib_music(self):
        voices.speak('MUSIC_DIR')
        uri = url + '/Music'
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
            self.change_mode(C_MODE_LIBRARY)

        # if nothing to play switch to LIBRARY mode
        elif self.current_mode == C_MODE_PLAYER:
            if len(self.core.tracklist.tl_tracks.get()) == 0:
                self.change_mode(C_MODE_LIBRARY)
        # if nothing was pressed after 10 seconds in mode TRACKLIST
        # switch back to PLAYER mode
        elif self.current_mode == C_MODE_TRACKLIST:
            sec_left = time.time() - self.change_mode_time
            print('check_mode sec_left: ' + str(sec_left))
            if sec_left > 10:
                self.change_mode(C_MODE_PLAYER)

        # if nothing was pressed after 20 seconds in mode SETTINGS
        # switch back to LIBRARY or PLAYER mode
        elif self.current_mode == C_MODE_SETTINGS:
            sec_left = time.time() - self.change_mode_time
            print('check_mode sec_left: ' + str(sec_left))
            if sec_left > 20:
                if len(self.core.tracklist.tl_tracks.get()) == 0:
                    self.change_mode(C_MODE_LIBRARY)
                else:
                    self.change_mode(C_MODE_PLAYER)
        # reset the change mode time after echa command
        self.change_mode_time = time.time()

    def onCommand(self, cmd):
        # main commands - avalible on each remote
        if cmd == 'mode':
            if self.current_mode == C_MODE_PLAYER or \
               self.current_mode == C_MODE_TRACKLIST:
                    self.go_to_library()
                    return
            elif self.current_mode == C_MODE_LIBRARY:
                self.go_to_settings()
                return
            elif self.current_mode == C_MODE_SETTINGS:
                self.go_to_player()
                return
        # test/change the current mode
        print(cmd + ': on Command started, mode: ' + str(self.current_mode))
        self.check_mode()
        print('mode after check_mode: ' + self.current_mode)
        # test/change the current mode
        if self.current_mode == C_MODE_SETTINGS:
            return Settings.onCommand(cmd)
            # TODO the same for all modes should be done

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
                self.core.playback.pause()
                ai.ask_bot()
            except Exception:
                str("Error in ai.ask_bot")
                traceback.print_exc()

        if cmd == 'ask_bot_2':
            self.change_mode(C_MODE_PLAYER)
            try:
                self.core.playback.pause()
                ai.ask_bot('sysdefault')
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
