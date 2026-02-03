import pytest

from comet.emulator.rohde_schwarz.nge100 import NGE100Emulator


@pytest.fixture
def emulator():
    return NGE100Emulator()


def test_identify(emulator):
    assert emulator("*IDN?") == "Rohde&Schwarz,NGE103B,5601.3800k03/101863,1.54"


def test_channel_selection(emulator):

    for channel in range(3):
        emulator(f"INSTrument {channel+1}")
        assert emulator("INSTrument?") == f"{channel+1}"


def test_initialization(emulator):

    for channel in range(3):
        emulator(f"INSTrument {channel+1}")
        assert emulator("INSTrument?") == f"{channel+1}"
        assert emulator("OUTPut?") == "0"
        assert emulator("VOLTage?") == "0.0"
        assert emulator("CURRent?") == "0.0"


def test_enable_channel(emulator):

    for channel in range(3):
        emulator(f"INSTrument {channel+1}")
        emulator("OUTPut 1")
        assert emulator("OUTPut?") == "1"

    for channel in range(3):
        emulator(f"INSTrument {channel+1}")
        assert emulator("VOLT?") == "0.0"
        assert emulator("CURR?") == "0.0"

    for channel in range(3):
        emulator(f"INSTrument {channel+1}")
        emulator("OUTPut 0")
        assert emulator("OUTPut?") == "0"


def test_set_voltage(emulator):

    for channel in range(3):
        emulator(f"INSTrument {channel+1}")
        emulator("VOLTage 1.0")
        assert emulator("VOLTage?") == "1.0"


def test_set_current(emulator):

    for channel in range(3):
        emulator(f"INSTrument {channel+1}")
        emulator("CURRent 2.0")
        assert emulator("CURRent?") == "2.0"


def test_set_output(emulator):

    for channel in range(3):
        emulator(f"INSTrument {channel+1}")
        emulator("OUTPut 1")
        assert emulator("OUTPut?") == "1"

    for channel in range(3):
        emulator(f"INSTrument {channel+1}")
        emulator("OUTPut 0")
        assert emulator("OUTPut?") == "0"


def test_set_voltage_limit(emulator):
    """Voltage limited operation with high enough current limit"""
    expected_current = [1.0, 0.001, 0.0]

    for channel in range(3):
        emulator(f"INSTrument {channel+1}")
        emulator("CURR 1.0")
        emulator("OUTPut 1")
        emulator("VOLTage 1.0")

        assert emulator("OUTPut?") == "1"
        assert emulator("CURR?") == "1.0"
        assert emulator("VOLT?") == "1.0"

    for channel in range(3):
        emulator(f"INSTrument {channel+1}")
        assert emulator("MEAS:VOLT?") == "1.0"
        assert emulator("MEAS:CURR?") == f"{expected_current[channel]}"


def test_set_current_limit(emulator):
    """Voltage limited by current limit"""

    current_limit = 0.001
    current_expected = ["0.001", "0.001", "0.0"]
    voltages_expected = ["0.001", "1.0", "1.0"]

    for channel in range(3):
        emulator(f"INSTrument {channel+1}")
        emulator("VOLTage 1.0")
        emulator(f"CURR {current_limit}")
        emulator("OUTPut 1")

        assert emulator("OUTPut?") == "1"
        assert emulator("MEAS:CURR?") == current_expected[channel]
        assert emulator("MEAS:VOLT?") == voltages_expected[channel]
