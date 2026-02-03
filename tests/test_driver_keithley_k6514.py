import pytest

from comet.driver.keithley import K6514


@pytest.fixture
def driver(resource):
    return K6514(resource)


def test_basic(driver, resource):
    resource.buffer = ["Keithley Model 6514", "1", "1"]
    assert driver.identify() == "Keithley Model 6514"
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
