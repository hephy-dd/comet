import unittest

from comet.driver.hephy import EnvironBox
from comet.driver.hephy.environbox import parse_pc_data


class Resource:

    def __init__(self, buffer):
        self.buffer = buffer

    def write(self, message: str):
        self.buffer.append(message)
        return len(message)

    def query(self, message: str):
        self.buffer.append(message)
        return self.buffer.pop(0)


class BrandBoxTest(unittest.TestCase):

    def test_basic(self):
        buffer = []
        driver = EnvironBox(Resource(buffer))

        buffer.extend(['EnvironBox V1.0', 'OK', 'OK'])
        self.assertEqual(driver.identify(), 'EnvironBox V1.0')
        self.assertEqual(driver.reset(), None)
        self.assertEqual(driver.clear(), None)
        self.assertEqual(buffer, ['*IDN?', '*RST', '*CLS'])

    def test_errors(self):
        buffer = []
        driver = EnvironBox(Resource(buffer))

        self.assertEqual(driver.next_error(), None)

        buffer.append('Err99')
        driver.clear()  # performs query
        self.assertEqual(buffer.pop(0), '*CLS')
        error = driver.next_error()
        self.assertEqual(error.code, 99)
        self.assertEqual(error.message, 'Invalid command')
        self.assertEqual(driver.next_error(), None)

        buffer.append('Err999')
        driver.clear()  # performs query
        self.assertEqual(buffer.pop(0), '*CLS')
        error = driver.next_error()
        self.assertEqual(error.code, 999)
        self.assertEqual(error.message, 'Unknown command')
        self.assertEqual(driver.next_error(), None)

    def test_discharge(self):
        buffer = []
        driver = EnvironBox(Resource(buffer))

        self.assertEqual(driver.set_discharge(driver.DISCARGE_ON), None)
        self.assertEqual(driver.set_discharge(driver.DISCARGE_OFF), None)

    def test_environment(self):
        buffer = []
        driver = EnvironBox(Resource(buffer))

        buffer.append(format(30.1, '.1f'))
        self.assertEqual(driver.get_box_humidity(), 30.1)
        self.assertEqual(buffer.pop(0), 'GET:HUM ?')

        buffer.append(format(25.2, '.1f'))
        self.assertEqual(driver.get_box_temperature(), 25.2)
        self.assertEqual(buffer.pop(0), 'GET:TEMP ?')

        buffer.append(format(1, '.1f'))
        self.assertEqual(driver.get_box_lux(), 1)
        self.assertEqual(buffer.pop(0), 'GET:LUX ?')

        buffer.append(format(25.5, '.1f'))
        self.assertEqual(driver.get_chuck_temperature(), 25.5)
        self.assertEqual(buffer.pop(0), 'GET:PT100_1 ?')

        buffer.append(format(25.1, '.1f'))
        self.assertEqual(driver.get_chuck_block_temperature(), 25.1)
        self.assertEqual(buffer.pop(0), 'GET:PT100_2 ?')

    def test_box_door(self):
        buffer = []
        driver = EnvironBox(Resource(buffer))

        buffer.append('0')
        self.assertEqual(driver.get_box_door_state(), driver.BOX_DOOR_CLOSED)
        self.assertEqual(buffer.pop(0), 'GET:DOOR ?')

        buffer.append('1')
        self.assertEqual(driver.get_box_door_state(), driver.BOX_DOOR_OPEN)
        self.assertEqual(buffer.pop(0), 'GET:DOOR ?')

    def test_box_light(self):
        buffer = []
        driver = EnvironBox(Resource(buffer))

        buffer.append('0')
        self.assertEqual(driver.get_box_light(), driver.BOX_LIGHT_OFF)
        self.assertEqual(buffer.pop(0), 'GET:LIGHT ?')

        buffer.append('1')
        self.assertEqual(driver.get_box_light(), driver.BOX_LIGHT_ON)
        self.assertEqual(buffer.pop(0), 'GET:LIGHT ?')

        buffer.append('OK')
        self.assertEqual(driver.set_box_light(driver.BOX_LIGHT_ON), None)
        self.assertEqual(buffer.pop(0), 'SET:BOX_LIGHT ON')

        buffer.append('OK')
        self.assertEqual(driver.set_box_light(driver.BOX_LIGHT_OFF), None)
        self.assertEqual(buffer.pop(0), 'SET:BOX_LIGHT OFF')

    def test_parse_pc_data(self):
        response = "2,1.23,2.34,11.1,0,0,0,0,0,0,0,0,0,HUM,0,0,0,0,0,0,0,0,0,85,1,0,0,0,0,0,0,3.45,0.21,0.23,0.34,0,M,1,0"
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
        assert data["pid_control_mode"] == "HUM"
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
        assert data["pid_drop_mode"] == "M"
        assert data["pt100_1_enabled"] == True
        assert data["pt100_2_enabled"] == False
