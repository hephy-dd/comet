import pytest

from comet.driver.keithley import K6510


@pytest.fixture
def driver(resource):
    return K6510(resource)


def test_basic(driver, resource):
    resource.buffer = ["Keithley Model DAQ6510", "1", "1"]
    assert driver.identify() == "Keithley Model DAQ6510"
    assert driver.reset() is None
    assert driver.clear() is None
    assert resource.buffer == ["*IDN?", "*RST", "*OPC?", "*CLS", "*OPC?"]


def test_errors(driver, resource):
    resource.buffer = ["0,\"no error\""]
    assert driver.next_error() is None
    assert resource.buffer == [":SYST:ERR:NEXT?"]

    resource.buffer = ["42,\"test error\""]
    error = driver.next_error()
    assert error.code == 42
    assert error.message == "test error"


def test_route_terminal(driver, resource):
    resource.buffer = ["FRON"]
    assert driver.route_terminal == "front"
    assert resource.buffer == [":ROUT:TERM?"]

    resource.buffer = ["REAR"]
    assert driver.route_terminal == "rear"
    assert resource.buffer == [":ROUT:TERM?"]


def test_measure_voltage(driver, resource):
    resource.buffer = ["+4.200000E-03"]
    assert driver.measure_voltage() == 4.2e-03
    assert resource.buffer == [":MEAS:VOLT?"]


def test_measure_current(driver, resource):
    resource.buffer = ["+4.200000E-06"]
    assert driver.measure_current() == 4.2e-06
    assert resource.buffer == [":MEAS:CURR?"]
