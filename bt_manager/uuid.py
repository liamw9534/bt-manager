from __future__ import unicode_literals
from exceptions import BTUUIDNotSpecifiedException


_BASE_UUID = '00000000-0000-1000-8000-00805F9B34FB'


class BTUUID:
    def __init__(self, uuid=None, uuid16=None,
                 uuid32=None, name=None, desc=None):
        self.name = name
        self.desc = desc
        if (uuid):
            self.uuid = uuid.upper()
        elif (uuid16):
            self.uuid = _BASE_UUID[0:4] + uuid16[0:4].upper() + _BASE_UUID[8:]
        elif (uuid32):
            self.uuid = uuid32[0:8].upper() + _BASE_UUID[8:]
        else:
            raise BTUUIDNotSpecifiedException

    @property
    def uuid16(self):
        return self.uuid[4:8]

    @property
    def uuid32(self):
        return self.uuid[0:8]

    def __repr__(self):
        return '<uuid:' + self.uuid + ' name:' + \
            str(self.name) + ' desc:' + str(self.desc) + '>'


class BTUUID16(BTUUID):

    def __init__(self, uuid, name, desc=None):
        BTUUID.__init__(self, uuid16=uuid, name=name, desc=desc)


class BTUUID32(BTUUID):

    def __init__(self, uuid, name, desc=None):
        BTUUID.__init__(self, uuid32=uuid, name=name, desc=desc)


BASE_UUID = BTUUID(uuid=_BASE_UUID, name='BASE_UUID',
                   desc='Base Universally Unique Identifier')
