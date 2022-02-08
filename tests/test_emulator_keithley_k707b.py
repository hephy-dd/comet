import unittest

from comet.emulator.keithley.k707b import K707BEmulator
from comet.utils import combine_matrix


class K707BEmulatorTest(unittest.TestCase):

    def setUp(self):
        self.emulator = K707BEmulator()

    def test_constants(self):
        channels = combine_matrix('1234', 'ABCDEFGH', (format(i, '02d') for i in range(1, 13)))
        self.assertEqual(self.emulator.CHANNELS, channels)

    def test_basic(self):
        self.assertEqual(self.emulator('*IDN?'), 'Keithley Inc., Model 707B, 43768438, v1.0 (Emulator)')
        self.assertEqual(self.emulator('*RST'), None)
        self.assertEqual(self.emulator('*CLS'), None)
        self.assertEqual(self.emulator('*OPC?'), '1')
        self.assertEqual(self.emulator('print(errorqueue.count)'), '0')

    def test_channels(self):
        self.assertEqual(self.emulator('print(channel.getclose("allslots"))'), 'nil')
        self.assertEqual(self.emulator('print(errorqueue.count)'), '0')
        self.assertEqual(self.emulator('channel.close("1A01,1A07")'), None)
        self.assertEqual(self.emulator('print(errorqueue.count)'), '0')
        self.assertEqual(self.emulator('print(channel.getclose("allslots"))'), '1A01;1A07')
        self.assertEqual(self.emulator('print(errorqueue.count)'), '0')
        self.assertEqual(self.emulator('channel.open("allslots")'), None)
        self.assertEqual(self.emulator('print(errorqueue.count)'), '0')
        self.assertEqual(self.emulator('print(channel.getclose("allslots"))'), 'nil')
        self.assertEqual(self.emulator('print(errorqueue.count)'), '0')
