import unittest

from comet.emulator.keithley.k6517b import K6517BEmulator


class K6517BEmulatorTest(unittest.TestCase):
    def setUp(self):
        self.emulator = K6517BEmulator()

    def test_basic(self):
        self.assertEqual(self.emulator("*IDN?"),"Keithley Inc., Model 6517B, 43768438, v1.0 (Emulator)")
        self.assertEqual(self.emulator("*RST"), None)
        self.assertEqual(self.emulator("*OPC?"), "1")

    def test_output_state(self):
        for command in ("OUTP", ":OUTP", "OUTP:STAT", ":OUTP:STAT"):
            self.assertEqual(self.emulator(f"{command}?"), "0")
            self.assertEqual(self.emulator(f"{command} ON"), None)
            self.assertEqual(self.emulator(f"{command}?"), "1")
            self.assertEqual(self.emulator(f"{command} OFF"), None)
            self.assertEqual(self.emulator(f"{command}?"), "0")
            self.assertEqual(self.emulator(f"{command} 1"), None)
            self.assertEqual(self.emulator(f"{command}?"), "1")
            self.assertEqual(self.emulator(f"{command} 0"), None)
            self.assertEqual(self.emulator(f"{command}?"), "0")

    def test_source_voltage_level_immediate_amplitude(self):
        for command in ("SOUR:VOLT", ":SOUR:VOLT", ":SOUR:VOLT:LEV", ":SOUR:VOLT:LEV:IMM:AMPL"):
            self.assertEqual(self.emulator(f"{command}?"), format(0, "E"))
            self.assertEqual(self.emulator(f"{command} 42.5"), None)
            self.assertEqual(self.emulator(f"{command}?"), format(42.5, "E"))
            self.assertEqual(self.emulator(f"{command} 0"), None)
            self.assertEqual(self.emulator(f"{command}?"), format(0, "E"))

    def test_source_voltage_range(self):
        for command in ("SOUR:VOLT:RANG", ":SOUR:VOLT:RANG"):
            self.assertEqual(self.emulator(f"{command}?"), format(100, "E"))
            self.assertEqual(self.emulator(f"{command} 101"), None)
            self.assertEqual(self.emulator(f"{command}?"), format(1000, "E"))
            self.assertEqual(self.emulator(f"{command} 42"), None)
            self.assertEqual(self.emulator(f"{command}?"), format(100, "E"))

    def test_source_voltage_mconnect(self):
        commands = [
            (":SOUR:VOLT:MCON?", "0"),
            (":SOUR:VOLT:MCON ON", None),
            (":SOUR:VOLT:MCON?", "1"),
            ("SOUR:VOLT:MCON OFF", None),
            ("SOUR:VOLT:MCON?", "0"),
            ("SOUR:VOLT:MCON 0", None),
        ]
        for command, result in commands:
            self.assertEqual(self.emulator(command), result)

    def test_source_current_limit_state(self):
        commands = [
            ("SOUR:CURR:LIM?", "0"),
            ("SOUR:CURR:LIM:STAT?", "0"),
            (":SOUR:CURR:LIM?", "0"),
            (":SOUR:CURR:LIM:STAT?", "0"),
        ]
        for command, result in commands:
            self.assertEqual(self.emulator(command), result)
