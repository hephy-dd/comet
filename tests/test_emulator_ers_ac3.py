import pytest

from comet.emulator.ers.ac3 import AC3Emulator


@pytest.fixture
def emulator():
    return AC3Emulator()


def test_identify(emulator):
    assert emulator("RI") == "I1"


def test_get_temperature(emulator):
    assert emulator("RC") == "C+0250"


def test_get_target_temperature(emulator):
    assert emulator("RT") == "T+0250"


def test_set_target_temperature(emulator):
    assert emulator("ST+0300") == "OK"
    assert emulator.target_temperature == 30.0

    assert emulator("ST-0300") == "OK"
    assert emulator.target_temperature == -30.0


def test_get_mode(emulator):
    assert emulator("RO") == "O1"


def test_set_mode(emulator):
    assert emulator("SO2") == "OK"
    assert emulator.mode == 2


def test_get_dewpoint(emulator):
    assert emulator("RF") == "F-0200"


def test_get_dewpoint_control_status(emulator):
    assert emulator("RD") == "D1"


def test_set_dewpoint_control_status(emulator):
    assert emulator("SD0") == "OK"
    assert emulator.dewpoint_control_status == False

    assert emulator("SD1") == "OK"
    assert emulator.dewpoint_control_status == True


def test_get_hold_mode(emulator):
    assert emulator("RH") == "H11"


def test_set_hold_mode(emulator):
    assert emulator("SH1") == "OK"
    assert emulator.hold_mode == 11

    assert emulator("SH0") == "OK"
    assert emulator.hold_mode == 0


def test_get_control_status(emulator):
    assert emulator("RI") == "I1"


def test_get_error_code(emulator):
    assert emulator("RE") == "E000"
