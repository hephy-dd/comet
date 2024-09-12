import datetime
import re
from math import log
from typing import Iterable, Optional, Union

from pint import UnitRegistry, Quantity

__all__ = [
    "ureg",
    "to_unit",
    "auto_scale",
    "combine_matrix",
    "inverse_square",
    "t_dew",
    "make_iso",
    "safe_filename",
]

ureg = UnitRegistry()


def to_unit(value: Union[float, str, Quantity], unit: str) -> float:
    """Convert value or string representation with or without unit to another
    unit."""
    if isinstance(value, Quantity):
        return value.to(unit).m
    if isinstance(value, str):
        return ureg(value).to(unit).m
    return (ureg(unit) * value).to(unit).m


def auto_scale(value: float) -> tuple[float, str, str]:
    scales = [
        (1e24, "Y", "yotta"),
        (1e21, "Z", "zetta"),
        (1e18, "E", "exa"),
        (1e15, "P", "peta"),
        (1e12, "T", "tera"),
        (1e9, "G", "giga"),
        (1e6, "M", "mega"),
        (1e3, "k", "kilo"),
        (1e0, "", ""),
        (1e-3, "m", "milli"),
        (1e-6, "u", "micro"),
        (1e-9, "n", "nano"),
        (1e-12, "p", "pico"),
        (1e-15, "f", "femto"),
        (1e-18, "a", "atto"),
        (1e-21, "z", "zepto"),
        (1e-24, "y", "yocto"),
    ]
    for scale, prefix, name in scales:
        if abs(value) >= scale:
            return scale, prefix, name
    return 1e0, "", ""


def combine_matrix(a: Iterable, b: Iterable, *args: Iterable) -> list[str]:
    c = ["".join((x, y)) for x in a for y in b]
    if args:
        return combine_matrix(c, *args)
    return c


def inverse_square(value: float) -> float:
    """Return 1/x^2 for value."""
    return 1.0 / value**2


def t_dew(t: float, rh: float) -> float:
    """Calculating dew point.
    See https://en.wikipedia.org/wiki/Dew_point
    """
    a: float = 17.27
    b: float = 237.3
    m: float = log(rh / 100.) + ((a * t) / (b + t))
    return (b * m) / (a - m)


def make_iso(dt: Optional[Union[float, datetime.datetime]] = None) -> str:
    """Return filesystem safe ISO date time.

    >>> make_iso()
    '2019-12-24T12-21-42'

    >>> make_iso(1423456789.8)
    '2015-02-09T05-39-49'
    """
    if dt is None:
        dt = datetime.datetime.now()
    if not isinstance(dt, datetime.datetime):
        dt = datetime.datetime.fromtimestamp(dt)
    return dt.replace(microsecond=0).isoformat().replace(":", "-")


def safe_filename(filename: str) -> str:
    return re.sub(r"[^a-zA-Z0-9\_\/\.\-]+", "_", filename)
