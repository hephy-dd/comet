import pytest

from comet.driver.keysight import E4980A

from .test_driver import resource, buffer


@pytest.fixture
def driver(resource):
    return E4980A(resource)


def test_basic(driver, resource):
    resource.buffer = ["Keysight Model E4980A", "1", "1"]
    assert driver.identify() == "Keysight Model E4980A"
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
