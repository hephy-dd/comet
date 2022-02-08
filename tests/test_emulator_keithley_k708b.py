import unittest

from comet.emulator.keithley.k708b import K708BEmulator
from comet.utils import combine_matrix


class K708BEmulatorTest(unittest.TestCase):

    def setUp(self):
        self.emulator = K708BEmulator()

    def test_constants(self):
        channels = combine_matrix('1', 'ABCDEFGH', '0', '12345678')
        self.assertEqual(self.emulator.CHANNELS, channels)

    def test_basic(self):
        self.assertEqual(self.emulator('*IDN?'), 'Keithley Inc., Model 708B, 43768438, v1.0 (Emulator)')
        self.assertEqual(self.emulator('reset()'), None)
        self.assertEqual(self.emulator('*CLS'), None)
        self.assertEqual(self.emulator('*OPC?'), '1')
