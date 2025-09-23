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


def test_channe_waveform_data_header(emulator):
    assert emulator(":CHAN1:DATA:HEAD?") == "-5.000000E-04,5.000000E-04,1000,1"
    assert emulator(":CHAN1:WAV1:DATA:HEAD?") == "-5.000000E-04,5.000000E-04,1000,1"


def test_channe_waveform_data_value(emulator):
    assert bytes(emulator(":CHAN1:DATA?"))[:6] == b"#44000"
    assert bytes(emulator(":CHAN2:DATA:VAL?"))[:6] == b"#44000"
    assert bytes(emulator(":CHAN1:WAV1:DATA?"))[:6] == b"#44000"
    assert bytes(emulator(":CHAN2:WAV1:DATA:VAL?"))[:6] == b"#44000"
