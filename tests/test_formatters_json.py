import unittest
from io import StringIO

from comet.formatters import JsonFormatter

class JsonFormatterTest(unittest.TestCase):

    def testJsonFormatter(self):
        with StringIO() as f:
            formatter = JsonFormatter(f)

if __name__ == '__main__':
    unittest.main()
