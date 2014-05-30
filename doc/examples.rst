********
Examples
********


Management
==========

The following code block will display a list of bluetooth :term:`adapter`\s on your system.

.. code-block:: python

	import BTManager

  	mgr = bt_manager.BTManager()
  	adapters = mgr.list_adapters()
  	print adapters

**Example output:**

.. code-block:: python

	dbus.Array([dbus.ObjectPath('/org/bluez/2823/hci0')], signature=dbus.Signature('o'))


Adapter
=======

The following code block will, using the default adapter, display all the adapter's
properties.

.. code-block:: python

    import BTManager

    adapter = bt_manager.BTAdapter()
    print '========================================================='
    print adapter
    print '========================================================='
    cod = bt_manager.BTCoD(adapter.Class)
    print 'Vendor Name:', bt_manager.VENDORS.get(adapter.Vendor, 'Unknown')
    print 'Device Class:', hex(adapter.Class)
    print 'Major Service Class:', str(cod.major_service_class)
    print 'Major Device Class:', str(cod.major_device_class)
    print 'Minor Device Class:', str(cod.minor_device_class)
    print '========================================================='
    uuids = adapter.UUIDs
    for i in uuids:
        uuid = bt_manager.BTUUID(i)
        print bt_manager.SERVICES.get(uuid.uuid16, uuid)
    print '========================================================='

**Example output:**

.. code-block:: python

  =========================================================
  dbus.Dictionary({dbus.String(u'Name'): dbus.String(u'raspberrypi-0', variant_level=1), dbus.String(u'Powered'): dbus.Boolean(True, variant_level=1), dbus.String(u'Devices'): dbus.Array([dbus.ObjectPath('/org/bluez/2823/hci0/dev_00_88_65_A8_EA_79'), dbus.ObjectPath('/org/bluez/2823/hci0/dev_00_11_67_D2_AB_EE')], signature=dbus.Signature('o'), variant_level=1), dbus.String(u'DiscoverableTimeout'): dbus.UInt32(0L, variant_level=1), dbus.String(u'PairableTimeout'): dbus.UInt32(0L, variant_level=1), dbus.String(u'Discoverable'): dbus.Boolean(False, variant_level=1), dbus.String(u'Address'): dbus.String(u'00:02:72:CC:9C:92', variant_level=1), dbus.String(u'Discovering'): dbus.Boolean(False, variant_level=1), dbus.String(u'Pairable'): dbus.Boolean(True, variant_level=1), dbus.String(u'Class'): dbus.UInt32(4325632L, variant_level=1), dbus.String(u'UUIDs'): dbus.Array([dbus.String(u'00001000-0000-1000-8000-00805f9b34fb'), dbus.String(u'00001001-0000-1000-8000-00805f9b34fb'), dbus.String(u'0000112d-0000-1000-8000-00805f9b34fb'), dbus.String(u'00001112-0000-1000-8000-00805f9b34fb'), dbus.String(u'0000111f-0000-1000-8000-00805f9b34fb'), dbus.String(u'0000110c-0000-1000-8000-00805f9b34fb'), dbus.String(u'0000110e-0000-1000-8000-00805f9b34fb'), dbus.String(u'00001103-0000-1000-8000-00805f9b34fb')], signature=dbus.Signature('s'), variant_level=1)}, signature=dbus.Signature('sv'))
  =========================================================
  Vendor Name: Unknown
  Device Class: 0x420100L
  Major Service Class: [u'Telephony (Cordless telephony, Modem, Headset service, ...)', u'Networking (LAN, Ad hoc, ...)']
  Major Device Class: Computer (desktop, notebook, PDA, organizer, ... )
  Minor Device Class: [u'Uncategorized, code for device not assigned']
  =========================================================
  <uuid:00001000-0000-1000-8000-00805F9B34FB name:ServiceDiscoveryServerServiceClassID desc:Bluetooth Core Specification>
  <uuid:00001001-0000-1000-8000-00805F9B34FB name:BrowseGroupDescriptorServiceClassID desc:Bluetooth Core Specification>
  <uuid:0000112D-0000-1000-8000-00805F9B34FB name:SIMAccess desc:SIM Access Profile (SAP) NOTE: Used as both Service Class Identifier and Profile Identifier.>
  <uuid:00001112-0000-1000-8000-00805F9B34FB name:HeadsetAudioGateway desc:Headset Profile (HSP)>
  <uuid:0000111F-0000-1000-8000-00805F9B34FB name:HandsfreeAudioGateway desc:Hands-free Profile (HFP)>
  <uuid:0000110C-0000-1000-8000-00805F9B34FB name:AVRemoteControlTarget desc:Audio/Video Remote Control Profile (AVRCP)>
  <uuid:0000110E-0000-1000-8000-00805F9B34FB name:AVRemoteControl desc:Audio/Video Remote Control Profile (AVRCP) NOTE: Used as both Service Class Identifier and Profile Identifier.>
  <uuid:00001103-0000-1000-8000-00805F9B34FB name:DialupNetworking desc:Dial-up Networking Profile (DUN) NOTE: Used as both Service Class Identifier and Profile Identifier.>
  =========================================================


