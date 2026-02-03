import pytest

from comet.driver.hephy import EnvironBox
from comet.driver.hephy.environbox import parse_pc_data


@pytest.fixture
def driver(resource):
    return EnvironBox(resource)


def test_basic(driver, resource):
    resource.buffer = ["EnvironBox V1.0"]
    assert driver.identify() == "EnvironBox V1.0"
    assert driver.reset() is None  # no query!
    assert driver.clear() is None  # no query!
    assert resource.buffer == ["*IDN?"]


def test_errors(driver, resource):
    assert driver.next_error() is None

    resource.buffer = ["Err99"]
    driver.write("1")
    error = driver.next_error()
    assert error.code == 99
    assert error.message == "Invalid command"
    assert driver.next_error() is None

    resource.buffer = ["Err999"]
    driver.query("GET:FOO ?")
    error = driver.next_error()
    assert error.code == 999
    assert error.message == "Unknown command"
    assert driver.next_error() is None


def test_discharge(driver, resource):
    resource.buffer = ["OK"]
    assert driver.set_discharge(driver.DISCARGE_ON) is None
    assert resource.buffer == ["SET:DISCHARGE ON"]

    resource.buffer = ["OK"]
    assert driver.set_discharge(driver.DISCARGE_OFF) is None
    assert resource.buffer == ["SET:DISCHARGE OFF"]


def test_pid_control(driver, resource):
    resource.buffer = ["OK"]
    assert driver.set_pid_control(driver.PID_CONTROL_ON) is None
    assert resource.buffer == ["SET:CTRL ON"]

    resource.buffer = ["OK"]
    assert driver.set_pid_control(driver.PID_CONTROL_OFF) is None
    assert resource.buffer == ["SET:CTRL OFF"]

    resource.buffer = ["0"]
    assert driver.get_pid_control() == driver.PID_CONTROL_OFF
    assert resource.buffer == ["GET:CTRL ?"]

    resource.buffer = ["1"]
    assert driver.get_pid_control() == driver.PID_CONTROL_ON
    assert resource.buffer == ["GET:CTRL ?"]


def test_pid_control_mode(driver, resource):
    resource.buffer = ["OK"]
    assert driver.set_pid_control_mode(driver.PID_CONTROL_MODE_HUM) is None
    assert resource.buffer == ["SET:CTRL_MODE HUM"]

    resource.buffer = ["OK"]
    assert driver.set_pid_control_mode(driver.PID_CONTROL_MODE_DEW) is None
    assert resource.buffer == ["SET:CTRL_MODE DEW"]

    resource.buffer = ["0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"]
    assert driver.get_pid_control_mode() == driver.PID_CONTROL_MODE_HUM
    assert resource.buffer == ["GET:PC_DATA ?"]

    resource.buffer = ["0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"]
    assert driver.get_pid_control_mode() == driver.PID_CONTROL_MODE_DEW
    assert resource.buffer == ["GET:PC_DATA ?"]


def test_environment(driver, resource):
    resource.buffer = ["30.1"]
    assert driver.get_box_humidity() == 30.1
    assert resource.buffer == ["GET:HUM ?"]

    resource.buffer = ["25.2"]
    assert driver.get_box_temperature() == 25.2
    assert resource.buffer == ["GET:TEMP ?"]

    resource.buffer = ["1.0"]
    assert driver.get_box_lux() == 1
    assert resource.buffer == ["GET:LUX ?"]

    resource.buffer = ["25.5"]
    assert driver.get_chuck_temperature() == 25.5
    assert resource.buffer == ["GET:PT100_1 ?"]

    resource.buffer = ["25.1"]
    assert driver.get_chuck_block_temperature() == 25.1
    assert resource.buffer == ["GET:PT100_2 ?"]


def test_box_door(driver, resource):
    resource.buffer = ["0"]
    assert driver.get_box_door_state() == driver.BOX_DOOR_CLOSED
    assert resource.buffer == ["GET:DOOR ?"]

    resource.buffer = ["1"]
    assert driver.get_box_door_state() == driver.BOX_DOOR_OPEN
    assert resource.buffer == ["GET:DOOR ?"]


def test_box_light(driver, resource):
    resource.buffer = ["0"]
    assert driver.get_box_light() == driver.BOX_LIGHT_OFF
    assert resource.buffer == ["GET:LIGHT ?"]

    resource.buffer = ["1"]
    assert driver.get_box_light() == driver.BOX_LIGHT_ON
    assert resource.buffer == ["GET:LIGHT ?"]

    resource.buffer = ["OK"]
    assert driver.set_box_light(driver.BOX_LIGHT_ON) is None
    assert resource.buffer == ["SET:BOX_LIGHT ON"]

    resource.buffer = ["OK"]
    assert driver.set_box_light(driver.BOX_LIGHT_OFF) is None
    assert resource.buffer == ["SET:BOX_LIGHT OFF"]


