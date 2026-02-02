import pytest

from comet.driver.keithley import K2470


@pytest.fixture
def driver(resource):
    return K2470(resource)


def test_basic(driver, resource):
    resource.buffer = ["Keithley Model 2470", "1", "1"]
    assert driver.identify() == "Keithley Model 2470"
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

    resource.buffer = ["1"]
    driver.route_terminal = "front"
    assert resource.buffer == [":ROUT:TERM FRON", "*OPC?"]

    resource.buffer = ["1"]
    driver.route_terminal = "rear"
    assert resource.buffer == [":ROUT:TERM REAR", "*OPC?"]


def test_output(driver, resource):
    resource.buffer = ["0"]
    assert driver.output == driver.OUTPUT_OFF
    assert resource.buffer == [":OUTP:STAT?"]

    resource.buffer = ["1"]
    assert driver.output == driver.OUTPUT_ON
    assert resource.buffer == [":OUTP:STAT?"]

    resource.buffer = ["1"]
    driver.output = driver.OUTPUT_OFF
    assert resource.buffer == [":OUTP:STAT OFF", "*OPC?"]

    resource.buffer = ["1"]
    driver.output = driver.OUTPUT_ON
    assert resource.buffer == [":OUTP:STAT ON", "*OPC?"]


def test_function(driver, resource):
    resource.buffer = ["VOLT"]
    assert driver.function == driver.FUNCTION_VOLTAGE
    assert resource.buffer == [":SOUR:FUNC:MODE?"]

    resource.buffer = ["CURR"]
    assert driver.function == driver.FUNCTION_CURRENT
    assert resource.buffer == [":SOUR:FUNC:MODE?"]

    resource.buffer = ["1", "1"]
    driver.function = driver.FUNCTION_VOLTAGE
    assert resource.buffer == [":SOUR:FUNC:MODE VOLT", "*OPC?", ":SENS:FUNC 'CURR'", "*OPC?"]

    resource.buffer = ["1", "1"]
    driver.function = driver.FUNCTION_CURRENT
    assert resource.buffer == [":SOUR:FUNC:MODE CURR", "*OPC?", ":SENS:FUNC 'VOLT'", "*OPC?"]


def test_measure_voltage(driver, resource):
    resource.buffer = ["+4.200000E-03"]
    assert driver.measure_voltage() == 4.2e-03
    assert resource.buffer == [":MEAS:VOLT?"]


def test_measure_current(driver, resource):
    resource.buffer = ["+4.200000E-06"]
    assert driver.measure_current() == 4.2e-06
    assert resource.buffer == [":MEAS:CURR?"]
