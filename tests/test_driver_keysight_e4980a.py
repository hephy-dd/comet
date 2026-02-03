import pytest

from comet.driver.keysight import E4980A


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


def test_function(driver, resource):
    resource.buffer = ["CPRP"]
    assert driver.function == driver.FUNCTION_CPRP
    assert resource.buffer == [":FUNC:IMP:TYPE?"]

    resource.buffer = ["1"]
    driver.function = driver.FUNCTION_CPD
    assert resource.buffer == [":FUNC:IMP:TYPE CPD", "*OPC?"]


def test_amplitude(driver, resource):
    resource.buffer = ["1.000000E+00"]
    assert driver.amplitude == 1.0
    assert resource.buffer == [":VOLT:LEV?"]

    resource.buffer = ["1"]
    driver.amplitude = 2.0
    assert resource.buffer == [":VOLT:LEV 2.000000E+00", "*OPC?"]


def test_frequency(driver, resource):
    resource.buffer = ["1.000000E+03"]
    assert driver.frequency == 1000.0
    assert resource.buffer == [":FREQ:CW?"]

    resource.buffer = ["1"]
    driver.frequency = 200.0
    assert resource.buffer == [":FREQ:CW 2.000000E+02", "*OPC?"]


# TODO
def test_measurement_time(driver, resource):
    resource.buffer = ["1"]
    driver.set_measurement_time("MED")
    assert resource.buffer == [":APER MED", "*OPC?"]


def test_correction_length(driver, resource):
    resource.buffer = ["1"]
    assert driver.correction_length == 1
    assert resource.buffer == [":CORR:LENG?"]

    resource.buffer = ["1"]
    driver.correction_length = 2
    assert resource.buffer == [":CORR:LENG 2", "*OPC?"]


def test_measure_impedance(driver, resource):
    resource.buffer = ["1.002000E+00,2.004000E-03"]
    assert driver.measure_impedance() == (1.002e+0, 2.004e-3)
    assert resource.buffer == [":FETC:IMP:FORM?"]