def test_pid_door_stop(driver, resource):
    resource.buffer = ["OK"]
    assert driver.set_pid_door_stop(driver.PID_DOOR_STOP_ON) is None
    assert resource.buffer == ["SET:PID_DOOR_STOP ON"]

    resource.buffer = ["OK"]
    assert driver.set_pid_door_stop(driver.PID_DOOR_STOP_OFF) is None
    assert resource.buffer == ["SET:PID_DOOR_STOP OFF"]

    resource.buffer = ["1"]
    assert driver.get_pid_door_stop() == driver.PID_DOOR_STOP_OFF
    assert resource.buffer == ["GET:PID_DOOR_STOP ?"]

    resource.buffer = ["2"]
    assert driver.get_pid_door_stop() == driver.PID_DOOR_STOP_ON
    assert resource.buffer == ["GET:PID_DOOR_STOP ?"]


def test_door_auto_light(driver, resource):
    resource.buffer = ["OK"]
    assert driver.set_door_auto_light(driver.DOOR_AUTO_LIGHT_ON) is None
    assert resource.buffer == ["SET:DOOR_AUTO_LIGHT ON"]

    resource.buffer = ["OK"]
    assert driver.set_door_auto_light(driver.DOOR_AUTO_LIGHT_OFF) is None
    assert resource.buffer == ["SET:DOOR_AUTO_LIGHT OFF"]

    resource.buffer = ["1"]
    assert driver.get_door_auto_light() == driver.DOOR_AUTO_LIGHT_OFF
    assert resource.buffer == ["GET:DOOR_AUTO_LIGHT ?"]

    resource.buffer = ["2"]
    assert driver.get_door_auto_light() == driver.DOOR_AUTO_LIGHT_ON
    assert resource.buffer == ["GET:DOOR_AUTO_LIGHT ?"]


def test_uptime(driver, resource):
    resource.buffer = ["00,08,42,01"]
    assert driver.get_uptime() == 31321.0
    assert resource.buffer == ["GET:UPTIME ?"]


def test_parse_pc_data():
    response = "2,1.23,2.34,11.1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,85,1,0,0,0,0,0,0,3.45,0.21,0.23,0.34,0,1,1,0"
    data = parse_pc_data(response)
    assert data["sensor_count"] == 2
    assert data["box_humidity"] == 1.23
    assert data["box_temperature"] == 2.34
    assert data["box_dewpoint"] == 11.1
    assert not data["pid_status"]
    assert data["pid_setpoint"] == 0.
    assert data["pid_input"] == 0.
    assert data["pid_output"] == 0.
    assert data["pid_kp_1"] == 0.
    assert data["pid_ki_1"] == 0.
    assert data["pid_kd_1"] == 0.
    assert data["pid_min"] == 0
    assert data["pid_max"] == 0
    assert data["pid_control_mode"] == 1
    assert data["pid_kp_2"] == 0.
    assert data["pid_ki_2"] == 0.
    assert data["pid_kd_2"] == 0.
    assert data["parameter_set"] == 0
    assert data["parameter_threshold"] == 0.
    assert data["hum_flow_dir"] == 0
    assert data["pid_threshold"] == 0.
    assert data["vac_valve_current"] == 0.
    assert data["vac_valve_count"] == 0
    assert data["power_microscope_ctrl"]
    assert not data["power_box_light"]
    assert data["power_probecard_light"]
    assert not data["power_laser_sensor"]
    assert data["power_probecard_camera"]
    assert not data["power_microscope_camera"]
    assert data["power_microscope_light"]
    assert data["box_light"]
    assert not data["box_door"]
    assert not data["safety_alert"]
    assert not data["stepper_motor_control"]
    assert not data["air_flow_sensor"]
    assert not data["vac_flow_sensor"]
    assert not data["test_led"]
    assert data["discharge_time"] == 3.45
    assert data["box_lux"] == 0.21
    assert data["pt100_1"] == 0.23
    assert data["pt100_2"] == 0.34
    assert data["pid_sample_time"] == 0.
    assert data["pid_prop_mode"] == 1
    assert data["pt100_1_enabled"]
    assert not data["pt100_2_enabled"]
