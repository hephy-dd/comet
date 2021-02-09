import unittest
import random

from comet.resource import Resource
from comet.driver import Driver

from comet.driver.keithley import K2700

from .test_driver import BaseDriverTest

class K2700Test(BaseDriverTest):

    driver_type = K2700

    def testSystemBeeper(self):
        for value in (True, False, 1, 0):
            self.resource.buffer = ['1']
            self.driver.system.beeper.status = value
            self.assertEqual(self.resource.buffer, [f':SYST:BEEP:STAT {value:d}', '*OPC?'])

            self.resource.buffer = [f'{value:d}']
            self.assertEqual(self.driver.system.beeper.status, value)
            self.assertEqual(self.resource.buffer, [':SYST:BEEP:STAT?'])

if __name__ == '__main__':
    unittest.main()
