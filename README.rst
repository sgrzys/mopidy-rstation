******************
Mopidy-rstation
******************

Extension for reading track info and controlling Mopidy via IR remote

Dependencies
============

- ``Mopidy`` >= 1.0
- ``Pykka`` >= 1.1
- ``pygame``


Installation
============

Install by running::

    clone rstation

    cd rstation

    pip install . --upgrade


Basic Configuration
===================

Before starting Mopidy, you must add configuration for
Mopidy-Rstation to your Mopidy configuration file::

    [rstation]
    enabled = true
    screen_width = 320
    screen_height = 240
    resolution_factor = 8
    cursor = True
    fullscreen = False
    cache_dir = $XDG_CACHE_DIR/mopidy/touchscreen

The following configuration values are available:

- ``touchscreen/enabled``: If the Touchscreen extension should be enabled or
  not.

- ``touchscreen/screen_width``: The width of the resolution you want to use in
  pixels.

- ``touchscreen/screen_height``: The width of the resolution you want to use in
  pixels.

- ``touchscreen/resolutin_factor``: This value sets how big content is shown. Smaller values will make content bigger and less content will be displayed at once.

- ``touchscreen/cursor``: If the mouse cursor should be shown. (If you use a
  touchscreen it should be false)

- ``touchscreen/fullscreen``: If you want to be shown as a window or in
  fullscreen.

- ``touchscreen/cache_dir``: The folder to be used as cache. Defaults to
  ``$XDG_CACHE_DIR/mopidy/touchscreen``, which usually means
  ``~/.cache/mopidy/touchscreen``


How to Setup
============

Use the basic configuration to setup as most standard screens works fine without further configuration.

Raspberry Pi
------------

If you are using this on a raspberry pi you have to run mopidy with root privileges:

Run Mopidy with root privileges
```````````````````````````````

You can use ``sudo mopidy``.

In case you are using musicbox edit ``/etc/init.d/mopidy`` file. Change ``DAEMON_USER=mopidy`` to ``DAEMON_USER=root``

Do not forget that this is a workaround and that mopidy will run with root privileges.

LCD Shields
```````````

If you are using a LCD Shield in Raspberry Pi you need to config your LCD:

Configure your LCD Shield
'''''''''''''''''''''''''

Add to the config the next variables::

    [touchscreen]
    sdl_fbdev = /dev/fb1
    sdl_mousdrv = TSLIB
    sdl_mousedev = event0

This is just an example. It may work but each LCD Shield seems to have its own configuration.
To find your values find an example of using pygame with your LCD Shield and it should be something like this in the code::

    os.environ["SDL_FBDEV"] = "/dev/fb1"
    os.environ["SDL_MOUSEDRV"] = "TSLIB"
    os.environ["SDL_MOUSEDEV"] = "event0"

GPIO Buttons
````````````

You can use GPIO buttons to controll mopidy touchscreen. To do that set the configuration::

    [touchscreen]
    gpio = True
    gpio_left = 4
    gpio_right = 27
    gpio_up = 22
    gpio_down = 23
    gpio_enter = 24

You can choose what pins to use:

- ``touchscreen/gpio``: If you want to use gpio buttons. If this is set to false other gpio configuration values will be ignored.
- ``touchscreen/gpio_left``: Pin used to simulate left key press.
- ``touchscreen/gpio_right``: Pin used to simulate right key press.
- ``touchscreen/gpio_up``: Pin used to simulate up key press.
- ``touchscreen/gpio_down``: Pin used to simulate down key press.
- ``touchscreen/gpio_enter``: Pin used to simulate enter key press.

All pins numbers are in BCM mode. You can check `here <http://raspberrypi.stackexchange.com/a/12967>`_ to see the numbers for your board.

The buttons must be connected to GROUND.

Pin - Button - Ground

How To Use
==========

You can use it with a touchscreen or mouse clicking on the icons.
In case you are using a keyboard use arrow keys to navigate and enter to select.
The GPIO buttons simulate keyboard keys so the use is exactly the same as using a keyboard.

Help
====

You can use `mopidy discuss <https://discuss.mopidy.com/>`_


Features
========




Screenshots
===========



Video
=====
