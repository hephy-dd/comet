import pytest

from comet.emulator.rohde_schwarz.rto6 import RTO6Emulator


@pytest.fixture
def emulator():
    return RTO6Emulator()


def test_identify(emulator):
    assert emulator("*IDN?") == "Rohde&Schwarz,RTO6,1802.0001k04/123456,5.50.2.0"
