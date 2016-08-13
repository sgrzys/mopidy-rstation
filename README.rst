******************
Mopidy-rstation
******************

Extension for remotely controlling Mopidy

Dependencies
============

- ``Mopidy`` >= 1.0
- ``Pykka`` >= 1.1


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
