from __future__ import unicode_literals

from interface import BTInterface
from manager import BTManager


class BTAdapter(BTInterface):
    """Wrapper around Dbus to encapsulate the BT adapter entity"""

    SIGNAL_DEVICE_FOUND = 'DeviceFound'
    SIGNAL_DEVICE_REMOVED = 'DeviceRemoved'
    SIGNAL_DEVICE_CREATED = 'DeviceCreated'
    SIGNAL_DEVICE_DISAPPEARED = 'DeviceDisappeared'

    def __init__(self, adapter_id=None):
        manager = BTManager()
        if (adapter_id is None):
            adapter_path = manager.default_adapter()
        else:
            adapter_path = manager.find_adapter(adapter_id)
        BTInterface.__init__(self, adapter_path, 'org.bluez.Adapter')
        self._register_signal_name(BTAdapter.SIGNAL_DEVICE_FOUND)
        self._register_signal_name(BTAdapter.SIGNAL_DEVICE_REMOVED)
        self._register_signal_name(BTAdapter.SIGNAL_DEVICE_CREATED)
        self._register_signal_name(BTAdapter.SIGNAL_DEVICE_DISAPPEARED)
        self._register_signal_name(BTAdapter.SIGNAL_PROPERTY_CHANGED)

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

    def create_paired_device(self, dev_id, agent_path,
                             caps, cb_notify_device, cb_notify_error):
        """Create a new paired device entry for this adapter by
        device MAC address using the provided agent path"""
        return self._interface.CreatePairedDevice(dev_id,
                                                  agent_path,
                                                  caps,
                                                  reply_handler=cb_notify_device,  # noqa
                                                  error_handler=cb_notify_error)   # noqa

    def remove_device(self, dev_path):
        """Remove an existing paired device entry on this adapter
        by device path"""
        self._interface.RemoveDevice(dev_path)

    def register_agent(self, path, caps):
        """Register a pairing agent on this adapter"""
        self._interface.RegisterAgent(path, caps)

    def unregister_agent(self, path):
        """Unregister a pairing agent on this adapter"""
        self._interface.UnregisterAgent(path)
