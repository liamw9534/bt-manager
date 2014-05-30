********
Glossary
********

.. glossary::
	:sorted:

    A2DP
        Advanced Audio Distribution Profile.  :term:`A2DP` is used for audio
        streaming between a computer and audio capable device.  An :term:`A2DP`
        device may be a :term:`source` or a :term:`sink`.

        :term:`A2DP` supports different :term:`codec`\s depending on the type
        of audio link being established.  The only mandatory :term:`codec` is
        :term:`SBC`.

    AVCTP
		Audio/Video Control Transport Protocol.  The protocol used
		to carry the commands that form part of the :term:`AVRCP` profile.

    AVRCP
		Audio Video Remote Control Profile.  :term:`AVRCP` allows for both
		an originator (i.e., controller) and recipient (i.e., controllee)
		to send or receive :term:`AVRCP` commands.  All :term:`AVRCP` capable
		devices advertise which commands they support during the link
		establishment.

		Note: an :term:`AVCTP` link is established automatically
		by :term:`bluez` whenever a device connection is made (e.g., audio)
		provided the ``Control`` profile is enabled as part of your ``audio.conf``
		bluetooth settings.

    SBC
		Low complexity subband coding.  The :term:`SBC` :term:`codec` is
		a mandatory requirement for :term:`A2DP` capable devices.  It
		employs a psycho-acoustic model in order to compress frequency
		bands present in an audio source in accordance with human hearing
		sensitivity.  The compression algorithm is `lossy` which means that
		the original source is never constructed perfectly once it has
		been through the encoding/decoding process.

    SDP
		Service Discovery Protocol.  :term:`SDP` is used in order for a host to
		discover the services provided by a device.  :term:`SDP` uses an
		attribute identification based scheme with a generic set of
		attributes being applicable to all classes and types of devices
		and service-specific attributes in accordance with the :term:`UUID`s
		supported by the device.

    UUID
		Universally Unique Identifier.  A :term:`UUID` is a 128-bit number
		used to represent a service, protocol or other attribute
		as part of the bluetooth standard.  UUIDs generally take
		a 16-bit short-form that is derived from their 128-bit
		representation since, generally, no more than 65536 UUIDs
		are ever used simultaneously within the context of
		one application.
		
    dbus
		A message bus system providing a simple way for applications
		to talk to one another.  :term:`Bluez` provides dbus hooks allowing
		applications to establish bluetooth sessions and manage
		bluetooth hardware and devices.

    bluez
		Bluez provides the upper layers (i.e., above :term:`PHY`) and
		management interface of the bluetooth protocol stack under
		Linux.

    PHY
		Physical layer.  In bluetooth this refers to the radio (RF)
		channel which is operating in the 2.4GHz frequency band.
		The `PHY` employs coding/decoding and modulation/demodulation
		techiques to allow information to be sent over-the-air.

    HFP
		Hands-free profile.  The service profile used by devices that
		support a hands-free mode of operation, such as, a mobile
		phone connected to a car.

    HSP
		Headset profile.  The service profile used by bluetooth
		headphones or earpieces.

    source
		An entity capable of generating media content for streaming.
		For example, a music player.

    sink
		An entity capable of receiving media content for rendering.
		For example, a headset or speaker.

    codec
		An en(cod)er/d(ec)oder.  A `codec` may be implemented in software
		or hardware and typically perform compression of the original
		source to a lower bit-rate prior to transmission and
		decompression back to the original bit-rate following
		reception.  The algorithms employed may be lossy (meaning the
		original signal source is not reconstructed perfectly but
		is generally a good enough approximation not to be perceived) or
		lossless (meaning the original signal source is reconstructed
		perfectly).

    adapter
		A (bluetooth) adapter is a piece of physical hardware that
		allows a device to transmit and receive in accordance
		with the bluetooth standards.  The adapter typically implements
		the :term:`PHY` (i.e., physical layer).

    device
		A generic term referring to any piece of hardware that provides
		services over bluetooth.

    transport
		The transport or transport layer normally refers to the link
		layer (or L2) link that is established between two devices over
		bluetooth.  It allows for bi-directional communications
		and employs error checksums and re-transmissions for improved
		reliability so that the application layer need not worry
		about this.

    SCO
		Synchronous Connection-Orientated.

    ACL
		Asynchronous Connection.

    PCM
		Pulse-coded Modulation.

    HCI
		Host controller interface.  This is typically a serial link
		between the bluetooth stack and the bluetooth adapter and provides
		a standard interface such that different stack implementation
		can be easily plugged-in.  It provides low-level commands
		for device setup, flow control, device discover, quality of service,
		physical links, authentication and encryption.
