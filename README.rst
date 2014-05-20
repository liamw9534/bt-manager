****************************
BT-Manager
****************************

.. image:: https://pypip.in/version/BT-Manager/badge.png?latest
    :target: https://pypi.python.org/pypi/BT-Manager/
    :alt: Latest PyPI version

.. image:: https://pypip.in/download/BT-Manager/badge.png
    :target: https://pypi.python.org/pypi/BT-Manager/
    :alt: Number of PyPI downloads

.. image:: https://travis-ci.org/liamw9534/bt-manager.png?branch=master
    :target: https://travis-ci.org/liamw9534/bt-manager
    :alt: Travis CI build status

.. image:: https://coveralls.io/repos/liamw9534/bt-manager/badge.png?branch=master
   :target: https://coveralls.io/r/liamw9534/bt-manager?branch=master
   :alt: Test coverage

A library for managing bluetooth devices using Python, Bluez and DBus.

Installation
============

Install by running::

    pip install BT-Manager


Project resources
=================

- `Source code <https://github.com/liamw9534/BT-Manager>`_
- `Issue tracker <https://github.com/liamw9534/BT-Manager/issues>`_
- `Download development snapshot <https://github.com/liamw9534/BT-Manager/archive/master.tar.gz#egg=BT-Manager-dev>`_


Changelog
=========

v0.1.0 (UNRELEASED)
----------------------------------------

Initial release supporting Bluez 4.x dbus API with following interfaces:

- BTManager (org.bluez.Manager)
- BTAdapter (org.bluez.Adapter)
- BTDevice (org.bluez.Device)
- BTMedia (org.bluez.Media)
- BTMediaTransport (org.bluez.MediaTransport)
- BTAudioSource (org.bluez.AudioSource)
- BTAudioSink (org.bluez.AudioSink)

Services:

- BTAgent (org.bluez.Agent)
- SBCAudioSink (org.bluez.MediaEndpoint): endpoint/transport setup only
- SBCAudioSource (org.bluez.MediaEndpoint): endpoint/transport setup only

Other:

- UUID decoding for identifying supported services
- Class of device decoding to device service, major and minor classes
- Device vendors codes and names for device vendor decoding
- Audio codec types and SBC codec configuration attributes
