import os
import unittest

from comet import utils

class UtilsTest(unittest.TestCase):

    def test_combine_matrix(self):
        self.assertEqual(utils.combine_matrix('a', 'b'), ['ab'])
        self.assertEqual(utils.combine_matrix('a', 'b', 'c'), ['abc'])
        self.assertEqual(utils.combine_matrix('a', '123'), ['a1', 'a2', 'a3'])
        self.assertEqual(utils.combine_matrix('ab', '123'), ['a1', 'a2', 'a3', 'b1', 'b2', 'b3'])
        self.assertEqual(utils.combine_matrix('ab', '12', 'XY'), ['a1X', 'a1Y', 'a2X', 'a2Y', 'b1X', 'b1Y', 'b2X', 'b2Y'])
        self.assertEqual(utils.combine_matrix(['0x'], ('32', '64')), ['0x32', '0x64'])
        self.assertEqual(utils.combine_matrix('ABC', '12'), ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'])
        self.assertEqual(utils.combine_matrix('12', 'AB', ['08', '16']), ['1A08', '1A16', '1B08', '1B16', '2A08', '2A16', '2B08', '2B16'])
