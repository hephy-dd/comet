import unittest

from comet import filters

class FiltersTest(unittest.TestCase):

    def test_std_mean_filter(self):
        self.assertEqual(filters.std_mean_filter([0.250, 0.249], 0.005), True)
        self.assertEqual(filters.std_mean_filter([0.250, 0.249], 0.0005), False)
