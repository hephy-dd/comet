import re
import unittest

from comet.emulator.cts.itc import ITCEmulator


class ITCEmulatorTest(unittest.TestCase):

    def setUp(self):
        self.emulator = ITCEmulator()

    def test_basic(self):
        self.assertEqual(self.emulator('S'), 'S11110100\x06')

    def test_time(self):
        self.assertTrue(re.match(r'^T\d{6}\d{6}$', self.emulator('T')))
        self.assertTrue(re.match(r'^T\d{6}\d{6}$', self.emulator('t010203010203')))

    def test_channels(self):
        self.assertTrue(re.match(r'A0 \-?\d+\.\d \-?\d+\.\d', self.emulator('A0')))
        self.assertTrue(re.match(r'A1 \-?\d+\.\d \-?\d+\.\d', self.emulator('A1')))
        self.assertTrue(re.match(r'A2 \-?\d+\.\d \-?\d+\.\d', self.emulator('A2')))
        self.assertTrue(re.match(r'A3 \-?\d+\.\d \-?\d+\.\d', self.emulator('A3')))
        self.assertTrue(re.match(r'A4 \-?\d+\.\d \-?\d+\.\d', self.emulator('A4')))
        self.assertTrue(re.match(r'A5 \-?\d+\.\d \-?\d+\.\d', self.emulator('A5')))
        self.assertTrue(re.match(r'A6 \-?\d+\.\d \-?\d+\.\d', self.emulator('A6')))
        self.assertTrue(re.match(r'A7 \-?\d+\.\d \-?\d+\.\d', self.emulator('A7')))
        self.assertTrue(re.match(r'A8 \-?\d+\.\d \-?\d+\.\d', self.emulator('A8')))
        self.assertTrue(re.match(r'A9 \-?\d+\.\d \-?\d+\.\d', self.emulator('A9')))
        self.assertTrue(re.match(r'A\: \-?\d+\.\d \-?\d+\.\d', self.emulator('A:')))
        self.assertTrue(re.match(r'A\; \-?\d+\.\d \-?\d+\.\d', self.emulator('A;')))
        self.assertTrue(re.match(r'A\< \-?\d+\.\d \-?\d+\.\d', self.emulator('A<')))
        self.assertTrue(re.match(r'A\= \-?\d+\.\d \-?\d+\.\d', self.emulator('A=')))
        self.assertTrue(re.match(r'A\> \-?\d+\.\d \-?\d+\.\d', self.emulator('A>')))
        self.assertTrue(re.match(r'A\? \-?\d+\.\d \-?\d+\.\d', self.emulator('A?')))

    def test_program(self):
        self.assertEqual(self.emulator('P'), 'P000')
        self.assertEqual(self.emulator('P004'), 'P004')
        self.assertEqual(self.emulator('P'), 'P004')
        self.assertEqual(self.emulator('P000'), 'P000')
        self.assertEqual(self.emulator('P'), 'P000')
