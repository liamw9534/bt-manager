Requirements
============

Basic
=====

Support bluez 4.x and bluez 5.x
Enumerate available bluetooth adapters
Scan for devices in locality
Provide device connection quality metrics
Register devices with local registry
Unregister devices from local registry
Identify devices by capabilities
Handle device pairing

Design
======

AGENT

	authorize
	request PIN
	request PASSKEY

DEVICE

	list
	services
	create
	disconnect
	discover -> XML records attrib/value pairs
	class e.g., 0x240414
	name e.g., BTS-06
	alias e.g., BTS-06
	trusted boolean
	blocked boolean

ADAPTER

	list
	address
	name
	powered
	pairable
	discoverable
	discoverableTimeout
	discovering

DBUS

	connect
	disconnect

DAEMON (bluetoothd)

	version
	start
	stop
	restart
	debug on/off

CONFIGURATION

	audio.conf
	main.conf
	input.conf
	network.conf
	proximity.conf
	serial.conf
	rfcomm.conf
