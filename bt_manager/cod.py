from __future__ import unicode_literals


class BTCoD:
    """
    Bluetooth class of device decoder for providing
    a human readable form of the device class value.

    The class of device is a 24-bit number allowing different
    types of bluetooth devices to be described consistently
    and succinctly using a hierarchical scheme.

    * **Major Service**: The major services that the
        device supports.  Several values can be OR'd together
        to form a device supporting multiple major services
        e.g., telephony, networking and audio could be
        the combined service set for a device.
    * **Major Device**: The form-factor or major type of device
        which may only take a single value e.g., Laptop,
        Toy, Health Device, Phone, etc.
    * **Minor Device**: The minor function of the device whose
        range of values depends on the major function e.g.,
        Car audio, SmartPhone, etc.

    :param integer cod: 24-bit integer value representing the
        class of device.

    .. note:: The class of device may be obtained from both
        the :py:class:`.BTAdapter` and :py:class:`.BTDevice`
        classes using the `Class` attribute.
    """

    _MAJOR_SERVICE_POS = 13
    _MAJOR_SERVICE_MASK = 0xFFE000
    _MAJOR_SERVICE_CLASS = {
        0x002000: 'Limited Discoverable Mode [Ref #1]',
        0x004000: '(reserved)',
        0x008000: '(reserved)',
        0x010000: 'Positioning (Location identification)',
        0x020000: 'Networking (LAN, Ad hoc, ...)',
        0x040000: 'Rendering (Printing, Speakers, ...)',
        0x080000: 'Capturing (Scanner, Microphone, ...)',
        0x100000: 'Object Transfer (v-Inbox, v-Folder, ...)',
        0x200000: 'Audio (Speaker, Microphone, Headset service, ...)',
        0x400000: 'Telephony (Cordless telephony, Modem, Headset service, ...)',  # noqa
        0x800000: 'Information (WEB-server, WAP-server, ...)',
    }

    _MAJOR_DEVICE_POS = 8
    _MAJOR_DEVICE_MASK = 0x001F00
    _MAJOR_DEVICE_CLASS = {
        0x0000: 'Miscellaneous [Ref #2]',
        0x0100: 'Computer (desktop, notebook, PDA, organizer, ... )',
        0x0200: 'Phone (cellular, cordless, pay phone, modem, ...)',
        0x0300: 'LAN /Network Access point',
        0x0400: 'Audio/Video (headset, speaker, stereo, video display, VCR, ...',  # noqa
        0x0500: 'Peripheral (mouse, joystick, keyboard, ... ',
        0x0600: 'Imaging (printer, scanner, camera, display, ...)',
        0x0700: 'Wearable',
        0x0800: 'Toy',
        0x0900: 'Health',
        0x1F00: 'Uncategorized: device code not specified'
    }

    _MINOR_DEVICE_CLASS = {
        0x0100: [{'mask': 0x1C, 'pos': 2,
                  0x00: 'Uncategorized, code for device not assigned',
                  0x04: 'Desktop workstation',
                  0x08: 'Server-class computer',
                  0x0C: 'Laptop',
                  0x10: 'Handheld PC/PDA (clamshell)',
                  0x14: 'Palm-size PC/PDA',
                  0x18: 'Wearable computer (watch size)',
                  0x1C: 'Tablet'}],
        0x0200: [{'mask': 0x1C, 'pos': 2,
                  0x00: 'Uncategorized, code for device not assigned',
                  0x04: 'Cellular',
                  0x08: 'Cordless',
                  0x0C: 'Smartphone',
                  0x10: 'Wired modem or voice gateway',
                  0x14: 'Common ISDN access'}],
        0x0300: [{'mask': 0xE0, 'pos': 5,
                  0x00: 'Fully available',
                  0x20: '1% to 17% utilized',
                  0x40: '17% to 33% utilized',
                  0x60: '33% to 50% utilized',
                  0x80: '50% to 67% utilized',
                  0xA0: '67% to 83% utilized',
                  0xC0: '83% to 99% utilized',
                  0xE0: 'No service available'}],
        0x0400: [{'mask': 0x7C, 'pos': 2,
                  0x00: 'Uncategorized, code not assigned',
                  0x04: 'Wearable Headset Device',
                  0x08: 'Hands-free Device',
                  0x0C: '(Reserved)',
                  0x10: 'Microphone',
                  0x14: 'Loudspeaker',
                  0x18: 'Headphones',
                  0x1C: 'Portable Audio',
                  0x20: 'Car audio',
                  0x24: 'Set-top box',
                  0x28: 'HiFi Audio Device',
                  0x2C: 'VCR',
                  0x30: 'Video Camera',
                  0x34: 'Camcorder',
                  0x38: 'Video Monitor',
                  0x3C: 'Video Display and Loudspeaker',
                  0x40: 'Video Conferencing',
                  0x44: '(Reserved)',
                  0x48: 'Gaming/Toy'}],
        0x0500: [{'mask': 0xC0, 'pos': 6,
                  0x00: 'Not Keyboard / Not Pointing Device',
                  0x40: 'Keyboard',
                  0x80: 'Pointing device',
                  0xC0: 'Combo keyboard/pointing device'},
                 {'mask': 0x3C, 'pos': 2,
                  0x00: 'Uncategorized device',
                  0x04: 'Joystick',
                  0x08: 'Gamepad',
                  0x0C: 'Remote control',
                  0x10: 'Sensing device',
                  0x14: 'Digitizer tablet',
                  0x18: 'Card Reader (e.g. SIM Card Reader)',
                  0x1C: 'Digital Pen',
                  0x20: 'Handheld scanner for bar-codes, RFID, etc.',
                  0x24: 'Handheld gestural input device (e.g., "wand" form factor)'}],  # noqa
        0x0600: [{'mask': 0xF0, 'pos': 4,
                  0x10: 'Display',
                  0x20: 'Camera',
                  0x40: 'Scanner',
                  0x80: 'Printer'}],
        0x0700: [{'mask': 0x1C, 'pos': 2,
                  0x04: 'Wristwatch',
                  0x08: 'Pager',
                  0x0C: 'Jacket',
                  0x10: 'Helmet',
                  0x14: 'Glasses'}],
        0x0800: [{'mask': 0x1C, 'pos': 2,
                  0x04: 'Robot',
                  0x08: 'Vehicle',
                  0x0C: 'Doll / Action figure',
                  0x10: 'Controller',
                  0x14: 'Game'}],
        0x0900: [{'mask': 0x3C, 'pos': 2,
                  0x00: 'Undefined',
                  0x04: 'Blood Pressure Monitor',
                  0x08: 'Thermometer',
                  0x0C: 'Weighing Scale',
                  0x10: 'Glucose Meter',
                  0x14: 'Pulse Oximeter',
                  0x18: 'Heart/Pulse Rate Monitor',
                  0x1C: 'Health Data Display',
                  0x20: 'Step Counter',
                  0x24: 'Body Composition Analyzer',
                  0x28: 'Peak Flow Monitor',
                  0x2C: 'Medication Monitor',
                  0x30: 'Knee Prosthesis',
                  0x34: 'Ankle Prosthesis',
                  0x38: 'Generic Health Manager',
                  0x3C: 'Personal Mobility Device'}]
    }

    def __init__(self, cod):
        self.cod = cod

    @property
    def major_service_class(self):
        """
        Return the major service class property decoded e.g.,
        Audio, Telephony, etc
        """
        major_service = []
        for i in BTCoD._MAJOR_SERVICE_CLASS.keys():
            if (self.cod & i):
                major_service.append(BTCoD._MAJOR_SERVICE_CLASS[i])
        return major_service

    @property
    def major_device_class(self):
        """
        Return the major device class property decoded e.g.,
        Computer, Audio/Video, Toy, etc.
        """
        return BTCoD._MAJOR_DEVICE_CLASS.get(self.cod &
                                             BTCoD._MAJOR_DEVICE_MASK,
                                             'Unknown')

    @property
    def minor_device_class(self):
        """
        Return the minor device class property decoded e.g.,
        Scanner, Printer, Loudspeaker, Camera, etc.
        """
        minor_device = []
        minor_lookup = BTCoD._MINOR_DEVICE_CLASS.get(self.cod &
                                                     BTCoD._MAJOR_DEVICE_MASK,
                                                     [])
        for i in minor_lookup:
            minor_value = self.cod & i.get('mask')
            minor_device.append(i.get(minor_value, 'Unknown'))
        return minor_device

    def __str__(self):
        """Stringify all elements of the class of device"""
        return '<cod:' + str(hex(self.cod)) + ' Major Service:' + str(self.major_service_class) + \
            ' Major Device:' + \
            self.major_device_class + ' Minor Device:' + \
            str(self.minor_device_class) + '>'

    def __repr__(self):
        return self.__str__()
