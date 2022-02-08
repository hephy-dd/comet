import os
import unittest

from comet.emulator.keithley.k2470 import K2470Emulator


class K2470EmulatorTest(unittest.TestCase):

    def setUp(self):
        self.emulator = K2470Emulator()

    def test_basic(self):
        self.assertEqual(self.emulator('*IDN?'), 'Keithley Inc., Model 2470, 43768438, v1.0 (Emulator)')
        self.assertEqual(self.emulator('*RST'), None)
        self.assertEqual(self.emulator('*OPC?'), '1')
        self.assertEqual(self.emulator('*LANG?'), 'SCPI')

    def test_output_state(self):
        for command in ('OUTP', ':OUTP', 'OUTP:STAT', ':OUTP:STAT'):
            self.assertEqual(self.emulator(f'{command}?'), '0')
            self.assertEqual(self.emulator(f'{command} ON'), None)
            self.assertEqual(self.emulator(f'{command}?'), '1')
            self.assertEqual(self.emulator(f'{command} OFF'), None)
            self.assertEqual(self.emulator(f'{command}?'), '0')
            self.assertEqual(self.emulator(f'{command} 1'), None)
            self.assertEqual(self.emulator(f'{command}?'), '1')
            self.assertEqual(self.emulator(f'{command} 0'), None)
            self.assertEqual(self.emulator(f'{command}?'), '0')

    def test_source_function(self):
        for command in ('SOUR:FUNC', ':SOUR:FUNC', ':SOUR:FUNC:MODE'):
            self.assertEqual(self.emulator(f'{command}?'), 'VOLT')
            self.assertEqual(self.emulator(f'{command} CURR'), None)
            self.assertEqual(self.emulator(f'{command}?'), 'CURR')
            self.assertEqual(self.emulator(f'{command} VOLT'), None)

    def test_source_level(self):
        for function in ('VOLT', 'CURR'):
            for command in (f'SOUR:{function}', f':SOUR:{function}:LEV'):
                self.assertEqual(self.emulator(f'{command}?'), format(0, 'E'))
                self.assertEqual(self.emulator(f'{command} 42.5'), None)
                self.assertEqual(self.emulator(f'{command}?'), format(42.5, 'E'))
                self.assertEqual(self.emulator(f'{command} 0'), None)
                self.assertEqual(self.emulator(f'{command}?'), format(0, 'E'))

    def test_source_range(self):
        for function in ('VOLT', 'CURR'):
            for command in (f'SOUR:{function}:RANG', f':SOUR:{function}:RANG'):
                self.assertEqual(self.emulator(f'{command}?'), format(0, 'E'))
                self.assertEqual(self.emulator(f'{command} 100'), None)
                self.assertEqual(self.emulator(f'{command}?'), format(100, 'E'))
                self.assertEqual(self.emulator(f'{command} 0'), None)
                self.assertEqual(self.emulator(f'{command}?'), format(0, 'E'))

    def test_source_range_auto(self):
        for function in ('VOLT', 'CURR'):
            for command in (f'SOUR:{function}:RANG:AUTO', f':SOUR:{function}:RANG:AUTO'):
                self.assertEqual(self.emulator(f'{command}?'), '1')
                self.assertEqual(self.emulator(f'{command} 0'), None)
                self.assertEqual(self.emulator(f'{command}?'), '0')
                self.assertEqual(self.emulator(f'{command} 1'), None)
                self.assertEqual(self.emulator(f'{command}?'), '1')
                self.assertEqual(self.emulator(f'{command} OFF'), None)
                self.assertEqual(self.emulator(f'{command}?'), '0')
                self.assertEqual(self.emulator(f'{command} ON'), None)
                self.assertEqual(self.emulator(f'{command}?'), '1')

    def test_source_voltage_protection_level(self):
        for command in (f'SOUR:VOLT:PROT', f':SOUR:VOLT:PROT', f'SOUR:VOLT:PROT:LEV', f':SOUR:VOLT:PROT:LEV'):
            self.assertEqual(self.emulator(f'{command}?'), format(1050, 'E'))
            self.assertEqual(self.emulator(f'{command} 60'), None)
            self.assertEqual(self.emulator(f'{command}?'), format(60, 'E'))
            self.assertEqual(self.emulator(f'{command} 1050'), None)
            self.assertEqual(self.emulator(f'{command}?'), format(1050, 'E'))

    def test_source_voltage_ilimit_level(self):
        for command in (f'SOUR:VOLT:ILIM', f':SOUR:VOLT:ILIM', f'SOUR:VOLT:ILIM:LEV', f':SOUR:VOLT:ILIM:LEV'):
            self.assertEqual(self.emulator(f'{command}?'), format(1.05e-4, 'E'))
            self.assertEqual(self.emulator(f'{command} 2.1E-5'), None)
            self.assertEqual(self.emulator(f'{command}?'), format(2.1e-5, 'E'))
            self.assertEqual(self.emulator(f'{command} 1.05E-4'), None)
            self.assertEqual(self.emulator(f'{command}?'), format(1.05e-4, 'E'))

    def test_source_voltage_ilimit_level_tripped(self):
        for command in (f'SOUR:VOLT:ILIM:TRIP', f':SOUR:VOLT:ILIM:TRIP', f'SOUR:VOLT:ILIM:LEV:TRIP', f':SOUR:VOLT:ILIM:LEV:TRIP'):
            self.assertEqual(self.emulator(f'{command}?'), format(False, 'E'))

    def test_source_current_vlimit_level(self):
        for command in (f'SOUR:CURR:VLIM', f':SOUR:CURR:VLIM', f'SOUR:CURR:VLIM:LEV', f':SOUR:CURR:VLIM:LEV'):
            self.assertEqual(self.emulator(f'{command}?'), format(2.1e-1, 'E'))
            self.assertEqual(self.emulator(f'{command} 0.0001'), None)
            self.assertEqual(self.emulator(f'{command}?'), format(0.0001, 'E'))
            self.assertEqual(self.emulator(f'{command} 2.1E-1'), None)
            self.assertEqual(self.emulator(f'{command}?'), format(2.1e-1, 'E'))

    def test_source_current_vlimit_level_tripped(self):
        for command in (f'SOUR:CURR:VLIM:TRIP', f':SOUR:CURR:VLIM:TRIP', f'SOUR:CURR:VLIM:LEV:TRIP', f':SOUR:CURR:VLIM:LEV:TRIP'):
            self.assertEqual(self.emulator(f'{command}?'), format(False, 'E'))
