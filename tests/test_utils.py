import re

import pytest

from comet import utils


def test_to_unit():
    assert utils.to_unit(42, "V") == 42.
    assert utils.to_unit(42, "mV") == 42.
    assert utils.to_unit("42V", "V") == 42.
    assert utils.to_unit("42mV", "V") == .042
    assert utils.to_unit("42 V", "mV") == 42e3
    assert utils.to_unit(utils.ureg("42 V"), "mV") == 42e3


def test_auto_scale():
    assert utils.auto_scale(1024) == (1e3, "k", "kilo")
    assert utils.auto_scale(256) == (1e0, "", "")
    assert utils.auto_scale(0) == (1e0, "", "")
    assert utils.auto_scale(0.042) == (1e-3, "m", "milli")
    assert utils.auto_scale(0.00042) == (1e-6, "u", "micro")


def test_combine_matrix():
    assert utils.combine_matrix("a", "b") == ["ab"]
    assert utils.combine_matrix("a", "b", "c") == ["abc"]
    assert utils.combine_matrix("a", "123") == ["a1", "a2", "a3"]
    assert utils.combine_matrix("ab", "123") == ["a1", "a2", "a3", "b1", "b2", "b3"]
    assert utils.combine_matrix("ab", "12", "XY") == ["a1X", "a1Y", "a2X", "a2Y", "b1X", "b1Y", "b2X", "b2Y"]
    assert utils.combine_matrix(["0x"], ("32", "64")) == ["0x32", "0x64"]
    assert utils.combine_matrix("ABC", "12") == ["A1", "A2", "B1", "B2", "C1", "C2"]
    assert utils.combine_matrix("12", "AB", ["08", "16"]) == ["1A08", "1A16", "1B08", "1B16", "2A08", "2A16", "2B08", "2B16"]


def test_inverse_square():
    with pytest.raises(ZeroDivisionError):
        utils.inverse_square(0)
    assert utils.inverse_square(1) == 1
    assert utils.inverse_square(2) == .25
    assert utils.inverse_square(8) == .015625


def test_t_dew():
    assert round(utils.t_dew(0, 50), 3) == -9.157
    assert round(utils.t_dew(20, 70), 3) == 14.364
    assert round(utils.t_dew(24, 40), 3) == 9.577
    assert round(utils.t_dew(60, 50), 3) == 45.766


def test_make_iso():
    assert re.match(r"^1970-01-01T0\d-00-00$", utils.make_iso(0))  # timezone
    assert re.match(r"^2015-02-09T0\d-39-49$", utils.make_iso(1423456789.8))  # timezone


def test_safe_filename():
    assert utils.safe_filename("Monty Python\"s!") == "Monty_Python_s_"
    assert utils.safe_filename("$2020-02-22 13:14:25") == "_2020-02-22_13_14_25"
