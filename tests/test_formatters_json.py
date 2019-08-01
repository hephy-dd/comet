import unittest
import _env

from comet.formatters import JsonFormatter

class JsonFormatterTest(unittest.TestCase):

    def testJsonFormatter(self):
        formatter = JsonFormatter()

if __name__ == '__main__':
    unittest.main()
