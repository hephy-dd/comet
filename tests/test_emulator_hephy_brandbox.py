import os
import unittest

from comet.emulator.hephy.brandbox import BrandBoxEmulator


class BrandBoxEmulatorTest(unittest.TestCase):

    def setUp(self):
        self.emulator = BrandBoxEmulator()

    def test_basic(self):
        self.assertEqual(self.emulator('*IDN?'), 'BrandBox, v2.0 (Emulator)')
        self.assertEqual(self.emulator('*RST'), 'OK')
        self.assertEqual(self.emulator('*CLS'), 'OK')
        self.assertEqual(self.emulator('*STB?'), '0,0,0,0,0,0')
        self.assertEqual(self.emulator('*STR?'), '0')
        self.assertEqual(self.emulator('*OPC?'), '1')

    def test_debug(self):
        self.assertEqual(self.emulator('DEBUG?'), 'Err99')

    def test_channels(self):
        self.assertEqual(self.emulator(':CLOS:STAT?'), "")
        self.assertEqual(self.emulator(':OPEN:STAT?'), 'A1,A2,B1,B2,C1,C2')
        self.assertEqual(self.emulator(':CLOS C1,A1'), "OK")
        self.assertEqual(self.emulator(':CLOS:STAT?'), 'A1,C1')
        self.assertEqual(self.emulator(':OPEN:STAT?'), 'A2,B1,B2,C2')
        self.assertEqual(self.emulator(':OPEN C1'), "OK")
        self.assertEqual(self.emulator(':CLOS:STAT?'), 'A1')
        self.assertEqual(self.emulator(':OPEN:STAT?'), 'A2,B1,B2,C1,C2')

        self.assertEqual(self.emulator(':OPEN A1,A2,B1'), "OK")
        self.assertEqual(self.emulator(':OPEN B2,C1,C2'), "OK")

        self.assertEqual(self.emulator('GET:A ?'), 'OFF,OFF')
        self.assertEqual(self.emulator('GET:A1 ?'), 'OFF')
        self.assertEqual(self.emulator('GET:A2 ?'), 'OFF')
        self.assertEqual(self.emulator('GET:B ?'), 'OFF,OFF')
        self.assertEqual(self.emulator('GET:B1 ?'), 'OFF')
        self.assertEqual(self.emulator('GET:B2 ?'), 'OFF')
        self.assertEqual(self.emulator('GET:C ?'), 'OFF,OFF')
        self.assertEqual(self.emulator('GET:C1 ?'), 'OFF')
        self.assertEqual(self.emulator('GET:C2 ?'), 'OFF')

        self.assertEqual(self.emulator('SET:A2_ON'), 'OK')
        self.assertEqual(self.emulator('SET:B1_ON'), 'OK')
        self.assertEqual(self.emulator('SET:C_ON'), 'OK')

        self.assertEqual(self.emulator('GET:A ?'), 'OFF,ON')
        self.assertEqual(self.emulator('GET:A1 ?'), 'OFF')
        self.assertEqual(self.emulator('GET:A2 ?'), 'ON')
        self.assertEqual(self.emulator('GET:B ?'), 'ON,OFF')
        self.assertEqual(self.emulator('GET:B1 ?'), 'ON')
        self.assertEqual(self.emulator('GET:B2 ?'), 'OFF')
        self.assertEqual(self.emulator('GET:C ?'), 'ON,ON')
        self.assertEqual(self.emulator('GET:C1 ?'), 'ON')
        self.assertEqual(self.emulator('GET:C2 ?'), 'ON')

        self.assertEqual(self.emulator('SET:A_OFF'), 'OK')
        self.assertEqual(self.emulator('SET:B_OFF'), 'OK')
        self.assertEqual(self.emulator('SET:C1_OFF'), 'OK')
        self.assertEqual(self.emulator('SET:C2_OFF'), 'OK')

        self.assertEqual(self.emulator('GET:A ?'), 'OFF,OFF')
        self.assertEqual(self.emulator('GET:A1 ?'), 'OFF')
        self.assertEqual(self.emulator('GET:A2 ?'), 'OFF')
        self.assertEqual(self.emulator('GET:B ?'), 'OFF,OFF')
        self.assertEqual(self.emulator('GET:B1 ?'), 'OFF')
        self.assertEqual(self.emulator('GET:B2 ?'), 'OFF')
        self.assertEqual(self.emulator('GET:C ?'), 'OFF,OFF')
        self.assertEqual(self.emulator('GET:C1 ?'), 'OFF')
        self.assertEqual(self.emulator('GET:C2 ?'), 'OFF')

        self.assertEqual(self.emulator(':CLOS:STAT?'), "")
        self.assertEqual(self.emulator('*STB?'), '0,0,0,0,0,0')

    def test_mod(self):
        self.assertEqual(self.emulator('GET:MOD ?'), 'N/A')
        self.assertEqual(self.emulator('SET:MOD IV'), 'OK')
        self.assertEqual(self.emulator('GET:MOD ?'), 'IV')
        self.assertEqual(self.emulator('SET:MOD CV'), 'OK')
        self.assertEqual(self.emulator('GET:MOD ?'), 'CV')
        self.assertEqual(self.emulator('SET:MOD CC'), 'Err99')
        self.assertEqual(self.emulator('GET:MOD ?'), 'CV')

    def test_test_state(self):
        self.assertEqual(self.emulator('GET:TST ?'), 'OFF')
        self.assertEqual(self.emulator('SET:TST ON'), "OK")
        self.assertEqual(self.emulator('GET:TST ?'), 'ON')
        self.assertEqual(self.emulator('SET:TST OFF'), "OK")
        self.assertEqual(self.emulator('GET:TST ?'), 'OFF')
