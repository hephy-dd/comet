import unittest
import random

from comet.resource import Resource
from comet.driver import Driver

# Check default imports
from comet.driver.corvus import *
from comet.driver.cts import *
from comet.driver.hephy import *
from comet.driver.keithley import *
from comet.driver.keysight import *

class FakeResource(Resource):

    def __init__(self):
        super().__init__(None)
        self.buffer = []

    def read(self):
        return self.buffer.pop(0)

    def write(self, message):
        self.buffer.append(message)

    def query(self, message):
        self.write(message)
        return self.read()

class BaseDriverTest(unittest.TestCase):

    driver_type = None

    def setUp(self):
        self.resource = FakeResource()
        self.driver = self.driver_type(self.resource)

class DriverTest(unittest.TestCase):

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
