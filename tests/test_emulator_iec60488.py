import os
import unittest

from comet.emulator.iec60488 import IEC60488Emulator


class IEC60488EmulatorTest(unittest.TestCase):

    def setUp(self):
        self.emulator = IEC60488Emulator()

    def test_basic(self):
        self.assertEqual(self.emulator('*IDN?'), 'Generic IEC60488 Instrument (Emulator)')
        self.assertTrue(self.emulator('*ESR?') in ('0', '1'))
        self.assertEqual(self.emulator('*ESE?'), '0')
        self.assertEqual(self.emulator('*ESE 1'), None)
        self.assertEqual(self.emulator('*STB?'), '0')
        self.assertEqual(self.emulator('*OPC?'), '1')
        self.assertEqual(self.emulator('*OPC 1'), None)
        self.assertEqual(self.emulator('*RST'), None)
        self.assertEqual(self.emulator('*CLS'), None)
        self.assertEqual(self.emulator('*TST?'), '0')
        self.assertEqual(self.emulator('*WAI'), None)
