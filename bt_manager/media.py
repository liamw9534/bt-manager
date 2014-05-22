from __future__ import unicode_literals

from interface import BTSimpleInterface, BTInterface
from manager import BTManager
from adapter import BTAdapter
from exceptions import BTDeviceNotSpecifiedException
import dbus.service


class BTMedia(BTSimpleInterface):
    """Wrapper around Dbus to encapsulate the BT media"""
    def __init__(self, adapter_id=None):
        manager = BTManager()
        if (adapter_id is None):
            adapter_path = manager.default_adapter()
        else:
            adapter_path = manager.find_adapter(adapter_id)
        BTSimpleInterface.__init__(self, adapter_path, 'org.bluez.Media')

    def register_endpoint(self, path, properties):
        self._interface.RegisterEndpoint(path, properties)

    def register_player(self, path, properties):
        self._interface.RegisterPlayer(path, properties)

    def unregister_endpoint(self, path):
        self._interface.UnregisterEndpoint(path)

    def unregister_player(self, path):
        self._interface.UnregisterPlayer(path)


class BTMediaTransport(BTInterface):
    """Wrapper around Dbus to encapsulate the BT media transport"""
    def __init__(self, path, fd=None, adapter_id=None,
                 dev_path=None, dev_id=None):
        if (not path):
            fd_suffix = '/fd' + str(fd)
            if (dev_path):
                path = dev_path + fd_suffix
            elif (dev_id):
                if (adapter_id):
                    adapter = BTAdapter(adapter_id)
                else:
                    adapter = BTAdapter()
                    path = adapter.find_device(dev_id) + fd_suffix
            else:
                raise BTDeviceNotSpecifiedException
        BTInterface.__init__(self, path, 'org.bluez.MediaTransport')

    def acquire(self, access_type):
        """Acquire transport file descriptor and the MTU for read
        and write respectively.  Possible access_type:
            "r" : Read only access
            "w" : Write only access
            "rw": Read and write access"""
        return self._interface.Acquire(access_type)

    def release(self, access_type):
        """Releases file descriptor."""
        return self._interface.Release(access_type)


# GenericEndpoint can't be directly instantiated.  It should be
# sub-classed and provides a template class only.
class GenericEndpoint(dbus.service.Object):
    def __init__(self, path):
        bus = dbus.SystemBus()
        super(GenericEndpoint, self).__init__(bus, path)

    def get_properties(self):
        """Returns the properties of the endpoint -- these should
        be initialized by a suitable subclass implementation"""
        return self.properties

    # Service object entry points defined below here --
    # you will need to implement these in your subclass
    @dbus.service.method("org.bluez.MediaEndpoint",
                         in_signature="", out_signature="")
    def Release(self):
        """Called by bluez to let us know our registration
        has been released - the endpoint no longer exists"""
        pass

    @dbus.service.method("org.bluez.MediaEndpoint",
                         in_signature="", out_signature="")
    def ClearConfiguration(self):
        """Called by bluez to let us know that the audio
        streaming process has been reset, for whatever reason, and
        we should clean-up."""
        pass

    @dbus.service.method("org.bluez.MediaEndpoint",
                         in_signature="oay", out_signature="")
    def SetConfiguration(self, transport, config):
        """Provides a path to the media transport to use and the active
        configuration that has been negotiated."""
        pass

    @dbus.service.method("org.bluez.MediaEndpoint",
                         in_signature="ay", out_signature="ay")
    def SelectConfiguration(self, caps):
        """Initiates negotiations of the capabilities"""
        pass
