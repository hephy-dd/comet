import pytest

from comet.emulator.rohde_schwarz.sma100b import SMA100BEmulator


@pytest.fixture
def emulator():
    return SMA100BEmulator()


def test_basic(emulator):
    assert (
        emulator("*IDN?") == "Rohde&Schwarz,SMA100B,1419.8888K02/120399,5.00.122.24 SP1"
    )
    assert emulator("*RST") is None
    assert emulator("*CLS") is None

    assert emulator(":SYST:ERR:NEXT?") == '0, "no error"'


def test_frequency_mode(emulator):
    assert emulator("SOUR1:FREQ:MODE?") == "FIXed"
    assert emulator("SOUR1:FREQ:MODE FIXed") is None
    assert emulator("SOUR1:FREQ:MODE?") == "FIXed"

    assert emulator("SOUR1:FREQ:MODE SWEep") is None
    assert emulator("SOUR1:FREQ:MODE?") == "SWEep"


def test_frequency(emulator):
    assert float(emulator("SOUR1:FREQuency:FIXed?")) == 1e10
    assert emulator("SOUR1:FREQuency:FIXed 1e9") is None
    assert float(emulator("SOUR1:FREQuency:FIXed?")) == 1e9

    assert emulator("SOUR1:FREQuency:FIXed 1e4") is None
    assert float(emulator("SOUR1:FREQuency:FIXed?")) == 1e4


def test_frequency_error(emulator):
    assert emulator("SOUR1:FREQuency:FIXed 1e11") is None
    assert emulator("SYST:ERR:NEXT?") == '222, "Parameter Data Out of Range"'
    assert emulator("SYST:ERR:NEXT?") == '0, "no error"'

    assert emulator("SOUR1:FREQuency:FIXed 1e3") is None
    assert emulator("SYSTem:ERR:NEXT?") == '222, "Parameter Data Out of Range"'
    assert emulator("SYST:ERR:NEXT?") == '0, "no error"'


def test_power(emulator):
    assert float(emulator("SOUR1:POWer:POWer?")) == 0
    assert emulator("SOUR1:POWer:POWer 10") is None
    assert float(emulator("SOUR1:POWer:POWer?")) == 10

    assert emulator("SOUR1:POWer:POWer 20") is None
    assert float(emulator("SOUR1:POWer:POWer?")) == 20


def test_power_error(emulator):
    assert emulator("SOUR1:POWer:POWer 41") is None
    assert emulator("SYST:ERR:NEXT?") == '222, "Parameter Data Out of Range"'
    assert emulator("SYST:ERR:NEXT?") == '0, "no error"'

    assert emulator("SOUR1:POWer:POWer -146") is None
    assert emulator("SYSTem:ERR:NEXT?") == '222, "Parameter Data Out of Range"'
    assert emulator("SYST:ERR:NEXT?") == '0, "no error"'


def test_output(emulator):
    assert emulator("OUTPut:STAT?") == "0"
    assert emulator("OUTPut:STAT ON") is None
    assert emulator("OUTPut:STAT?") == "1"

    assert emulator("OUTPut:STAT OFF") is None
    assert emulator("OUTPut:STAT?") == "0"
