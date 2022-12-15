import unittest

from comet.emulator.marzhauser.tango import TangoEmulator


class TangoEmulatorTest(unittest.TestCase):

    def setUp(self):
        self.emulator = TangoEmulator()
        self.emulator("!autostatus 0")

    def test_basic(self):
        self.assertEqual(self.emulator("?version"), "TANGO-MINI3-EMULATOR, Version 1.00, Mar 11 2022, 13:51:01")
        self.assertTrue(self.emulator("?pos"), "0.000 0.000 0.000")
        self.assertTrue(self.emulator("?pos x"), "0.000")
        self.assertTrue(self.emulator("?pos y"), "0.000")
        self.assertTrue(self.emulator("?pos z"), "0.000")

    def test_cal_rm(self):
        self.assertEqual(self.emulator("!cal"), None)
        self.assertEqual(self.emulator("!cal x"), None)
        self.assertEqual(self.emulator("!rm"), None)
        self.assertEqual(self.emulator("!rm"), None)

    def test_move(self):
        self.assertEqual(self.emulator("!moa x 0.000"), None)
        self.assertEqual(self.emulator("!mor x 0.000"), None)

    def test_autostatus(self):
        self.assertEqual(self.emulator("!autostatus 1"), None)
        self.assertEqual(self.emulator("?autostatus"), "1")
        self.assertEqual(self.emulator("!autostatus 0"), None)
        self.assertEqual(self.emulator("?autostatus"), "0")

    def test_statusaxis(self):
        self.assertEqual(self.emulator("?statusaxis"), "@@@-.-")
        self.assertEqual(self.emulator("?statusaxis x"), "@")
        self.assertEqual(self.emulator("?statusaxis y"), "@")
        self.assertEqual(self.emulator("?statusaxis z"), "@")

    def test_calst(self):
        self.assertEqual(self.emulator("?calst"), "3 3 3")
        self.assertEqual(self.emulator("?calst x"), "3")
        self.assertEqual(self.emulator("?calst y"), "3")
        self.assertEqual(self.emulator("?calst z"), "3")

    def test_err(self):
        self.assertEqual(self.emulator("?err"), "0")
