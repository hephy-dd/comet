import re
import warnings

import pytest

from comet.utils import (
    auto_scale,
    combine_matrix,
    inverse_square,
    make_iso,
    parse_model_urn,
    safe_filename,
    t_dew,
)


def test_auto_scale():
    assert auto_scale(1024) == (1e3, "k", "kilo")
    assert auto_scale(256) == (1e0, "", "")
    assert auto_scale(0) == (1e0, "", "")
    assert auto_scale(0.042) == (1e-3, "m", "milli")
    assert auto_scale(0.00042) == (1e-6, "u", "micro")


def test_combine_matrix():
    assert combine_matrix("a", "b") == ["ab"]
    assert combine_matrix("a", "b", "c") == ["abc"]
    assert combine_matrix("a", "123") == ["a1", "a2", "a3"]
    assert combine_matrix("ab", "123") == ["a1", "a2", "a3", "b1", "b2", "b3"]
    assert combine_matrix("ab", "12", "XY") == [
        "a1X",
        "a1Y",
        "a2X",
        "a2Y",
        "b1X",
        "b1Y",
        "b2X",
        "b2Y",
    ]
    assert combine_matrix(["0x"], ("32", "64")) == ["0x32", "0x64"]
    assert combine_matrix("ABC", "12") == ["A1", "A2", "B1", "B2", "C1", "C2"]
    assert combine_matrix("12", "AB", ["08", "16"]) == [
        "1A08",
        "1A16",
        "1B08",
        "1B16",
        "2A08",
        "2A16",
        "2B08",
        "2B16",
    ]


def test_inverse_square():
    with pytest.raises(ZeroDivisionError):
        inverse_square(0)
    assert inverse_square(1) == 1
    assert inverse_square(2) == 0.25
    assert inverse_square(8) == 0.015625


def test_t_dew():
    assert round(t_dew(0, 50), 3) == -9.157
    assert round(t_dew(20, 70), 3) == 14.364
    assert round(t_dew(24, 40), 3) == 9.577
    assert round(t_dew(60, 50), 3) == 45.766


def test_make_iso():
    assert re.match(r"^1970-01-01T0\d-00-00$", make_iso(0))  # timezone
    assert re.match(r"^2015-02-09T0\d-39-49$", make_iso(1423456789.8))  # timezone


def test_safe_filename():
    assert safe_filename('Monty Python"s!') == "Monty_Python_s_"
    assert safe_filename("$2020-02-22 13:14:25") == "_2020-02-22_13_14_25"


def test_parse_model_urn():
    assert parse_model_urn("urn:comet:model:shrubbery:3") == "shrubbery.s3"
    assert parse_model_urn("urn:comet:model:shrubbery:ni") == "shrubbery.ni"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert parse_model_urn("shrubbery.3") == "shrubbery.s3"
        assert parse_model_urn("shrubbery.ni") == "shrubbery.ni"
