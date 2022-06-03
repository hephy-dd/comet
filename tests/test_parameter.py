import pytest

from comet.parameter import Parameter, ParameterBase


class TestParameter:

    def test_parameter_empty(self):
        p = Parameter()
        assert p.default is None
        assert p.validate(.42) == .42

    def test_parameter_default(self):
        p = Parameter(42)
        assert p.default == 42
        assert p.validate(.42) == .42

    def test_parameter_choice(self):
        p = Parameter("left", choice=["auto", "left", "right"])
        assert p.default == "left"
        assert p.choice == ["auto", "left", "right"]
        assert p.validate("auto") == "auto"
        with pytest.raises(ValueError):
            p.validate("down")

    def test_parameter_range(self):
        p = Parameter(42, type=float, minimum=1, maximum=42)
        assert p.default == 42
        assert p.type is float
        assert p.minimum == 1
        assert p.maximum == 42
        assert p.validate(4.2) == 4.2
        with pytest.raises(ValueError):
            p.validate(100.)
        with pytest.raises(ValueError):
            p.validate(0.)

    def test_parameter_unit(self):
        p = Parameter("25 mV", unit="V")
        assert p.default == .025
        assert p.type is None
        assert p.unit == "V"
        assert p.validate(.100) == .100
        assert p.validate("1kV") == 1000.
