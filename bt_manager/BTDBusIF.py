from __future__ import unicode_literals

import dbus
import types
import pprint


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


class BTSignalNameNotRecognisedException:
    """Exception raised for when a signal name is not recognized.
    Check the originating class for a list of supported signal names"""
    pass


class BTDeviceNotSpecifiedException:
    """Exception raised for when a device is not specified"""
    pass


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


class BTAudio(BTGenericDevice):
    """Wrapper around Dbus to encapsulate the BT audio entity"""

    def __init__(self, *args, **kwargs):
        BTGenericDevice.__init__(self, addr='org.bluez.Audio',
                                 *args, **kwargs)

    def connect(self):
        """Connect all supported audio profiles on the device."""
        self._interface.Connect()

    def disconnect(self):
        """Disconnect all audio profiles on the device"""
        self._interface.Disconnect()


class BTAudioSource(BTAudio):
    """Wrapper around Dbus to encapsulate the BT audio source entity"""

    def __init__(self, *args, **kwargs):
        BTGenericDevice.__init__(self, addr='org.bluez.AudioSource',
                                 *args, **kwargs)


class BTAudioSink(BTAudio):
    """Wrapper around Dbus to encapsulate the BT audio sink entity"""

    SIGNAL_CONNECTED = 'Connected'
    SIGNAL_DISCONNECTED = 'Disconnected'
    SIGNAL_PLAYING = 'Playing'
    SIGNAL_STOPPED = 'Stopped'

    def __init__(self, *args, **kwargs):
        BTGenericDevice.__init__(self, addr='org.bluez.AudioSink',
                                 *args, **kwargs)
        self._register_signal_name(BTAudioSink.SIGNAL_CONNECTED)
        self._register_signal_name(BTAudioSink.SIGNAL_DISCONNECTED)
        self._register_signal_name(BTAudioSink.SIGNAL_PLAYING)
        self._register_signal_name(BTAudioSink.SIGNAL_STOPPED)

    def is_connected(self):
        """Returns TRUE if a stream is setup to a A2DP sink on
        the remote device."""
        return self._interface.IsConnected()


class BTHeadset(BTAudio):
    """Wrapper around Dbus to encapsulate the BT headset entity"""

    SIGNAL_ANSWER_REQUESTED = 'AnswerRequested'
    SIGNAL_SPEAKER_GAIN_CHANGED = 'SpeakerGainChanged'
    SIGNAL_MICROPHONE_GAIN_CHANGED = 'MicrophoneGainChanged'

    def __init__(self, *args, **kwargs):
        BTGenericDevice.__init__(self, addr='org.bluez.Headset',
                                 *args, **kwargs)
        self._register_signal_name(BTAudioSink.SIGNAL_ANSWER_REQUESTED)
        self._register_signal_name(BTAudioSink.SIGNAL_SPEAKER_GAIN_CHANGED)
        self._register_signal_name(BTAudioSink.SIGNAL_MICROPHONE_GAIN_CHANGED)

    def is_connected(self):
        return self._interface.IsConnected()

    def indicate_call(self):
        """Indicate an incoming call on the headset
        connected to the stream. Will continue to
        ring the headset about every 3 seconds."""
        return self._interface.IndicateCall()

    def cancel_call(self):
        """Cancel the incoming call indication"""
        return self._interface.CancelCall()

    def play(self):
        """Open the audio connection to the headset"""
        return self._interface.Play()

    def stop(self):
        """Close the audio connection"""
        return self._interface.Stop()


class BTHeadsetGateway(BTAudio):
    """Wrapper around Dbus to encapsulate the BT headset
    gateway entity"""

    SIGNAL_RING = 'Ring'
    SIGNAL_CALL_TERMINATED = 'CallTerminated'
    SIGNAL_CALL_STARTED = 'CallStarted'
    SIGNAL_CALL_ENDED = 'CallEnded'

    def __init__(self, *args, **kwargs):
        BTGenericDevice.__init__(self, addr='org.bluez.Headset',
                                 *args, **kwargs)
        self._register_signal_name(BTAudioSink.SIGNAL_RING)
        self._register_signal_name(BTAudioSink.SIGNAL_CALL_TERMINATED)
        self._register_signal_name(BTAudioSink.SIGNAL_CALL_STARTED)
        self._register_signal_name(BTAudioSink.SIGNAL_CALL_ENDED)

    def answer_call(self):
        """It has to called only after Ring signal received."""
        return self._interface.AnswerCall()

    def terminate_call(self):
        """Terminate call which is running or reject an incoming
        call. This has nothing with any 3-way situation incl.
        RaH. Just plain old PDH."""
        return self._interface.TerminateCall()

    def call(self, dial_number):
        """Dial a number. No number processing is done
        thus if AG would reject to dial it don't blame me"""
        return self._interface.Call(dial_number)

    def get_operator_name(self):
        """Find out the name of the currently selected network
        operator by AG."""
        return self._interface.GetOperatorName()

    def send_dtmf(self, digits):
        """Will send each digit in the 'digits' sequentially. Would
        send nothing if there is non-DTMF digit."""
        return self._interface.SendDTMF(digits)

    def get_subscriber_number(self):
        """Get the voicecall subscriber number of AG"""
        return self._interface.GetSubscriberNumber()
