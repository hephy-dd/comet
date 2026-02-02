import pytest

from comet.driver.keithley import K2657A


@pytest.fixture
def driver(resource):
    return K2657A(resource)


def test_basic(driver, resource):
    resource.buffer = ['Keithley Model 2657A', '1', '1']
    assert driver.identify() == 'Keithley Model 2657A'
    assert driver.reset() is None
    assert driver.clear() is None
    assert resource.buffer == ['*IDN?', '*RST', '*OPC?', '*CLS', '*OPC?']


def test_errors(driver, resource):
    resource.buffer = ['0\t"no error"\t0\t0']
    assert driver.next_error() is None
    assert resource.buffer == ['print(errorqueue.next())']

    resource.buffer = ['42\t"test error"\t0\t0']
    error = driver.next_error()
    assert error.code == 42
    assert error.message == 'test error'


def test_output(driver, resource):
    resource.buffer = ['0']
    assert driver.output == driver.OUTPUT_OFF
    assert resource.buffer == ['print(smua.source.output)']

    resource.buffer = ['1']
    assert driver.output == driver.OUTPUT_ON
    assert resource.buffer == ['print(smua.source.output)']

    resource.buffer = ['1']
    driver.output = driver.OUTPUT_OFF
    assert resource.buffer == ['smua.source.output = 0', '*OPC?']

    resource.buffer = ['1']
    driver.output = driver.OUTPUT_ON
    assert resource.buffer == ['smua.source.output = 1', '*OPC?']


def test_function(driver, resource):
    resource.buffer = ['1']
    assert driver.function == driver.FUNCTION_VOLTAGE
    assert resource.buffer == ['print(smua.source.func)']

    resource.buffer = ['0']
    assert driver.function == driver.FUNCTION_CURRENT
    assert resource.buffer == ['print(smua.source.func)']

    resource.buffer = ['1']
    driver.function = driver.FUNCTION_VOLTAGE
    assert resource.buffer == ['smua.source.func = 1', '*OPC?']

    resource.buffer = ['1']
    driver.function = driver.FUNCTION_CURRENT
    assert resource.buffer == ['smua.source.func = 0', '*OPC?']


def test_measure_voltage(driver, resource):
    resource.buffer = ['+4.200000E-03']
    assert driver.measure_voltage() == 4.2e-03
    assert resource.buffer == ['print(smua.measure.v())']


def test_measure_current(driver, resource):
    resource.buffer = ['+4.200000E-06']
    assert driver.measure_current() == 4.2e-06
    assert resource.buffer == ['print(smua.measure.i())']
