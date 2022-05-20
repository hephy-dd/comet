import unittest

from comet import utils

class UtilsTest(unittest.TestCase):

    def test_to_unit(self):
        self.assertEqual(utils.to_unit(42, "V"), 42.)
        self.assertEqual(utils.to_unit(42, "mV"), 42.)
        self.assertEqual(utils.to_unit("42V", "V"), 42.)
        self.assertEqual(utils.to_unit("42mV", "V"), .042)
        self.assertEqual(utils.to_unit("42 V", "mV"), 420.)

    def test_auto_scale(self):
        self.assertEqual(utils.auto_scale(1024), (1e3, 'k', 'kilo'))
        self.assertEqual(utils.auto_scale(256), (1e0, '', ''))
        self.assertEqual(utils.auto_scale(0), (1e0, '', ''))
        self.assertEqual(utils.auto_scale(0.042), (1e-3, 'm', 'milli'))
        self.assertEqual(utils.auto_scale(0.00042), (1e-6, 'u', 'micro'))

    def test_combine_matrix(self):
        self.assertEqual(utils.combine_matrix('a', 'b'), ['ab'])
        self.assertEqual(utils.combine_matrix('a', 'b', 'c'), ['abc'])
        self.assertEqual(utils.combine_matrix('a', '123'), ['a1', 'a2', 'a3'])
        self.assertEqual(utils.combine_matrix('ab', '123'), ['a1', 'a2', 'a3', 'b1', 'b2', 'b3'])
        self.assertEqual(utils.combine_matrix('ab', '12', 'XY'), ['a1X', 'a1Y', 'a2X', 'a2Y', 'b1X', 'b1Y', 'b2X', 'b2Y'])
        self.assertEqual(utils.combine_matrix(['0x'], ('32', '64')), ['0x32', '0x64'])
        self.assertEqual(utils.combine_matrix('ABC', '12'), ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'])
        self.assertEqual(utils.combine_matrix('12', 'AB', ['08', '16']), ['1A08', '1A16', '1B08', '1B16', '2A08', '2A16', '2B08', '2B16'])

    def test_inverse_square(self):
        with self.assertRaises(ZeroDivisionError):
            utils.inverse_square(0)
        self.assertEqual(utils.inverse_square(1), 1)
        self.assertEqual(utils.inverse_square(2), .25)
        self.assertEqual(utils.inverse_square(8), .015625)

    def test_make_iso(self):
        pass

    def test_safe_filename(self):
        self.assertEqual(utils.safe_filename('Monty Python\'s!'), 'Monty_Python_s_')
        self.assertEqual(utils.safe_filename('$2020-02-22 13:14:25'), '_2020-02-22_13_14_25')
