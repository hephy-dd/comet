import unittest

from comet.driver.keithley import K2400

from .test_driver import BaseDriverTest


class K2400Test(BaseDriverTest):

    driver_cls = K2400

    def test_basic(self):
        self.resource.buffer = ['Keithley Model K2400', '1', '1']
        self.assertEqual(self.driver.identify(), 'Keithley Model K2400')
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

    def test_route_terminal(self):
        self.resource.buffer = ['FRON']
        self.assertEqual(self.driver.get_route_terminal(), self.driver.ROUTE_TERMINAL_FRONT)
        self.assertEqual(self.resource.buffer, [':ROUT:TERM?'])

        self.resource.buffer = ['1']
        self.assertEqual(self.driver.set_route_terminal(self.driver.ROUTE_TERMINAL_REAR), None)
        self.assertEqual(self.resource.buffer, [':ROUT:TERM REAR', '*OPC?'])
