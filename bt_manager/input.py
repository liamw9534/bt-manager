from __future__ import unicode_literals

from device import BTGenericDevice


class BTInput(BTGenericDevice):
    """
    Wrapper around dbus to encapsulate the org.bluez.Input
    interface.

    :Properties:

    * **Connected(boolean) [readonly]**:
        Indicates if the device is connected.

    See also: :py:class:`.BTGenericDevice` for setup params.
    """
    def __init__(self, *args, **kwargs):
        BTGenericDevice.__init__(self, addr='org.bluez.Input',
                                 *args, **kwargs)

    def connect(self):
        """
        Connect to the input device.

        :return:
        :raises dbus.Exception: org.bluez.Error.AlreadyConnected
        :raises dbus.Exception: org.bluez.Error.ConnectionAttemptFailed
        """
        return self._interface.Connect()

    def disconnect(self):
        """
        Disconnect from the input device.

        To abort a connection attempt in case of errors or
        timeouts in the client it is fine to call this method.

        :return:
        :raises dbus.Exception: org.bluez.Error.Failed
        """
        return self._interface.Disconnect()
