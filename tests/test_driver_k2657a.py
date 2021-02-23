import unittest
import random

from comet.resource import Resource
from comet.driver import Driver

from comet.driver.keithley import K2657A

from .test_driver import BaseDriverTest

class K2657ATest(BaseDriverTest):

    driver_type = K2657A

    def test_beeper_enable(self):
        values = (
            ('1', True),
            ('0', False),
            ('1', 1),
            ('0', 0),
            ('1', 44)
        )
        for key, value in values:
            # write
            self.resource.buffer = ['1']
            self.driver.beeper.enable = value
            self.assertEqual(self.resource.buffer, [f'beeper.enable = {key}', '*OPC?'])
            # query
            self.resource.buffer = [key]
            self.assertEqual(self.driver.beeper.enable, bool(value))
            self.assertEqual(self.resource.buffer, ['print(beeper.enable)'])

    def test_sense(self):
        values = (
            ('0', self.driver.SENSE_LOCAL),
            ('1', self.driver.SENSE_REMOTE),
            ('2', self.driver.SENSE_CALA)
        )
        for key, value in values:
            # write
            self.resource.buffer = [key]
            self.driver.sense = value
            self.assertEqual(self.resource.buffer, [f'smua.sense = {key}', '*OPC?'])
            # query
            self.resource.buffer = [key]
            self.assertEqual(self.driver.sense, value)
            self.assertEqual(self.resource.buffer, ['print(smua.sense)'])



if __name__ == '__main__':
    unittest.main()
