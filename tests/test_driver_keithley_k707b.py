import unittest

from comet.driver.keithley import K707B

from .test_driver import BaseDriverTest


class K707BTest(BaseDriverTest):

    driver_cls = K707B

    def test_basic(self):
        self.resource.buffer = ['Keithley Model K707B', '1', '1']
        self.assertEqual(self.driver.identify(), 'Keithley Model K707B')
        self.assertEqual(self.driver.reset(), None)
        self.assertEqual(self.driver.clear(), None)
        self.assertEqual(self.resource.buffer, ['*IDN?', '*RST', '*OPC?', '*CLS', '*OPC?'])

    def test_errors(self):
        self.resource.buffer = ['0\t"Queue is Empty"\t0\t0']
        self.assertEqual(self.driver.next_error(), None)
        self.assertEqual(self.resource.buffer, ['print(errorqueue.next())'])

        self.resource.buffer = ['42\t"test error"\t0\t0']
        error = self.driver.next_error()
        self.assertEqual(error.code, 42)
        self.assertEqual(error.message, 'test error')

    def test_channels(self):
        self.resource.buffer = ['']
        self.assertEqual(self.driver.closed_channels(), [])
        self.assertEqual(self.resource.buffer, ['print(channel.getclose("allslots"))'])

        self.resource.buffer = ['1B01']
        self.assertEqual(self.driver.closed_channels(), ['1B01'])
        self.assertEqual(self.resource.buffer, ['print(channel.getclose("allslots"))'])

        self.resource.buffer = ['1B01;1A02']
        self.assertEqual(self.driver.closed_channels(), ['1A02', '1B01'])
        self.assertEqual(self.resource.buffer, ['print(channel.getclose("allslots"))'])

        self.resource.buffer = ['1']
        self.assertEqual(self.driver.close_channels(['1A02']), None)
        self.assertEqual(self.resource.buffer, ['channel.close("1A02")', '*OPC?'])

        self.resource.buffer = ['1']
        self.assertEqual(self.driver.close_channels(['1A02', '1B01']), None)
        self.assertEqual(self.resource.buffer, ['channel.close("1A02,1B01")', '*OPC?'])

        self.resource.buffer = ['1']
        self.assertEqual(self.driver.open_channels(['1A02', '1B01']), None)
        self.assertEqual(self.resource.buffer, ['channel.open("1A02,1B01")', '*OPC?'])

        self.resource.buffer = ['1']
        self.assertEqual(self.driver.open_all_channels(), None)
        self.assertEqual(self.resource.buffer, ['channel.open("allslots")', '*OPC?'])
