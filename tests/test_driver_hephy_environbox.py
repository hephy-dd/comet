import unittest

from comet.driver.hephy import EnvironBox

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
