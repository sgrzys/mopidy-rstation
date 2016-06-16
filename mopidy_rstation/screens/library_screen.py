# This Python file uses the following encoding: utf-8
from base_screen import BaseScreen

import mopidy.models
import logging

from ..graphic_utils import ListView
from ..tts import tts

logger = logging.getLogger(__name__)


class LibraryScreen(BaseScreen):
    def __init__(self, size, base_size, manager, fonts):
        BaseScreen.__init__(self, size, base_size, manager, fonts)
        self.list_view = ListView((0, 0), (
            self.size[0], self.size[1] -
            self.base_size), self.base_size, self.fonts['base'])
        self.directory_list = []
        self.current_directory = None
        self.library = None
        self.library_strings = None
        self.browse_uri(None)

    def go_inside_directory(self, uri):
        self.directory_list.append(self.current_directory)
        self.current_directory = uri
        self.browse_uri(uri)

    def browse_uri(self, uri):
        self.library_strings = []
        if uri is not None:
            self.library_strings.append("../")
            logger.debug('browse_uri: ' + str(uri))
        self.library = self.manager.core.library.browse(uri).get()
        for lib in self.library:
            self.library_strings.append(lib.name)
        self.list_view.set_list(self.library_strings)

    def go_up_directory(self):
        if len(self.directory_list):
            directory = self.directory_list.pop()
            self.current_directory = directory
            self.browse_uri(directory)

    def should_update(self):
        return self.list_view.should_update()

    def update(self, screen, update_type, rects):
        update_all = (update_type == BaseScreen.update_all)
        self.list_view.render(screen, update_all, rects)

    def touch_event(self, touch_event):
        clicked = self.list_view.touch_event(touch_event)
        selected = self.list_view.selected
        if self.library_strings[0] == "../":
                selected = selected - 1
        if selected == -1:
            if tts.lang == 'pl':
                selected_name = u'Wyjście do góry'
            else:
                selected_name = u'Up'
        else:
            selected_name = self.library[selected].name
        print(selected_name)

        if clicked is not None:
            if self.current_directory is not None:
                if clicked == 0:
                    self.go_up_directory()
                    tts.speak('GO_UP_DIR')
                else:
                    if self.library[clicked - 1].type\
                            == mopidy.models.Ref.TRACK:
                        self.play_uri(clicked-1)
                        tts.speak(
                            'PLAY_URI', val=selected_name)
                    else:
                        self.go_inside_directory(
                            self.library[clicked - 1].uri)
                        tts.speak(
                            'ENTER_DIR', val=selected_name)
            else:
                self.go_inside_directory(self.library[clicked].uri)
                tts.speak(
                    'ENTER_DIR', val=selected_name)
        else:
            tts.speak('LIST_ITEM', val=selected_name)

    def play_uri(self, track_pos):
        self.manager.core.tracklist.clear()
        tracks = []
        for item in self.library:
            if item.type == mopidy.models.Ref.TRACK:
                tracks.append(self.manager.core.library.lookup(
                    item.uri).get()[0])
            else:
                track_pos -= 1
        self.manager.core.tracklist.add(tracks)
        self.manager.core.playback.play(
            tl_track=self.manager.core.tracklist.tl_tracks.get()
            [track_pos])
