import unittest

from comet.driver.hephy import BrandBox


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
        driver = BrandBox(Resource(buffer))

        buffer.extend(['BrandBox V1.0', 'OK', 'OK'])
        self.assertEqual(driver.identify(), 'BrandBox V1.0')
        self.assertEqual(driver.reset(), None)
        self.assertEqual(driver.clear(), None)
        self.assertEqual(buffer, ['*IDN?', '*RST', '*CLS'])

    def test_errors(self):
        buffer = []
        driver = BrandBox(Resource(buffer))

        self.assertEqual(driver.next_error(), None)

        buffer.append('Err99')
        driver.clear()
        error = driver.next_error()
        self.assertEqual(error.code, 99)
        self.assertEqual(error.message, 'Invalid command')
        self.assertEqual(driver.next_error(), None)

    def test_channels(self):
        buffer = []
        driver = BrandBox(Resource(buffer))

        buffer.append('')
        self.assertEqual(driver.closed_channels, [])
        self.assertEqual(buffer, [':CLOS:STAT?'])

        buffer.clear()
        buffer.append('A1')
        self.assertEqual(driver.closed_channels, ['A1'])
        self.assertEqual(buffer, [':CLOS:STAT?'])

        buffer.clear()
        buffer.append('B1,B2,C2')
        self.assertEqual(driver.closed_channels, ['B1', 'B2', 'C2'])
        self.assertEqual(buffer, [':CLOS:STAT?'])

        buffer.clear()
        buffer.append('OK')
        self.assertEqual(driver.close_channels(['B1']), None)
        self.assertEqual(buffer, [':CLOS B1'])

        buffer.clear()
        buffer.append('OK')
        self.assertEqual(driver.close_channels(['A2', 'B2', 'C1']), None)
        self.assertEqual(buffer, [':CLOS A2,B2,C1'])

        buffer.clear()
        buffer.append('OK')
        self.assertEqual(driver.open_channels(['B2']), None)
        self.assertEqual(buffer, [':OPEN B2'])

        buffer.clear()
        buffer.append('OK')
        self.assertEqual(driver.open_channels(['B2', 'A1']), None)
        self.assertEqual(buffer, [':OPEN A1,B2'])

        buffer.clear()
        buffer.append('OK')
        self.assertEqual(driver.open_all_channels(), None)
        self.assertEqual(buffer, [':OPEN A1,A2,B1,B2,C1,C2'])
