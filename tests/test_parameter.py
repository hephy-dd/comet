import unittest

from comet.parameter import Parameter, ParameterBase


class ParameterTest(unittest.TestCase):

    def test_parameter_empty(self):
        p = Parameter()
        self.assertEqual(p.default, None)
        self.assertEqual(p.validate(.42), .42)

    def test_parameter_default(self):
        p = Parameter(42)
        self.assertEqual(p.default, 42)
        self.assertEqual(p.validate(.42), .42)

    def test_parameter_range(self):
        p = Parameter(42, type=float, minimum=1, maximum=42)
        self.assertEqual(p.default, 42)
        self.assertEqual(p.type, float)
        self.assertEqual(p.minimum, 1)
        self.assertEqual(p.maximum, 42)
        self.assertEqual(p.validate(4.2), 4.2)
