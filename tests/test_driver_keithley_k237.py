import unittest

from comet.driver.keithley import K237

from .test_driver import BaseDriverTest

K237.WRITE_DELAY = 0.


class K237Test(BaseDriverTest):

    driver_cls = K237

    def test_basic(self):
        self.resource.buffer = ['23714a']
        self.assertEqual(self.driver.identify(), 'Keithley Inc., Model 237, rev. 14a')
        self.assertEqual(self.driver.reset(), None)
        self.assertEqual(self.driver.clear(), None)
        self.assertEqual(self.resource.buffer, ['U0X'])

    def test_errors(self):
        self.resource.buffer = ['ERS00000000000000000000000000']
        self.assertEqual(self.driver.next_error(), None)
        self.assertEqual(self.resource.buffer, ['U1X'])

        self.resource.buffer = ['ERS00100000000000000000000000']
        error = self.driver.next_error()
        self.assertEqual(error.code, 2)
        self.assertEqual(error.message, 'IDDCO')

    def test_output(self):
        self.resource.buffer = ['MSTG01,0,0K0M000,0N0R1T4,0,0,0V1Y0']
        self.assertEqual(self.driver.output, self.driver.OUTPUT_OFF)
        self.assertEqual(self.resource.buffer, ['U3X'])

        self.resource.buffer = ['MSTG01,0,0K0M000,0N1R1T4,0,0,0V1Y0']
        self.assertEqual(self.driver.output, self.driver.OUTPUT_ON)
        self.assertEqual(self.resource.buffer, ['U3X'])

        self.resource.buffer = []
        self.driver.output = self.driver.OUTPUT_OFF
        self.assertEqual(self.resource.buffer, ['N0X'])

        self.resource.buffer = []
        self.driver.output = self.driver.OUTPUT_ON
        self.assertEqual(self.resource.buffer, ['N1X'])

    def test_function(self):
        self.resource.buffer = ['IMPL,08F0,0O0P0S0W1Z0']
        self.assertEqual(self.driver.function, self.driver.FUNCTION_VOLTAGE)
        self.assertEqual(self.resource.buffer, ['U4X'])

        self.resource.buffer = ['IMPL,08F1,0O0P0S0W1Z0']
        self.assertEqual(self.driver.function, self.driver.FUNCTION_CURRENT)
        self.assertEqual(self.resource.buffer, ['U4X'])

        self.resource.buffer = []
        self.driver.function = self.driver.FUNCTION_VOLTAGE
        self.assertEqual(self.resource.buffer, ['F0,0X'])

        self.resource.buffer = []
        self.driver.function = self.driver.FUNCTION_CURRENT
        self.assertEqual(self.resource.buffer, ['F1,0X'])

    def test_voltage(self):
        for level in (-2.5, 0., +2.5):
            self.resource.buffer = [format(level, '.3E')]
            self.assertEqual(self.driver.voltage_level, level)
            self.assertEqual(self.resource.buffer, ['G1,2,0X', 'X'])

        for level in (-2.5, 0., +2.5):
            self.resource.buffer = []
            self.driver.voltage_level = level
            self.assertEqual(self.resource.buffer, [f'B{level:.3E},,X'])

    def test_current(self):
        for level in (-2.5e-06, 0., +2.5e-06):
            self.resource.buffer = [format(level, '.3E')]
            self.assertEqual(self.driver.current_level, level)
            self.assertEqual(self.resource.buffer, ['G1,2,0X', 'X'])

        for level in (-2.5e-06, 0., +2.5e-06):
            self.resource.buffer = []
            self.driver.current_level = level
            self.assertEqual(self.resource.buffer, [f'B{level:.3E},,X'])

    def test_compliance_tripped(self):
        self.resource.buffer = ['OS000']
        self.assertEqual(self.driver.compliance_tripped, True)
        self.assertEqual(self.resource.buffer, ['G1,0,0X', 'X'])

        self.resource.buffer = ['OP000']
        self.assertEqual(self.driver.compliance_tripped, False)
        self.assertEqual(self.resource.buffer, ['G1,0,0X', 'X'])

    def test_measure_voltage(self):
        self.resource.buffer = ['+4.200E-03']
        self.assertEqual(self.driver.measure_voltage(), 4.2e-03)
        self.assertEqual(self.resource.buffer, ['G4,2,0X', 'X'])

    def test_measure_voltage(self):
        self.resource.buffer = ['+4.200E-06']
        self.assertEqual(self.driver.measure_current(), 4.2e-06)
        self.assertEqual(self.resource.buffer, ['G4,2,0X', 'X'])
