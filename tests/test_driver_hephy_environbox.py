import pytest

from comet.driver.hephy import EnvironBox
from comet.driver.hephy.environbox import parse_pc_data

from .test_driver import resource, buffer


@pytest.fixture
def driver(resource):
    return EnvironBox(resource)


def test_basic(driver, buffer):
    buffer.extend(['EnvironBox V1.0'])
    assert driver.identify() == 'EnvironBox V1.0'
    assert driver.reset() is None  # no query!
    assert driver.clear() is None  # no query!
    assert buffer == ['*IDN?']


def test_errors(driver, buffer):
    assert driver.next_error() is None

    buffer.append('Err99')
    driver.write('1')
    error = driver.next_error()
    assert error.code == 99
    assert error.message == 'Invalid command'
    assert driver.next_error() is None

    buffer.clear()
    buffer.append('Err999')
    driver.query('GET:FOO ?')
    error = driver.next_error()
    assert error.code == 999
    assert error.message == 'Unknown command'
    assert driver.next_error() is None


def test_discharge(driver):
    assert driver.set_discharge(driver.DISCARGE_ON) is None
    assert driver.set_discharge(driver.DISCARGE_OFF) is None


def test_environment(driver, buffer):
    buffer.append(format(30.1, '.1f'))
    assert driver.get_box_humidity() == 30.1
    assert buffer.pop(0) == 'GET:HUM ?'

    buffer.append(format(25.2, '.1f'))
    assert driver.get_box_temperature() == 25.2
    assert buffer.pop(0) == 'GET:TEMP ?'

    buffer.append(format(1, '.1f'))
    assert driver.get_box_lux() == 1
    assert buffer.pop(0) == 'GET:LUX ?'

    buffer.append(format(25.5, '.1f'))
    assert driver.get_chuck_temperature() == 25.5
    assert buffer.pop(0) == 'GET:PT100_1 ?'

    buffer.append(format(25.1, '.1f'))
    assert driver.get_chuck_block_temperature() == 25.1
    assert buffer.pop(0) == 'GET:PT100_2 ?'


def test_box_door(driver, buffer):
    buffer.append('0')
    assert driver.get_box_door_state() == driver.BOX_DOOR_CLOSED
    assert buffer.pop(0) == 'GET:DOOR ?'

    buffer.append('1')
    assert driver.get_box_door_state() == driver.BOX_DOOR_OPEN
    assert buffer.pop(0) == 'GET:DOOR ?'


def test_box_light(driver, buffer):
    buffer.append('0')
    assert driver.get_box_light() == driver.BOX_LIGHT_OFF
    assert buffer.pop(0) == 'GET:LIGHT ?'

    buffer.append('1')
    assert driver.get_box_light() == driver.BOX_LIGHT_ON
    assert buffer.pop(0) == 'GET:LIGHT ?'

    buffer.append('OK')
    assert driver.set_box_light(driver.BOX_LIGHT_ON) is None
    assert buffer.pop(0) == 'SET:BOX_LIGHT ON'

    buffer.append('OK')
    assert driver.set_box_light(driver.BOX_LIGHT_OFF) is None
    assert buffer.pop(0) == 'SET:BOX_LIGHT OFF'


def test_parse_pc_data():
    response = "2,1.23,2.34,11.1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,85,1,0,0,0,0,0,0,3.45,0.21,0.23,0.34,0,1,1,0"
    data = parse_pc_data(response)
    assert data["sensor_count"] == 2
    assert data["box_humidity"] == 1.23
    assert data["box_temperature"] == 2.34
    assert data["box_dewpoint"] == 11.1
    assert data["pid_status"] == False
    assert data["pid_setpoint"] == 0.
    assert data["pid_input"] == 0.
    assert data["pid_output"] == 0.
    assert data["pid_kp_1"] == 0.
    assert data["pid_ki_1"] == 0.
    assert data["pid_kd_1"] == 0.
    assert data["pid_min"] == 0
    assert data["pid_max"] == 0
    assert data["pid_control_mode"] == "1"
    assert data["pid_kp_2"] == 0.
    assert data["pid_ki_2"] == 0.
    assert data["pid_kd_2"] == 0.
    assert data["parameter_set"] == 0
    assert data["parameter_threshold"] == 0.
    assert data["hum_flow_dir"] == 0
    assert data["pid_threshold"] == 0.
    assert data["vac_valve_current"] == 0.
    assert data["vac_valve_count"] == 0
    assert data["power_microscope_ctrl"] == True
    assert data["power_box_light"] == False
    assert data["power_probecard_light"] == True
    assert data["power_laser_sensor"] == False
    assert data["power_probecard_camera"] == True
    assert data["power_microscope_camera"] == False
    assert data["power_microscope_light"] == True
    assert data["box_light"] == True
    assert data["box_door"] == False
    assert data["safety_alert"] == False
    assert data["stepper_motor_control"] == False
    assert data["air_flow_sensor"] == False
    assert data["vac_flow_sensor"] == False
    assert data["test_led"] == False
    assert data["discharge_time"] == 3.45
    assert data["box_lux"] == 0.21
    assert data["pt100_1"] == 0.23
    assert data["pt100_2"] == 0.34
    assert data["pid_sample_time"] == 0.
    assert data["pid_drop_mode"] == "1"
    assert data["pt100_1_enabled"] == True
    assert data["pt100_2_enabled"] == False
