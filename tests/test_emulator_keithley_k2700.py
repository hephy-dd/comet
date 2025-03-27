import pytest

from comet.emulator.keithley.k2700 import K2700Emulator


@pytest.fixture
def emulator():
    return K2700Emulator()


def test_basic(emulator):
    assert emulator("*IDN?") == "Keithley Inc., Model 2700, 43768438, v1.0 (Emulator)"
    assert emulator("*RST") is None
    assert emulator("*OPC?") == "1"


def test_format_elements(emulator):
    assert emulator(":FORM:ELEM?") == "READ,,UNIT,RNUM,TST,"
    assert emulator(":FORM:ELEM READ") is None
    assert emulator(":FORM:ELEM?") == "READ,,,,,"
    assert emulator(":FORM:ELEM CHAN, CHAN ,UNIT") is None
    assert emulator(":FORM:ELEM?")  == ",CHAN,UNIT,,,"
    assert emulator(":FORM:ELEM CHAN,TST,READ,UNIT,LIM,LIM,RNUM") is None
    assert emulator(":FORM:ELEM?") == "READ,CHAN,UNIT,RNUM,TST,LIM"


def test_reading(emulator):
    assert emulator(":FORM:ELEM READ") is None
    assert emulator(":READ?") is not None
