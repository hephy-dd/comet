import pytest

from comet.driver.keithley import K237

from .test_driver import resource, buffer


@pytest.fixture
def driver(resource):
    driver = K237(resource)
    driver.WRITE_DELAY = 0.
    return driver


def test_basic(driver, resource):
    resource.buffer = ["23714a"]
    assert driver.identify() == "Keithley Inc., Model 237, rev. 14a"
    assert driver.reset() is None
    assert driver.clear() is None
    assert resource.buffer == ["U0X"]


def test_errors(driver, resource):
    resource.buffer = ["ERS00000000000000000000000000"]
    assert driver.next_error() is None
    assert resource.buffer == ["U1X"]

    resource.buffer = ["ERS00100000000000000000000000"]
    error = driver.next_error()
    assert error.code == 2
    assert error.message == "IDDCO"


def test_output(driver, resource):
    resource.buffer = ["MSTG01,0,0K0M000,0N0R1T4,0,0,0V1Y0"]
    assert driver.output == driver.OUTPUT_OFF
    assert resource.buffer == ["U3X"]

    resource.buffer = ["MSTG01,0,0K0M000,0N1R1T4,0,0,0V1Y0"]
    assert driver.output == driver.OUTPUT_ON
    assert resource.buffer == ["U3X"]

    resource.buffer = []
    driver.output = driver.OUTPUT_OFF
    assert resource.buffer == ["N0X"]

    resource.buffer = []
    driver.output = driver.OUTPUT_ON
    assert resource.buffer == ["N1X"]


def test_function(driver, resource):
    resource.buffer = ["IMPL,08F0,0O0P0S0W1Z0"]
    assert driver.function == driver.FUNCTION_VOLTAGE
    assert resource.buffer == ["U4X"]

    resource.buffer = ["IMPL,08F1,0O0P0S0W1Z0"]
    assert driver.function == driver.FUNCTION_CURRENT
    assert resource.buffer == ["U4X"]

    resource.buffer = []
    driver.function = driver.FUNCTION_VOLTAGE
    assert resource.buffer == ["F0,0X"]

    resource.buffer = []
    driver.function = driver.FUNCTION_CURRENT
    assert resource.buffer == ["F1,0X"]


def test_voltage(driver, resource):
    for level in (-2.5, 0., +2.5):
        resource.buffer = [format(level, ".3E")]
        assert driver.voltage_level == level
        assert resource.buffer == ["G1,2,0X", "X"]

    for level in (-2.5, 0., +2.5):
        resource.buffer = []
        driver.voltage_level = level
        assert resource.buffer == [f"B{level:.3E},,X"]


def test_current(driver, resource):
    for level in (-2.5e-06, 0., +2.5e-06):
        resource.buffer = [format(level, ".3E")]
        assert driver.current_level == level
        assert resource.buffer == ["G1,2,0X", "X"]

    for level in (-2.5e-06, 0., +2.5e-06):
        resource.buffer = []
        driver.current_level = level
        assert resource.buffer == [f"B{level:.3E},,X"]


def test_compliance_tripped(driver, resource):
    resource.buffer = ["OS000"]
    assert driver.compliance_tripped
    assert resource.buffer == ["G1,0,0X", "X"]

    resource.buffer = ["OP000"]
    assert not driver.compliance_tripped
    assert resource.buffer == ["G1,0,0X", "X"]


def test_measure_voltage(driver, resource):
    resource.buffer = ["+4.200E-03"]
    assert driver.measure_voltage() == 4.2e-03
    assert resource.buffer == ["G4,2,0X", "X"]


def test_measure_voltage(driver, resource):
    resource.buffer = ["+4.200E-06"]
    assert driver.measure_current() == 4.2e-06
    assert resource.buffer == ["G4,2,0X", "X"]
