import unittest
import random

from comet.resource import Resource
from comet.driver import Driver

from comet.driver.keithley import K707B

from .test_driver import BaseDriverTest

class K707BTest(BaseDriverTest):

    driver_type = K707B

    def test_channel(self):
        self.resource.buffer = ['nil']
        self.assertEqual(self.driver.channel.getclose(), [])
        self.assertEqual(self.resource.buffer, ['print(channel.getclose("allslots"))'])

        self.resource.buffer = ['42A']
        self.assertEqual(self.driver.channel.getclose(), ['42A'])
        self.assertEqual(self.resource.buffer, ['print(channel.getclose("allslots"))'])

        self.resource.buffer = ['42A;44B;C3']
        self.assertEqual(self.driver.channel.getclose(), ['42A', '44B', 'C3'])
        self.assertEqual(self.resource.buffer, ['print(channel.getclose("allslots"))'])

        self.resource.buffer = ['1']
        self.driver.channel.close(['42A', '44C', '1E6'])
        self.assertEqual(self.resource.buffer, ['channel.close("42A,44C,1E6")', '*OPC?'])

        self.resource.buffer = ['1']
        self.driver.channel.close(['42A6'])
        self.assertEqual(self.resource.buffer, ['channel.close("42A6")', '*OPC?'])

        self.resource.buffer = ['1']
        self.driver.channel.open()
        self.assertEqual(self.resource.buffer, ['channel.open("allslots")', '*OPC?'])

        self.resource.buffer = ['1']
        self.driver.channel.open(['44B', '16A'])
        self.assertEqual(self.resource.buffer, ['channel.open("44B,16A")', '*OPC?'])

    def test_identification(self):
        self.resource.buffer = ['Keithley K707B matrix ']
        self.assertEqual(self.driver.identification, 'Keithley K707B matrix')
        self.assertEqual(self.resource.buffer, ['*IDN?'])


if __name__ == '__main__':
    unittest.main()
