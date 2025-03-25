import pytest

from comet.emulator.keithley.k6510 import K6510Emulator


@pytest.fixture
def emulator():
    return K6510Emulator()


def test_basic(emulator):
    assert emulator("*IDN?") == "Keithley Inc., Model DAQ6510, 54313645, v1.0 (Emulator)"
    assert emulator("*RST") is None
    assert emulator("*OPC?") == "1"


def test_route_terminal(emulator):
    assert emulator(":ROUT:TERM?") == "FRON"


def test_measure_voltage(emulator):
    value = emulator(":MEAS:VOLT?")
    assert value is not None
    assert isinstance(float(value), float)


def test_measure_current(emulator):
    value = emulator(":MEAS:CURR?")
    assert value is not None
    assert isinstance(float(value), float)
