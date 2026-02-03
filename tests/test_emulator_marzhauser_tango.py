import pytest

from comet.emulator.marzhauser.tango import TangoEmulator


@pytest.fixture
def emulator():
    emulator = TangoEmulator()
    emulator("!autostatus 0")
    return emulator


def test_basic(emulator):
    assert emulator("?version") == "TANGO-MINI3-EMULATOR, Version 1.00, Mar 11 2022, 13:51:01"
    assert emulator("?pos") == "0.000 0.000 0.000"
    assert emulator("?pos x") == "0.000"
    assert emulator("?pos y") == "0.000"
    assert emulator("?pos z") == "0.000"


def test_cal_rm(emulator):
    assert emulator("!cal") is None
    assert emulator("!cal x") is None
    assert emulator("!rm") is None
    assert emulator("!rm") is None


def test_move(emulator):
    assert emulator("!moa x 0.000") is None
    assert emulator("!mor x 0.000") is None


def test_autostatus(emulator):
    assert emulator("!autostatus 1") is None
    assert emulator("?autostatus") == "1"
    assert emulator("!autostatus 0") is None
    assert emulator("?autostatus") == "0"


def test_statusaxis(emulator):
    assert emulator("?statusaxis") == "@@@-.-"
    assert emulator("?statusaxis x") == "@"
    assert emulator("?statusaxis y") == "@"
    assert emulator("?statusaxis z") == "@"


def test_calst(emulator):
    assert emulator("?calst") == "3 3 3"
    assert emulator("?calst x") == "3"
    assert emulator("?calst y") == "3"
    assert emulator("?calst z") == "3"


def test_err(emulator):
    assert emulator("?err") == "0"
