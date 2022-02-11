import unittest

from comet.driver.keithley import K6514

from .test_driver import BaseDriverTest


class K6514Test(BaseDriverTest):

    driver_cls = K6514

    def test_basic(self):
        self.resource.buffer = ['Keithley Model 6514', '1', '1']
        self.assertEqual(self.driver.identify(), 'Keithley Model 6514')
        self.assertEqual(self.driver.reset(), None)
        self.assertEqual(self.driver.clear(), None)
        self.assertEqual(self.resource.buffer, ['*IDN?', '*RST', '*OPC?', '*CLS', '*OPC?'])

    def test_errors(self):
        self.resource.buffer = ['0,"no error"']
        self.assertEqual(self.driver.next_error(), None)
        self.assertEqual(self.resource.buffer, [':SYST:ERR:NEXT?'])

        self.resource.buffer = ['42,"test error"']
        error = self.driver.next_error()
        self.assertEqual(error.code, 42)
        self.assertEqual(error.message, 'test error')
