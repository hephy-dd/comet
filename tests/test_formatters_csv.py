import unittest
from io import StringIO

from comet.formatters import CsvFormatter

class CsvFormatterTest(unittest.TestCase):

    def testCsvFormatter(self):
        with StringIO() as f:
            formatter = CsvFormatter(f, [])

if __name__ == '__main__':
    unittest.main()
