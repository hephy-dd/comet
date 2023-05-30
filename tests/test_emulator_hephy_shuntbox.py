import pytest

from comet.emulator.hephy.shuntbox import ShuntBoxEmulator


@pytest.fixture
def emulator():
    return ShuntBoxEmulator()


def test_basic(emulator):
    assert emulator("*IDN?") == "ShuntBox, v1.0 (Emulator)"
    assert int(emulator("GET:UP ?")) >= 0
    assert int(emulator("GET:RAM ?")) == 4200


def test_temp(emulator):
    assert len(emulator("GET:TEMP ALL").split(",")) == ShuntBoxEmulator.CHANNELS
    for index in range(ShuntBoxEmulator.CHANNELS):
        assert float(emulator(f"GET:TEMP {index}")) > 0


def test_set_rel(emulator):
    assert emulator("SET:REL_ON ALL") == "OK"
    assert emulator("SET:REL_OFF ALL") == "OK"
    for index in range(ShuntBoxEmulator.CHANNELS):
        assert emulator(f"SET:REL_ON {index}") == "OK"
        assert emulator(f"SET:REL_OFF {index}") == "OK"


def test_get_rel(emulator):
    assert emulator("GET:REL ALL") == ",".join(["0"] * (ShuntBoxEmulator.CHANNELS + 4))
    for index in range(ShuntBoxEmulator.CHANNELS):
        assert emulator(f"GET:REL {index}") == "0"


def test_error(emulator):
    assert emulator("FOO") == "Err99"
