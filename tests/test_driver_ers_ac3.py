import pytest
from comet.driver.ers import AC3


def test_identify(resource):
    """Test identify method."""
    resource.buffer = ["RI"]
    device = AC3(resource)
    assert device.identify() == "ERS AC3 Thermal Chuck"


def test_temperature_query(resource):
    """Test temperature query."""
    resource.buffer = ["C-600"]  # -60.0°C
    device = AC3(resource)
    assert device.temperature == -60.0
    assert resource.buffer[0] == "RC"

    resource.buffer = ["C+2450"]  # 245.0°C
    assert device.temperature == 245.0
    assert resource.buffer[0] == "RC"


def test_target_temperature_setter(resource):
    """Test target temperature setter."""
    device = AC3(resource)
    resource.buffer = ["OK"]
    device.target_temperature = 30.5
    assert resource.buffer[0] == "ST+0305"

    resource.buffer = ["OK"]
    device.target_temperature = -25.0
    assert resource.buffer[0] == "ST-0250"

    resource.buffer = ["OK"]
    device.target_temperature = 125.1
    assert resource.buffer[0] == "ST+1251"

    resource.buffer = ["OK"]
    device.target_temperature = -70.0
    assert resource.buffer[0] == "ST-0700"

    resource.buffer = ["OK"]
    device.target_temperature = 300.0
    assert resource.buffer[0] == "ST+3000"

    with pytest.raises(ValueError):
        device.target_temperature = -70.1

    resource.buffer = ["OK"]
    with pytest.raises(ValueError):
        device.target_temperature = 300.1


def test_operating_mode_getter(resource):

    device = AC3(resource)
    resource.buffer = ["O1"]  # Mode 1
    assert device.operating_mode == device.MODE_NORMAL

    resource.buffer = ["O2"]  # Mode 2
    assert device.operating_mode == device.MODE_STANDBY

    resource.buffer = ["O3"]  # Mode 3
    assert device.operating_mode == device.MODE_DEFROST

    resource.buffer = ["O4"]  # Mode 4
    assert device.operating_mode == device.MODE_PURGE


def test_operating_mode_setter(resource):
    device = AC3(resource)
    resource.buffer = ["OK"]
    device.operating_mode = device.MODE_NORMAL
    assert resource.buffer[0] == "SO1"

    resource.buffer = ["OK"]
    device.operating_mode = device.MODE_STANDBY
    assert resource.buffer[0] == "SO2"

    resource.buffer = ["OK"]
    device.operating_mode = device.MODE_DEFROST
    assert resource.buffer[0] == "SO3"

    resource.buffer = ["OK"]
    device.operating_mode = device.MODE_PURGE
    assert resource.buffer[0] == "SO4"

    with pytest.raises(ValueError):
        device.operating_mode = 5

    with pytest.raises(ValueError):
        device.operating_mode = 0

    with pytest.raises(ValueError):
        device.operating_mode = -1


def test_dewpoint_getter(resource):
    device = AC3(resource)
    resource.buffer = ["F-0585"]  # -58.5°C
    assert device.dewpoint == -58.5

    resource.buffer = ["F+2450"]  # 245.0°C
    assert device.dewpoint == 245.0


def test_dewpoint_control_getter(resource):
    device = AC3(resource)
    resource.buffer = ["D1"]  # Dewpoint control on
    assert device.dewpoint_control

    resource.buffer = ["D0"]  # Dewpoint control off
    assert not device.dewpoint_control


def test_dewpoint_control_setter(resource):
    device = AC3(resource)
    resource.buffer = ["OK"]
    device.dewpoint_control = True
    assert resource.buffer[0] == "SD1"

    resource.buffer = ["OK"]
    device.dewpoint_control = False
    assert resource.buffer[0] == "SD0"


def test_hold_mode_getter(resource):
    device = AC3(resource)
    resource.buffer = ["H10"]  # Hold mode on (but not yet reached)
    assert device.hold_mode

    resource.buffer = ["H11"]  # Hold mode on (and reached)
    assert device.hold_mode

    resource.buffer = ["H00"]  # Hold mode off
    assert not device.hold_mode


def test_hold_mode_setter(resource):
    device = AC3(resource)
    resource.buffer = ["OK"]
    device.hold_mode = True
    assert resource.buffer[0] == "SH1"

    resource.buffer = ["OK"]
    device.hold_mode = False
    assert resource.buffer[0] == "SH0"


def test_control_status(resource):
    device = AC3(resource)
    resource.buffer = ["I0"]
    assert device.control_status == device.STATUS_TEMPERATURE_REACHED
    assert resource.buffer == ["RI"]

    resource.buffer = ["I1"]
    assert device.control_status == device.STATUS_HEATING
    assert resource.buffer == ["RI"]

    resource.buffer = ["I2"]
    assert device.control_status == device.STATUS_COOLING
    assert resource.buffer == ["RI"]

    resource.buffer = ["I8"]
    assert device.control_status == device.STATUS_ERROR
    assert resource.buffer == ["RI"]


def test_next_error(resource):
    device = AC3(resource)
    resource.buffer = ["E000"]
    assert device.next_error() is None
    assert resource.buffer == ["RE"]

    resource.buffer = ["E001"]
    error = device.next_error()
    assert error.message == AC3.ERROR_MESSAGES[1]
    assert error.code == 1
    assert resource.buffer == ["RE"]
