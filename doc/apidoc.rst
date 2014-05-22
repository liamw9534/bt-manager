*****************
API documentation
*****************

Generic
=======


Service Discovery Helpers
-------------------------

.. automodule:: bt_manager.serviceuuids
    :members: SERVICES

.. automodule:: bt_manager.attributes
    :members: ATTRIBUTES

.. automodule:: bt_manager.uuid
    :members: BTUUID, BTUUID16, BTUUID32


Device Identification
---------------------

.. automodule:: bt_manager.cod
    :members: BTCoD


Vendor Identification
---------------------

.. automodule:: bt_manager.vendors
    :members: VENDORS


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
    :members: __all__
	:inherited-members:
    :show-inheritance:
