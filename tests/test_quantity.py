import pytest

from comet.quantity import Quantity, convert


@pytest.mark.parametrize(
    ("value", "from_unit", "to_unit", "expected"),
    [
        (1, "V", "mV", 1000),
        (1000, "mV", "V", 1),
        (1, "kΩ", "Ω", 1000),
        (1, "Ohm", "Ω", 1),
        (1, "kOhm", "Ω", 1000),
    ],
)
def test_convert(value, from_unit, to_unit, expected):
    assert convert(value, from_unit, to_unit) == expected


def test_convert_incompatible_units():
    with pytest.raises(ValueError, match="Cannot convert"):
        convert(1, "V", "A")


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1V", Quantity(1, "V")),
        ("1.5V", Quantity(1.5, "V")),
        ("100mV", Quantity(100, "mV")),
        ("  2.5kΩ  ", Quantity(2.5, "kΩ")),
        ("1Ohm", Quantity(1, "Ω")),
        ("1kOhm", Quantity(1, "kΩ")),
    ],
)
def test_parse(text, expected):
    assert Quantity.parse(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "",
        "abc",
        "1",
        "1foo",
    ],
)
def test_parse_invalid_quantity(text):
    with pytest.raises(ValueError):
        Quantity.parse(text)


def test_equality_across_prefixes():
    assert Quantity(1, "V") == Quantity(1000, "mV")


def test_inequality():
    assert Quantity(1, "V") != Quantity(2, "V")
    assert Quantity(1, "V") != Quantity(1, "A")


def test_hash_matches_equality():
    assert hash(Quantity(1, "V")) == hash(Quantity(1000, "mV"))


def test_add():
    assert Quantity(1, "V") + Quantity(500, "mV") == Quantity(1.5, "V")


def test_subtract():
    assert Quantity(1, "V") - Quantity(500, "mV") == Quantity(0.5, "V")


def test_scalar_multiplication():
    quantity = Quantity(2, "V")

    assert quantity * 3 == Quantity(6, "V")
    assert 3 * quantity == Quantity(6, "V")


def test_scalar_division():
    assert Quantity(6, "V") / 3 == Quantity(2, "V")


def test_to():
    assert Quantity(1, "V").to("mV") == Quantity(1000, "mV")


@pytest.mark.parametrize("magnitude", [float("inf"), float("-inf"), float("nan")])
def test_rejects_non_finite_magnitude(magnitude):
    with pytest.raises(ValueError, match="finite"):
        Quantity(magnitude, "V")


def test_rejects_invalid_unit():
    with pytest.raises(ValueError, match="Unsupported unit"):
        Quantity(1, "potato")
