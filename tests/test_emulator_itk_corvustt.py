import pytest

from comet.emulator.itk.corvustt import CorvusTTEmulator


@pytest.fixture
def emulator():
    return CorvusTTEmulator()


def test_basic(emulator):
    assert emulator("identify") == "Corvus 0 0 0 0"
    assert emulator("version") == "1.0"
    assert emulator("getmacadr") == "00:00:00:00:00:00"
    assert emulator("getserialno") == "01011234"
    assert emulator("getoptions") == "3"
    assert int(emulator("getticks")) >= 0
    assert int(emulator("gt")) >= 0
    assert emulator("10 beep") is None
    # assert emulator("reset") is None
    assert emulator("status") == "0"
    assert emulator("st") == "0"


def test_position(emulator):
    assert emulator("pos") == "0.000000 0.000000 0.000000"
    assert emulator("1 2 3 move") is None
    assert emulator("pos") == "1.000000 2.000000 3.000000"
    assert emulator("2 0 -2 rmove") is None
    assert emulator("pos") == "3.000000 2.000000 1.000000"
    assert emulator("randmove") is None
    assert emulator("pos") != "3.000000 2.000000 1.000000"


def test_limits(emulator):
    # getlimit returns three lines
    assert emulator("getlimit") == ['0.000000 0.000000', '0.000000 1000000.000000', '100000.000000 25000.000000']
    assert emulator("1 2 3 4 5 6 setlimit") is None
    assert emulator("getlimit") == ['1.000000 2.000000', '3.000000 4.000000', '5.000000 6.000000']


def test_calibration(emulator):
    assert emulator("-1 getcaldone") == "3 3 3"
    assert emulator("1 getcaldone") == "3"
    assert emulator("2 getcaldone") == "3"
    assert emulator("3 getcaldone") == "3"

    assert emulator("-1 getaxis") == "1 1 1"
    assert emulator("1 getaxis") == "1"
    assert emulator("2 getaxis") == "1"
    assert emulator("3 getaxis") == "1"


def test_errors(emulator):
    assert emulator("geterror") == "0"
    assert emulator("ge") == "0"
    assert emulator("getmerror") == "0"
    assert emulator("gme") == "0"


def test_joystick(emulator):
    assert emulator("getjoystick") == "0"
    assert emulator("1 joystick") is None
    assert emulator("gj") == "1"
    assert emulator("0 j") is None
    assert emulator("getjoystick") == "0"


def test_units(emulator):
    assert emulator("-1 getunit") == "1 1 1 1"
    assert emulator("1 getunit") == "1"
    assert emulator("2 getunit") == "1"
    assert emulator("3 getunit") == "1"
    assert emulator("2 1 setunit") is None
    assert emulator("3 2 setunit") is None
    assert emulator("4 3 setunit") is None
    assert emulator("-1 getunit") == "2 3 4 1"
    assert emulator("1 getunit") == "2"
    assert emulator("2 getunit") == "3"
    assert emulator("3 getunit") == "4"


def test_calibrate_range_measure(emulator):
    assert emulator("-1 getcaldone") == "3 3 3"
    assert emulator("1 ncal") is None
    assert emulator("-1 getcaldone") == "1 3 3"
    assert emulator("2 ncal") is None
    assert emulator("-1 getcaldone") == "1 1 3"
    assert emulator("3 ncal") is None
    assert emulator("-1 getcaldone") == "1 1 1"
    assert emulator("1 nrm") is None
    assert emulator("-1 getcaldone") == "3 1 1"
    assert emulator("2 nrm") is None
    assert emulator("-1 getcaldone") == "3 3 1"
    assert emulator("3 nrm") is None
    assert emulator("-1 getcaldone") == "3 3 3"
