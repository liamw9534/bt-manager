from __future__ import unicode_literals

import unittest

import bt_manager


class UUIDServiceLookup(unittest.TestCase):

    def test_service_lookup(self):
        for i in sorted(bt_manager.SERVICES):
            service = bt_manager.SERVICES[i]
            print service

    def test_attribute_lookup(self):
        for i in sorted(bt_manager.SERVICES):
            service = bt_manager.SERVICES[i]
            uuid16 = service.uuid16
            attribs = bt_manager.ATTRIBUTES.get(uuid16, None)
            print service.name, '['+service.uuid16+']', attribs
