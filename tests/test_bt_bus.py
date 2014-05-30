from __future__ import unicode_literals

import unittest

import bt_manager
import mock
import dbus
import os


class MockDBusInterface:
    """Mock dbus.Interface implementation for purpose of testing"""
    def __init__(self, obj, addr):
        self.addr = addr
        if (self.addr == 'org.bluez.Adapter'):
            self._props = dbus.Dictionary({dbus.String(u'Name'): dbus.String(u'new-name', variant_level=1),  # noqa
                                           dbus.String(u'Powered'): dbus.Boolean(True, variant_level=1),  # noqa
                                           dbus.String(u'Devices'):
                                           dbus.Array([dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE')],  # noqa
                                                      signature=dbus.Signature('o'), variant_level=1),  # noqa
                                           dbus.String(u'DiscoverableTimeout'): dbus.UInt32(0L, variant_level=1),  # noqa
                                           dbus.String(u'PairableTimeout'): dbus.UInt32(0L, variant_level=1),  # noqa
                                           dbus.String(u'Discoverable'): dbus.Boolean(True, variant_level=1),  # noqa
                                           dbus.String(u'Address'): dbus.String(u'AC:7B:A1:3C:13:82', variant_level=1),  # noqa
                                           dbus.String(u'Discovering'): dbus.Boolean(False, variant_level=1),  # noqa
                                           dbus.String(u'Pairable'): dbus.Boolean(True, variant_level=1),  # noqa
                                           dbus.String(u'Class'): dbus.UInt32(7209216L, variant_level=1),  # noqa
                                           dbus.String(u'UUIDs'):
                                           dbus.Array([dbus.String(u'00001000-0000-1000-8000-00805f9b34fb'),  # noqa
                                                       dbus.String(u'00001001-0000-1000-8000-00805f9b34fb'),  # noqa
                                                       dbus.String(u'0000112d-0000-1000-8000-00805f9b34fb'),  # noqa
                                                       dbus.String(u'00001112-0000-1000-8000-00805f9b34fb'),  # noqa
                                                       dbus.String(u'0000111f-0000-1000-8000-00805f9b34fb'),  # noqa
                                                       dbus.String(u'0000111e-0000-1000-8000-00805f9b34fb'),  # noqa
                                                       dbus.String(u'0000110a-0000-1000-8000-00805f9b34fb'),  # noqa
                                                       dbus.String(u'0000110b-0000-1000-8000-00805f9b34fb'),  # noqa
                                                       dbus.String(u'0000110c-0000-1000-8000-00805f9b34fb'),  # noqa
                                                       dbus.String(u'0000110e-0000-1000-8000-00805f9b34fb'),  # noqa
                                                       dbus.String(u'00001103-0000-1000-8000-00805f9b34fb')],  # noqa
                                                      signature=dbus.Signature('s'), variant_level=1)},  # noqa
                                          signature=dbus.Signature('sv'))
        elif (self.addr == 'org.bluez.Device'):
            self._props = dbus.Dictionary({dbus.String(u'Product'): dbus.UInt16(5028, variant_level=1),  # noqa
                                           dbus.String(u'Vendor'): dbus.UInt16(57, variant_level=1),  # noqa
                                           dbus.String(u'Name'): dbus.String(u'BTS-06', variant_level=1),  # noqa
                                           dbus.String(u'Paired'): dbus.Boolean(True, variant_level=1),  # noqa
                                           dbus.String(u'Adapter'): dbus.ObjectPath('/org/bluez/985/hci0',  # noqa
                                                                                    variant_level=1),  # noqa
                                           dbus.String(u'Alias'): dbus.String(u'BTS-06', variant_level=1),  # noqa
                                           dbus.String(u'Version'): dbus.UInt16(260, variant_level=1),  # noqa
                                           dbus.String(u'Connected'): dbus.Boolean(False, variant_level=1),  # noqa
                                           dbus.String(u'UUIDs'):
                                                dbus.Array([dbus.String(u'00001108-0000-1000-8000-00805f9b34fb'),  # noqa
                                                            dbus.String(u'0000110b-0000-1000-8000-00805f9b34fb'),  # noqa
                                                            dbus.String(u'0000110c-0000-1000-8000-00805f9b34fb'),  # noqa
                                                            dbus.String(u'0000110e-0000-1000-8000-00805f9b34fb'),  # noqa
                                                            dbus.String(u'0000111e-0000-1000-8000-00805f9b34fb'),  # noqa
                                                            dbus.String(u'00001200-0000-1000-8000-00805f9b34fb')],  # noqa
                                                           signature=dbus.Signature('s'), variant_level=1),  # noqa
                                           dbus.String(u'Address'): dbus.String(u'00:11:67:D2:AB:EE', variant_level=1),  # noqa
                                           dbus.String(u'Services'): dbus.Array([], signature=dbus.Signature('o'), variant_level=1),  # noqa
                                           dbus.String(u'Blocked'): dbus.Boolean(False, variant_level=1),  # noqa
                                           dbus.String(u'Class'): dbus.UInt32(2360340L, variant_level=1),  # noqa
                                           dbus.String(u'Trusted'): dbus.Boolean(True, variant_level=1),  # noqa
                                           dbus.String(u'Icon'): dbus.String(u'audio-card', variant_level=1)},  # noqa
                                          signature=dbus.Signature('sv'))

            service_xml = (
                """<?xml version="1.0" encoding="UTF-8" ?>
<record>
    <attribute id="0x0000">
        <uint32 value="0x00010001" />
    </attribute>
    <attribute id="0x0001">
        <sequence>
            <uuid value="0x1200" />
        </sequence>
    </attribute>
    <attribute id="0x0004">
        <sequence>
            <sequence>
                <uuid value="0x0100" />
                <uint16 value="0x0001" />
            </sequence>
            <sequence>
                <uuid value="0x0001" />
            </sequence>
        </sequence>
    </attribute>
    <attribute id="0x0006">
        <sequence>
            <uint16 value="0x656e" />
            <uint16 value="0x006a" />
            <uint16 value="0x0100" />
        </sequence>
    </attribute>
    <attribute id="0x0009">
        <sequence>
            <sequence>
                <uuid value="0x1200" />
                <uint16 value="0x0100" />
            </sequence>
        </sequence>
    </attribute>
    <attribute id="0x0200">
        <uint16 value="0x0103" />
    </attribute>
    <attribute id="0x0201">
        <uint16 value="0x0039" />
    </attribute>
    <attribute id="0x0202">
        <uint16 value="0x13a4" />
    </attribute>
    <attribute id="0x0203">
        <uint16 value="0x0104" />
    </attribute>
    <attribute id="0x0204">
        <boolean value="true" />
    </attribute>
    <attribute id="0x0205">
        <uint16 value="0x0001" />
    </attribute>
</record>
""",

                """<?xml version="1.0" encoding="UTF-8" ?>
<record>
    <attribute id="0x0000">
        <uint32 value="0x00010002" />
    </attribute>
    <attribute id="0x0001">
        <sequence>
            <uuid value="0x1108" />
            <uuid value="0x1203" />
        </sequence>
    </attribute>
    <attribute id="0x0004">
        <sequence>
            <sequence>
                <uuid value="0x0100" />
            </sequence>
            <sequence>
                <uuid value="0x0003" />
                <uint8 value="0x02" />
            </sequence>
        </sequence>
    </attribute>
    <attribute id="0x0006">
        <sequence>
            <uint16 value="0x656e" />
            <uint16 value="0x006a" />
            <uint16 value="0x0100" />
        </sequence>
    </attribute>
    <attribute id="0x0009">
        <sequence>
            <sequence>
                <uuid value="0x1108" />
                <uint16 value="0x0100" />
            </sequence>
        </sequence>
    </attribute>
    <attribute id="0x0100">
        <text value="Headset unit" />
    </attribute>
    <attribute id="0x0302">
        <boolean value="true" />
    </attribute>
</record>
""",

                """<?xml version="1.0" encoding="UTF-8" ?>
<record>
    <attribute id="0x0000">
        <uint32 value="0x00010003" />
    </attribute>
    <attribute id="0x0001">
        <sequence>
            <uuid value="0x111e" />
            <uuid value="0x1203" />
        </sequence>
    </attribute>
    <attribute id="0x0004">
        <sequence>
            <sequence>
                <uuid value="0x0100" />
            </sequence>
            <sequence>
                <uuid value="0x0003" />
                <uint8 value="0x01" />
            </sequence>
        </sequence>
    </attribute>
    <attribute id="0x0006">
        <sequence>
            <uint16 value="0x656e" />
            <uint16 value="0x006a" />
            <uint16 value="0x0100" />
        </sequence>
    </attribute>
    <attribute id="0x0009">
        <sequence>
            <sequence>
                <uuid value="0x111e" />
                <uint16 value="0x0105" />
            </sequence>
        </sequence>
    </attribute>
    <attribute id="0x0100">
        <text value="Hands-free unit" />
    </attribute>
    <attribute id="0x0311">
        <uint16 value="0x001f" />
    </attribute>
</record>
""",

                """<?xml version="1.0" encoding="UTF-8" ?>
<record>
    <attribute id="0x0000">
        <uint32 value="0x00010006" />
    </attribute>
    <attribute id="0x0001">
        <sequence>
            <uuid value="0x110e" />
        </sequence>
    </attribute>
    <attribute id="0x0004">
        <sequence>
            <sequence>
                <uuid value="0x0100" />
                <uint16 value="0x0017" />
            </sequence>
            <sequence>
                <uuid value="0x0017" />
                <uint16 value="0x0102" />
            </sequence>
        </sequence>
    </attribute>
    <attribute id="0x0006">
        <sequence>
            <uint16 value="0x656e" />
            <uint16 value="0x006a" />
            <uint16 value="0x0100" />
        </sequence>
    </attribute>
    <attribute id="0x0009">
        <sequence>
            <sequence>
                <uuid value="0x110e" />
                <uint16 value="0x0103" />
            </sequence>
        </sequence>
    </attribute>
    <attribute id="0x0100">
        <text value="AVRCP CT" />
    </attribute>
    <attribute id="0x0102">
        <text value="ISSC" />
    </attribute>
    <attribute id="0x0311">
        <uint16 value="0x0001" />
    </attribute>
</record>
""",

                """<?xml version="1.0" encoding="UTF-8" ?>
<record>
    <attribute id="0x0000">
        <uint32 value="0x00010008" />
    </attribute>
    <attribute id="0x0001">
        <sequence>
            <uuid value="0x110b" />
        </sequence>
    </attribute>
    <attribute id="0x0004">
        <sequence>
            <sequence>
                <uuid value="0x0100" />
                <uint16 value="0x0019" />
            </sequence>
            <sequence>
                <uuid value="0x0019" />
                <uint16 value="0x0100" />
            </sequence>
        </sequence>
    </attribute>
    <attribute id="0x0006">
        <sequence>
            <uint16 value="0x656e" />
            <uint16 value="0x006a" />
            <uint16 value="0x0100" />
        </sequence>
    </attribute>
    <attribute id="0x0009">
        <sequence>
            <sequence>
                <uuid value="0x110d" />
                <uint16 value="0x0100" />
            </sequence>
        </sequence>
    </attribute>
    <attribute id="0x0100">
        <text value="Audio SNK" />
    </attribute>
    <attribute id="0x0102">
        <text value="ISSC" />
    </attribute>
    <attribute id="0x0311">
        <uint16 value="0x0003" />
    </attribute>
</record>
""",

                """<?xml version="1.0" encoding="UTF-8" ?>
<record>
    <attribute id="0x0000">
        <uint32 value="0x0001000c" />
    </attribute>
    <attribute id="0x0001">
        <sequence>
            <uuid value="0x110c" />
        </sequence>
    </attribute>
    <attribute id="0x0004">
        <sequence>
            <sequence>
                <uuid value="0x0100" />
                <uint16 value="0x0017" />
            </sequence>
            <sequence>
                <uuid value="0x0017" />
                <uint16 value="0x0100" />
            </sequence>
        </sequence>
    </attribute>
    <attribute id="0x0006">
        <sequence>
            <uint16 value="0x656e" />
            <uint16 value="0x006a" />
            <uint16 value="0x0100" />
        </sequence>
    </attribute>
    <attribute id="0x0009">
        <sequence>
            <sequence>
                <uuid value="0x110e" />
                <uint16 value="0x0100" />
            </sequence>
        </sequence>
    </attribute>
    <attribute id="0x0100">
        <text value="AVRCP TG" />
    </attribute>
    <attribute id="0x0102">
        <text value="ISSC" />
    </attribute>
    <attribute id="0x0311">
        <uint16 value="0x0002" />
    </attribute>
</record>
""",

                """<?xml version="1.0" encoding="UTF-8" ?>
<record>
    <attribute id="0x0000">
        <uint32 value="0x0001000f" />
    </attribute>
    <attribute id="0x0001">
        <sequence>
            <uuid value="0x112e" />
        </sequence>
    </attribute>
    <attribute id="0x0006">
        <sequence>
            <uint16 value="0x656e" />
            <uint16 value="0x006a" />
            <uint16 value="0x0100" />
        </sequence>
    </attribute>
    <attribute id="0x0009">
        <sequence>
            <sequence>
                <uuid value="0x1130" />
                <uint16 value="0x0100" />
            </sequence>
        </sequence>
    </attribute>
</record>
"""
                )

            self._services = dbus.Dictionary({dbus.UInt32(65537L): dbus.String(service_xml[0]),  # noqa
                                              dbus.UInt32(65538L): dbus.String(service_xml[1]),  # noqa
                                              dbus.UInt32(65539L): dbus.String(service_xml[2]),  # noqa
                                              dbus.UInt32(65542L): dbus.String(service_xml[3]),  # noqa
                                              dbus.UInt32(65544L): dbus.String(service_xml[4]),  # noqa
                                              dbus.UInt32(65548L): dbus.String(service_xml[5]),  # noqa
                                              dbus.UInt32(65551L): dbus.String(service_xml[6]),  # noqa
                                              }, signature=dbus.Signature('us'))  # noqa

        elif (self.addr == 'org.bluez.Manager'):
            self._props = {u'Adapters': ['/org/bluez/985/hci0']}
        elif (self.addr == 'org.bluez.AudioSink'):
            self._props = {u'Connected': False}
        elif (self.addr == 'org.bluez.Control'):
            self._props = {u'Connected': False}
        elif (self.addr == 'org.bluez.Media'):
            pass
        elif (self.addr == 'org.freedesktop.DBus.Introspectable'):
            self._introspect = \
                """
<!DOCTYPE node PUBLIC "-//freedesktop//DTD D-BUS Object Introspection 1.0//EN"
"http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd">
<node>
    <interface name="org.freedesktop.DBus.Introspectable">
        <method name="Introspect">
            <arg type="s" direction="out"/>
        </method>
    </interface>
    <interface name="org.bluez.Device">
        <method name="GetProperties">
            <arg type="a{sv}" direction="out"/>
        </method>
        <method name="SetProperty">
            <arg type="s" direction="in"/>
            <arg type="v" direction="in"/>
        </method>
        <method name="DiscoverServices">
            <arg type="s" direction="in"/>
            <arg type="a{us}" direction="out"/>
        </method>
        <method name="CancelDiscovery"/>
        <method name="Disconnect"/>
        <signal name="PropertyChanged">
            <arg type="s"/>
            <arg type="v"/>
        </signal>
        <signal name="DisconnectRequested"/>
    </interface>
    <interface name="org.bluez.Serial">
        <method name="Connect">
            <arg type="s" direction="in"/>
            <arg type="s" direction="out"/>
        </method>
        <method name="ConnectFD">
            <arg type="s" direction="in"/>
            <arg type="h" direction="out"/>
        </method>
        <method name="Disconnect">
            <arg type="s" direction="in"/>
        </method>
    </interface>
    <interface name="org.bluez.Input">
        <method name="Connect"/>
        <method name="Disconnect"/>
        <method name="GetProperties">
            <arg type="a{sv}" direction="out"/>
        </method>
        <signal name="PropertyChanged">
            <arg type="s"/>
            <arg type="v"/>
        </signal>
    </interface>
    <interface name="org.bluez.Audio">
        <method name="Connect"/>
        <method name="Disconnect"/>
        <method name="GetProperties">
            <arg type="a{sv}" direction="out"/>
        </method>
        <signal name="PropertyChanged">
            <arg type="s"/>
            <arg type="v"/>
        </signal>
    </interface>
    <interface name="org.bluez.Headset">
        <method name="Connect"/>
        <method name="Disconnect"/>
        <method name="IsConnected">
            <arg type="b" direction="out"/>
        </method>
        <method name="IndicateCall"/>
        <method name="CancelCall"/>
        <method name="Play"/>
        <method name="Stop"/>
        <method name="IsPlaying">
            <arg type="b" direction="out"/>
        </method>
        <method name="GetSpeakerGain">
            <arg type="q" direction="out"/>
        </method>
        <method name="GetMicrophoneGain">
            <arg type="q" direction="out"/>
        </method>
        <method name="SetSpeakerGain">
            <arg type="q" direction="in"/>
        </method>
        <method name="SetMicrophoneGain">
            <arg type="q" direction="in"/>
        </method>
        <method name="GetProperties">
            <arg type="a{sv}" direction="out"/>
        </method>
        <method name="SetProperty">
            <arg type="s" direction="in"/>
            <arg type="v" direction="in"/>
        </method>
        <signal name="Connected"/>
        <signal name="Disconnected"/>
        <signal name="AnswerRequested"/>
        <signal name="Stopped"/>
        <signal name="Playing"/>
        <signal name="SpeakerGainChanged">
            <arg type="q"/>
        </signal>
        <signal name="MicrophoneGainChanged">
            <arg type="q"/>
        </signal>
        <signal name="CallTerminated"/>
        <signal name="PropertyChanged">
            <arg type="s"/>
            <arg type="v"/>
        </signal>
    </interface>
    <interface name="org.bluez.AudioSink">
        <method name="Connect"/>
        <method name="Disconnect"/>
        <method name="IsConnected">
            <arg type="b" direction="out"/>
        </method>
        <method name="GetProperties">
            <arg type="a{sv}" direction="out"/>
        </method>
        <signal name="Connected"/>
        <signal name="Disconnected"/>
        <signal name="Playing"/>
        <signal name="Stopped"/>
        <signal name="PropertyChanged">
            <arg type="s"/>
            <arg type="v"/>
        </signal>
    </interface>
    <interface name="org.bluez.Control">
        <method name="IsConnected">
            <arg type="b" direction="out"/>
        </method>
        <method name="GetProperties">
            <arg type="a{sv}" direction="out"/>
        </method>
        <method name="VolumeUp"/>
        <method name="VolumeDown"/>
        <signal name="Connected"/>
        <signal name="Disconnected"/>
        <signal name="PropertyChanged">
            <arg type="s"/>
            <arg type="v"/>
        </signal>
    </interface>
</node>
"""

    def Introspect(self, addr):
        return self._introspect[1:]  # Strip leading \n

    def StartDiscovery(self):
        self._props[dbus.String(u'Discovering')] = \
            dbus.Boolean(True, variant_level=1)

    def StopDiscovery(self):
        self._props[dbus.String(u'Discovering')] = \
            dbus.Boolean(False, variant_level=1)

    def ListAdapters(self):
        return ['/org/bluez/985/hci0']

    def FindAdapter(self, *args):
        return '/org/bluez/985/hci0'

    def DefaultAdapter(self, *args):
        return '/org/bluez/985/hci0'

    def SetProperty(self, name, value):
        self._props[name] = value

    def GetProperties(self):
        return self._props

    def FindDevice(self, *args):
        return '/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE'

    def ListDevices(self, *args):
        return ['/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE']

    def CreatePairedDevice(self, dev_id, path, caps,
                           reply_handler, error_handler):
        self._cb_notify_dev_id = dev_id
        self._cb_notify_device = reply_handler
        self._cb_notify_error = error_handler

    def RemoveDevice(self, dev_obj):
        pass

    def RegisterAgent(self, path, caps):
        pass

    def UnregisterAgent(self, path):
        pass

    def Connect(self):
        self._props['Connected'] = True

    def IsConnected(self):
        return self._props['Connected']

    def Disconnect(self):
        self._props['Connected'] = False

    def VolumeUp(self):
        pass

    def VolumeDown(self):
        pass

    def DiscoverServices(self, pattern):
        return self._services

    def RegisterEndpoint(self, path, properties):
        pass

    def RegisterPlayer(self, path, properties):
        pass

    def UnregisterEndpoint(self, path):
        pass

    def UnregisterPlayer(self, path):
        pass

    def Acquire(self, access_mode):
        pass

    def Release(self, access_mode):
        pass

    def _test_notify_device_created_ok(self):
        self._cb_notify_device('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE')  # noqa

    def _test_notify_device_created_error(self):
        self._cb_notify_error('Unable to create device: ' +
                              self._cb_notify_dev_id)


class BTDbusTypeTranslation(unittest.TestCase):

    def test_all(self):

        val = [1, 2, 3, 4, 5]
        self.assertEqual(bt_manager.interface.translate_to_dbus_type(dbus.Array, val),  # noqa
                         dbus.Array(val))
        val = -1
        self.assertEqual(bt_manager.interface.translate_to_dbus_type(dbus.Int32, val),  # noqa
                         dbus.Int32(val))
        val = 1
        self.assertEqual(bt_manager.interface.translate_to_dbus_type(dbus.UInt32, val),  # noqa
                         dbus.UInt32(val))
        val = 'Test'
        self.assertEqual(bt_manager.interface.translate_to_dbus_type(dbus.String, val),  # noqa
                         dbus.String(val))
        val = {'Hello': 1}
        self.assertEqual(bt_manager.interface.translate_to_dbus_type(dbus.Dictionary,  # noqa
                                                           val),
                         dbus.Dictionary(val))
        val = 'True'
        self.assertEqual(bt_manager.interface.translate_to_dbus_type(dbus.Boolean, val),  # noqa
                         dbus.Boolean(True))
        val = 'False'
        self.assertEqual(bt_manager.interface.translate_to_dbus_type(dbus.Boolean, val),  # noqa
                         dbus.Boolean(False))


class BTManagerTest(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('dbus.Interface', MockDBusInterface)
        patcher.start()
        self.addCleanup(patcher.stop)
        patcher = mock.patch('dbus.SystemBus')
        patched_system_bus = patcher.start()
        self.addCleanup(patcher.stop)
        mock_system_bus = mock.MagicMock()
        patched_system_bus.return_value = mock_system_bus
        mock_system_bus.get_object.return_value = dbus.ObjectPath('/org/bluez')
        self.mock_system_bus = mock_system_bus

    def test_manager_adapters(self):
        manager = bt_manager.BTManager()
        print repr(manager)
        print '========================================================='
        print manager
        print '========================================================='
        print 'Adapters:', manager.list_adapters()
        print 'Default:', manager.default_adapter()


class BTAdapterTest(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('dbus.Interface', MockDBusInterface)
        patcher.start()
        self.addCleanup(patcher.stop)
        patcher = mock.patch('dbus.SystemBus')
        patched_system_bus = patcher.start()
        self.addCleanup(patcher.stop)
        mock_system_bus = mock.MagicMock()
        patched_system_bus.return_value = mock_system_bus
        mock_system_bus.get_object.return_value = dbus.ObjectPath('/org/bluez')
        self.mock_system_bus = mock_system_bus

    def test_get_adapter_properties(self):
        adapter = bt_manager.BTAdapter()
        print repr(adapter)
        print '========================================================='
        print adapter
        print '========================================================='
        cod = bt_manager.BTCoD(adapter.Class)
        print 'Adapter Class:', hex(adapter.Class)
        print 'Major Service Class:', str(cod.major_service_class)
        print 'Major Device Class:', str(cod.major_device_class)
        print 'Minor Device Class:', str(cod.minor_device_class)
        print '========================================================='
        uuids = adapter.UUIDs
        for i in uuids:
            uuid = bt_manager.BTUUID(i)
            print bt_manager.SERVICES.get(uuid.uuid16, 'Unknown')
        print '========================================================='

    def test_get_adapter_by_dev_id(self):
        adapter = bt_manager.BTAdapter()
        adapter_by_dev_id = bt_manager.BTAdapter(adapter.Address)
        self.assertEqual(adapter_by_dev_id.Address, adapter.Address)

    def test_set_adapter_property(self):
        adapter = bt_manager.BTAdapter()
        new_name = 'NewAdapterName-0'
        adapter.Name = new_name
        self.assertEqual(adapter.Name, new_name)

    def test_adapter_list_devices(self):
        adapter = bt_manager.BTAdapter()
        print adapter.list_devices()
        print '========================================================='

    def test_adapter_discovery(self):
        adapter = bt_manager.BTAdapter()
        adapter.start_discovery()
        self.assertTrue(adapter.Discovering)
        adapter.stop_discovery()
        self.assertFalse(adapter.Discovering)

    def test_adapter_signal_device_found(self):
        name = '11:22:33:44:55:66'
        properties = 'Test Properties'
        signal = bt_manager.BTAdapter.SIGNAL_DEVICE_FOUND

        user = mock.MagicMock()
        adapter = bt_manager.BTAdapter()
        adapter.add_signal_receiver(user.callback_fn, signal, self)
        self.mock_system_bus.add_signal_receiver.assert_called()
        cb = self.mock_system_bus.add_signal_receiver.call_args_list[0][0][0]
        cb(name, properties)
        user.callback_fn.assert_called_with(signal, self, name, properties)
        adapter.remove_signal_receiver(signal)
        self.mock_system_bus.remove_signal_receiver.assert_called()

    def test_adapter_signal_property_changed(self):
        name = 'Property'
        value = 'New Value'
        signal = bt_manager.BTAdapter.SIGNAL_PROPERTY_CHANGED

        user = mock.MagicMock()
        adapter = bt_manager.BTAdapter()
        adapter.add_signal_receiver(user.callback_fn, signal, self)
        self.mock_system_bus.add_signal_receiver.assert_called()
        cb = self.mock_system_bus.add_signal_receiver.call_args_list[0][0][0]
        cb(name, value)
        user.callback_fn.assert_called_with(signal, self, name, value)
        adapter.remove_signal_receiver(signal)
        self.mock_system_bus.remove_signal_receiver.assert_called()

    def test_adapter_signal_name_exception(self):
        adapter = bt_manager.BTAdapter()
        try:
            exception_caught = False
            adapter.add_signal_receiver(None, 'Invalid Signal Name', None)
        except bt_manager.BTSignalNameNotRecognisedException:
            exception_caught = True
        self.assertTrue(exception_caught)

    def test_adapter_find_device(self):
        adapter = bt_manager.BTAdapter()
        dev = adapter.find_device('00:11:67:D2:AB:EE')
        self.assertEqual(dev,
                         dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE'))  # noqa

    def test_adapter_create_device(self):

        user = mock.MagicMock()
        adapter = bt_manager.BTAdapter()
        dev_id = '00:11:67:D2:AB:EE'
        path = '/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE'
        caps = None

        adapter.create_paired_device(dev_id, path,
                                     caps, user.cb_notify_device,
                                     user.cb_notify_error)
        adapter._interface._test_notify_device_created_ok()
        user.cb_notify_device.assert_called()
        adapter._interface._test_notify_device_created_error()
        user.cb_notify_error.assert_called()

    def test_adapter_remove_device(self):
        adapter = bt_manager.BTAdapter()
        adapter.remove_device('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE')

    def test_adapter_register_agent(self):
        adapter = bt_manager.BTAdapter()
        adapter.register_agent('/test/agent', 'DisplayYesNo')
        adapter.unregister_agent('/test/agent')


class BTDeviceTest(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('dbus.Interface', MockDBusInterface)
        patcher.start()
        self.addCleanup(patcher.stop)
        patcher = mock.patch('dbus.SystemBus')
        patched_system_bus = patcher.start()
        self.addCleanup(patcher.stop)
        mock_system_bus = mock.MagicMock()
        patched_system_bus.return_value = mock_system_bus
        mock_system_bus.get_object.return_value = dbus.ObjectPath('/org/bluez')

    def test_get_device_properties(self):
        adapter = bt_manager.BTAdapter()
        adapter_id = adapter.Address
        devices = adapter.list_devices()
        dev_path = devices[0]
        device = bt_manager.BTDevice(dev_path=dev_path)
        print 'Vendor Name:', bt_manager.VENDORS.get(device.Vendor, 'Unknown')
        print device
        print '========================================================='
        cod = bt_manager.BTCoD(device.Class)
        print 'Device Class:', hex(device.Class)
        print 'Major Service Class:', str(cod.major_service_class)
        print 'Major Device Class:', str(cod.major_device_class)
        print 'Minor Device Class:', str(cod.minor_device_class)
        print '========================================================='
        print repr(cod)
        print '========================================================='
        print cod
        print '========================================================='
        uuids = device.UUIDs
        for i in uuids:
            uuid = bt_manager.BTUUID(i)
            print bt_manager.SERVICES.get(uuid.uuid16, 'Unknown')
        print '========================================================='
        device = bt_manager.BTDevice(adapter_id=adapter_id,
                                     dev_path=dev_path)
        print device
        print '========================================================='
        device = bt_manager.BTDevice(dev_id='00:11:67:D2:AB:EE')
        print device
        print '========================================================='
        print repr(device)
        print '========================================================='

    def test_set_device_property(self):
        devices = bt_manager.BTAdapter().list_devices()
        dev_path = devices[0]
        device = bt_manager.BTDevice(dev_path=dev_path)
        device.Trusted = False
        self.assertEqual(device.Trusted, False)

    def test_discover_services(self):
        device = bt_manager.BTDevice(dev_id='00:11:67:D2:AB:EE')
        services = device.discover_services()
        print '========================================================='
        for rec in services.keys():
            print bt_manager.BTDiscoveryInfo(services[rec])
        print '========================================================='


class BTAudioSinkTest(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('dbus.Interface', MockDBusInterface)
        patcher.start()
        self.addCleanup(patcher.stop)
        patcher = mock.patch('dbus.SystemBus')
        patched_system_bus = patcher.start()
        self.addCleanup(patcher.stop)
        mock_system_bus = mock.MagicMock()
        patched_system_bus.return_value = mock_system_bus
        mock_system_bus.get_object.return_value = dbus.ObjectPath('/org/bluez')

    def test_audio_sink_properties(self):
        sink = bt_manager.BTAudioSink(dev_id='00:11:67:D2:AB:EE')
        print sink
        print '========================================================='
        print repr(sink)
        print '========================================================='

    def test_audio_sink_connectivity(self):
        sink = bt_manager.BTAudioSink(dev_id='00:11:67:D2:AB:EE')
        sink.connect()
        self.assertTrue(sink.is_connected())
        sink.disconnect()
        self.assertFalse(sink.is_connected())


class BTControlTest(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('dbus.Interface', MockDBusInterface)
        patcher.start()
        self.addCleanup(patcher.stop)
        patcher = mock.patch('dbus.SystemBus')
        patched_system_bus = patcher.start()
        self.addCleanup(patcher.stop)
        mock_system_bus = mock.MagicMock()
        patched_system_bus.return_value = mock_system_bus
        mock_system_bus.get_object.return_value = dbus.ObjectPath('/org/bluez')

    def test_control_properties(self):
        ctrl = bt_manager.BTControl(dev_id='00:11:67:D2:AB:EE')
        print ctrl
        print '========================================================='
        print repr(ctrl)
        print '========================================================='

    def test_control_volume(self):
        ctrl = bt_manager.BTControl(dev_id='00:11:67:D2:AB:EE')
        ctrl.volume_up()
        ctrl.volume_down()


class BTMediaTest(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('dbus.Interface', MockDBusInterface)
        patcher.start()
        self.addCleanup(patcher.stop)
        patcher = mock.patch('dbus.SystemBus')
        patched_system_bus = patcher.start()
        self.addCleanup(patcher.stop)
        mock_system_bus = mock.MagicMock()
        patched_system_bus.return_value = mock_system_bus
        mock_system_bus.get_object.return_value = dbus.ObjectPath('/org/bluez')

    def test_media_endpoint(self):
        media = bt_manager.BTMedia()
        path = '/test/sbcaudiosink'
        endpoint = bt_manager.SBCAudioSink(path=path)
        media.register_endpoint(path, endpoint.get_properties())
        media.unregister_endpoint(path)


class BTAgentTest(unittest.TestCase):

    @mock.patch('dbus.SystemBus')
    def test_agent_with_defaults(self, patched_system_bus):
        mock_system_bus = mock.MagicMock()
        patched_system_bus.return_value = mock_system_bus
        mock_system_bus.get_object.return_value = dbus.ObjectPath('/org/bluez')
        agent = bt_manager.BTAgent()

        obj = dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE')
        uuid = dbus.String(u'00001108-0000-1000-8000-00805f9b34fb')
        pin_code = dbus.String('0000')
        pass_key = dbus.UInt32(0)
        mode = 'Mode'

        self.assertEqual(agent.Release(), None)
        self.assertEqual(agent.Authorize(obj, uuid), None)
        self.assertEqual(agent.RequestPinCode(obj), pin_code)
        self.assertEqual(agent.RequestPasskey(obj), pass_key)
        self.assertEqual(agent.DisplayPasskey(obj, pass_key), None)
        self.assertEqual(agent.RequestConfirmation(obj, pass_key), None)
        self.assertEqual(agent.ConfirmModeChange(mode), None)
        self.assertEqual(agent.Cancel(), None)

    @mock.patch('dbus.SystemBus')
    def test_agent_with_callbacks(self, patched_system_bus):
        mock_system_bus = mock.MagicMock()
        patched_system_bus.return_value = mock_system_bus
        mock_system_bus.get_object.return_value = dbus.ObjectPath('/org/bluez')
        user = mock.MagicMock()
        agent = bt_manager.BTAgent(cb_notify_on_release=user.cb_notify_on_release,  # noqa
                                   cb_notify_on_authorize=user.cb_notify_on_authorize,  # noqa
                                   cb_notify_on_request_pin_code=user.cb_notify_on_request_pin_code,  # noqa
                                   cb_notify_on_request_pass_key=user.cb_notify_on_request_pass_key,  # noqa
                                   cb_notify_on_display_pass_key=user.cb_notify_on_display_pass_key,  # noqa
                                   cb_notify_on_request_confirmation=user.cb_notify_on_request_confirmation,  # noqa
                                   cb_notify_on_confirm_mode_change=user.cb_notify_on_confirm_mode_change,  # noqa
                                   cb_notify_on_cancel=user.cb_notify_on_cancel)  # noqa

        obj = dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE')
        uuid = dbus.String(u'00001108-0000-1000-8000-00805f9b34fb')
        pin_code = dbus.String('0000')
        pass_key = dbus.UInt32(0x12345678L)
        mode = 'Mode'

        self.assertEqual(agent.Release(), None)
        user.cb_notify_on_release.assert_once_called_with()

        user.cb_notify_on_authorize.return_value = True
        self.assertEqual(agent.Authorize(obj, uuid), None)
        user.cb_notify_on_authorize.assert_called_once_with(bt_manager.BTAgent.NOTIFY_ON_AUTHORIZE,  # noqa
                                                            obj, uuid)

        user.reset_mock()
        user.cb_notify_on_authorize.return_value = False
        try:
            exception_raised = False
            agent.Authorize(obj, uuid)
        except bt_manager.BTRejectedException:
            exception_raised = True
        user.cb_notify_on_authorize.assert_called_once_with(bt_manager.BTAgent.NOTIFY_ON_AUTHORIZE,  # noqa
                                                            obj, uuid)
        self.assertTrue(exception_raised)

        user.cb_notify_on_request_pin_code.return_value = pin_code
        self.assertEqual(agent.RequestPinCode(obj), pin_code)
        user.cb_notify_on_request_pin_code.assert_called_once_with(bt_manager.BTAgent.NOTIFY_ON_REQUEST_PIN_CODE,  # noqa
                                                                   obj)

        user.reset_mock()
        user.cb_notify_on_request_pin_code.return_value = None
        try:
            exception_raised = False
            agent.RequestPinCode(obj)
        except bt_manager.BTRejectedException:
            exception_raised = True
        user.cb_notify_on_request_pin_code.assert_called_once_with(bt_manager.BTAgent.NOTIFY_ON_REQUEST_PIN_CODE,  # noqa
                                                                   obj)
        self.assertTrue(exception_raised)

        user.cb_notify_on_request_pass_key.return_value = pass_key
        self.assertEqual(agent.RequestPasskey(obj), pass_key)
        user.cb_notify_on_request_pass_key.assert_called_once_with(bt_manager.BTAgent.NOTIFY_ON_REQUEST_PASS_KEY,  # noqa
                                                                   obj)

        user.reset_mock()
        user.cb_notify_on_request_pass_key.return_value = None
        try:
            exception_raised = False
            agent.RequestPasskey(obj)
        except bt_manager.BTRejectedException:
            exception_raised = True
        user.cb_notify_on_request_pass_key.assert_called_once_with(bt_manager.BTAgent.NOTIFY_ON_REQUEST_PASS_KEY,  # noqa
                                                                   obj)
        self.assertTrue(exception_raised)

        self.assertEqual(agent.DisplayPasskey(obj, pass_key), None)
        user.cb_notify_on_display_pass_key.assert_called_once_with(bt_manager.BTAgent.NOTIFY_ON_DISPLAY_PASS_KEY,  # noqa
                                                                   obj,
                                                                   pass_key)

        user.cb_notify_on_request_confirmation.return_value = True
        self.assertEqual(agent.RequestConfirmation(obj, pass_key), None)
        user.cb_notify_on_request_confirmation.assert_called_once_with(bt_manager.BTAgent.NOTIFY_ON_REQUEST_CONFIRMATION,  # noqa
                                                                       obj,
                                                                       pass_key)  # noqa

        user.reset_mock()
        user.cb_notify_on_request_confirmation.return_value = False
        try:
            exception_raised = False
            agent.RequestConfirmation(obj, pass_key)
        except bt_manager.BTRejectedException:
            exception_raised = True
        user.cb_notify_on_request_confirmation.assert_called_once_with(bt_manager.BTAgent.NOTIFY_ON_REQUEST_CONFIRMATION,  # noqa
                                                                       obj,
                                                                       pass_key)  # noqa
        self.assertTrue(exception_raised)

        user.cb_notify_on_confirm_mode_change.return_value = True
        self.assertEqual(agent.ConfirmModeChange(mode), None)
        user.cb_notify_on_confirm_mode_change.assert_called_once_with(bt_manager.BTAgent.NOTIFY_ON_CONFIRM_MODE_CHANGE,  # noqa
                                                                      mode)

        user.reset_mock()
        user.cb_notify_on_confirm_mode_change.return_value = False
        try:
            exception_raised = False
            agent.ConfirmModeChange(mode)
        except bt_manager.BTRejectedException:
            exception_raised = True
        user.cb_notify_on_confirm_mode_change.assert_called_once_with(bt_manager.BTAgent.NOTIFY_ON_CONFIRM_MODE_CHANGE,  # noqa
                                                                      mode)
        self.assertTrue(exception_raised)

        self.assertEqual(agent.Cancel(), None)
        user.cb_notify_on_cancel.assert_called_once_with(bt_manager.BTAgent.NOTIFY_ON_CANCEL)  # noqa

    @mock.patch('dbus.SystemBus')
    def test_agent_corner_cases(self, patched_system_bus):
        mock_system_bus = mock.MagicMock()
        patched_system_bus.return_value = mock_system_bus
        mock_system_bus.get_object.return_value = dbus.ObjectPath('/org/bluez')
        agent = bt_manager.BTAgent(default_pin_code=None,
                                   default_pass_key=None)

        obj = dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE')

        try:
            exception_raised = False
            agent.RequestPinCode(obj)
        except bt_manager.BTRejectedException:
            exception_raised = True
        self.assertTrue(exception_raised)

        try:
            exception_raised = False
            agent.RequestPasskey(obj)
        except bt_manager.BTRejectedException:
            exception_raised = True
        self.assertTrue(exception_raised)


class SBCAudioTest(unittest.TestCase):

    @mock.patch('dbus.SystemBus')
    def test_sbc_caps_conversion(self, patched_system_bus):

        mock_system_bus = mock.MagicMock()
        patched_system_bus.return_value = mock_system_bus
        mock_system_bus.get_object.return_value = dbus.ObjectPath('/org/bluez')

        media = bt_manager.SBCAudioCodec(uuid='uuid', path='/endpoint/test')
        config = bt_manager.SBCCodecConfig(bt_manager.SBCChannelMode.ALL,
                                           bt_manager.SBCSamplingFrequency.ALL,
                                           bt_manager.SBCAllocationMethod.ALL,
                                           bt_manager.SBCSubbands.ALL,
                                           bt_manager.SBCBlocks.ALL,
                                           2,
                                           64)
        dbus_config = media._make_config(config)
        self.assertEqual(dbus_config, dbus.Array([dbus.Byte(0xFF),
                                                  dbus.Byte(0xFF),
                                                  dbus.Byte(2),
                                                  dbus.Byte(64)]))
        self.assertEqual(media._parse_config(dbus_config), config)

    def test_sbc_default_bitpool(self):

        frequency = bt_manager.SBCSamplingFrequency.FREQ_16KHZ
        channel_mode = 0   # Don't care
        bitpool = bt_manager.SBCAudioCodec._default_bitpool(frequency,
                                                            channel_mode)
        self.assertEqual(bitpool, 53)

        frequency = bt_manager.SBCSamplingFrequency.FREQ_32KHZ
        channel_mode = 0   # Don't care
        bitpool = bt_manager.SBCAudioCodec._default_bitpool(frequency,
                                                            channel_mode)
        self.assertEqual(bitpool, 53)

        frequency = bt_manager.SBCSamplingFrequency.FREQ_44_1KHZ
        channel_mode = bt_manager.SBCChannelMode.CHANNEL_MODE_MONO
        bitpool = bt_manager.SBCAudioCodec._default_bitpool(frequency,
                                                            channel_mode)
        self.assertEqual(bitpool, 31)

        frequency = bt_manager.SBCSamplingFrequency.FREQ_44_1KHZ
        channel_mode = bt_manager.SBCChannelMode.CHANNEL_MODE_DUAL
        bitpool = bt_manager.SBCAudioCodec._default_bitpool(frequency,
                                                            channel_mode)
        self.assertEqual(bitpool, 31)

        frequency = bt_manager.SBCSamplingFrequency.FREQ_44_1KHZ
        channel_mode = bt_manager.SBCChannelMode.CHANNEL_MODE_JOINT_STEREO
        bitpool = bt_manager.SBCAudioCodec._default_bitpool(frequency,
                                                            channel_mode)
        self.assertEqual(bitpool, 53)

        frequency = bt_manager.SBCSamplingFrequency.FREQ_44_1KHZ
        channel_mode = bt_manager.SBCChannelMode.CHANNEL_MODE_STEREO
        bitpool = bt_manager.SBCAudioCodec._default_bitpool(frequency,
                                                            channel_mode)
        self.assertEqual(bitpool, 53)

        frequency = bt_manager.SBCSamplingFrequency.FREQ_48KHZ
        channel_mode = bt_manager.SBCChannelMode.CHANNEL_MODE_STEREO
        bitpool = bt_manager.SBCAudioCodec._default_bitpool(frequency,
                                                            channel_mode)
        self.assertEqual(bitpool, 51)

        frequency = bt_manager.SBCSamplingFrequency.FREQ_48KHZ
        channel_mode = bt_manager.SBCChannelMode.CHANNEL_MODE_JOINT_STEREO
        bitpool = bt_manager.SBCAudioCodec._default_bitpool(frequency,
                                                            channel_mode)
        self.assertEqual(bitpool, 51)

        frequency = bt_manager.SBCSamplingFrequency.FREQ_48KHZ
        channel_mode = bt_manager.SBCChannelMode.CHANNEL_MODE_MONO
        bitpool = bt_manager.SBCAudioCodec._default_bitpool(frequency,
                                                            channel_mode)
        self.assertEqual(bitpool, 29)

        frequency = bt_manager.SBCSamplingFrequency.FREQ_48KHZ
        channel_mode = bt_manager.SBCChannelMode.CHANNEL_MODE_DUAL
        bitpool = bt_manager.SBCAudioCodec._default_bitpool(frequency,
                                                            channel_mode)
        self.assertEqual(bitpool, 29)

        frequency = -1     # Out of range
        channel_mode = -1  # Out of range
        bitpool = bt_manager.SBCAudioCodec._default_bitpool(frequency,
                                                            channel_mode)
        self.assertEqual(bitpool, 53)

    @mock.patch('dbus.SystemBus')
    def test_sbc_caps_negotiation(self, patched_system_bus):
        mock_system_bus = mock.MagicMock()
        patched_system_bus.return_value = mock_system_bus
        mock_system_bus.get_object.return_value = dbus.ObjectPath('/org/bluez')

        media = bt_manager.SBCAudioSource()
        caps = bt_manager.SBCCodecConfig(bt_manager.codecs.SBCChannelMode.ALL,
                                         bt_manager.codecs.SBCSamplingFrequency.ALL,  # noqa
                                         bt_manager.codecs.SBCAllocationMethod.ALL,  # noqa
                                         bt_manager.codecs.SBCSubbands.ALL,
                                         bt_manager.codecs.SBCBlocks.ALL,
                                         2,
                                         64)
        expected = bt_manager.SBCCodecConfig(bt_manager.codecs.SBCChannelMode.CHANNEL_MODE_JOINT_STEREO,  # noqa
                                             bt_manager.codecs.SBCSamplingFrequency.FREQ_44_1KHZ,  # noqa
                                             bt_manager.codecs.SBCAllocationMethod.LOUDNESS,  # noqa
                                             bt_manager.codecs.SBCSubbands.SUBBANDS_8,  # noqa
                                             bt_manager.codecs.SBCBlocks.BLOCKS_16,  # noqa
                                             2,
                                             53)
        dbus_caps = media._make_config(caps)
        expected_dbus = media._make_config(expected)
        actual_dbus = media.SelectConfiguration(dbus_caps)
        self.assertEqual(actual_dbus, expected_dbus)

        caps = bt_manager.SBCCodecConfig(bt_manager.codecs.SBCChannelMode.CHANNEL_MODE_MONO,  # noqa
                                         bt_manager.codecs.SBCSamplingFrequency.FREQ_48KHZ,  # noqa
                                         bt_manager.codecs.SBCAllocationMethod.SNR,  # noqa
                                         bt_manager.codecs.SBCSubbands.SUBBANDS_4,  # noqa
                                         bt_manager.codecs.SBCBlocks.BLOCKS_12,
                                         2,
                                         64)
        expected = bt_manager.SBCCodecConfig(bt_manager.codecs.SBCChannelMode.CHANNEL_MODE_MONO,  # noqa
                                             bt_manager.codecs.SBCSamplingFrequency.FREQ_44_1KHZ,  # noqa
                                             bt_manager.codecs.SBCAllocationMethod.SNR,  # noqa
                                             bt_manager.codecs.SBCSubbands.SUBBANDS_4,  # noqa
                                             bt_manager.codecs.SBCBlocks.BLOCKS_12,  # noqa
                                             2,
                                             31)
        dbus_caps = media._make_config(caps)
        expected_dbus = media._make_config(expected)
        actual_dbus = media.SelectConfiguration(dbus_caps)
        self.assertEqual(actual_dbus, expected_dbus)

        caps = bt_manager.SBCCodecConfig(bt_manager.codecs.SBCChannelMode.CHANNEL_MODE_DUAL,  # noqa
                                         bt_manager.codecs.SBCSamplingFrequency.FREQ_44_1KHZ,  # noqa
                                         bt_manager.codecs.SBCAllocationMethod.LOUDNESS,  # noqa
                                         bt_manager.codecs.SBCSubbands.SUBBANDS_8,  # noqa
                                         bt_manager.codecs.SBCBlocks.BLOCKS_8,
                                         2,
                                         64)
        expected = bt_manager.SBCCodecConfig(bt_manager.codecs.SBCChannelMode.CHANNEL_MODE_DUAL,  # noqa
                                             bt_manager.codecs.SBCSamplingFrequency.FREQ_44_1KHZ,  # noqa
                                             bt_manager.codecs.SBCAllocationMethod.LOUDNESS,  # noqa
                                             bt_manager.codecs.SBCSubbands.SUBBANDS_8,  # noqa
                                             bt_manager.codecs.SBCBlocks.BLOCKS_8,  # noqa
                                             2,
                                             31)
        dbus_caps = media._make_config(caps)
        expected_dbus = media._make_config(expected)
        actual_dbus = media.SelectConfiguration(dbus_caps)
        self.assertEqual(actual_dbus, expected_dbus)

        caps = bt_manager.SBCCodecConfig(bt_manager.codecs.SBCChannelMode.CHANNEL_MODE_STEREO,  # noqa
                                         bt_manager.codecs.SBCSamplingFrequency.FREQ_32KHZ,  # noqa
                                         bt_manager.codecs.SBCAllocationMethod.ALL,  # noqa
                                         bt_manager.codecs.SBCSubbands.SUBBANDS_8,  # noqa
                                         bt_manager.codecs.SBCBlocks.BLOCKS_4,
                                         2,
                                         64)
        expected = bt_manager.SBCCodecConfig(bt_manager.codecs.SBCChannelMode.CHANNEL_MODE_STEREO,  # noqa
                                             bt_manager.codecs.SBCSamplingFrequency.FREQ_44_1KHZ,  # noqa
                                             bt_manager.codecs.SBCAllocationMethod.LOUDNESS,  # noqa
                                             bt_manager.codecs.SBCSubbands.SUBBANDS_8,  # noqa
                                             bt_manager.codecs.SBCBlocks.BLOCKS_4,  # noqa
                                             2,
                                             53)
        dbus_caps = media._make_config(caps)
        expected_dbus = media._make_config(expected)
        actual_dbus = media.SelectConfiguration(dbus_caps)
        self.assertEqual(actual_dbus, expected_dbus)

    @mock.patch('os.close')
    @mock.patch('dbus.SystemBus')
    @mock.patch('bt_manager.audio.BTAudioSink')
    @mock.patch('bt_manager.audio.BTMediaTransport')
    def test_sbc_audio_source(self, patched_transport, patched_audio,
                              patched_system_bus, mock_close):

        mock_system_bus = mock.MagicMock()
        patched_system_bus.return_value = mock_system_bus
        mock_system_bus.get_object.return_value = dbus.ObjectPath('/org/bluez')

        mock_audio = mock.MagicMock()
        patched_audio.return_value = mock_audio
        patched_audio.SIGNAL_PROPERTY_CHANGED = 'PropertyChanged'
        mock_audio.State = 'disconnected'

        mock_transport = mock.MagicMock()
        patched_transport.return_value = mock_transport

        media = bt_manager.SBCAudioSource()
        caps = bt_manager.SBCCodecConfig(bt_manager.SBCChannelMode.ALL,
                                         bt_manager.SBCSamplingFrequency.ALL,
                                         bt_manager.SBCAllocationMethod.ALL,
                                         bt_manager.SBCSubbands.ALL,
                                         bt_manager.SBCBlocks.ALL,
                                         2,
                                         64)
        dbus_caps = media._make_config(caps)
        transport = dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE/fd0')  # noqa
        config = bt_manager.SBCCodecConfig(bt_manager.SBCChannelMode.CHANNEL_MODE_JOINT_STEREO,  # noqa
                                           bt_manager.SBCSamplingFrequency.FREQ_44_1KHZ,  # noqa
                                           bt_manager.SBCAllocationMethod.LOUDNESS,  # noqa
                                           bt_manager.SBCSubbands.SUBBANDS_8,
                                           bt_manager.SBCBlocks.BLOCKS_16,
                                           2,
                                           53)
        dbus_config = dbus.Dictionary({'Device': dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE'),  # noqa
                                       'Configuration': media._make_config(config)})  # noqa
        media.SelectConfiguration(dbus_caps)
        media.SetConfiguration(transport, dbus_config)
        mock_audio.add_signal_receiver.assert_called_once_with(media._property_change_event_handler,  # noqa
                                                               bt_manager.BTAudioSink.SIGNAL_PROPERTY_CHANGED,  # noqa
                                                               transport)

        fd_value = os.open('/dev/null', os.O_WRONLY)
        read_mtu = 503
        write_mtu = 503
        fd = mock.MagicMock()
        fd.take.return_value = fd_value
        mock_transport.acquire.return_value = (fd, write_mtu, read_mtu)

        mock_audio.State = 'connecting'
        media._property_change_event_handler('State',
                                             transport, mock_audio.State)
        mock_audio.State = 'connected'
        media._property_change_event_handler('State',
                                             transport, mock_audio.State)
        mock_transport.acquire.assert_called_once_with('w')
        mock_audio.State = 'disconnected'

        data = [b'\x00'] * 512
        media.write_transport(data)

        try:
            exception_caught = False
            media.read_transport()
        except bt_manager.BTIncompatibleTransportAccessType:
            exception_caught = True
        self.assertTrue(exception_caught)

        media._property_change_event_handler('State', transport,
                                             mock_audio.State)
        mock_transport.release.assert_called_once_with('w')
        mock_close.assert_called_with(fd_value)

        media.ClearConfiguration()
        media.Release()

    @mock.patch('os.close')
    @mock.patch('dbus.SystemBus')
    @mock.patch('bt_manager.audio.BTAudioSource')
    @mock.patch('bt_manager.audio.BTMediaTransport')
    def test_sbc_audio_sink(self, patched_transport, patched_audio,
                            patched_system_bus, mock_close):

        mock_system_bus = mock.MagicMock()
        patched_system_bus.return_value = mock_system_bus
        mock_system_bus.get_object.return_value = dbus.ObjectPath('/org/bluez')

        mock_audio = mock.MagicMock()
        patched_audio.return_value = mock_audio
        patched_audio.SIGNAL_PROPERTY_CHANGED = 'PropertyChanged'
        mock_audio.State = 'disconnected'

        mock_transport = mock.MagicMock()
        patched_transport.return_value = mock_transport

        media = bt_manager.SBCAudioSink()
        caps = bt_manager.SBCCodecConfig(bt_manager.SBCChannelMode.ALL,
                                         bt_manager.SBCSamplingFrequency.ALL,
                                         bt_manager.SBCAllocationMethod.ALL,
                                         bt_manager.SBCSubbands.ALL,
                                         bt_manager.SBCBlocks.ALL,
                                         2,
                                         64)
        dbus_caps = media._make_config(caps)
        transport = dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE/fd0')  # noqa
        config = bt_manager.SBCCodecConfig(bt_manager.SBCChannelMode.CHANNEL_MODE_JOINT_STEREO,  # noqa
                                           bt_manager.SBCSamplingFrequency.FREQ_44_1KHZ,  # noqa
                                           bt_manager.SBCAllocationMethod.LOUDNESS,  # noqa
                                           bt_manager.SBCSubbands.SUBBANDS_8,
                                           bt_manager.SBCBlocks.BLOCKS_16,
                                           2,
                                           53)
        dbus_config = dbus.Dictionary({'Device': dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE'),  # noqa
                                       'Configuration': media._make_config(config)})  # noqa
        media.SelectConfiguration(dbus_caps)
        media.SetConfiguration(transport, dbus_config)
        mock_audio.add_signal_receiver.assert_called_once_with(media._property_change_event_handler,  # noqa
                                                               'PropertyChanged',  # noqa
                                                               transport)

        fd_value = os.open('tests/vector.dat', os.O_RDONLY)
        read_mtu = 503
        write_mtu = 503
        fd = mock.MagicMock()
        fd.take.return_value = fd_value
        mock_transport.acquire.return_value = (fd, write_mtu, read_mtu)

        mock_audio.State = 'connected'
        media._property_change_event_handler('State',
                                             transport, mock_audio.State)
        mock_audio.State = 'playing'
        media._property_change_event_handler('State',
                                             transport, mock_audio.State)
        mock_transport.acquire.assert_called_once_with('r')
        mock_audio.State = 'connected'

        data = media.read_transport()
        self.assertEqual(len(data), 512)

        try:
            exception_caught = False
            media.write_transport('dummy data')
        except bt_manager.BTIncompatibleTransportAccessType:
            exception_caught = True
        self.assertTrue(exception_caught)

        media._property_change_event_handler('State', transport,
                                             mock_audio.State)
        mock_transport.release.assert_called_once_with('r')
        mock_close.assert_called_with(fd_value)

        media.ClearConfiguration()
        media.Release()
