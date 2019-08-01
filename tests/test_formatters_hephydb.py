import unittest
import _env

from comet.formatters import HephyDbFormatter

class HephyDbFormatterTest(unittest.TestCase):

    def testHephyDbFormatter(self):
        formatter = HephyDbFormatter()

if __name__ == '__main__':
    unittest.main()