Pairing
=======

The following code installs a simple pairing agent and automatically pairs and
creates a new device given its address.  Note that the pairing process runs as
part of a ``gobject`` main loop and so requires ``glib``.

.. code-block:: python

    import bt_manager
    import gobject
    import dbus

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    # Create some default handlers
    def agent_event_handler(*args):
        print '\n========================================================='
        print 'Agent event:', args
        return True


    def device_created_ok(*args):
        print '\n========================================================='
        print 'New Device Paired:', args


    def device_created_error(*args):
        print '\n========================================================='
        print 'Pairing Error:', args

    path = '/test/agent'
    agent = bt_manager.BTAgent(path=path,
                               cb_notify_on_release=agent_event_handler,
                               cb_notify_on_authorize=agent_event_handler,
                               cb_notify_on_request_confirmation=agent_event_handler,
                               cb_notify_on_confirm_mode_change=agent_event_handler,
                               cb_notify_on_cancel=agent_event_handler)
    caps = 'DisplayYesNo'

    # This should be substituted for a bluetooth device on your network
    dev_id = '00:11:67:D2:AB:EE'
    adapter.create_paired_device(dev_id, path, caps,
                                 device_created_ok,
                                 device_created_error)

    gobject.MainLoop().run()

**Example output:**

.. code-block:: python

  =========================================================
  Agent event: (u'Release',)

  =========================================================
  New Device Paired: (dbus.ObjectPath('/org/bluez/2823/hci0/dev_00_11_67_D2_AB_EE'),)


Discovery
=========

The following code will initiate the device discovery procedure and report back
the services for the discovered device.

.. code-block:: python

    import bt_manager

    # This should be substituted for a paired device on your system
    dev_path = '/org/bluez/2823/hci0/dev_00_11_67_D2_AB_EE'
    device = bt_manager.BTDevice(dev_path=dev_path)
    discovery = device.discover_services()
    if (discovery):
        for rec in discovery.keys():
            print '========================================================='
            print bt_manager.BTDiscoveryInfo(discovery[rec])
    print '========================================================='

**Example output:**

.. code-block:: python

  =========================================================
  {u'BluetoothProfileDescriptorList': [[{u'uuid': <uuid:00001200-0000-1000-8000-00805F9B34FB name:PnPInformation desc:Device Identification (DID) NOTE: Used as both Service Class Identifier and Profile Identifier.>},
                                        '0x0100']],
   u'LanguageBaseAttributeIDList': ['0x656e', '0x006a', '0x0100'],
   u'PrimaryRecord': 'true',
   u'ProductID': '0x13a4',
   u'ProtocolDescriptorList': [[{u'uuid': <uuid:00000100-0000-1000-8000-00805F9B34FB name:L2CAP desc:Bluetooth Core Specification>},
                                '0x0001'],
                               [{u'uuid': <uuid:00000001-0000-1000-8000-00805F9B34FB name:SDP desc:Bluetooth Core Specification>}]],
   u'ServiceClassIDList': [{u'uuid': <uuid:00001200-0000-1000-8000-00805F9B34FB name:PnPInformation desc:Device Identification (DID) NOTE: Used as both Service Class Identifier and Profile Identifier.>}],
   u'ServiceRecordHandle': '0x00010001',
   u'SpecificationID': '0x0103',
   u'VendorID': '0x0039',
   u'VendorIDSource': '0x0001',
   u'Version': '0x0104'}

   ... etc etc
