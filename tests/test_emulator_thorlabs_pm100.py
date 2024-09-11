import pytest

from comet.emulator.thorlabs.pm100 import PM100Emulator


@pytest.fixture
def emulator():
    return PM100Emulator()


def test_basic(emulator):
    assert emulator("*IDN?") == "Thorlabs,PM100USB,P2004525,1.4.0"
    assert emulator("*CLS") is None
    assert emulator("*RST") is None


def test_average_count(emulator):
    assert emulator("SENSe:AVERage:COUNt?") == "100"
    assert emulator("SENSe:AVERage:COUNt 200") is None
    assert emulator("SENSe:AVERage:COUNt?") == "200"


def test_wavelength(emulator):
    assert emulator("SENSe:CORRection:WAVelength?") == "370"
    assert emulator("SENSe:CORRection:WAVelength 1060") is None
    assert emulator("SENSe:CORRection:WAVelength?") == "1060"


def test_measure_power(emulator):

    power = float(emulator("MEASure:SCALar:POWer"))
    assert power >= 1e-9
    assert power <= 2e-9
