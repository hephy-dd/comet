import pytest

from comet.emulator.hephy.environbox import EnvironBoxEmulator


@pytest.fixture
def emulator():
    emulator = EnvironBoxEmulator()
    emulator.options.update({
            "box_temperature.min": 24.0,
            "box_temperature.max": 24.0,
            "box_humidity.min": 40.0,
            "box_humidity.max": 40.0,
            "pt100_1.min": 21.5,
            "pt100_1.max": 21.5,
            "pt100_2.min": 22.5,
            "pt100_2.max": 22.5,
        })
    return emulator


def test_basic(emulator):
    assert emulator("*IDN?") == "EnvironBox, v2.0 (Emulator)"
    # assert emulator("*RST") == "OK"


def test_sensor_address(emulator):
    assert emulator("SET:NEW_ADDR 45") == "OK"
    assert emulator.sensor_address == 45
    assert emulator("SET:NEW_ADDR 40") == "OK"
    assert emulator.sensor_address == 40


def test_test_led(emulator):
    assert emulator("GET:TEST_LED ?") == "0"
    assert emulator("SET:TEST_LED ON") == "OK"
    assert emulator("GET:TEST_LED ?") == "1"
    assert emulator("SET:TEST_LED OFF") == "OK"
    assert emulator("GET:TEST_LED ?") == "0"


def test_discharge(emulator):
    assert emulator("SET:DISCHARGE AUTO") == "OK"
    assert emulator("SET:DISCHARGE ON") == "OK"
    assert emulator("SET:DISCHARGE OFF") == "OK"


def test_discharge_time(emulator):
    assert emulator("GET:DISCHARGE_TIME ?") == "1000"
    assert emulator("SET:DISCHARGE_TIME 42") == "OK"
    assert emulator("GET:DISCHARGE_TIME ?") == "42"
    assert emulator("SET:DISCHARGE_TIME 1000") == "OK"
    assert emulator("GET:DISCHARGE_TIME ?") == "1000"


def test_set_pt100_1(emulator):
    assert emulator("SET:PT100_1 OFF") == "OK"
    assert emulator("GET:PT100_1 ?") == "NAN"
    assert emulator("SET:PT100_1 ON") == "OK"
    assert emulator("GET:PT100_1 ?") == "21.50"


def test_set_pt100_2(emulator):
    assert emulator("SET:PT100_2 OFF") == "OK"
    assert emulator("GET:PT100_2 ?") == "NAN"
    assert emulator("SET:PT100_2 ON") == "OK"
    assert emulator("GET:PT100_2 ?") == "22.50"


def test_microscope_ctrl(emulator):
    assert emulator("GET:MICROSCOPE_CTRL ?") == "0"
    assert emulator("SET:MICROSCOPE_CTRL ON") == "OK"
    assert emulator("GET:MICROSCOPE_CTRL ?") == "1"
    assert emulator("SET:MICROSCOPE_CTRL OFF") == "OK"
    assert emulator("GET:MICROSCOPE_CTRL ?") == "0"


def test_microscope_light(emulator):
    assert emulator("GET:MICROSCOPE_LIGHT ?") == "0"
    assert emulator("SET:MICROSCOPE_LIGHT ON") == "OK"
    assert emulator("GET:MICROSCOPE_LIGHT ?") == "1"
    assert emulator("SET:MICROSCOPE_LIGHT OFF") == "OK"
    assert emulator("GET:MICROSCOPE_LIGHT ?") == "0"


def test_microscope_camera(emulator):
    assert emulator("GET:MICROSCOPE_CAM ?") == "0"
    assert emulator("SET:MICROSCOPE_CAM ON") == "OK"
    assert emulator("GET:MICROSCOPE_CAM ?") == "1"
    assert emulator("SET:MICROSCOPE_CAM OFF") == "OK"
    assert emulator("GET:MICROSCOPE_CAM ?") == "0"


def test_probecard_light(emulator):
    assert emulator("GET:PROBCARD_LIGHT ?") == "0"
    assert emulator("SET:PROBCARD_LIGHT ON") == "OK"
    assert emulator("GET:PROBCARD_LIGHT ?") == "1"
    assert emulator("SET:PROBCARD_LIGHT OFF") == "OK"
    assert emulator("GET:PROBCARD_LIGHT ?") == "0"


def test_probecard_camera(emulator):
    assert emulator("GET:PROBCARD_CAM ?") == "0"
    assert emulator("SET:PROBCARD_CAM ON") == "OK"
    assert emulator("GET:PROBCARD_CAM ?") == "1"
    assert emulator("SET:PROBCARD_CAM OFF") == "OK"
    assert emulator("GET:PROBCARD_CAM ?") == "0"


def test_laser_sensor(emulator):
    assert emulator("SET:LASER_SENSOR ON") == "OK"
    assert emulator("SET:LASER_SENSOR OFF") == "OK"


def test_box_light(emulator):
    assert emulator("GET:LIGHT ?") == "0"
    assert emulator("SET:BOX_LIGHT ON") == "OK"
    assert emulator("GET:LIGHT ?") == "1"
    assert emulator("SET:BOX_LIGHT OFF") == "OK"
    assert emulator("GET:LIGHT ?") == "0"


def test_door(emulator):
    assert emulator("GET:DOOR ?") == "0"


def test_laser(emulator):
    assert emulator("GET:LASER ?") == "0"


def test_relay_status(emulator):
    assert emulator("GET:RELAY_STATUS ?") == "0"


def test_env(emulator):
    assert emulator("GET:ENV ?") == "24.0,40.0,0,21.5"


def test_version(emulator):
    assert emulator("GET:VERSION ?") == "V2.0"


def test_pc_data(emulator):
    assert emulator("GET:PC_DATA ?") == "2,40.0,24.0,9.58,0,30.0,0.0,0.00,0.250000,0.010000,1.230000,0.00,0.00,1,22.400000,1.250000,3.560000,1,0.00,0,0.00,0.00,0,0,0,0,0,0,0,0,0,1000,0.0,21.50,NAN,0,1,1,0"
