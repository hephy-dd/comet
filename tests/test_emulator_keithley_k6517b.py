import pytest

from comet.emulator.keithley.k6517b import K6517BEmulator


@pytest.fixture
def emulator():
    return K6517BEmulator()


def test_basic(emulator):
    assert emulator("*IDN?") == "Keithley Inc., Model 6517B, 43768438, v1.0 (Emulator)"
    assert emulator("*RST") is None
    assert emulator("*OPC?") == "1"


def test_output_state(emulator):
    for command in ("OUTP", ":OUTP", "OUTP:STAT", ":OUTP:STAT"):
        assert emulator(f"{command}?") == "0"
        assert emulator(f"{command} ON") is None
        assert emulator(f"{command}?") == "1"
        assert emulator(f"{command} OFF") is None
        assert emulator(f"{command}?") == "0"
        assert emulator(f"{command} 1") is None
        assert emulator(f"{command}?") == "1"
        assert emulator(f"{command} 0") is None
        assert emulator(f"{command}?") == "0"


def test_source_voltage_level_immediate_amplitude(emulator):
    for command in ("SOUR:VOLT", ":SOUR:VOLT", ":SOUR:VOLT:LEV", ":SOUR:VOLT:LEV:IMM:AMPL"):
        assert emulator(f"{command}?") == format(0, "E")
        assert emulator(f"{command} 42.5") is None
        assert emulator(f"{command}?") == format(42.5, "E")
        assert emulator(f"{command} 0") is None
        assert emulator(f"{command}?") == format(0, "E")


def test_source_voltage_range(emulator):
    for command in ("SOUR:VOLT:RANG", ":SOUR:VOLT:RANG"):
        assert emulator(f"{command}?") == format(100, "E")
        assert emulator(f"{command} 101")is None
        assert emulator(f"{command}?") == format(1000, "E")
        assert emulator(f"{command} 42")is None
        assert emulator(f"{command}?") == format(100, "E")


def test_source_voltage_mconnect(emulator):
    assert emulator(":SOUR:VOLT:MCON?") == "0"
    assert emulator(":SOUR:VOLT:MCON ON") is None
    assert emulator(":SOUR:VOLT:MCON?") == "1"
    assert emulator("SOUR:VOLT:MCON OFF") is None
    assert emulator("SOUR:VOLT:MCON?") == "0"
    assert emulator("SOUR:VOLT:MCON 0") is None


def test_source_current_limit_state(emulator):
    assert emulator("SOUR:CURR:LIM?") == "0"
    assert emulator("SOUR:CURR:LIM:STAT?") == "0"
    assert emulator(":SOUR:CURR:LIM?") == "0"
    assert emulator(":SOUR:CURR:LIM:STAT?") == "0"
