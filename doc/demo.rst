****
Demo
****

A demo application is provided under ``demo/demo.py`` with the source code
distribution.  The demo is a simple command-line parser and may be launched by running:

    ``python demo/demo.py``

The application shows display a command prompt:

.. code-block:: python

  BT>

At the command-prompt, you can type ``help`` to get a list of commands and their
options.

.. code-block:: python

  BT> help
  media-sbc-source-start <endpoint_path> : Start media endpoint for SBC audio source (i.e., connects to a sink device)
  help [command] : Display a list of commands or get help for a specific command
  device-get <dev_path> <property> : Get device property by name
  agent-stop <agent_path> : Stop pairing agent
  discovery-stop None : Stop device discovery
  agent-start <agent_path> [dev_id e.g., 11:22:33:44:55:66] : Start pairing agent
  source-disconnect <dev_path> : Audio source connect
  adapter-info None : Display information about default BT adapter
  source-info <dev_path> : Audio source properties
  media-encode <endpoint_path> <audio_filename> : Start media encode for SBC audio source
  device-discovery <dev_path> : Run BT device discovery session
  sink-info <dev_path> : Audio sink properties
  exit None : Cleanup and exit
  adapter-get <property> : Get adapter property by name
  device-disconnect <dev_path> : Disconnect a BT device
  list-devices None : Display a list of paired BT devices
  control-info <dev_path> : Control device info
  media-decode <endpoint_path> <audio_filename> : Start media decode for SBC audio sink
  sink-connect <dev_path> : Audio sink connect
  control-vol-up <dev_path> : Control volume up
  list-adapters None : Provide a list of available BT adapters
  device-set <dev_path> <property> <value> : Set device property by name, value
  device-info <dev_path> : Display information about a paired BT device
  source-connect <dev_path> : Audio source connect
  control-vol-down <dev_path> : Control volume down
  device-rm <dev_path> : Remove device from adapter
  discovery-start None : Start device discovery
  media-sbc-sink-start <endpoint_path> : Start media endpoint for SBC audio sink (i.e., connects to a source device)
  sink-disconnect <dev_path> : Audio sink connect
  adapter-set <property> <value> : Set adapter property by name, value
  media-stop <endpoint_path> : Stop media endpoint


Each command implements a legitimate use-case of the BT-Manager API.  Following are
some example scenarios to get started.


Get a list of devices
=====================

You can find out which devices have been previously registered on your system
by using the ``list-devices`` command.

.. code-block:: python

  BT> list-devices
  =========================================================
  dbus.Array([dbus.ObjectPath('/org/bluez/2202/hci0/dev_00_88_65_A8_EA_79'),
    dbus.ObjectPath('/org/bluez/2202/hci0/dev_00_11_67_D2_AB_EE')],
    signature=dbus.Signature('o'))

Run a service discovery on a device
===================================

You can then choose a device and initiate a service discovery on it using
the ``device-discovery`` command.  This will output a comprehensive list of
the device's services and properties.

