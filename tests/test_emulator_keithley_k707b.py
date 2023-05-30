import pytest

from comet.emulator.keithley.k707b import K707BEmulator


@pytest.fixture
def emulator():
    return K707BEmulator()


def test_constants(emulator):
    channels = [
        "1A01", "1A02", "1A03", "1A04", "1A05", "1A06",
        "1A07", "1A08", "1A09", "1A10", "1A11", "1A12",
    ]
    assert emulator.CHANNELS == channels


def test_basic(emulator):
    assert emulator("*IDN?") == "Keithley Inc., Model 707B, 43768438, v1.0 (Emulator)"
    assert emulator("*RST") is None
    assert emulator("*CLS") is None
    assert emulator("*OPC?") == "1"
    assert emulator("print(errorqueue.count)") == "0"


def test_channels(emulator):
    assert emulator("print(channel.getclose(\"allslots\"))") == "nil"
    assert emulator("print(errorqueue.count)") == "0"
    assert emulator("channel.close(\"1A01,1A07\")") is None
    assert emulator("print(errorqueue.count)") == "0"
    assert emulator("print(channel.getclose(\"allslots\"))") == "1A01;1A07"
    assert emulator("print(errorqueue.count)") == "0"
    assert emulator("channel.open(\"allslots\")") is None
    assert emulator("print(errorqueue.count)") == "0"
    assert emulator("print(channel.getclose(\"allslots\"))") == "nil"
    assert emulator("print(errorqueue.count)") == "0"
