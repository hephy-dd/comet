import pytest

from comet.emulator.keysight.e4980a import E4980AEmulator


@pytest.fixture
def emulator():
    return E4980AEmulator()


def test_basic(emulator):
    assert emulator("*IDN?") == "Keysight Inc., Model E4980A, v1.0 (Emulator)"
    assert emulator("*RST") is None
    assert emulator("*OPC?") == "1"


def test_correction_method(emulator):
    assert emulator(":CORR:METH?") == "SING"
    assert emulator(":CORR:METH MULT") is None
    assert emulator(":CORR:METH?") == "MULT"
    assert emulator(":CORR:METH SING") is None
    assert emulator(":CORR:METH?") == "SING"


def test_fetch_impedance_format(emulator):
    def get_types(result):
        tokens = result.split(",")
        assert len(tokens) == 3
        a, b, c = tokens
        float(a), float(b)
        return True
    for command in ("FETC", ":FETC", "FETCH:FORM", ":FETCH:FORM", "FETCH:IMP:FORM", ":FETCH:IMP:FORM"):
        assert get_types(emulator(f"{command}?"))


def test_bias_voltage_level(emulator):
    for command in ("BIAS:VOLT", ":BIAS:VOLT", "BIAS:VOLT:LEV", ":BIAS:VOLT:LEV"):
        assert float(emulator(f"{command}?")) == 0
        assert emulator(f"{command} 4.5E+0") is None
        assert float(emulator(f"{command}?")) == 4.5
        assert emulator(f"{command} 0") is None
        assert float(emulator(f"{command}?")) == 0


def test_bias_state(emulator):
    for command in ("BIAS:STAT", ":BIAS:STAT"):
        assert emulator(f"{command}?") == "0"
        assert emulator(f"{command} 1") is None
        assert emulator(f"{command}?") == "1"
        assert emulator(f"{command} 0") is None
        assert emulator(f"{command}?") == "0"
        assert emulator(f"{command} ON") is None
        assert emulator(f"{command}?") == "1"
        assert emulator(f"{command} OFF") is None
        assert emulator(f"{command}?") == "0"
