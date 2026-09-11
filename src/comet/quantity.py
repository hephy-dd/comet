from __future__ import annotations

from collections.abc import Collection
from dataclasses import dataclass
from math import isfinite

__all__ = ["Quantity", "convert"]

PREFIXES: dict[str, float] = {
    "": 1.0,
    "Q": 1e30,
    "R": 1e27,
    "Y": 1e24,
    "Z": 1e21,
    "E": 1e18,
    "P": 1e15,
    "T": 1e12,
    "G": 1e9,
    "M": 1e6,
    "k": 1e3,
    "d": 1e-1,
    "c": 1e-2,
    "m": 1e-3,
    "u": 1e-6,
    "µ": 1e-6,
    "n": 1e-9,
    "p": 1e-12,
    "f": 1e-15,
    "a": 1e-18,
    "z": 1e-21,
    "y": 1e-24,
    "r": 1e-27,
    "q": 1e-30,
}

BASE_UNITS: set[str] = {
    "V",  # volt
    "A",  # ampere
    "W",  # watt
    "F",  # farad
    "H",  # henry
    "Ω",  # ohm
    "m",  # metre
    "s",  # second
    "Hz",  # hertz
}

ALIASES: dict[str, str] = {
    "Ohm": "Ω",
    "ohm": "Ω",
}


def _match_suffix(value: str, choices: Collection[str]) -> str:
    matches = (choice for choice in choices if value.endswith(choice))
    return max(matches, key=len, default="")


def _canonicalize_unit(unit: str) -> str:
    for alias, canonical in ALIASES.items():
        if unit.endswith(alias):
            return unit.removesuffix(alias) + canonical
    return unit


def _unit(unit: str) -> tuple[float, str]:
    if not unit:
        raise ValueError("Unit cannot be empty")

    unit = _canonicalize_unit(unit)

    base = _match_suffix(unit, BASE_UNITS)
    if not base:
        raise ValueError(f"Unsupported unit: {unit!r}")

    prefix = unit.removesuffix(base)
    if prefix not in PREFIXES:
        raise ValueError(f"Unsupported unit: {unit!r}")

    return PREFIXES[prefix], base


def _scale(from_unit: str, to_unit: str) -> float:
    from_scale, from_base = _unit(from_unit)
    to_scale, to_base = _unit(to_unit)

    if from_base != to_base:
        raise ValueError(f"Cannot convert {from_unit!r} to {to_unit!r}")

    return from_scale / to_scale


def convert(value: float, from_unit: str, to_unit: str) -> float:
    return value * _scale(from_unit, to_unit)


@dataclass(frozen=True, slots=True)
class Quantity:
    magnitude: float
    unit: str

    def __post_init__(self) -> None:
        if not isfinite(self.magnitude):
            raise ValueError("magnitude must be finite")
        _unit(self.unit)

    def __str__(self) -> str:
        return f"{self.magnitude:g}{self.unit}"

    def __mul__(self, other: float) -> Quantity:
        return type(self)(self.magnitude * other, self.unit)

    def __rmul__(self, other: float) -> Quantity:
        return self * other

    def __truediv__(self, other: float) -> Quantity:
        return type(self)(self.magnitude / other, self.unit)

    def __add__(self, other: Quantity) -> Quantity:
        other = other.to(self.unit)
        return type(self)(self.magnitude + other.magnitude, self.unit)

    def __sub__(self, other: Quantity) -> Quantity:
        other = other.to(self.unit)
        return type(self)(self.magnitude - other.magnitude, self.unit)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Quantity):
            return NotImplemented
        return self._canonical() == other._canonical()

    def __hash__(self) -> int:
        return hash(self._canonical())

    def _canonical(self) -> tuple[str, float]:
        scale, base = _unit(self.unit)
        return base, self.magnitude * scale

    def to(self, unit: str) -> Quantity:
        return type(self)(
            self.magnitude * _scale(self.unit, unit),
            unit,
        )

    @classmethod
    def parse(cls, value: str) -> Quantity:
        s = _canonicalize_unit(value.strip())

        base = _match_suffix(s, BASE_UNITS)
        if not base:
            raise ValueError(f"Invalid quantity: {value!r}")

        magnitude = s.removesuffix(base)

        prefix = _match_suffix(magnitude, PREFIXES)
        if prefix:
            magnitude = magnitude.removesuffix(prefix)

        try:
            magnitude = float(magnitude)
        except ValueError:
            raise ValueError(f"Invalid magnitude: {magnitude!r}") from None

        return cls(magnitude, prefix + base)
