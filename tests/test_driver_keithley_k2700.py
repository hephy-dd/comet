import pytest

from comet.driver.keithley import K2700


@pytest.fixture
def driver(resource):
    return K2700(resource)


def test_basic(driver, resource):
    resource.buffer = ["Keithley Model 2700", "1", "1"]
    assert driver.identify() == "Keithley Model 2700"
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


def test_measure_voltage(driver, resource):
    resource.buffer = ["+4.200000E-03", "-4.200000E-03"]
    assert driver.measure_voltage() == +4.2e-03
    assert driver.measure_voltage() == -4.2e-03
    assert resource.buffer == [":SENS:FUNC 'VOLT:DC'", ":FORM:ELEM READ", ":READ?", ":READ?"]


def test_measure_current(driver, resource):
    resource.buffer = ["+4.200000E-06", "-4.200000E-06"]
    assert driver.measure_current() == +4.2e-06
    assert driver.measure_current() == -4.2e-06
    assert resource.buffer == [":SENS:FUNC 'CURR:DC'", ":FORM:ELEM READ", ":READ?", ":READ?"]
