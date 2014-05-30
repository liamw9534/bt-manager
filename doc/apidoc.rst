*****************
API documentation
*****************

Generic
=======


Service & Discovery Helpers
---------------------------

.. py:data:: bt_manager.serviceuuids.SERVICES

:data dict SERVICES: A dictionary of service UUIDs which allows all
    bluetooth standard-based services to be keyed by either
    their short-form name or their UUID16 value.

    Example:

    ``SERVICES['AudioSource']`` shall return a :py:class:`.BTUUID16`
        denoting the A2DP audio source profile UUID.
    ``SERVICES['110A']`` shall return the same :py:class:`.BTUUID16`
        denoting the A2DP audio source profile UUID.

.. py:data:: bt_manager.attributes.ATTRIBUTES

:data dict ATTRIBUTES: A dictionary of attribute dictionaries which
    allows all bluetooth standard-based attribute sets associated
    with a given service UUID to be found.

    Example:

    ``ATTRIBUTES['*']`` shall return a dictionary of the universal
    	service attributes.
    ``ATTRIBUTES['*']['0000']`` shall return the universal service
    	attribute name string for attribute `0000` which is
    	`ServiceRecordHandle` in this instance.
    ``ATTRIBUTES['110A']`` shall return the audio source service
    	attributes dictionary.

.. automodule:: bt_manager.attributes
    :members: ATTRIBUTES

.. automodule:: bt_manager.uuid
    :members: BTUUID, BTUUID16, BTUUID32, BASE_UUID

.. automodule:: bt_manager.discovery
    :members: BTDiscoveryInfo


Device Identification
---------------------

.. automodule:: bt_manager.cod
    :members: BTCoD


Vendor Identification
---------------------

.. py:data:: bt_manager.vendors.VENDORS

:data dict VENDOR: A dictionary of vendor IDs which allows all
    registered bluetooth vendors to be keyed by their unique vendor
    ID to obtain the vendor name string.

    Example:

    ``VENDORS[2]`` shall return `Intel Corp.`

    ``VENDORS[25]`` shall return `Broadcom Corporation`

.. note:: The device vendor ID can be obtained from the :py:class:`.BTDevice`
	class' `Vendor` attribute following the service discovery procedure.

Bluetooth Interfaces & Services
===============================


Interface
---------

.. inheritance-diagram:: bt_manager.interface

.. automodule:: bt_manager.interface
    :members: BTInterface
    :inherited-members:
    :show-inheritance:
	:inheritance-diagram:


Manager
-------

.. inheritance-diagram:: bt_manager.manager

.. automodule:: bt_manager.manager
    :members: BTManager
    :inherited-members:
    :show-inheritance:


Adapter
-------

.. inheritance-diagram:: bt_manager.adapter

.. automodule:: bt_manager.adapter
    :members: BTAdapter
    :inherited-members:
    :show-inheritance:


Device
------

.. inheritance-diagram:: bt_manager.device

.. automodule:: bt_manager.device
    :members: BTDevice
    :inherited-members:
    :show-inheritance:


Agent
-----

.. inheritance-diagram:: bt_manager.agent

.. automodule:: bt_manager.agent
    :members: BTAgent
    :inherited-members:
    :show-inheritance:


Media
-----

.. inheritance-diagram:: bt_manager.media

.. automodule:: bt_manager.media
    :members: GenericEndpoint, BTMedia, BTMediaTransport
    :inherited-members:
    :show-inheritance:


Audio
-----

.. inheritance-diagram:: bt_manager.audio

.. automodule:: bt_manager.audio
    :members: BTAudioSource, BTAudioSink, SBCAudioCodec, SBCAudioSource, SBCAudioSink
    :inherited-members:
    :show-inheritance:

.. automodule:: bt_manager.codecs
    :members: A2DP_CODECS, SBCCodecConfig, SBCSamplingFrequency, SBCBlocks, \
		SBCChannelMode, SBCAllocationMethod, SBCSubbands, SBCCodec
    :inherited-members:
    :show-inheritance:


Headset
-------

.. inheritance-diagram:: bt_manager.headset

.. automodule:: bt_manager.headset
    :members: BTHeadset, BTHeadsetGateway
    :inherited-members:
    :show-inheritance:


Exceptions
----------

.. automodule:: bt_manager.exceptions
    :members: BTSignalNameNotRecognisedException, BTDeviceNotSpecifiedException,
    	BTRejectedException, BTInvalidConfiguration, BTIncompatibleTransportAccessType,
    	BTUUIDNotSpecifiedException
	:inherited-members:
    :show-inheritance:
