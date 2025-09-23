import pytest

from comet.emulator.keithley.k2410 import K2410Emulator
from comet.emulator.emulator import get_routes, emulator_factory


def test_emulator_factory():
    cls = emulator_factory("keithley.k2410")
    assert cls is K2410Emulator


def test_emulator_factory_not_found():
    with pytest.raises(ModuleNotFoundError):
        emulator_factory("shrubbery.ni")


def test_get_routes():
    routes = get_routes(K2410Emulator)
    route_patterns = {r.route: r for r in routes}
    assert r"\*IDN\?$" in route_patterns
    assert r"\*CLS$" in route_patterns
    assert r"\*CLS$" in route_patterns
