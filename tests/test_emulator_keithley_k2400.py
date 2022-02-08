import unittest

from comet.emulator.keithley.k2400 import K2400Emulator


class K2400EmulatorTest(unittest.TestCase):

    def setUp(self):
        self.emulator = K2400Emulator()

    def test_basic(self):
        self.assertEqual(self.emulator('*IDN?'), 'Keithley Inc., Model 2400, 43768438, v1.0 (Emulator)')
        self.assertEqual(self.emulator('*RST'), None)
        self.assertEqual(self.emulator('*OPC?'), '1')

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
            self.assertEqual(self.emulator(f'{command}?'), format(210, 'E'))
            self.assertEqual(self.emulator(f'{command} 60'), None)
            self.assertEqual(self.emulator(f'{command}?'), format(60, 'E'))
            self.assertEqual(self.emulator(f'{command} 210'), None)
            self.assertEqual(self.emulator(f'{command}?'), format(210, 'E'))

    def test_sense_voltage_protection_level(self):
        for command in (f':VOLT:PROT', f':SENS:VOLT:PROT', f'SENS:VOLT:PROT:LEV', f':SENS:VOLT:PROT:LEV'):
            self.assertEqual(self.emulator(f'{command}?'), format(2.1e+1, 'E'))
            self.assertEqual(self.emulator(f'{command} 1.5E-3'), None)
            self.assertEqual(self.emulator(f'{command}?'), format(1.5e-3, 'E'))
            self.assertEqual(self.emulator(f'{command} 2.10E+1'), None)
            self.assertEqual(self.emulator(f'{command}?'), format(2.1e+1, 'E'))

    def test_sense_voltage_protection_tripped(self):
        for command in (f':VOLT:PROT:TRIP', f':SENS:VOLT:PROT:TRIP', f'SENS:VOLT:PROT:TRIP'):
            self.assertEqual(self.emulator(f'{command}?'), format(False, 'E'))

    def test_sense_current_protection_level(self):
        for command in (f':CURR:PROT', f':SENS:CURR:PROT', f'SENS:CURR:PROT:LEV', f':SENS:CURR:PROT:LEV'):
            self.assertEqual(self.emulator(f'{command}?'), format(1.05e-5, 'E'))
            self.assertEqual(self.emulator(f'{command} 0.0001'), None)
            self.assertEqual(self.emulator(f'{command}?'), format(0.0001, 'E'))
            self.assertEqual(self.emulator(f'{command} 1.05E-5'), None)
            self.assertEqual(self.emulator(f'{command}?'), format(1.05e-5, 'E'))

    def test_sense_current_protection_tripped(self):
        for command in (f':CURR:PROT:TRIP', f':SENS:CURR:PROT:TRIP', f'SENS:CURR:PROT:TRIP', ):
            self.assertEqual(self.emulator(f'{command}?'), format(False, 'E'))

    def test_sense_function(self):
        for command in (f':FUNC', f':FUNC:ON', f'SENS:FUNC:ON', f':SENS:FUNC:ON'):
            self.assertEqual(self.emulator(f'{command}?'), '\'CURR:DC\'')
            self.assertEqual(self.emulator(f'{command} \'VOLT\''), None)
            self.assertEqual(self.emulator(f'{command}?'), '\'VOLT:DC\'')
            self.assertEqual(self.emulator(f'{command} \'CURR\''), None)
            self.assertEqual(self.emulator(f'{command}?'), '\'CURR:DC\'')
