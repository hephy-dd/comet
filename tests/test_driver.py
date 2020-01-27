import tempfile
import unittest
import os

from comet.driver import Resource, Driver

class DeviceTest(unittest.TestCase):

    def testDriver(self):
        instr = Driver(Resource("GBIP0::8"))
        self.assertEqual(instr.resource.resource_name, "GBIP0::8")
        self.assertEqual(instr.resource.options.get("read_terminiation"), None)
        instr.resource.options["read_terminiation"] = "\r\n"
        self.assertEqual(instr.resource.options.get("read_terminiation"), "\r\n")
        instr.resource.resource_name = "GBIP0::16"
        self.assertEqual(instr.resource.resource_name, "GBIP0::16")

if __name__ == '__main__':
    unittest.main()
