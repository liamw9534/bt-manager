from __future__ import unicode_literals
from collections import namedtuple

import dbus
import dbus.service
import types


def _translate_to_dbus_type(value):
    """Helper function to map values from their native Python types
    to Dbus types"""
    if (isinstance(value, list)):
        return dbus.Array([_translate_to_dbus_type(k) for k in value])
    elif (isinstance(value, int) and value < 0):
        return dbus.Int32(value)
    elif (isinstance(value, int) and value >= 0):
        return dbus.UInt32(value)
    elif (isinstance(value, str)):
        return dbus.String(value)
    elif (isinstance(value, bool)):
        return dbus.Boolean(value)
    elif (isinstance(value, types.UnicodeType)):
        return dbus.String(value)
    else:
        return value


class BTSignalNameNotRecognisedException:
    """Exception raised for when a signal name is not recognized.
    Check the originating class for a list of supported signal names"""
    pass


class BTInterface:
    """Wrapper around DBus to encapsulated a BT interface
    entry point e.g., an adapter, a device, etc"""
    def __init__(self, path, addr):
        self._bus = dbus.SystemBus()
        self._object = self._bus.get_object('org.bluez', path)
        self._interface = dbus.Interface(self._object, addr)


class BTManager(BTInterface):
    """Wrapper around Dbus to encapsulate the BT manager entity"""
    def __init__(self):
        BTInterface.__init__(self, '/', 'org.bluez.Manager')

    def default_adapter(self):
        """Obtain the default BT adapter object"""
        return self._interface.DefaultAdapter()

    def find_adapter(self, dev_id):
        """Find a BT adapter by its MAC address e.g., 11:22:33:44:55:66"""
        return self._interface.FindAdapter(dev_id)


class BTAdapter(BTInterface):
    """Wrapper around Dbus to encapsulate the BT adapter entity"""

    SIGNAL_NAME_DEVICE_FOUND = 'DeviceFound'
    SIGNAL_NAME_PROPERTY_CHANGED = 'PropertyChanged'

    def __init__(self, dev_id=None):
        manager = BTManager()
        if (dev_id is None):
            adapter_path = manager.default_adapter()
        else:
            adapter_path = manager.find_adapter(dev_id)
        self._cb_user = {}
        self._cb_internal = {BTAdapter.SIGNAL_NAME_DEVICE_FOUND:
                             self._device_found_signal_handler,
                             BTAdapter.SIGNAL_NAME_PROPERTY_CHANGED:
                             self._property_changed_signal_handler}
        BTInterface.__init__(self, adapter_path, 'org.bluez.Adapter')
        self._properties = self._interface.GetProperties().keys()

    def _device_found_signal_handler(self, address, properties):
        """Wrapper for DeviceFound signal"""
        signal_name = BTAdapter.SIGNAL_NAME_DEVICE_FOUND
        user_cb = self._cb_user.get(signal_name)
        if (user_cb):
            user_cb.callback_fn(user_cb.user_arg, address, properties)

    def _property_changed_signal_handler(self, name, value):
        """Wrapper for PropertyChanged signal"""
        signal_name = BTAdapter.SIGNAL_NAME_PROPERTY_CHANGED
        user_cb = self._cb_user.get(signal_name)
        if (user_cb):
            user_cb.callback_fn(user_cb.user_arg, name, value)

    def add_signal_receiver(self, callback_fn, signal_name, user_arg):
        """Add a signal receiver callback with user argument.  The
        params for each signal are dependent on the signal name"""
        cb = self._cb_internal.get(signal_name)
        if (cb):
            UserCallback = namedtuple('UserCallback', 'callback_fn user_arg')
            self._cb_user[signal_name] = UserCallback(callback_fn, user_arg)
            self._bus.add_signal_receiver(cb,
                                          signal_name,
                                          dbus_interface="org.bluez.Adapter")
        else:
            raise BTSignalNameNotRecognisedException

    def remove_signal_receiver(self, signal_name):
        """Remove an installed signal receiver by signal name"""
        cb = self._cb_internal.get(signal_name)
        if (cb):
            self._bus.remove_signal_receiver(cb,
                                             signal_name,
                                             dbus_interface="org.bluez.Adapter")   # noqa
            self._cb_user.pop(signal_name)
        else:
            raise BTSignalNameNotRecognisedException

    def start_discovery(self):
        """Start device discovery which will signal
        events on installed notifiers"""
        return self._interface.StartDiscovery()

    def stop_discovery(self):
        """Stop a previously started device discovery"""
        return self._interface.StopDiscovery()

    def find_device(self, dev_id):
        """Find a device by its MAC address e.g., 11:22:33:44:55:66"""
        return self._interface.FindDevice(dev_id)

    def list_devices(self):
        """List all registered BT devices by their DBus object path"""
        return self._interface.ListDevices()

    def create_paired_device(self, dev_id, path,
                             caps, cb_notify_device, cb_notify_error):
        """Create a new paired device entry for
        this adapter by device MAC addr"""
        return self._interface.CreatePairedDevice(dev_id, path,
                                                  caps, cb_notify_device,
                                                  cb_notify_error)

    def remove_device(self, dev_id):
        """Remove an existing paired device entry
        on this adapter by device MAC addr"""
        dev_obj = self.find_device(dev_id)
        if (dev_obj):
            self._interface.RemoveDevice(dev_obj)

    def register_agent(self, path, caps):
        """Register a pairing agent on this adapter"""
        self._interface.RegisterAgent(path, caps)

    def _get_property(self, name):
        """Helper to get a property value by name"""
        return self._interface.GetProperties()[name]

    def _set_property(self, name, value):
        """Helper to set a property value by name, translating to correct
        DBus type"""
        self._interface.SetProperty(name, _translate_to_dbus_type(value))

    def __getattr__(self, name):
        """Override default getattr behaviours to allow DBus object
        properties to be exposed in the class for getting"""
        if name in self.__dict__:
            return self.__dict__[name]
        elif '_properties' in self.__dict__ and name in self._properties:
            return self._get_property(name)

    def __setattr__(self, name, value):
        """Override default setattr behaviours to allow DBus object
        properties to be exposed in the class for setting"""
        if '_properties' in self.__dict__ and name not in self.__dict__:
            self._set_property(name, value)
        else:
            self.__dict__[name] = value

    def __repr__(self):
        """Stringify the Dbus interface properties as raw"""
        h = self._interface.GetProperties()
        return str(h)

    def __str__(self):
        """Stringify the Dbus interface properties in a nice format"""
        h = self._interface.GetProperties()
        s = ''
        for i in h.keys():
            s += i + ': ' + str(h[i]) + '\n'
        return s


