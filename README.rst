=============
znc-relay-out
=============
.. image:: https://circleci.com/gh/nerdfarm/znc-relay-out.svg?style=shield&circle-token=bf98652abc0adcbf2b423f50d33b23dae20ed1ef
``znc-relay-out`` is a Python ZNC module for passing IRC messages to mosquitto.

Intended for use with `obs <https://github.com/nerdfarm/obs>`_, a service for `mosquitto <http://mosquitto.org>`_ messages to Google Hangouts

Dependencies
============
- ZNC built with ``--enable-python``
- ``modpython``
- Python dependencies (``pip install``): 
  - ``paho-mqtt``

Installation
============
1. Install the dependencies listed above
2. Copy ``relay_out.py`` to your ZNC profile
3. Load the ZNC module

These module parameters are required::

    --topic         mosquitto topic to subscribe, messages from IRC will be published to this topic
    --host          mosquitto host
    --port          mosquitto port
    --qos           mosquitto QOS for the subscribing connection
    --client-id     mosquitto subscribing client ID
    --network-name  ZNC-configured IRC network name
    --channel       IRC channel (including #) to publish messages

Example::

    /msg *status loadmod relay_out --topic=a_topic --host=localhost --port=1883 --qos=2 --client-id=an_id --network-name=irc_network --channel=#channel

Configuration
=============
All required parameters should be passed on module load, see example under ``Installation``.
Currently, no module commands to configure while module is loaded. Reload with new parameters if needed.

License
=======
MIT
