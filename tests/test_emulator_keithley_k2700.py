import pytest

from comet.emulator.keithley.k2700 import K2700Emulator


@pytest.fixture
def emulator():
    return K2700Emulator()


def test_basic(emulator):
    assert emulator("*IDN?") == "Keithley Inc., Model 2700, 43768438, v1.0 (Emulator)"
    assert emulator("*RST") is None
    assert emulator("*OPC?") == "1"
