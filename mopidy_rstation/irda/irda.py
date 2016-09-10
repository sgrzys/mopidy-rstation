# This Python file uses the following encoding: utf-8
import pylirc
import logging
import threading
import select
from mopidy.core import PlaybackState
import os
from threading import Thread
from ..utils import Utils

logger = logging.getLogger('mopidy_Rstation')
LIRC_PROG_NAME = "mopidyRstation"
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
        buttonPressEvent.append(self.handleCommand)

    def handleCommand(self, cmd):
        t = Thread(target=self.beep_thread)
        t.start()
        # send the command to all the
        # CoreListener.send("handleRemoteCommand", cmd=cmd)

        # handle command in frontend
        self.onCommand(cmd)

    def onCommand(self, cmd):
        if cmd == 'ch_minus':
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

        if cmd == 'ch':
            # enter on track list
            tracks = self.core.tracklist.tl_tracks.get()
            if len(tracks) == 0:
                pass
            else:
                item = tracks[Utils.curr_track_id]
                Utils.speak('PLAY_URI', val=item.track.name)
                self.core.playback.play(tlid=item.tlid)

        if cmd == 'ch_plus':
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

        if cmd == 'prev':
            # prev in player
            self.core.playback.previous()

        if cmd == 'next':
            # next in player
            self.core.playback.next()

        if cmd == 'play_pause':
            if self.core.playback.state.get() == PlaybackState.PLAYING:
                self.core.playback.pause()
                Utils.speak('PAUSE')
            else:
                Utils.speak('PLAY')
                self.core.playback.play()

        if cmd == 'vol_down':
            vol = max(int(self.core.playback.volume.get()) - 10, 0)
            self.core.playback.volume = vol

        if cmd == 'vol_up':
            vol = min(int(self.core.playback.volume.get()) + 10, 100)
            self.core.playback.volume = vol

        if cmd == 'eq':
            if Utils.lang == 'pl':
                Utils.lang = 'en'
                Utils.speak_text('English')
            else:
                Utils.lang = 'pl'
                Utils.speak_text('Polski')

        if cmd == 'num0':
            pass

        if cmd == 'fl_plus':
            Utils.backlight_up()

        if cmd == 'fl_minus':
            Utils.backlight_down()

        if cmd == 'num2':
            # go up in library
            Utils.speak('CHP')
            self.core.library.browse(url)

        if cmd == 'num4':
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

        if cmd == 'num5':
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

                if cmd == 'num2':
                    # library go to level 0
                    self.core.library.browse(url)
                    Utils.speak('CHP')

        if cmd == 'num6':
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

        if cmd == 'num7':
            Utils.speak('AUDIOBOOKS_DIR')
            uri = url + '/Audiobuki'
            self.core.library.browse(uri)

        if cmd == 'num8':
            Utils.speak('RADIO_DIR')
            uri = url + '/Radia'
            self.core.library.browse(uri)

        if cmd == 'num9':
            Utils.speak('MUSIC_DIR')
            uri = url + '/Muzyka'
            self.core.library.browse(uri)

    def beep_thread(self):
        cmd = "aplay /home/pi/mopidy-rstation/Ulubione/covers/"
        cmd += "alert.wav > /dev/null 2>&1"
        os.system(cmd)

    def registerHandler(self, cmd, handler):
        self._handlers[cmd] = handler


class LircThread(threading.Thread):
    def __init__(self, configFile):
        threading.Thread.__init__(self)
        self.name = 'Lirc worker thread'
        self.configFile = configFile
        self.frontendActive = True
        self.ButtonPressed = Event()

    def run(self):
        try:
            self.run_inside_try()
        except Exception as e:
            logger.warning('Rstation has problems starting pylirc: ' + str(e))

    def run_inside_try(self):
        self.startPyLirc()

    def startPyLirc(self):
        logger.debug('Rstation start pylirc')
        lircHandle = pylirc.init(LIRC_PROG_NAME, self.configFile, 0)
        if(lircHandle != 0):
            while(self.frontendActive):
                self.consumePylirc(lircHandle)
            pylirc.exit()

    def consumePylirc(self, lircHandle):
        try:
            if(select.select([lircHandle], [], [], 1) == ([], [], [])):
                pass
            else:
                s = pylirc.nextcode(1)
                self.handleNextCode(s)
        except Exception as e:
            logger.warning('Exception during handling a command: ' + str(e))

    def handleNextCode(self, s):
        if s:
            self.handleLircCode(s)

    def handleLircCode(self, s):
        for code in s:
            self.handleCommand(code['config'])

    def handleCommand(self, cmd):
        self.ButtonPressed(cmd)
