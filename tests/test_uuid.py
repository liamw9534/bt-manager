from __future__ import unicode_literals

import unittest

import bt_manager


class UUIDTest(unittest.TestCase):

    def test_uuid(self):
        name = 'UUID Name'
        desc = 'UUID Description'
        uuid = '12345678-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        obj = bt_manager.BTUUID(uuid=uuid, name=name, desc=desc)
        self.assertEqual(obj.uuid, uuid.upper())
        self.assertEqual(obj.uuid16, uuid[4:8])
        self.assertEqual(obj.uuid32, uuid[0:8])
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.desc, desc)

    def test_uuid16(self):
        name = 'UUID Name'
        desc = 'UUID Description'
        uuid = '1234'
        obj = bt_manager.BTUUID16(uuid=uuid, name=name, desc=desc)
        self.assertEqual(obj.uuid16, uuid)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.desc, desc)

    def test_uuid32(self):
        name = 'UUID Name'
        desc = 'UUID Description'
        uuid = '12345678'
        obj = bt_manager.BTUUID32(uuid=uuid, name=name, desc=desc)
        self.assertEqual(obj.uuid32, uuid)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.desc, desc)

    def test_base_uuid(self):
        uuid = '00000000-0000-1000-8000-00805F9B34FB'
        self.assertEqual(bt_manager.BASE_UUID.uuid, uuid)

    def test_UUIDNotSpecifiedException(self):
        try:
            caught = False
            bt_manager.BTUUID()
        except bt_manager.BTUUIDNotSpecifiedException:
            caught = True
        self.assertTrue(caught)
