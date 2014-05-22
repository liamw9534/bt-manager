from __future__ import unicode_literals

from interface import BTInterface
from adapter import BTAdapter
from exceptions import BTDeviceNotSpecifiedException


# This class is not intended to be instantiated directly and should be
# sub-classed with a concrete implementation for an interface
class BTGenericDevice(BTInterface):
    """Generic BT device which has its own interface bus address but is
    associated with a BT adapter"""
    def __init__(self, addr, adapter_id=None, dev_path=None, dev_id=None):
        if (dev_path):
            path = dev_path
        elif (dev_id):
            if (adapter_id):
                adapter = BTAdapter(adapter_id)
            else:
                adapter = BTAdapter()
            path = adapter.find_device(dev_id)
        else:
            raise BTDeviceNotSpecifiedException
        BTInterface.__init__(self, path, addr)


class BTDevice(BTGenericDevice):
    """Wrapper around Dbus to encapsulate the BT device entity"""

    SIGNAL_DISCONNECT_REQUESTED = 'DisconnectRequested'
    SIGNAL_NODE_CREATED = 'NodeCreated'
    SIGNAL_NODE_REMOVED = 'NodeRemoved'

    def __init__(self, *args, **kwargs):
        BTGenericDevice.__init__(self, addr='org.bluez.Device',
                                 *args, **kwargs)
        self._register_signal_name(BTDevice.SIGNAL_DISCONNECT_REQUESTED)
        self._register_signal_name(BTDevice.SIGNAL_NODE_CREATED)
        self._register_signal_name(BTDevice.SIGNAL_NODE_REMOVED)

    def discover_services(self, pattern=''):
        """This method starts the service discovery to retrieve
        remote service records. The pattern parameter can
        be used to specify specific UUIDs. And empty string
        will look for the public browse group.
        The return value is a dictionary with the record
        handles as keys and the service record in XML format
        as values. The key is uint32 and the value a string
        for this dictionary.  Refer to BTDiscoveryInfo
        to decode each XML service record"""
        return self._interface.DiscoverServices(pattern)

    def cancel_discovery(self):
        """This method will cancel any previous DiscoverServices
        transaction."""
        return self._interface.CancelDiscovery()

    def disconnect(self):
        """This method disconnects a specific remote device by
        terminating the low-level ACL connection. The use of
        this method should be restricted to administrator
        use.
        A 'DisconnectRequested' signal will be sent and the
        actual disconnection will only happen 2 seconds later.
        This enables upper-level applications to terminate
        their connections gracefully before the ACL connection
        is terminated."""
        self._interface.Disconnect()
