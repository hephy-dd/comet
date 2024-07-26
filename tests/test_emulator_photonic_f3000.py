import pytest

from comet.emulator.photonic.f3000 import F3000Emulator


@pytest.fixture
def emulator():
    return F3000Emulator()


def test_identify(emulator):
    assert emulator("V?") == "F3000 v2.09, Emulator"


def test_read_brightness(emulator):
    assert emulator("B?") == "B50"


def test_set_brightness(emulator):
    assert emulator("B0") == None
    assert emulator("B?") == "B0"

    assert emulator("B50") == None
    assert emulator("B?") == "B50"

    assert emulator("B100") == None
    assert emulator("B?") == "B100"

    assert emulator("B101") == None
    assert emulator("B?") == "B100"


def test_read_light_enabled(emulator):
    assert emulator("S?") == "S1"


def test_set_light_enabled(emulator):
    assert emulator("S1") == None
    assert emulator("S?") == "S1"

    assert emulator("S0") == None
    assert emulator("S?") == "S0"
