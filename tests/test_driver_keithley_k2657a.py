import unittest

from comet.driver.keithley import K2657A

from .test_driver import BaseDriverTest


class K2657ATest(BaseDriverTest):

    driver_cls = K2657A

    def test_basic(self):
        self.resource.buffer = ['Keithley Model 2657A', '1', '1']
        self.assertEqual(self.driver.identify(), 'Keithley Model 2657A')
        self.assertEqual(self.driver.reset(), None)
        self.assertEqual(self.driver.clear(), None)
        self.assertEqual(self.resource.buffer, ['*IDN?', '*RST', '*OPC?', '*CLS', '*OPC?'])

    def test_errors(self):
        self.resource.buffer = ['0\t"no error"\t0\t0']
        self.assertEqual(self.driver.next_error(), None)
        self.assertEqual(self.resource.buffer, ['print(errorqueue.next())'])

        self.resource.buffer = ['42\t"test error"\t0\t0']
        error = self.driver.next_error()
        self.assertEqual(error.code, 42)
        self.assertEqual(error.message, 'test error')

    def test_output(self):
        self.resource.buffer = ['0']
        self.assertEqual(self.driver.output, self.driver.OUTPUT_OFF)
        self.assertEqual(self.resource.buffer, ['print(smua.source.output)'])

        self.resource.buffer = ['1']
        self.assertEqual(self.driver.output, self.driver.OUTPUT_ON)
        self.assertEqual(self.resource.buffer, ['print(smua.source.output)'])

        self.resource.buffer = ['1']
        self.driver.output = self.driver.OUTPUT_OFF
        self.assertEqual(self.resource.buffer, ['smua.source.output = 0', '*OPC?'])

        self.resource.buffer = ['1']
        self.driver.output = self.driver.OUTPUT_ON
        self.assertEqual(self.resource.buffer, ['smua.source.output = 1', '*OPC?'])

    def test_function(self):
        self.resource.buffer = ['1']
        self.assertEqual(self.driver.function, self.driver.FUNCTION_VOLTAGE)
        self.assertEqual(self.resource.buffer, ['print(smua.source.func)'])

        self.resource.buffer = ['0']
        self.assertEqual(self.driver.function, self.driver.FUNCTION_CURRENT)
        self.assertEqual(self.resource.buffer, ['print(smua.source.func)'])

        self.resource.buffer = ['1']
        self.driver.function = self.driver.FUNCTION_VOLTAGE
        self.assertEqual(self.resource.buffer, ['smua.source.func = 1', '*OPC?'])

        self.resource.buffer = ['1']
        self.driver.function = self.driver.FUNCTION_CURRENT
        self.assertEqual(self.resource.buffer, ['smua.source.func = 0', '*OPC?'])

    def test_measure_voltage(self):
        self.resource.buffer = ['+4.200000E-03']
        self.assertEqual(self.driver.measure_voltage(), 4.2e-03)
        self.assertEqual(self.resource.buffer, ['print(smua.measure.v())'])

    def test_measure_voltage(self):
        self.resource.buffer = ['+4.200000E-06']
        self.assertEqual(self.driver.measure_current(), 4.2e-06)
        self.assertEqual(self.resource.buffer, ['print(smua.measure.i())'])
