from __future__ import unicode_literals

from interface import BTInterface


class BTManager(BTInterface):
    """
    Wrapper around dbus to encapsulate the org.bluez.manager interface
    which notionally is used to manage available bluetooth adapters.

    :Properties:

    * **Adapters(list{str}) [readonly]**: List of adapter object paths.

    See also :py:class:`.BTAdapter`
    """

    SIGNAL_ADAPTER_ADDED = 'AdapterAdded'
    """
    :signal AdapterAdded(signal_name, user_arg, object_path):
        Signal notifying when an adapter is added.
    """
    SIGNAL_ADAPTER_REMOVED = 'AdapterRemoved'
    """
    :signal AdapterRemoved(signal_name, user_arg, object_path):
        Signal notifying when an adapter is removed.
        .. note: In case all adapters are removed this signal will not
        be emitted. The AdapterRemoved signal has to be used to
        detect that no default adapter is selected or available
        anymore.
    """
    SIGNAL_DEFAULT_ADAPTER_CHANGED = 'DefaultAdapterChanged'
    """
    :signal DefaultAdapterChanged(signal_name, user_arg, object_path):
        Signal notifying when the default adapter has been changed.
    """

    def __init__(self):
        BTInterface.__init__(self, '/', 'org.bluez.Manager')
        self._register_signal_name(BTManager.SIGNAL_ADAPTER_ADDED)
        self._register_signal_name(BTManager.SIGNAL_ADAPTER_REMOVED)
        self._register_signal_name(BTManager.SIGNAL_DEFAULT_ADAPTER_CHANGED)

    def default_adapter(self):
        """
        Obtain the default BT adapter object path.

        :return: Object path of default adapter
        :rtype: str
        :raises dbus.Exception: org.bluez.Error.InvalidArguments
        :raises dbus.Exception: org.bluez.Error.NoSuchAdapter
        """
        return self._interface.DefaultAdapter()

    def find_adapter(self, pattern):
        """
        Returns object path for the specified adapter.

        :param str pattern:  Valid patterns are "hci0" or "00:11:22:33:44:55".
        :return: Object path of adapter
        :rtype: str
        :raises dbus.Exception: org.bluez.Error.InvalidArguments
        :raises dbus.Exception: org.bluez.Error.NoSuchAdapter
        """
        return self._interface.FindAdapter(pattern)

    def list_adapters(self):
        """
        Returns list of adapter object paths under /org/bluez

        :return: List of object paths or each adapter attached
        :rtype: list
        :raises dbus.Exception: org.bluez.Error.InvalidArguments
        :raises dbus.Exception: org.bluez.Error.Failed
        :raises dbus.Exception: org.bluez.Error.OutOfMemory
        """
        return self._interface.ListAdapters()
