import os
import unittest

from comet.emulator.keithley.k2700 import K2700Emulator


class K2700EmulatorTest(unittest.TestCase):

    def setUp(self):
        self.emulator = K2700Emulator()

    def test_basic(self):
        self.assertEqual(self.emulator('*IDN?'), 'Keithley Inc., Model 2700, 43768438, v1.0 (Emulator)')
        self.assertEqual(self.emulator('*RST'), None)
        self.assertEqual(self.emulator('*OPC?'), '1')
