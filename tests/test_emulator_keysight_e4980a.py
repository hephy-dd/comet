import unittest

from comet.emulator.keysight.e4980a import E4980AEmulator


class E4980AEmulatorTest(unittest.TestCase):

    def setUp(self):
        self.emulator = E4980AEmulator()

    def test_basic(self):
        self.assertEqual(self.emulator('*IDN?'), 'Keysight Inc., Model E4980A, v1.0 (Emulator)')
        self.assertEqual(self.emulator('*RST'), None)
        self.assertEqual(self.emulator('*OPC?'), '1')

    def test_correction_method(self):
        self.assertEqual(self.emulator(':CORR:METH?'), '0')
        self.assertEqual(self.emulator(':CORR:METH MULT'), None)
        self.assertEqual(self.emulator(':CORR:METH?'), '1')
        self.assertEqual(self.emulator(':CORR:METH SING'), None)
        self.assertEqual(self.emulator(':CORR:METH?'), '0')

    def test_fetch_impedance_format(self):
        def get_types(result):
            tokens = result.split(',')
            self.assertEqual(len(tokens), 3)
            a, b, c = tokens
            float(a), float(b)
            return True
        for command in ('FETC', ':FETC', 'FETCH:FORM', ':FETCH:FORM', 'FETCH:IMP:FORM', ':FETCH:IMP:FORM'):
            self.assertTrue(get_types(self.emulator(f'{command}?')))

    def test_bias_voltage_level(self):
        for command in ('BIAS:VOLT', ':BIAS:VOLT', 'BIAS:VOLT:LEV', ':BIAS:VOLT:LEV'):
            self.assertEqual(float(self.emulator(f'{command}?')), 0)
            self.assertEqual(self.emulator(f'{command} 4.5E+0'), None)
            self.assertEqual(float(self.emulator(f'{command}?')), 4.5)
            self.assertEqual(self.emulator(f'{command} 0'), None)
            self.assertEqual(float(self.emulator(f'{command}?')), 0)

    def test_bias_state(self):
        for command in ('BIAS:STAT', ':BIAS:STAT'):
            self.assertEqual(self.emulator(f'{command}?'), '0')
            self.assertEqual(self.emulator(f'{command} 1'), None)
            self.assertEqual(self.emulator(f'{command}?'), '1')
            self.assertEqual(self.emulator(f'{command} 0'), None)
            self.assertEqual(self.emulator(f'{command}?'), '0')
            self.assertEqual(self.emulator(f'{command} ON'), None)
            self.assertEqual(self.emulator(f'{command}?'), '1')
            self.assertEqual(self.emulator(f'{command} OFF'), None)
            self.assertEqual(self.emulator(f'{command}?'), '0')
