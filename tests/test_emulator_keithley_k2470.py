import pytest

from comet.emulator.keithley.k2470 import K2470Emulator


@pytest.fixture
def emulator():
    return K2470Emulator()


def test_basic(emulator):
    assert emulator("*IDN?") == "Keithley Inc., Model 2470, 43768438, v1.0 (Emulator)"
    assert emulator("*RST") is None
    assert emulator("*OPC?") == "1"
    assert emulator("*LANG?") == "SCPI"


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


def test_source_function(emulator):
    for command in ("SOUR:FUNC", ":SOUR:FUNC", ":SOUR:FUNC:MODE"):
        assert emulator(f"{command}?") == "VOLT"
        assert emulator(f"{command} CURR") is None
        assert emulator(f"{command}?") == "CURR"
        assert emulator(f"{command} VOLT") is None


def test_source_level(emulator):
    for function in ("VOLT", "CURR"):
        for command in (f"SOUR:{function}", f":SOUR:{function}:LEV"):
            assert float(emulator(f"{command}?")) == 0
            assert emulator(f"{command} 42.5") is None
            assert float(emulator(f"{command}?")) == 42.5
            assert emulator(f"{command} 0") is None
            assert float(emulator(f"{command}?")) == 0


def test_source_range(emulator):
    for function in ("VOLT", "CURR"):
        for command in (f"SOUR:{function}:RANG", f":SOUR:{function}:RANG"):
            assert float(emulator(f"{command}?")) == 0
            assert emulator(f"{command} 100") is None
            assert float(emulator(f"{command}?")) == 100
            assert emulator(f"{command} 0") is None
            assert float(emulator(f"{command}?")) == 0


def test_source_range_auto(emulator):
    for function in ("VOLT", "CURR"):
        for command in (f"SOUR:{function}:RANG:AUTO", f":SOUR:{function}:RANG:AUTO"):
            assert emulator(f"{command}?") == "1"
            assert emulator(f"{command} 0") is None
            assert emulator(f"{command}?") == "0"
            assert emulator(f"{command} 1") is None
            assert emulator(f"{command}?") == "1"
            assert emulator(f"{command} OFF") is None
            assert emulator(f"{command}?") == "0"
            assert emulator(f"{command} ON") is None
            assert emulator(f"{command}?") == "1"


def test_source_voltage_protection_level(emulator):
    for command in ("SOUR:VOLT:PROT", ":SOUR:VOLT:PROT", "SOUR:VOLT:PROT:LEV", ":SOUR:VOLT:PROT:LEV"):
        assert float(emulator(f"{command}?")) == 1050
        assert emulator(f"{command} 60") is None
        assert float(emulator(f"{command}?")) == 60
        assert emulator(f"{command} 1050") is None
        assert float(emulator(f"{command}?")) == 1050


def test_source_voltage_ilimit_level(emulator):
    for command in ("SOUR:VOLT:ILIM", ":SOUR:VOLT:ILIM", "SOUR:VOLT:ILIM:LEV", ":SOUR:VOLT:ILIM:LEV"):
        assert float(emulator(f"{command}?")) == 1.05e-4
        assert emulator(f"{command} 2.1E-5") is None
        assert float(emulator(f"{command}?")) == 2.1e-5
        assert emulator(f"{command} 1.05E-4") is None
        assert float(emulator(f"{command}?")) == 1.05e-4


def test_source_voltage_ilimit_level_tripped(emulator):
    for command in ("SOUR:VOLT:ILIM:TRIP", ":SOUR:VOLT:ILIM:TRIP", "SOUR:VOLT:ILIM:LEV:TRIP", ":SOUR:VOLT:ILIM:LEV:TRIP"):
        assert float(emulator(f"{command}?")) == 0


def test_source_current_vlimit_level(emulator):
    for command in ("SOUR:CURR:VLIM", ":SOUR:CURR:VLIM", "SOUR:CURR:VLIM:LEV", ":SOUR:CURR:VLIM:LEV"):
        assert float(emulator(f"{command}?")) == 2.1e-1
        assert emulator(f"{command} 0.0001") is None
        assert float(emulator(f"{command}?")) == 0.0001
        assert emulator(f"{command} 2.1E-1") is None
        assert float(emulator(f"{command}?")) == 2.1e-1


def test_source_current_vlimit_level_tripped(emulator):
    for command in ("SOUR:CURR:VLIM:TRIP", ":SOUR:CURR:VLIM:TRIP", "SOUR:CURR:VLIM:LEV:TRIP", ":SOUR:CURR:VLIM:LEV:TRIP"):
        assert float(emulator(f"{command}?")) == 0