class BTDevice(BTInterface):
    """Wrapper around Dbus to encapsulate the BT device entity"""
    def __init__(self, adapter_id=None, dev_object_path=None, dev_id=None):
        if (adapter_id):
            adapter = BTAdapter(adapter_id)
        else:
            adapter = BTAdapter()

        if (dev_object_path is None):
            device_path = adapter.find_device(dev_id)
        else:
            device_path = dev_object_path
        BTInterface.__init__(self, device_path, 'org.bluez.Device')
        self._properties = self._interface.GetProperties().keys()

    def _get_property(self, name):
        """Helper to get a property value by name"""
        return self._interface.GetProperties()[name]

    def _set_property(self, name, value):
        """Helper to set a property value by name, translating to correct
        DBus type"""
        self._interface.SetProperty(name, _translate_to_dbus_type(value))

    def __getattr__(self, name):
        """Override default getattr behaviours to allow DBus object
        properties to be exposed in the class for getting"""
        if name in self.__dict__:
            return self.__dict__[name]
        elif '_properties' in self.__dict__ and name in self._properties:
            return self._get_property(name)

    def __setattr__(self, name, value):
        """Override default setattr behaviours to allow DBus object
        properties to be exposed in the class for setting"""
        if '_properties' in self.__dict__ and name not in self.__dict__:
            self._set_property(name, value)
        else:
            self.__dict__[name] = value

    def __repr__(self):
        """Stringify the Dbus interface properties as raw"""
        h = self._interface.GetProperties()
        return str(h)

    def __str__(self):
        """Stringify the Dbus interface properties in a nice format"""
        h = self._interface.GetProperties()
        s = ''
        for i in h.keys():
            s += i + ': ' + str(h[i]) + '\n'
        return s


class RejectedException(dbus.DBusException):
    _dbus_error_name = "org.bluez.Error.Rejected"


