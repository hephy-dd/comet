import tempfile
import unittest
import os

from comet.driver import Resource, Driver

# Check default imports
from comet.driver.corvus import *
from comet.driver.cts import *
from comet.driver.hephy import *
from comet.driver.keithley import *
from comet.driver.keysight import *

class DeviceTest(unittest.TestCase):

    def testDriverPlain(self):
        instr = Driver("GBIP0::8")
        self.assertEqual(instr.resource.resource_name, "GBIP0::8")

    def testDriverResource(self):
        instr = Driver(Resource("GBIP0::8"))
        self.assertEqual(instr.resource.resource_name, "GBIP0::8")
        self.assertEqual(instr.resource.options.get("read_terminiation"), None)
        instr.resource.options["read_terminiation"] = "\r\n"
        self.assertEqual(instr.resource.options.get("read_terminiation"), "\r\n")
        instr.resource.resource_name = "GBIP0::16"
        self.assertEqual(instr.resource.resource_name, "GBIP0::16")

if __name__ == '__main__':
    unittest.main()
