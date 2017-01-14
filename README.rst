******************
Mopidy-rStation
******************

Extension for remotely controlling Mopidy

Dependencies
============

- ``Mopidy`` >= 2.1
- ``Pykka`` >= 1.1
- ``geopy``
- ``wikipedia``
- ``fuzzywuzzy``
- ``pyaudio``
- ``python-i18n``
- ``evdev``
- ``python-Levenshtein``


System Requirements
============
- apt install python-gst-1.0 \
    gir1.2-gstreamer-1.0 gir1.2-gst-plugins-base-1.0 \
    gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly \
    gstreamer1.0-plugins-bad gstreamer1.0-tools \
    python-alsaaudio python-pygame build-essential \
    python-dev python-pip portaudio19-dev python-all-dev \
    python-pyudev gstreamer1.0-alsa gstreamer0.10-alsa at



Installation
============

Install by running::

    git clone https://github.com/araczkowski/mopidy-rstation.git

    cd rstation

    pip install . -U


Basic Configuration
===================

Before starting Mopidy, you must add configuration for
Mopidy-Rstation to your Mopidy configuration file::

    [rstation]
    enabled = true
    wit_token_pl = XXX
    wit_token_en = XXX
    wit_token_ru = XXX
    wit_token_fr = XXX
    ivona_access_key = XXX
    ivona_secret_key = X/X
    language = pl-PL
    voice_name = Ewa
    location_gps = 51.199688,16.6093018
    weather_api_key = XXX
    audio_in_name = Airmouse: USB Audio
    audio_out_name = hdmi
    media_dir = /home/pi/media
    media_remote_url =  https://xxx/yyy/media.git
    app_source_dir = /home/pi/mopidy-rstation
    app_source_remote_url = https://xxx/yyy/mopidy-rstation.git
