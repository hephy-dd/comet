import pytest

from comet.emulator.rohde_schwarz.rtp164 import RTP164Emulator


@pytest.fixture
def emulator():
    return RTP164Emulator()


def test_identify(emulator):
    assert emulator("*IDN?") == "Rohde&Schwarz,RTP,1320.5007k16/123456,5.50.2.0"


def test_error(emulator):
    assert emulator("SHRUBBERY?") is None
    assert emulator("SYST:ERR?") == "-113,\"Undefined header\""
