from __future__ import unicode_literals

from device import BTGenericDevice


class BTControl(BTGenericDevice):
    """Wrapper around Dbus to encapsulate the BT control entity"""

    SIGNAL_CONNECTED = 'Connected'
    SIGNAL_DISCONNECTED = 'Disconnected'

    def __init__(self, *args, **kwargs):
        BTGenericDevice.__init__(self, addr='org.bluez.Control',
                                 *args, **kwargs)
        self._register_signal_name(BTControl.SIGNAL_CONNECTED)
        self._register_signal_name(BTControl.SIGNAL_DISCONNECTED)

    def is_connected(self):
        return self._interface.IsConnected()

    def volume_up(self):
        """Adjust remote volume one step up"""
        self._interface.VolumeUp()

    def volume_down(self):
        """Adjust remote volume one step down"""
        self._interface.VolumeDown()
