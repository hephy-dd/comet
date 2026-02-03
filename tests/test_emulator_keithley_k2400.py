import pytest

from comet.emulator.keithley.k2400 import K2400Emulator


@pytest.fixture
def emulator():
    return K2400Emulator()


def test_basic(emulator):
    assert emulator("*IDN?") == "Keithley Inc., Model 2400, 43768438, v1.0 (Emulator)"
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
        assert float(emulator(f"{command}?")) == 210
        assert emulator(f"{command} 60") is None
        assert float(emulator(f"{command}?")) == 60
        assert emulator(f"{command} 210") is None
        assert float(emulator(f"{command}?")) == 210


def test_sense_voltage_protection_level(emulator):
    for command in (":VOLT:PROT", ":SENS:VOLT:PROT", "SENS:VOLT:PROT:LEV", ":SENS:VOLT:PROT:LEV"):
        assert float(emulator(f"{command}?")) == 2.1e+1
        assert emulator(f"{command} 1.5E-3") is None
        assert float(emulator(f"{command}?")) == 1.5e-3
        assert emulator(f"{command} 2.10E+1") is None
        assert float(emulator(f"{command}?")) == 2.1e+1


def test_sense_voltage_protection_tripped(emulator):
    for command in (":VOLT:PROT:TRIP", ":SENS:VOLT:PROT:TRIP", "SENS:VOLT:PROT:TRIP"):
        assert float(emulator(f"{command}?")) == 0


def test_sense_current_protection_level(emulator):
    for command in (":CURR:PROT", ":SENS:CURR:PROT", "SENS:CURR:PROT:LEV", ":SENS:CURR:PROT:LEV"):
        assert float(emulator(f"{command}?")) == 1.05e-5
        assert emulator(f"{command} 0.0001") is None
        assert float(emulator(f"{command}?")) == 0.0001
        assert emulator(f"{command} 1.05E-5") is None
        assert float(emulator(f"{command}?")) == 1.05e-5


def test_sense_current_protection_tripped(emulator):
    for command in (":CURR:PROT:TRIP", ":SENS:CURR:PROT:TRIP", "SENS:CURR:PROT:TRIP", ):
        assert float(emulator(f"{command}?")) == 0


def test_sense_function(emulator):
    for command in (":FUNC", ":FUNC:ON", "SENS:FUNC:ON", ":SENS:FUNC:ON"):
        assert emulator(f"{command}?") == "\'CURR:DC\'"
        assert emulator(f"{command} \'CURR\'") is None
        assert emulator(f"{command}?") == "\'CURR:DC\'"  # TODO
