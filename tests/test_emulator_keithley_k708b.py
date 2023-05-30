import pytest

from comet.emulator.keithley.k708b import K708BEmulator


@pytest.fixture
def emulator():
    return K708BEmulator()


def test_constants(emulator):
    channels = [
        "1A01", "1A02", "1A03", "1A04", "1A05", "1A06", "1A07", "1A08",
        "1B01", "1B02", "1B03", "1B04", "1B05", "1B06", "1B07", "1B08",
        "1C01", "1C02", "1C03", "1C04", "1C05", "1C06", "1C07", "1C08",
        "1D01", "1D02", "1D03", "1D04", "1D05", "1D06", "1D07", "1D08",
        "1E01", "1E02", "1E03", "1E04", "1E05", "1E06", "1E07", "1E08",
        "1F01", "1F02", "1F03", "1F04", "1F05", "1F06", "1F07", "1F08",
        "1G01", "1G02", "1G03", "1G04", "1G05", "1G06", "1G07", "1G08",
        "1H01", "1H02", "1H03", "1H04", "1H05", "1H06", "1H07", "1H08",
    ]
    assert emulator.CHANNELS == channels


def test_basic(emulator):
    assert emulator("*IDN?") == "Keithley Inc., Model 708B, 43768438, v1.0 (Emulator)"
    assert emulator("*RST") is None
    assert emulator("*CLS") is None
    assert emulator("*OPC?") == "1"
