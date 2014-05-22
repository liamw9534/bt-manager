from __future__ import unicode_literals

from interface import BTInterface


class BTManager(BTInterface):
    """Wrapper around Dbus to encapsulate the BT manager entity"""

    SIGNAL_ADAPTER_ADDED = 'AdapterAdded'
    SIGNAL_ADAPTER_REMOVED = 'AdapterRemoved'
    SIGNAL_DEFAULT_ADAPTER_CHANGED = 'DefaultAdapterChanged'

    def __init__(self):
        BTInterface.__init__(self, '/', 'org.bluez.Manager')
        self._register_signal_name(BTManager.SIGNAL_ADAPTER_ADDED)
        self._register_signal_name(BTManager.SIGNAL_ADAPTER_REMOVED)
        self._register_signal_name(BTManager.SIGNAL_DEFAULT_ADAPTER_CHANGED)

    def default_adapter(self):
        """Obtain the default BT adapter object path"""
        return self._interface.DefaultAdapter()

    def find_adapter(self, dev_id):
        """Find a BT adapter by its MAC address e.g., 11:22:33:44:55:66"""
        return self._interface.FindAdapter(dev_id)

    def list_adapters(self):
        """List all attached BT adapters"""
        return self._interface.ListAdapters()
