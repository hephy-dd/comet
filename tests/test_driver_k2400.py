import unittest
import random

from comet.resource import Resource
from comet.driver import Driver

from comet.driver.keithley import K2400

from .test_driver import BaseDriverTest

class K2400Test(BaseDriverTest):

    driver_type = K2400

    def test_route_terminals(self):
        for key, value in (
            ('VOLT,TIME', ('VOLTAGE', 'TIME')),
            ('CURR', ('CURRENT', )),
            ('VOLT,CURR,RES,TIME', ('VOLTAGE', 'CURRENT', 'RES', 'TIME'))
            ):
            self.resource.buffer = ['1']
            self.driver.route.terminals = value
            self.assertEqual(self.resource.buffer, [f':FORM:ELEM {key}', '*OPC?'])

            self.resource.buffer = [key]
            self.assertEqual(self.driver.route.terminals, value)
            self.assertEqual(self.resource.buffer, [':FORM:ELEM?'])

    def test_route_terminals(self):
        for key_in, key_out, value in (
            ('FRON', '0', 'FRONT'),
            ('REAR', '1', 'REAR')
            ):
            self.resource.buffer = ['1']
            self.driver.route.terminals = value
            self.assertEqual(self.resource.buffer, [f':ROUT:TERM {key_in}', '*OPC?'])

            self.resource.buffer = [key_out]
            self.assertEqual(self.driver.route.terminals, value)
            self.assertEqual(self.resource.buffer, [':ROUT:TERM?'])

    def test_system_error(self):
        for key, value in (
            (0, 'no error'),
            (42, 'spam alert')
            ):
            self.resource.buffer = [f'{key},"{value}"']
            self.assertEqual(self.driver.system.error, (key, value))
            self.assertEqual(self.resource.buffer, [':SYST:ERR?'])

    def test_system_rsense(self):

        self.resource.buffer = ['1']
        self.driver.system.rsense = 'OFF'
        self.assertEqual(self.resource.buffer, [':SYST:RSEN 0', '*OPC?'])

        self.resource.buffer = ['0']
        self.assertEqual(self.driver.system.rsense, 'OFF')
        self.assertEqual(self.resource.buffer, [':SYST:RSEN?'])

        self.resource.buffer = ['1']
        self.driver.system.rsense = 'ON'
        self.assertEqual(self.resource.buffer, [':SYST:RSEN 1', '*OPC?'])

        self.resource.buffer = ['1']
        self.assertEqual(self.driver.system.rsense, 'ON')
        self.assertEqual(self.resource.buffer, [':SYST:RSEN?'])

    def test_system_beeper(self):
        for value in (True, False, 1, 0):
            self.resource.buffer = ['1']
            self.driver.system.beeper.status = value
            self.assertEqual(self.resource.buffer, [f':SYST:BEEP:STAT {value:d}', '*OPC?'])

            self.resource.buffer = [f'{value:d}']
            self.assertEqual(self.driver.system.beeper.status, value)
            self.assertEqual(self.resource.buffer, [':SYST:BEEP:STAT?'])

    def test_source(self):
        self.resource.buffer = ['1']
        self.driver.source.clear()
        self.assertEqual(self.resource.buffer, [':SOUR:CLE', '*OPC?'])

    def test_source_function(self):
        for key, value in (
            ('CURR', 'CURRENT'),
            ('VOLT', 'VOLTAGE'),
            ('MEM', 'MEMORY')
            ):
            self.resource.buffer = ['1']
            self.driver.source.function.mode = value
            self.assertEqual(self.resource.buffer, [f':SOUR:FUNC:MODE {key}', '*OPC?'])

            self.resource.buffer = [f'{key}']
            self.assertEqual(self.driver.source.function.mode, value)
            self.assertEqual(self.resource.buffer, [':SOUR:FUNC:MODE?'])

    def test_source_voltage(self):
        for value in (float(format(random.randrange(-1100, +1100), 'E')) for _ in range(8)):
            self.resource.buffer = ['1']
            self.driver.source.voltage.level = value
            self.assertEqual(self.resource.buffer, [f':SOUR:VOLT:LEV {value:E}', '*OPC?'])

            self.resource.buffer = [f'{value:E}']
            self.assertEqual(self.driver.source.voltage.level, value)
            self.assertEqual(self.resource.buffer, [':SOUR:VOLT:LEV?'])

    def test_source_voltage_range_auto(self):
        for value in (True, False, 1, 0):
            self.resource.buffer = ['1']
            self.driver.source.voltage.range.auto = value
            self.assertEqual(self.resource.buffer, [f':SOUR:VOLT:RANG:AUTO {value:d}', '*OPC?'])

            self.resource.buffer = [f'{value:d}']
            self.assertEqual(self.driver.source.voltage.range.auto, value)
            self.assertEqual(self.resource.buffer, [':SOUR:VOLT:RANG:AUTO?'])

    def test_source_voltage_range_level(self):
        for value in (float(format(random.randrange(-1100, +1100), 'E')) for _ in range(8)):
            self.resource.buffer = ['1']
            self.driver.source.voltage.range.level = value
            self.assertEqual(self.resource.buffer, [f':SOUR:VOLT:RANG {value:E}', '*OPC?'])

            self.resource.buffer = [f'{value:E}']
            self.assertEqual(self.driver.source.voltage.range.level, value)
            self.assertEqual(self.resource.buffer, [':SOUR:VOLT:RANG?'])

if __name__ == '__main__':
    unittest.main()
