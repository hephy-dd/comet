import os
import unittest

from comet.emulator.keithley.k2657a import K2657AEmulator


class K2657AEmulatorTest(unittest.TestCase):

    def setUp(self):
        self.emulator = K2657AEmulator()

    def test_basic(self):
        self.assertEqual(self.emulator('*IDN?'), 'Keithley Inc., Model 2657A, 43768438, v1.0 (Emulator)')
        self.assertEqual(self.emulator('*RST'), None)
        self.assertEqual(self.emulator('*CLS'), None)
        self.assertEqual(self.emulator('*OPC?'), '1')
        self.assertEqual(self.emulator('*WAI'), None)

    def test_source_output(self):
        self.assertEqual(float(self.emulator('print(smua.source.output)')), 0.)
        self.assertEqual(self.emulator('smua.source.output = 1'), None)
        self.assertEqual(float(self.emulator('print(smua.source.output)')), 1.)
        self.assertEqual(self.emulator('smua.source.output = 0'), None)
        self.assertEqual(float(self.emulator('print(smua.source.output)')), 0.)
        self.assertEqual(self.emulator('smua.source.output = smua.OUTPUT_ON'), None)
        self.assertEqual(float(self.emulator('print(smua.source.output)')), 1.)
        self.assertEqual(self.emulator('smua.source.output = smua.OUTPUT_OFF'), None)
        self.assertEqual(float(self.emulator('print(smua.source.output)')), 0.)

    def test_source_function(self):
        self.assertEqual(float(self.emulator('print(smua.source.func)')), 1)
        self.assertEqual(self.emulator('smua.source.func = 0'), None)
        self.assertEqual(float(self.emulator('print(smua.source.func)')), 0)
        self.assertEqual(self.emulator('smua.source.func = 1'), None)
        self.assertEqual(float(self.emulator('print(smua.source.func)')), 1)
        self.assertEqual(self.emulator('smua.source.func = smua.OUTPUT_DCAMPS'), None)
        self.assertEqual(float(self.emulator('print(smua.source.output)')), 0)
        self.assertEqual(self.emulator('smua.source.func = smua.OUTPUT_DCVOLTS'), None)
        self.assertEqual(float(self.emulator('print(smua.source.func)')), 1)

    def test_source_levelv(self):
        self.assertEqual(float(self.emulator(f'print(smua.source.levelv)')), 0)
        self.assertEqual(self.emulator('smua.source.levelv = 420'), None)
        self.assertEqual(float(self.emulator(f'print(smua.source.levelv)')), 420.)
        self.assertEqual(self.emulator('smua.source.levelv = 0'), None)
        self.assertEqual(float(self.emulator(f'print(smua.source.levelv)')), 0)

    def test_source_leveli(self):
        self.assertEqual(float(self.emulator(f'print(smua.source.leveli)')), 0)
        self.assertEqual(self.emulator('smua.source.leveli = 2.5E-6'), None)
        self.assertEqual(float(self.emulator(f'print(smua.source.leveli)')), 2.5E-6)
        self.assertEqual(self.emulator('smua.source.leveli = 0'), None)
        self.assertEqual(float(self.emulator(f'print(smua.source.leveli)')), 0)

    def test_source_rangev(self):
        self.assertEqual(float(self.emulator('print(smua.source.rangev)')), 0)
        self.assertEqual(self.emulator('smua.source.rangev = 300'), None)
        self.assertEqual(float(self.emulator('print(smua.source.rangev)')), 300.)
        self.assertEqual(self.emulator('smua.source.rangev = 0'), None)
        self.assertEqual(float(self.emulator('print(smua.source.rangev)')), 0)

    def test_source_rangei(self):
        self.assertEqual(float(self.emulator('print(smua.source.rangei)')), 0)
        self.assertEqual(self.emulator('smua.source.rangei = 2.0E-3'), None)
        self.assertEqual(float(self.emulator('print(smua.source.rangei)')), 2.0E-3)
        self.assertEqual(self.emulator('smua.source.rangei = 0'), None)
        self.assertEqual(float(self.emulator('print(smua.source.rangei)')), 0)

    def test_source_autorangev(self):
        self.assertEqual(float(self.emulator('print(smua.source.autorangev)')), 1)
        self.assertEqual(self.emulator('smua.source.autorangev = 0'), None)
        self.assertEqual(float(self.emulator('print(smua.source.autorangev)')), 0)
        self.assertEqual(self.emulator('smua.source.autorangev = 1'), None)
        self.assertEqual(float(self.emulator('print(smua.source.autorangev)')), 1)
        self.assertEqual(self.emulator('smua.source.autorangev = smua.AUTORANGE_OFF'), None)
        self.assertEqual(float(self.emulator('print(smua.source.autorangev)')), 0)
        self.assertEqual(self.emulator('smua.source.autorangev = smua.AUTORANGE_ON'), None)
        self.assertEqual(float(self.emulator('print(smua.source.autorangev)')), 1)

    def test_source_autorangei(self):
        self.assertEqual(float(self.emulator('print(smua.source.autorangei)')), 1)
        self.assertEqual(self.emulator('smua.source.autorangei = 0'), None)
        self.assertEqual(float(self.emulator('print(smua.source.autorangei)')), 0)
        self.assertEqual(self.emulator('smua.source.autorangei = 1'), None)
        self.assertEqual(float(self.emulator('print(smua.source.autorangei)')), 1)
        self.assertEqual(self.emulator('smua.source.autorangei = smua.AUTORANGE_OFF'), None)
        self.assertEqual(float(self.emulator('print(smua.source.autorangei)')), 0)
        self.assertEqual(self.emulator('smua.source.autorangei = smua.AUTORANGE_ON'), None)
        self.assertEqual(float(self.emulator('print(smua.source.autorangei)')), 1)

    def test_source_protectv(self):
        self.assertEqual(float(self.emulator('print(smua.source.protectv)')), 0)
        self.assertEqual(self.emulator('smua.source.protectv = 300'), None)
        self.assertEqual(float(self.emulator('print(smua.source.protectv)')), 300.)
        self.assertEqual(self.emulator('smua.source.protectv = 0'), None)
        self.assertEqual(float(self.emulator('print(smua.source.protectv)')), 0)
