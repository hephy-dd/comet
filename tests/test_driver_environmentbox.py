import unittest
import random

from comet.resource import Resource
from comet.driver import Driver

from comet.driver.hephy import EnvironmentBox

from .test_driver import BaseDriverTest

class EnvironmentBoxTest(BaseDriverTest):

    driver_type = EnvironmentBox

    def test_identification(self):
        self.resource.buffer = ['HEPHY v1.0']
        self.assertEqual(self.driver.identification, 'HEPHY v1.0')
        self.assertEqual(self.resource.buffer, ['*IDN?'])

    def test_test_led(self):
        for value in (True, False, 1, 0):
            self.resource.buffer = ['OK']
            self.driver.test_led = value
            tr = {False: 'OFF', True: 'ON'}
            self.assertEqual(self.resource.buffer, [f'SET:TEST_LED {tr[value]}'])

            self.resource.buffer = [f'{value:d}']
            self.assertEqual(self.driver.test_led, value)
            self.assertEqual(self.resource.buffer, ['GET:TEST_LED ?'])

    def test_pid_control(self):
        for value in (True, False, 1, 0):
            self.resource.buffer = ['OK']
            self.driver.pid_control = value
            tr = {False: 'OFF', True: 'ON'}
            self.assertEqual(self.resource.buffer, [f'SET:CTRL {tr[value]}'])

            self.resource.buffer = [f'{value:d}']
            self.assertEqual(self.driver.pid_control, value)
            self.assertEqual(self.resource.buffer, ['GET:CTRL ?'])

if __name__ == '__main__':
    unittest.main()