.. code-block:: python

  # The object path will differ on your own system
  BT> device-discovery /org/bluez/2202/hci0/dev_00_11_67_D2_AB_EE
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
  =========================================================
  {'0100': 'Headset unit',
   u'BluetoothProfileDescriptorList': [[{u'uuid': <uuid:00001108-0000-1000-8000-00805F9B34FB name:Headset desc:Headset Profile (HSP) NOTE: Used as both Service Class Identifier and Profile Identifier.>},
                                        '0x0100']],
   u'LanguageBaseAttributeIDList': ['0x656e', '0x006a', '0x0100'],
   u'ProtocolDescriptorList': [[{u'uuid': <uuid:00000100-0000-1000-8000-00805F9B34FB name:L2CAP desc:Bluetooth Core Specification>}],
                               [{u'uuid': <uuid:00000003-0000-1000-8000-00805F9B34FB name:RFCOMM desc:RFCOMM with TS 07.10>},
                                '0x02']],
   u'Remote Audio Volume Control': 'true',
   u'ServiceClassIDList': [{u'uuid': <uuid:00001108-0000-1000-8000-00805F9B34FB name:Headset desc:Headset Profile (HSP) NOTE: Used as both Service Class Identifier and Profile Identifier.>},
                           {u'uuid': <uuid:00001203-0000-1000-8000-00805F9B34FB name:GenericAudio desc:N/A>}],
   u'ServiceRecordHandle': '0x00010002'}
  =========================================================
  {'0100': 'Hands-free unit',
   u'BluetoothProfileDescriptorList': [[{u'uuid': <uuid:0000111E-0000-1000-8000-00805F9B34FB name:Handsfree desc:Hands-Free Profile (HFP) NOTE: Used as both Service Class Identifier and Profile Identifier.>},
                                        '0x0105']],
   u'LanguageBaseAttributeIDList': ['0x656e', '0x006a', '0x0100'],
   u'ProtocolDescriptorList': [[{u'uuid': <uuid:00000100-0000-1000-8000-00805F9B34FB name:L2CAP desc:Bluetooth Core Specification>}],
                               [{u'uuid': <uuid:00000003-0000-1000-8000-00805F9B34FB name:RFCOMM desc:RFCOMM with TS 07.10>},
                                '0x01']],
   u'ServiceClassIDList': [{u'uuid': <uuid:0000111E-0000-1000-8000-00805F9B34FB name:Handsfree desc:Hands-Free Profile (HFP) NOTE: Used as both Service Class Identifier and Profile Identifier.>},
                           {u'uuid': <uuid:00001203-0000-1000-8000-00805F9B34FB name:GenericAudio desc:N/A>}],
   u'ServiceRecordHandle': '0x00010003',
   u'SupportedFeatures': '0x001f'}
  =========================================================
  {'0100': 'AVRCP CT',
   '0102': 'ISSC',
   u'BluetoothProfileDescriptorList': [[{u'uuid': <uuid:0000110E-0000-1000-8000-00805F9B34FB name:AVRemoteControl desc:Audio/Video Remote Control Profile (AVRCP) NOTE: Used as both Service Class Identifier and Profile Identifier.>},
                                        '0x0103']],
   u'LanguageBaseAttributeIDList': ['0x656e', '0x006a', '0x0100'],
   u'ProtocolDescriptorList': [[{u'uuid': <uuid:00000100-0000-1000-8000-00805F9B34FB name:L2CAP desc:Bluetooth Core Specification>},
                                '0x0017'],
                               [{u'uuid': <uuid:00000017-0000-1000-8000-00805F9B34FB name:AVCTP desc:Audio/Video Control Transport Protocol (AVCTP)>},
                                '0x0102']],
   u'ServiceClassIDList': [{u'uuid': <uuid:0000110E-0000-1000-8000-00805F9B34FB name:AVRemoteControl desc:Audio/Video Remote Control Profile (AVRCP) NOTE: Used as both Service Class Identifier and Profile Identifier.>}],
   u'ServiceRecordHandle': '0x00010006',
   u'SupportedFeatures': '0x0001'}
  =========================================================
  {'0100': 'Audio SNK',
   '0102': 'ISSC',
   '0311': '0x0003',
   u'BluetoothProfileDescriptorList': [[{u'uuid': <uuid:0000110D-0000-1000-8000-00805F9B34FB name:AdvancedAudioDistribution desc:Advanced Audio Distribution Profile (A2DP)>},
                                        '0x0100']],
   u'LanguageBaseAttributeIDList': ['0x656e', '0x006a', '0x0100'],
   u'ProtocolDescriptorList': [[{u'uuid': <uuid:00000100-0000-1000-8000-00805F9B34FB name:L2CAP desc:Bluetooth Core Specification>},
                                '0x0019'],
                               [{u'uuid': <uuid:00000019-0000-1000-8000-00805F9B34FB name:AVDTP desc:Audio/Video Distribution Transport Protocol (AVDTP)>},
                                '0x0100']],
   u'ServiceClassIDList': [{u'uuid': <uuid:0000110B-0000-1000-8000-00805F9B34FB name:AudioSink desc:Advanced Audio Distribution Profile (A2DP)>}],
   u'ServiceRecordHandle': '0x00010008'}
  =========================================================
  { '0100': 'AVRCP TG',
   '0102': 'ISSC',
   u'BluetoothProfileDescriptorList': [[{u'uuid': <uuid:0000110E-0000-1000-8000-00805F9B34FB name:AVRemoteControl desc:Audio/Video Remote Control Profile (AVRCP) NOTE: Used as both Service Class Identifier and Profile Identifier.>},
                                        '0x0100']],
   u'LanguageBaseAttributeIDList': ['0x656e', '0x006a', '0x0100'],
   u'ProtocolDescriptorList': [[{u'uuid': <uuid:00000100-0000-1000-8000-00805F9B34FB name:L2CAP desc:Bluetooth Core Specification>},
                                '0x0017'],
                               [{u'uuid': <uuid:00000017-0000-1000-8000-00805F9B34FB name:AVCTP desc:Audio/Video Control Transport Protocol (AVCTP)>},
                                '0x0100']],
   u'ServiceClassIDList': [{u'uuid': <uuid:0000110C-0000-1000-8000-00805F9B34FB name:AVRemoteControlTarget desc:Audio/Video Remote Control Profile (AVRCP)>}],
   u'ServiceRecordHandle': '0x0001000c',
   u'SupportedFeatures': '0x0002'}
  =========================================================
  {u'BluetoothProfileDescriptorList': [[{u'uuid': <uuid:00001130-0000-1000-8000-00805F9B34FB name:PhonebookAccess desc:Phonebook Access Profile (PBAP)>},
                                        '0x0100']],
   u'LanguageBaseAttributeIDList': ['0x656e', '0x006a', '0x0100'],
   u'ServiceClassIDList': [{u'uuid': <uuid:0000112E-0000-1000-8000-00805F9B34FB name:PhonebookAccessPCE desc:Phonebook Access Profile (PBAP)>}],
   u'ServiceRecordHandle': '0x0001000f'}
  =========================================================


Recording an A2DP SBC input stream as raw PCM to a file
=======================================================

This example requires only two commands to be run and assumes you are using
a bluetooth capable media player, such as an iPhone.

.. code-block:: python

  # This registers your media endpoint service handler
  BT> media-sbc-sink-start /endpoint/a2dpsink

  # IMPORTANT: Connect and start the media playing on your device *before* entering
  # this command
  BT> media-decode /endpoint/a2dpsink a2dpstream.raw

  # When you're done, stop the media handler and unregister the endpoint
  BT> media-stop /endpoint/a2dpsink


Playing raw PCM to an A2DP SBC sink device
==========================================

If you have a bluetooth speaker (sink) supporting A2DP, you can now playback the
recorded file to it by creating a source media endpoint.

.. code-block:: python

  # This registers your media endpoint service handler
  BT> media-sbc-source-start /endpoint/a2dpsource

  # Speakers are nornally passive and we have to initiate the connection
  # for ourselves
  BT> sink-connect /org/bluez/2202/hci0/dev_00_11_67_D2_AB_EE
  
  # Now we can start playing the PCM file to the speaker
  BT> media-encode /endpoint/a2dpsource a2dpstream.raw

  # When you're done, stop the media handler and unregister the endpoint
  BT> media-stop /endpoint/a2dpsink
