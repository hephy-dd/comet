import os
import unittest

from comet.emulator.hephy.shuntbox import ShuntBoxEmulator


class BrandBoxEmulatorTest(unittest.TestCase):

    def setUp(self):
        self.emulator = ShuntBoxEmulator()

    def test_basic(self):
        self.assertEqual(self.emulator('*IDN?'), 'ShuntBox, v1.0 (Emulator)')
        self.assertTrue(int(self.emulator('GET:UP ?')) >= 0)
        self.assertEqual(int(self.emulator('GET:RAM ?')), 4200)

    def test_temp(self):
        self.assertEqual(len(self.emulator('GET:TEMP ALL').split(',')), ShuntBoxEmulator.CHANNELS)
        for index in range(ShuntBoxEmulator.CHANNELS):
            self.assertTrue(float(self.emulator(f'GET:TEMP {index}')) > 0)

    def test_set_rel(self):
        self.assertEqual(self.emulator('SET:REL_ON ALL'), 'OK')
        self.assertEqual(self.emulator('SET:REL_OFF ALL'), 'OK')
        for index in range(ShuntBoxEmulator.CHANNELS):
            self.assertEqual(self.emulator(f'SET:REL_ON {index}'), 'OK')
            self.assertEqual(self.emulator(f'SET:REL_OFF {index}'), 'OK')

    def test_get_rel(self):
        self.assertEqual(self.emulator('GET:REL ALL'), ','.join(['0'] * (ShuntBoxEmulator.CHANNELS + 4)))
        for index in range(ShuntBoxEmulator.CHANNELS):
            self.assertEqual(self.emulator(f'GET:REL {index}'), '0')

    def test_error(self):
        self.assertEqual(self.emulator('FOO'), 'Err99')
