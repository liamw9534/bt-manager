*************
Configuration
*************

The :term:`bluez` stack has a number of different files and tools for configuration.
In general, these files and tools may only be accessed by a system administrator but are
an important prerequisite area of understanding before attempting to manage bluetooth
using the :term:`dbus` API.

Configuration files
===================

Not all configuration files or settings are described here, but the most
important ones are herein.

/etc/bluetooth/main.conf
~~~~~~~~~~~~~~~~~~~~~~~~

The top-level configuration aspects are defined in here.  The
``main.conf`` file is read by ``bluetoothd`` on start-up.  Note
that if you override any of the settings via dbus, these settings will
not be persistent and will only survive the lifetime of ``bluetoothd`` e.g.,
a reboot would result in the original settings being used.

.. code-block:: python

    [General]
    # This is how your bluetooth adapter is identified and introduced to
    # other bluetooth devices.  %h is the hostname and %d is a unique
    # identifier given to all bluetooth adapters when they are registered
    # to bluez.  The name can also be updated through dbus.
    Name = %h-%d

    # Modify this if you known in advance which applications or services
    # your device will provide.  The format follows the class of device
    # 24-bit identifier defined by bluetooth.
    # Note that this is for device identification convenience only and
    # does not prevent specific services or profiles from being activated
    # dynamically at a later date.
    # An implementation of a CoD decoder is part of the bt-manager python
    # library.
    Class = 0x000100

    # When entering discovery mode, this is the timeout before going back
    # to non-discovery mode.  Expressed in seconds.  0 means the device is always
    # discoverable.  This attribute may be set from dbus.
    DiscoverableTimeout = 0

    # When entering pairing mode, this is the timeout before dropping
    # back to non-discoverable mode.  Expressed in seconds.  0 means the
    # device is always in pairing mode.
    PairableTimeout = 0

    # Determined whether or not the adapter should be powered on start-up
    # or whether the user should power the adapter manually.  This
    # attribute can be set via dbus.
    InitallyPowered = true

    # Allows the device identification SDP attributes to be set for
    # vendor code, product code and version.  The format is:
    # assigner:vid:pid:version
    DeviceID = bluetooth:1234:5678:0100


/etc/bluetooth/audio.conf
~~~~~~~~~~~~~~~~~~~~~~~~~

The audio configuration is split into three main sections for General, HFP and
A2DP profiles.

.. code-block:: python

    [General]

    # A list of the services on the host, which grants or denies permissions for
    # applications to use these services.  Possible values are:
    # 
    # Source - enables AudioSource
    # Sink - enables AudioSink
    # Control - enables AVRCP
    # Media - enables media endpoint/transport
    # Socket - auto-enables service endpoint selection; do not enable this if you want
    #          to register your own service endpoints via dbus
    Enable = Source,Sink,Control,Media
    #Disable = Socket

    # SCO (Synchronous Connection Orientated) link routing setting for headset or HFP
    #
    # HCI => Host Control Interface (connection is handled by ALSA audio layer)
    # PCM => Pulse Coded Modulation
    #
    # Set to PCM if you wish for a dbus service to handle SCO transport.
    SCORouting = HCI

    # Boolean to determine whether or not to automatically connect all audio profiles
    # i.e., A2DP and HFP.
    AutoConnect = true

    [Headset]

    # Determine which headset profile to support i.e., HFP or HSP.
    HFP = true

    # Maximum number of headset connections to allow
    MaxConnected = 1

    [A2DP]

    # Maximum number of A2DP connections to allow (source or sink)
    MaxConnected = 1

/etc/dbus-1/system.d/bluetooth.conf
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This file describes the dbus access control policies for the
interfaces exported by bluez over dbus.  This determines which
bluez services are accessible over dbus and which users or groups
may access them via dbus.

The file is intended to give a complete list of services although
not all services would normally be used.

.. code-block:: xml

    <busconfig>

      <!-- ../system.conf have denied everything, so we just punch some holes -->

      <policy user="root">
        <allow own="org.bluez"/>
        <allow send_destination="org.bluez"/>
        <allow send_interface="org.bluez.Agent"/>
        <allow send_interface="org.bluez.Audio"/>
        <allow send_interface="org.bluez.AudioSource"/>
        <allow send_interface="org.bluez.AudioSink"/>
        <allow send_interface="org.bluez.Control"/>
        <allow send_interface="org.bluez.Media"/>
        <allow send_interface="org.bluez.MediaEndpoint"/>
        <allow send_interface="org.bluez.MediaTransport"/>
        <allow send_interface="org.bluez.MediaPlayer"/>
        <allow send_interface="org.bluez.ThermometerWatcher"/>
        <allow send_interface="org.bluez.AlertAgent"/>
        <allow send_interface="org.bluez.Profile"/>
        <allow send_interface="org.bluez.HeartRateWatcher"/>
        <allow send_interface="org.bluez.CyclingSpeedWatcher"/>
        <allow send_interface="org.freedesktop.DBus.ObjectManager"/>
      </policy>

      <policy at_console="true">
        <allow send_destination="org.bluez"/>
      </policy>

      <!-- allow users of lp group (printing subsystem) to 
           communicate with bluetoothd -->
      <policy group="lp">
        <allow send_destination="org.bluez"/>
      </policy>

      <policy context="default">
        <deny send_destination="org.bluez"/>
      </policy>

    </busconfig>


Tools/Applications
==================

bluetoothd
~~~~~~~~~~

The `daemon` must be running before any bluetooth services can be used.
It is typically started up as part of ``/etc/init.d/bluetooth``
start-up script and depends upon the dbus service.

Useful logging is output ``/var/log/syslog`` by ``bluetoothd``.  It
is also possible for the root user to start the service manually with the
debug options turned and view the trace on the console e.g.,

.. code-block:: python

	bluetoothd -n -d

The above command will launch the daemon without detaching from the parent
process and will turn the debug trace level on.

hcitool
~~~~~~~

:term:`HCI` tool provides a command-line interface allowing the user to scan
for remote devices and also enquire the capabilities of a device by its
address e.g., `11:22:33:44:55:66`.

hcidump
~~~~~~~

A tool that allows :term:`HCI` interface transactions to be dumped
for debugging purposes.

hciconfig
~~~~~~~~~

A tool for configuring bluetooth devices via the :term:`HCI` interface.
