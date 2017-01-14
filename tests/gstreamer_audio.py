#!/usr/bin/env python
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

Gst.init(None)
mainloop = GObject.MainLoop()

# setting up a single "playbin" element which
# handles every part of the playback by itself
pl = Gst.ElementFactory.make("playbin", "player")
# copy a track to /tmp directory, just for testing
pl.set_property(
    'uri',
    'file://home/andrzej/speech_cache/0cd0f19fe384bab2e22e135a802828d4.ogg')
# setting the volume property for the playbin element, as an example
# pl.set_property('volume', 1)

# running the playbin
pl.set_state(Gst.State.PLAYING)
mainloop.run()
print('OK')
