import os
import unittest

from comet.emulator.hephy.environbox import EnvironBoxEmulator


class EnvironBoxEmulatorTest(unittest.TestCase):

    def setUp(self):
        self.emulator = EnvironBoxEmulator()

    def test_basic(self):
        self.assertEqual(self.emulator('*IDN?'), 'EnvironBox, v1.0 (Emulator)')
        # self.assertEqual(self.emulator('*RST'), 'OK')

    def test_sensor_address(self):
        self.assertEqual(self.emulator('SET:NEW_ADDR 45'), 'OK')
        self.assertEqual(self.emulator.sensor_address, 45)
        self.assertEqual(self.emulator('SET:NEW_ADDR 40'), 'OK')
        self.assertEqual(self.emulator.sensor_address, 40)

    def test_test_led(self):
        self.assertEqual(self.emulator('GET:TEST_LED ?'), '0')
        self.assertEqual(self.emulator('SET:TEST_LED ON'), 'OK')
        self.assertEqual(self.emulator('GET:TEST_LED ?'), '1')
        self.assertEqual(self.emulator('SET:TEST_LED OFF'), 'OK')
        self.assertEqual(self.emulator('GET:TEST_LED ?'), '0')

    def test_discharge(self):
        self.assertEqual(self.emulator('SET:DISCHARGE AUTO'), 'OK')
        self.assertEqual(self.emulator('SET:DISCHARGE ON'), 'OK')
        self.assertEqual(self.emulator('SET:DISCHARGE OFF'), 'OK')

    def test_discharge_time(self):
        self.assertEqual(self.emulator('GET:DISCHARGE_TIME ?'), '1000')
        self.assertEqual(self.emulator('SET:DISCHARGE_TIME 42'), 'OK')
        self.assertEqual(self.emulator('GET:DISCHARGE_TIME ?'), '42')
        self.assertEqual(self.emulator('SET:DISCHARGE_TIME 1000'), 'OK')
        self.assertEqual(self.emulator('GET:DISCHARGE_TIME ?'), '1000')

    def test_set_pt100(self):
        self.assertEqual(self.emulator('SET:PT100_1 OFF'), 'OK')
        self.assertEqual(self.emulator('SET:PT100_1 ON'), 'OK')
        self.assertEqual(self.emulator('SET:PT100_2 OFF'), 'OK')
        self.assertEqual(self.emulator('SET:PT100_2 ON'), 'OK')

    def test_get_pt100(self):
        self.assertEqual(self.emulator('GET:PT100_1 ?'), '22.5')
        self.assertEqual(self.emulator('GET:PT100_2 ?'), 'nan')

    def test_microscope_ctrl(self):
        self.assertEqual(self.emulator('GET:MICROSCOPE_CTRL ?'), '0')
        self.assertEqual(self.emulator('SET:MICROSCOPE_CTRL ON'), 'OK')
        self.assertEqual(self.emulator('GET:MICROSCOPE_CTRL ?'), '1')
        self.assertEqual(self.emulator('SET:MICROSCOPE_CTRL OFF'), 'OK')
        self.assertEqual(self.emulator('GET:MICROSCOPE_CTRL ?'), '0')

    def test_microscope_light(self):
        self.assertEqual(self.emulator('GET:MICROSCOPE_LIGHT ?'), '0')
        self.assertEqual(self.emulator('SET:MICROSCOPE_LIGHT ON'), 'OK')
        self.assertEqual(self.emulator('GET:MICROSCOPE_LIGHT ?'), '1')
        self.assertEqual(self.emulator('SET:MICROSCOPE_LIGHT OFF'), 'OK')
        self.assertEqual(self.emulator('GET:MICROSCOPE_LIGHT ?'), '0')

    def test_microscope_camera(self):
        self.assertEqual(self.emulator('GET:MICROSCOPE_CAM ?'), '0')
        self.assertEqual(self.emulator('SET:MICROSCOPE_CAM ON'), 'OK')
        self.assertEqual(self.emulator('GET:MICROSCOPE_CAM ?'), '1')
        self.assertEqual(self.emulator('SET:MICROSCOPE_CAM OFF'), 'OK')
        self.assertEqual(self.emulator('GET:MICROSCOPE_CAM ?'), '0')

    def test_probecard_light(self):
        self.assertEqual(self.emulator('GET:PROBCARD_LIGHT ?'), '0')
        self.assertEqual(self.emulator('SET:PROBCARD_LIGHT ON'), 'OK')
        self.assertEqual(self.emulator('GET:PROBCARD_LIGHT ?'), '1')
        self.assertEqual(self.emulator('SET:PROBCARD_LIGHT OFF'), 'OK')
        self.assertEqual(self.emulator('GET:PROBCARD_LIGHT ?'), '0')

    def test_probecard_camera(self):
        self.assertEqual(self.emulator('GET:PROBCARD_CAM ?'), '0')
        self.assertEqual(self.emulator('SET:PROBCARD_CAM ON'), 'OK')
        self.assertEqual(self.emulator('GET:PROBCARD_CAM ?'), '1')
        self.assertEqual(self.emulator('SET:PROBCARD_CAM OFF'), 'OK')
        self.assertEqual(self.emulator('GET:PROBCARD_CAM ?'), '0')

    def test_laser_sensor(self):
        self.assertEqual(self.emulator('SET:LASER_SENSOR ON'), 'OK')
        self.assertEqual(self.emulator('SET:LASER_SENSOR OFF'), 'OK')

    def test_box_light(self):
        self.assertEqual(self.emulator('GET:LIGHT ?'), '0')
        self.assertEqual(self.emulator('SET:BOX_LIGHT ON'), 'OK')
        self.assertEqual(self.emulator('GET:LIGHT ?'), '1')
        self.assertEqual(self.emulator('SET:BOX_LIGHT OFF'), 'OK')
        self.assertEqual(self.emulator('GET:LIGHT ?'), '0')

    def test_door(self):
        self.assertEqual(self.emulator('GET:DOOR ?'), '0')

    def test_laser(self):
        self.assertEqual(self.emulator('GET:LASER ?'), '0')

    def test_relay_status(self):
        self.assertEqual(self.emulator('GET:RELAY_STATUS ?'), '0')

    def test_env(self):
        self.assertEqual(self.emulator('GET:ENV ?'), '24.0,40.0,0,22.5')

    def test_version(self):
        self.assertEqual(self.emulator('GET:VERSION ?'), 'V2.0')
