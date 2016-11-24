******************
Mopidy-rstation
******************

Extension for remotely controlling Mopidy

Dependencies
============

- ``Mopidy`` >= 2.1
- ``Pykka`` >= 1.1


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
    wit_token = XXX
    ivona_access_key = XXX
    ivona_secret_key = X/X
    language = pl-PL
    location = Wrocław
    weather_api_key = XXX
    audio_in_name = Airmouse: USB Audio
