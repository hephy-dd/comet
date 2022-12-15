import unittest

from comet.emulator.marzhauser.tango import TangoEmulator


class TangoEmulatorTest(unittest.TestCase):

    def setUp(self):
        self.emulator = TangoEmulator()

    def test_basic(self):
        self.assertEqual(self.emulator("?version"), "TANGO-MINI3-EMULATOR, Version 1.00, Mar 11 2022, 13:51:01")
        self.assertTrue(self.emulator("?pos"), "0.000 0.000 0.000")

    def test_error(self):
        self.assertEqual(self.emulator("?err"), "0")
