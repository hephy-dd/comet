import tempfile
import unittest
import os

from comet.device import Device, DeviceManager, DeviceMixin

class DeviceTest(unittest.TestCase):

    def testDevice(self):
        d = Device("GBIP::8")
        self.assertEqual(d.options, {"resource_name": "GBIP::8"})
        self.assertEqual(d.options.get("read_terminiation"), None)
        self.assertEqual(d.resource, None)
        d.options["read_terminiation"] = "\r\n"
        self.assertEqual(d.options.get("read_terminiation"), "\r\n")
        d.options["resource_name"] = "GBIP::16"
        self.assertEqual(d.options.get("resource_name"), "GBIP::16")

    def testDeviceManager(self):
        d = Device("GBIP::8")
        m = DeviceManager()
        self.assertEqual(m.ValueType , type(d))
        m.add("device", d)
        self.assertEqual(m.get("device"), d)

    def testDeviceMixin(self):
        class C(DeviceMixin): pass
        d = Device("GBIP::8")
        c = C()
        c.devices.add("device", d)
        self.assertEqual(c.devices.get("device"), d)

if __name__ == '__main__':
    unittest.main()
