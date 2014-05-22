from __future__ import unicode_literals

import dbus


class BTSignalNameNotRecognisedException:
    """Exception raised for when a signal name is not recognized.
    Check the originating class for a list of supported signal names"""
    pass


class BTDeviceNotSpecifiedException:
    """Exception raised for when a device is not specified"""
    pass


class BTRejectedException(dbus.DBusException):
    _dbus_error_name = "org.bluez.Error.Rejected"


class BTInvalidConfiguration(dbus.DBusException):
    _dbus_error_name = "org.bluez.Error.InvalidConfiguration"


class BTIncompatibleTransportAccessType(dbus.DBusException):
    _dbus_error_name = "org.bluez.Error.InvalidConfiguration"


class BTUUIDNotSpecifiedException:
    pass
