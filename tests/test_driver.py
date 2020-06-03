import tempfile
import unittest
import os

from comet.resource import Resource
from comet.driver import Driver

# Check default imports
from comet.driver.corvus import *
from comet.driver.cts import *
from comet.driver.hephy import *
from comet.driver.keithley import *
from comet.driver.keysight import *

class DeviceTest(unittest.TestCase):

    def testDriverPlain(self):
        with Resource("ASRL1::INSTR", visa_library="@sim") as res:
            instr = Driver(res)
            self.assertEqual(instr.resource.resource_name, "ASRL1::INSTR")

    def testDriverResource(self):
        with Resource("ASRL1::INSTR", visa_library="@sim") as res:
            instr = Driver(res)
            self.assertEqual(instr.resource.resource_name, "ASRL1::INSTR")
            self.assertEqual(instr.resource.options.get("read_terminiation"), None)
            instr.resource.options["read_terminiation"] = "\r\n"
            self.assertEqual(instr.resource.options.get("read_terminiation"), "\r\n")
            instr.resource.resource_name = "ASRL1::INSTR"
            self.assertEqual(instr.resource.resource_name, "ASRL1::INSTR")

if __name__ == '__main__':
    unittest.main()
