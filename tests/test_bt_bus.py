from __future__ import unicode_literals

import unittest

import bt_manager
import mock
import dbus


class MockDBusInterface:
    """Mock dbus.Interface implementation for purpose of testing"""
    def __init__(self, obj, addr):
        self.addr = addr
        if (self.addr == 'org.bluez.Adapter'):
            self._props = dbus.Dictionary(
                                   {dbus.String(u'Name'): dbus.String(u'new-name', variant_level=1),
                                    dbus.String(u'Powered'): dbus.Boolean(True, variant_level=1),
                                    dbus.String(u'Devices'):
                                    dbus.Array([dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE')],
                                               signature=dbus.Signature('o'), variant_level=1),
                                    dbus.String(u'DiscoverableTimeout'): dbus.UInt32(0L, variant_level=1),
                                    dbus.String(u'PairableTimeout'): dbus.UInt32(0L, variant_level=1),
                                    dbus.String(u'Discoverable'): dbus.Boolean(True, variant_level=1),
                                    dbus.String(u'Address'): dbus.String(u'AC:7B:A1:3C:13:82', variant_level=1),
                                    dbus.String(u'Discovering'): dbus.Boolean(False, variant_level=1),
                                    dbus.String(u'Pairable'): dbus.Boolean(True, variant_level=1),
                                    dbus.String(u'Class'): dbus.UInt32(7209216L, variant_level=1),
                                    dbus.String(u'UUIDs'):
                                    dbus.Array([dbus.String(u'00001000-0000-1000-8000-00805f9b34fb'),
                                                dbus.String(u'00001001-0000-1000-8000-00805f9b34fb'),
                                                dbus.String(u'0000112d-0000-1000-8000-00805f9b34fb'),
                                                dbus.String(u'00001112-0000-1000-8000-00805f9b34fb'),
                                                dbus.String(u'0000111f-0000-1000-8000-00805f9b34fb'),
                                                dbus.String(u'0000111e-0000-1000-8000-00805f9b34fb'),
                                                dbus.String(u'0000110a-0000-1000-8000-00805f9b34fb'),
                                                dbus.String(u'0000110b-0000-1000-8000-00805f9b34fb'),
                                                dbus.String(u'0000110c-0000-1000-8000-00805f9b34fb'),
                                                dbus.String(u'0000110e-0000-1000-8000-00805f9b34fb'),
                                                dbus.String(u'00001103-0000-1000-8000-00805f9b34fb')],
                                               signature=dbus.Signature('s'), variant_level=1)},
                                   signature=dbus.Signature('sv'))
        elif (self.addr == 'org.bluez.Device'):
            self._props = dbus.Dictionary({dbus.String(u'Product'): dbus.UInt16(5028, variant_level=1),
                                           dbus.String(u'Vendor'): dbus.UInt16(57, variant_level=1),
                                           dbus.String(u'Name'): dbus.String(u'BTS-06', variant_level=1),
                                           dbus.String(u'Paired'): dbus.Boolean(True, variant_level=1),
                                           dbus.String(u'Adapter'): dbus.ObjectPath('/org/bluez/985/hci0',
                                                                                    variant_level=1),
                                           dbus.String(u'Alias'): dbus.String(u'BTS-06', variant_level=1),
                                           dbus.String(u'Version'): dbus.UInt16(260, variant_level=1),
                                           dbus.String(u'Connected'): dbus.Boolean(False, variant_level=1),
                                           dbus.String(u'UUIDs'):
                                                dbus.Array([dbus.String(u'00001108-0000-1000-8000-00805f9b34fb'),
                                                            dbus.String(u'0000110b-0000-1000-8000-00805f9b34fb'),
                                                            dbus.String(u'0000110c-0000-1000-8000-00805f9b34fb'),
                                                            dbus.String(u'0000110e-0000-1000-8000-00805f9b34fb'),
                                                            dbus.String(u'0000111e-0000-1000-8000-00805f9b34fb'),
                                                            dbus.String(u'00001200-0000-1000-8000-00805f9b34fb')],
                                                           signature=dbus.Signature('s'), variant_level=1),
                                           dbus.String(u'Address'): dbus.String(u'00:11:67:D2:AB:EE', variant_level=1),
                                           dbus.String(u'Services'): dbus.Array([], signature=dbus.Signature('o'), variant_level=1),
                                           dbus.String(u'Blocked'): dbus.Boolean(False, variant_level=1),
                                           dbus.String(u'Class'): dbus.UInt32(2360340L, variant_level=1),
                                           dbus.String(u'Trusted'): dbus.Boolean(True, variant_level=1),
                                           dbus.String(u'Icon'): dbus.String(u'audio-card', variant_level=1)},
                                          signature=dbus.Signature('sv'))

    def StartDiscovery(self):
        self._props[dbus.String(u'Discovering')] = dbus.Boolean(True, variant_level=1)

    def StopDiscovery(self):
        self._props[dbus.String(u'Discovering')] = dbus.Boolean(False, variant_level=1)

    def FindAdapter(self, *args):
        return dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE')

    def DefaultAdapter(self, *args):
        return dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE')

    def SetProperty(self, name, value):
        self._props[name] = value

    def GetProperties(self):
        return self._props

    def FindDevice(self, *args):
        return dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE')

    def ListDevices(self, *args):
        return dbus.Array([dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE')],
                                        signature=dbus.Signature('o'))

    def CreatePairedDevice(self, dev_id, path, caps, cb_notify_device, cb_notify_error):
        self._cb_notify_dev_id = dev_id
        self._cb_notify_device = cb_notify_device
        self._cb_notify_error = cb_notify_error

    def RemoveDevice(self, dev_obj):
        pass

    def RegisterAgent(self, path, caps):
        pass

    def _test_notify_device_created_ok(self):
        self._cb_notify_device(dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE'))

    def _test_notify_device_created_error(self):
        print "Callback notify device error"
        self._cb_notify_error('Unable to create device: ' + self._cb_notify_dev_id)
 

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
        global address, properties, is_called
        address = '11:22:33:44:55:66'
        properties = 'Test Properties'
        is_called = False
        def callback_fn(*args):
            global address, properties, is_called
            is_called = True
            self = args[0]
            self.assertEqual(args[1], address)
            self.assertEqual(args[2], properties)

        adapter = bt_manager.BTAdapter()
        adapter.add_signal_receiver(callback_fn, bt_manager.BTAdapter.SIGNAL_NAME_DEVICE_FOUND, self)
        self.mock_system_bus.add_signal_receiver.assert_called()
        cb = self.mock_system_bus.add_signal_receiver.call_args_list[0][0][0]
        cb(address, properties)
        self.assertTrue(is_called)
        adapter.remove_signal_receiver(bt_manager.BTAdapter.SIGNAL_NAME_DEVICE_FOUND)
        self.mock_system_bus.remove_signal_receiver.assert_called()

    def test_adapter_signal_property_changed(self):
        global name, value, is_called
        name = 'Property'
        value = 'New Value'
        is_called = False
        def callback_fn(*args):
            global name, value, is_called
            is_called = True
            self = args[0]
            self.assertEqual(args[1], name)
            self.assertEqual(args[2], value)

        adapter = bt_manager.BTAdapter()
        adapter.add_signal_receiver(callback_fn, bt_manager.BTAdapter.SIGNAL_NAME_PROPERTY_CHANGED, self)
        self.mock_system_bus.add_signal_receiver.assert_called()
        cb = self.mock_system_bus.add_signal_receiver.call_args_list[0][0][0]
        cb(name, value)
        self.assertTrue(is_called)
        adapter.remove_signal_receiver(bt_manager.BTAdapter.SIGNAL_NAME_PROPERTY_CHANGED)
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
        self.assertEqual(dev, dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE'))

    def test_adapter_create_device(self):

        global cb_notify_device_called, cb_notify_error_called
        cb_notify_device_called = False
        def cb_notify_device(*args):
            global cb_notify_device_called
            cb_notify_device_called = True
        cb_notify_error_called = False
        def cb_notify_error(*args):
            global cb_notify_error_called
            cb_notify_error_called = True


        adapter = bt_manager.BTAdapter()
        dev_id = '00:11:67:D2:AB:EE'
        path = dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE')
        caps = None

        adapter.create_paired_device(dev_id, path, caps, cb_notify_device, cb_notify_error)
        adapter._interface._test_notify_device_created_ok()
        self.assertTrue(cb_notify_device_called)
        adapter._interface._test_notify_device_created_error()
        self.assertTrue(cb_notify_error_called)

    def test_adapter_remove_device(self):
        adapter = bt_manager.BTAdapter()
        adapter.remove_device('00:11:67:D2:AB:EE')

    def test_adapter_register_agent(self):
        adapter = bt_manager.BTAdapter()
        adapter.register_agent('/test/agent', 'DisplayYesNo')


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
        device = bt_manager.BTDevice(dev_object_path=dev_path)
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
        device = bt_manager.BTDevice(adapter_id=adapter_id, dev_object_path=dev_path)
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
        device = bt_manager.BTDevice(dev_object_path=dev_path)
        device.Trusted = False
        self.assertEqual(device.Trusted, False)


class BTAgentTest(unittest.TestCase):
    
    @mock.patch('dbus.SystemBus')
    def test_agent_with_defaults(self, patched_system_bus):
        mock_system_bus = mock.MagicMock()
        patched_system_bus.return_value = mock_system_bus
        mock_system_bus.get_object.return_value = dbus.ObjectPath('/org/bluez')
        adapter = mock.MagicMock()
        agent = bt_manager.BTAgent(adapter)
        adapter.register_agent.assert_called_with('/test/agent', 'DisplayYesNo')

        obj = dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE')
        uuid = dbus.String(u'00001108-0000-1000-8000-00805f9b34fb')
        pin_code = dbus.String('0000')
        pass_key = dbus.UInt32(0x12345678L)
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
        adapter = mock.MagicMock()
        user = mock.MagicMock()
        agent = bt_manager.BTAgent(adapter,
                                   cb_notify_on_release = user.cb_notify_on_release,
                                   cb_notify_on_authorize = user.cb_notify_on_authorize,
                                   cb_notify_on_request_pin_code = user.cb_notify_on_request_pin_code,
                                   cb_notify_on_request_pass_key = user.cb_notify_on_request_pass_key,
                                   cb_notify_on_display_pass_key = user.cb_notify_on_display_pass_key,
                                   cb_notify_on_request_confirmation = user.cb_notify_on_request_confirmation,
                                   cb_notify_on_confirm_mode_change = user.cb_notify_on_confirm_mode_change,
                                   cb_notify_on_cancel = user.cb_notify_on_cancel)
        adapter.register_agent.assert_once_called_with('/test/agent', 'DisplayYesNo')

        obj = dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE')
        uuid = dbus.String(u'00001108-0000-1000-8000-00805f9b34fb')
        pin_code = dbus.String('0000')
        pass_key = dbus.UInt32(0x12345678L)
        mode = 'Mode'

        self.assertEqual(agent.Release(), None)
        user.cb_notify_on_release.assert_once_called_with()
        
        user.cb_notify_on_authorize.return_value = True
        self.assertEqual(agent.Authorize(obj, uuid), None)
        user.cb_notify_on_authorize.assert_called_once_with(obj, uuid)
        
        user.reset_mock()
        user.cb_notify_on_authorize.return_value = False
        try:
            exception_raised = False
            agent.Authorize(obj, uuid)
        except bt_manager.RejectedException:
            exception_raised = True
        user.cb_notify_on_authorize.assert_called_once_with(obj, uuid)
        self.assertTrue(exception_raised)

        user.cb_notify_on_request_pin_code.return_value = pin_code
        self.assertEqual(agent.RequestPinCode(obj), pin_code)
        user.cb_notify_on_request_pin_code.assert_called_once_with(obj)

        user.reset_mock()
        user.cb_notify_on_request_pin_code.return_value = None
        try:
            exception_raised = False
            agent.RequestPinCode(obj)
        except bt_manager.RejectedException:
            exception_raised = True
        user.cb_notify_on_request_pin_code.assert_called_once_with(obj)
        self.assertTrue(exception_raised)

        user.cb_notify_on_request_pass_key.return_value = pass_key
        self.assertEqual(agent.RequestPasskey(obj), pass_key)
        user.cb_notify_on_request_pass_key.assert_called_once_with(obj)

        user.reset_mock()
        user.cb_notify_on_request_pass_key.return_value = None
        try:
            exception_raised = False
            agent.RequestPasskey(obj)
        except bt_manager.RejectedException:
            exception_raised = True
        user.cb_notify_on_request_pass_key.assert_called_once_with(obj)
        self.assertTrue(exception_raised)

        self.assertEqual(agent.DisplayPasskey(obj, pass_key), None)
        user.cb_notify_on_display_pass_key.assert_called_once_with(obj, pass_key)

        user.cb_notify_on_request_confirmation.return_value = True
        self.assertEqual(agent.RequestConfirmation(obj, pass_key), None)
        user.cb_notify_on_request_confirmation.assert_called_once_with(obj, pass_key)

        user.reset_mock()
        user.cb_notify_on_request_confirmation.return_value = False
        try:
            exception_raised = False
            agent.RequestConfirmation(obj, pass_key)
        except bt_manager.RejectedException:
            exception_raised = True
        user.cb_notify_on_request_confirmation.assert_called_once_with(obj, pass_key)
        self.assertTrue(exception_raised)

        user.cb_notify_on_confirm_mode_change.return_value = True
        self.assertEqual(agent.ConfirmModeChange(mode), None)
        user.cb_notify_on_confirm_mode_change.assert_called_once_with(mode)

        user.reset_mock()
        user.cb_notify_on_confirm_mode_change.return_value = False
        try:
            exception_raised = False
            agent.ConfirmModeChange(mode)
        except bt_manager.RejectedException:
            exception_raised = True
        user.cb_notify_on_confirm_mode_change.assert_called_once_with(mode)
        self.assertTrue(exception_raised)

        self.assertEqual(agent.Cancel(), None)
        user.cb_notify_on_cancel.assert_called_once_with()

    @mock.patch('dbus.SystemBus')
    def test_agent_corner_cases(self, patched_system_bus):
        mock_system_bus = mock.MagicMock()
        patched_system_bus.return_value = mock_system_bus
        mock_system_bus.get_object.return_value = dbus.ObjectPath('/org/bluez')
        adapter = mock.MagicMock()
        agent = bt_manager.BTAgent(adapter,
                                   default_pin_code=None,
                                   default_pass_key=None)

        obj = dbus.ObjectPath('/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE')

        try:
            exception_raised = False
            agent.RequestPinCode(obj)
        except bt_manager.RejectedException:
            exception_raised = True
        self.assertTrue(exception_raised)

        try:
            exception_raised = False
            agent.RequestPasskey(obj)
        except bt_manager.RejectedException:
            exception_raised = True
        self.assertTrue(exception_raised)
