import pytest
import re

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
    assert emulator.sensor_address[0] == 45
    assert emulator("SET:NEW_ADDR 40") == "OK"
    assert emulator.sensor_address[0] == 40


def test_ctrl(emulator):
    assert emulator("GET:CTRL ?") == "0"
    assert emulator("SET:CTRL ON") == "OK"
    assert emulator("GET:CTRL ?") == "1"
    assert emulator("SET:CTRL OFF") == "OK"
    assert emulator("GET:CTRL ?") == "0"


def test_ctrl_mode(emulator):
    assert emulator("GET:PC_DATA ?").split(",")[13] == "1"
    assert emulator("SET:CTRL_MODE DEW") == "OK"
    assert emulator("GET:PC_DATA ?").split(",")[13] == "2"
    assert emulator("SET:CTRL_MODE HUM") == "OK"
    assert emulator("GET:PC_DATA ?").split(",")[13] == "1"


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


def test_chip(emulator):
    assert emulator("GET:CHIP_ADDR 1") == "40"
    assert emulator("GET:CHIP_ADDR 2") == "41"
    assert emulator("GET:CHIP_NBR ?") == "2"


def test_sensor_readings(emulator):
    assert emulator("GET:TEMP ?") == "24.00"
    assert emulator("GET:HUM ?") == "40.00"
    assert emulator("GET:LUX ?") == "0.0"
    assert emulator("GET:FLOW_RATE ?") == "0.0"
    assert emulator("GET:VALVE_ON ?") == "1"
    assert emulator("GET:DOOR ?") == "0"
    assert emulator("GET:LASER ?") == "0"
    assert emulator("GET:LASER_POWER ?") == "1"


def test_env_ii_pcb(emulator):
    assert emulator("SET:ENV_II_PCB YES") == "OK"
    assert emulator("SET:ENV_II_PCB NO") == "OK"


def test_pid_door_stop(emulator):
    assert emulator("GET:PID_DOOR_STOP ?") == "1"
    assert emulator("SET:PID_DOOR_STOP ON") == "OK"
    assert emulator("GET:PID_DOOR_STOP ?") == "2"
    assert emulator("SET:PID_DOOR_STOP OFF") == "OK"
    assert emulator("GET:PID_DOOR_STOP ?") == "1"


def test_door_auto_light(emulator):
    assert emulator("GET:DOOR_AUTO_LIGHT ?") == "1"
    assert emulator("SET:DOOR_AUTO_LIGHT ON") == "OK"
    assert emulator("GET:DOOR_AUTO_LIGHT ?") == "2"
    assert emulator("SET:DOOR_AUTO_LIGHT OFF") == "OK"
    assert emulator("GET:DOOR_AUTO_LIGHT ?") == "1"


def test_relay_status(emulator):
    assert emulator("GET:RELAY_STATUS ?") == "0"


def test_env(emulator):
    assert emulator("GET:ENV ?") == "24.0,40.0,0,21.5"


def test_uptime(emulator):
    assert re.match(r'^\d\d,\d\d,\d\d,\d\d$', emulator("GET:UPTIME ?")) is not None


def test_version(emulator):
    assert emulator("GET:VERSION ?") == "V2.0"


def test_pc_data(emulator):
    assert emulator("GET:PC_DATA ?") == "2,40.0,24.0,9.58,0,30.0,9.2,49.00,0.250000,0.010000,1.230000,1700.00,10.00,1,22.400000,1.250000,3.560000,1,25.50,0,0.00,2.25,1,0,0,0,0,0,0,0,0,1000,0.0,21.50,NAN,100,0,1,0"
