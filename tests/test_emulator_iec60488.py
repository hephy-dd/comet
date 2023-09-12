import pytest

from comet.emulator.iec60488 import IEC60488Emulator


@pytest.fixture
def emulator():
    return IEC60488Emulator()


def test_basic(emulator):
    assert emulator("*IDN?") == "Generic IEC60488 Instrument (Emulator)"
    assert emulator("*ESR?") in ("0", "1")
    assert emulator("*ESE?") == "0"
    assert emulator("*ESE 1") is None
    assert emulator("*STB?") == "0"
    assert emulator("*OPC?") == "1"
    assert emulator("*OPC") is None
    assert emulator("*RST") is None
    assert emulator("*CLS") is None
    assert emulator("*TST?") == "0"
    assert emulator("*WAI") is None
