import unittest
import _env

from comet.formatters import CsvFormatter

class CsvFormatterTest(unittest.TestCase):

    def testCsvFormatter(self):
        formatter = CsvFormatter()

if __name__ == '__main__':
    unittest.main()
