About pi-jukebox
================

Pi-Jukebox is an mpd client application which you can use with a 
Raspberry Pi with touchscreen. 

Do you have a huge music collection and wanted to be able to access it 
anywhere in your house? I did. I was inspired by some other Raspberry Pi
projects, like adafruit's pi radio project_. I wanted my music player to be able to access my music from my 
NAS drive, but also wanted to be able to play music brought by friends 
on their USB stick. These projects brought me to mpd: a music server program 
that allows you to control enormous amounts of music. It is easy to search 
through your music collection and play it. mpd has many client apps 
by which you can control your music on loads of different devices. But...
What if there's no wifi access? You must be able to control the device 
directly: enter the touchscreen and enter pi-jukebox.

Future plans include:
    - Modipy support.
    - Bluetooth streaming.
    - Switching between single room and multi-room simultaneous playback.
    - Although it is made with a adafruit 320x240 
      touchscreen in mind, it should be fairly simple to adjust it for larger 
      screens (in later versions I'm planning to do some scaling).

Running pi-jukebox on your Raspberry Pi
---------------------------------------

Be sure to check the value of **MPD_MUSIC_DIR** in the **mpd_client.py**, this should point to your music library (found in the **music_directory** entry of **mpd.conf**. Run pi-jukebox with:
    .. code-block:: bash

       sudo python pi-jukebox.py
       
.. _project: https://learn.adafruit.com/raspberry-pi-radio-player-with-touchscreen/overview       