class BTAgent(dbus.service.Object):
    """Simple BT device pairing agent"""
    def __init__(self,
                 adapter,
                 capability='DisplayYesNo',
                 path='/test/agent',
                 auto_authorize_connections=True,
                 default_pin_code='0000',
                 default_pass_key=0x12345678L,
                 cb_notify_on_release=None,
                 cb_notify_on_authorize=None,
                 cb_notify_on_request_pin_code=None,
                 cb_notify_on_request_pass_key=None,
                 cb_notify_on_display_pass_key=None,
                 cb_notify_on_request_confirmation=None,
                 cb_notify_on_confirm_mode_change=None,
                 cb_notify_on_cancel=None):

        self.auto_authorize_connections = auto_authorize_connections
        self.default_pin_code = default_pin_code
        self.default_pass_key = default_pass_key
        self.cb_notify_on_release = cb_notify_on_release
        self.cb_notify_on_authorize = cb_notify_on_authorize
        self.cb_notify_on_request_pin_code = cb_notify_on_request_pin_code
        self.cb_notify_on_request_pass_key = cb_notify_on_request_pass_key
        self.cb_notify_on_display_pass_key = cb_notify_on_display_pass_key
        self.cb_notify_on_request_confirmation = \
            cb_notify_on_request_confirmation
        self.cb_notify_on_confirm_mode_change = \
            cb_notify_on_confirm_mode_change
        self.cb_notify_on_cancel = cb_notify_on_cancel
        bus = dbus.SystemBus()
        super(BTAgent, self).__init__(bus, path)
        adapter.register_agent(path, capability)

    @dbus.service.method("org.bluez.Agent", in_signature="", out_signature="")
    def Release(self):
        if (self.cb_notify_on_release):
            self.cb_notify_on_release()

    @dbus.service.method("org.bluez.Agent", in_signature="os",
                         out_signature="")
    def Authorize(self, device, uuid):
        if (self.cb_notify_on_authorize):
            if (not self.cb_notify_on_authorize(device, uuid)):
                raise RejectedException('Connection not authorized by user')
        elif (not self.auto_authorize_connections):
            raise RejectedException('Auto authorize is off')

    @dbus.service.method("org.bluez.Agent", in_signature="o",
                         out_signature="s")
    def RequestPinCode(self, device):
        if (self.cb_notify_on_request_pin_code):
            pin_code = self.cb_notify_on_request_pin_code(device)
            if (pin_code is None):
                raise RejectedException('User did not provide PIN code')
        elif (self.default_pin_code is None):
            raise RejectedException('No default PIN code set')
        else:
            pin_code = self.default_pin_code
        return dbus.String(pin_code)

    @dbus.service.method("org.bluez.Agent", in_signature="o",
                         out_signature="s")
    def RequestPasskey(self, device):
        if (self.cb_notify_on_request_pass_key):
            pass_key = self.cb_notify_on_request_pass_key(device)
            if (pass_key is None):
                raise RejectedException('User did not provide pass key')
        elif (self.default_pass_key is None):
            raise RejectedException('No default pass key set')
        else:
            pass_key = self.default_pass_key
        return dbus.UInt32(pass_key)

    @dbus.service.method("org.bluez.Agent", in_signature="ou",
                         out_signature="")
    def DisplayPasskey(self, device, pass_key):
        if (self.cb_notify_on_display_pass_key):
            self.cb_notify_on_display_pass_key(device, pass_key)

    @dbus.service.method("org.bluez.Agent", in_signature="ou",
                         out_signature="")
    def RequestConfirmation(self, device, pass_key):
        if (self.cb_notify_on_request_confirmation):
            if (not self.cb_notify_on_request_confirmation(device, pass_key)):
                raise \
                    RejectedException('User confirmation of pass key negative')

    @dbus.service.method("org.bluez.Agent", in_signature="s", out_signature="")
    def ConfirmModeChange(self, mode):
        if (self.cb_notify_on_confirm_mode_change):
            if (not self.cb_notify_on_confirm_mode_change(mode)):
                raise \
                    RejectedException('User mode change confirmation negative')

    @dbus.service.method("org.bluez.Agent", in_signature="", out_signature="")
    def Cancel(self):
        if (self.cb_notify_on_cancel):
            self.cb_notify_on_cancel()
