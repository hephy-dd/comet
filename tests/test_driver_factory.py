import warnings

import pytest

from comet.driver.factory import driver_factory
from comet.driver.keithley import K2410


def test_driver_factory():
    assert driver_factory("urn:comet:model:keithley:2410") is K2410
    assert driver_factory("urn:comet:model:keithley:k2410") is K2410

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert driver_factory("keithley.k2410") is K2410


def test_driver_factory_not_found():
    with pytest.raises(ValueError):
        driver_factory("urn:model:keithley:2410")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        with pytest.raises(ModuleNotFoundError):
            driver_factory("shrubbery.antioch3")

        with pytest.raises(ModuleNotFoundError):
            driver_factory("urn:comet:model:shrubbery:antioch3")
