import unittest
from io import StringIO

from comet.formatters import HephyDbFormatter

class HephyDbFormatterTest(unittest.TestCase):

    def testHephyDbFormatter(self):
        with StringIO() as f:
            formatter = HephyDbFormatter(f)

if __name__ == '__main__':
    unittest.main()
