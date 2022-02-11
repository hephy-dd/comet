import unittest

from comet.driver.keithley import K2470

from .test_driver import BaseDriverTest


class K2470Test(BaseDriverTest):

    driver_cls = K2470

    def test_basic(self):
        self.resource.buffer = ['Keithley Model 2470', '1', '1']
        self.assertEqual(self.driver.identify(), 'Keithley Model 2470')
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
        self.assertEqual(self.driver.route_terminal, 'front')
        self.assertEqual(self.resource.buffer, [':ROUT:TERM?'])

        self.resource.buffer = ['REAR']
        self.assertEqual(self.driver.route_terminal, 'rear')
        self.assertEqual(self.resource.buffer, [':ROUT:TERM?'])

        self.resource.buffer = ['1']
        self.driver.route_terminal = 'front'
        self.assertEqual(self.resource.buffer, [':ROUT:TERM FRON', '*OPC?'])

        self.resource.buffer = ['1']
        self.driver.route_terminal = 'rear'
        self.assertEqual(self.resource.buffer, [':ROUT:TERM REAR', '*OPC?'])

    def test_output(self):
        self.resource.buffer = ['0']
        self.assertEqual(self.driver.output, self.driver.OUTPUT_OFF)
        self.assertEqual(self.resource.buffer, [':OUTP:STAT?'])

        self.resource.buffer = ['1']
        self.assertEqual(self.driver.output, self.driver.OUTPUT_ON)
        self.assertEqual(self.resource.buffer, [':OUTP:STAT?'])

        self.resource.buffer = ['1']
        self.driver.output = self.driver.OUTPUT_OFF
        self.assertEqual(self.resource.buffer, [':OUTP:STAT OFF', '*OPC?'])

        self.resource.buffer = ['1']
        self.driver.output = self.driver.OUTPUT_ON
        self.assertEqual(self.resource.buffer, [':OUTP:STAT ON', '*OPC?'])

    def test_function(self):
        self.resource.buffer = ['VOLT']
        self.assertEqual(self.driver.function, self.driver.FUNCTION_VOLTAGE)
        self.assertEqual(self.resource.buffer, [':SOUR:FUNC:MODE?'])

        self.resource.buffer = ['CURR']
        self.assertEqual(self.driver.function, self.driver.FUNCTION_CURRENT)
        self.assertEqual(self.resource.buffer, [':SOUR:FUNC:MODE?'])

        self.resource.buffer = ['1', '1']
        self.driver.function = self.driver.FUNCTION_VOLTAGE
        self.assertEqual(self.resource.buffer, [':SOUR:FUNC:MODE VOLT', '*OPC?', ':SENS:FUNC \'CURR\'', '*OPC?'])

        self.resource.buffer = ['1', '1']
        self.driver.function = self.driver.FUNCTION_CURRENT
        self.assertEqual(self.resource.buffer, [':SOUR:FUNC:MODE CURR', '*OPC?', ':SENS:FUNC \'VOLT\'', '*OPC?'])

    def test_measure_voltage(self):
        self.resource.buffer = ['+4.200000E-03']
        self.assertEqual(self.driver.measure_voltage(), 4.2e-03)
        self.assertEqual(self.resource.buffer, [':MEAS:VOLT?'])

    def test_measure_voltage(self):
        self.resource.buffer = ['+4.200000E-06']
        self.assertEqual(self.driver.measure_current(), 4.2e-06)
        self.assertEqual(self.resource.buffer, [':MEAS:CURR?'])
