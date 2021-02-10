import unittest
import random

from comet.resource import Resource
from comet.driver import Driver

from comet.driver.keithley import K2657A

from .test_driver import BaseDriverTest

class K2657ATest(BaseDriverTest):

    driver_type = K2657A

    def testBeeperEnable(self):
        for value in (True, False, 1, 0):
            self.resource.buffer = ['1']
            self.driver.beeper.enable = value
            self.assertEqual(self.resource.buffer, [f'beeper.enable = {value:d}', '*OPC?'])

            self.resource.buffer = [f'{value:d}']
            self.assertEqual(self.driver.beeper.enable, value)
            self.assertEqual(self.resource.buffer, ['print(beeper.enable)'])

if __name__ == '__main__':
    unittest.main()
