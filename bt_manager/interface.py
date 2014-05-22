from __future__ import unicode_literals

import dbus
import types
import pprint

from exceptions import BTSignalNameNotRecognisedException

def translate_to_dbus_type(typeof, value):
    """Helper function to map values from their native Python types
    to Dbus types"""
    if ((isinstance(value, types.UnicodeType) or
         isinstance(value, str)) and typeof is not dbus.String):
        # FIXME: This is potentially dangerous since it evaluates
        # a string in-situ
        return typeof(eval(value))
    else:
        return typeof(value)


class Signal():
    """Encapsulation of user callback wrapper for signals
    fired by dbus.  This allows us to prepend the signal
    name and the user callback argument."""
    def __init__(self, signal, user_callback, user_arg):
        self.signal = signal
        self.user_callback = user_callback
        self.user_arg = user_arg

    def signal_handler(self, *args):
        self.user_callback(self.signal, self.user_arg, *args)


# This class is not intended to be instantiated directly and should be
# sub-classed with a concrete implementation for an interface
class BTSimpleInterface:
    """Wrapper around DBus to encapsulated a BT simple interface
    entry point (i.e., has no signals or properties)"""
    def __init__(self, path, addr):
        self._dbus_addr = addr
        self._bus = dbus.SystemBus()
        self._object = self._bus.get_object('org.bluez', path)
        self._interface = dbus.Interface(self._object, addr)


# This class is not intended to be instantiated directly and should be
# sub-classed with a concrete implementation for an interface
class BTInterface(BTSimpleInterface):
    """Wrapper around DBus to encapsulated a BT interface
    entry point e.g., an adapter, a device, etc"""

    SIGNAL_PROPERTY_CHANGED = 'PropertyChanged'

    def __init__(self, path, addr):
        BTSimpleInterface.__init__(self, path, addr)
        self._signals = {}
        self._signal_names = []
        self._properties = self._interface.GetProperties().keys()
        self._register_signal_name(BTInterface.SIGNAL_PROPERTY_CHANGED)

    def _register_signal_name(self, name):
        """Helper function to register allowed signals on this
        instance.  Need only be called once per signal name."""
        self._signal_names.append(name)

    def add_signal_receiver(self, callback_fn, signal, user_arg):
        """Add a signal receiver callback with user argument"""
        if (signal in self._signal_names):
            s = Signal(signal, callback_fn, user_arg)
            self._signals[signal] = s
            self._bus.add_signal_receiver(s.signal_handler,
                                          signal,
                                          dbus_interface=self._dbus_addr)
        else:
            raise BTSignalNameNotRecognisedException

    def remove_signal_receiver(self, signal):
        """Remove an installed signal receiver by signal name"""
        if (signal in self._signal_names):
            s = self._signals.get(signal)
            if (s):
                self._bus.remove_signal_receiver(s.signal_handler,
                                                 signal,
                                                 dbus_interface=self._dbus_addr)  # noqa
                self._signals.pop(signal)
        else:
            raise BTSignalNameNotRecognisedException

    def get_property(self, name=None):
        """Helper to get a property value by name or all
        properties as a dictionary."""
        if (name):
            return self._interface.GetProperties()[name]
        else:
            return self._interface.GetProperties()

    def set_property(self, name, value):
        """Helper to set a property value by name, translating to correct
        DBus type"""
        typeof = type(self.get_property(name))
        self._interface.SetProperty(name,
                                    translate_to_dbus_type(typeof, value))

    def __getattr__(self, name):
        """Override default getattr behaviours to allow DBus object
        properties to be exposed in the class for getting"""
        if name in self.__dict__:
            return self.__dict__[name]
        elif '_properties' in self.__dict__ and name in self._properties:
            return self.get_property(name)

    def __setattr__(self, name, value):
        """Override default setattr behaviours to allow DBus object
        properties to be exposed in the class for setting"""
        if '_properties' in self.__dict__ and name not in self.__dict__:
            self.set_property(name, value)
        else:
            self.__dict__[name] = value

    def __repr__(self):
        """Stringify the Dbus interface properties as raw"""
        return self.__str__()

    def __str__(self):
        """Stringify the Dbus interface properties in a nice format"""
        return pprint.pformat(self._interface.GetProperties())
