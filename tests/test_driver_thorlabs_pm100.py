import pytest

from comet.driver.thorlabs import PM100

from .test_driver import resource


@pytest.fixture
def driver(resource):
    return PM100(resource)


def test_basic(driver, resource):
    resource.buffer = ["Keithley Model 6517B", "1", "1"]
    assert driver.identify() == "Keithley Model 6517B"
    assert driver.reset() is None
    assert driver.clear() is None


def test_average_count(driver, resource):

    resource.buffer = ["100"]
    assert driver.average_count == 100

    resource.buffer = ["200"]
    assert driver.average_count == 200

    resource.buffer = ["1"]
    driver.average_count = 1

    assert resource.buffer == ["SENSe:AVERage:COUNt 1", "*OPC?"]


def test_wavelength(driver, resource):

    resource.buffer = ["1", "1"]

    driver.wavelength = driver.WAVELENGTH_UV
    driver.wavelength = driver.WAVELENGTH_IR

    assert resource.buffer == [
        "SENSe:CORRection:WAVelength 370",
        "*OPC?",
        "SENSe:CORRection:WAVelength 1060",
        "*OPC?",
    ]

    resource.buffer = ["370", "1060", "500"]
    assert driver.wavelength == driver.WAVELENGTH_UV
    assert driver.wavelength == driver.WAVELENGTH_IR
    assert driver.wavelength == 500

    with pytest.raises(ValueError):
        driver.wavelength = 340

    with pytest.raises(ValueError):
        driver.wavelength = 1200

    with pytest.raises(ValueError):
        driver.wavelength = -1


def test_measure_power(resource, driver):
    resource.buffer = ["1e-9\n"]

    assert driver.measure_power() == 1e-9
