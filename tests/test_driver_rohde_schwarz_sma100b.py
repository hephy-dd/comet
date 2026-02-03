import pytest

from comet.driver.rohde_schwarz import SMA100B


@pytest.fixture
def driver(resource):
    return SMA100B(resource)


def test_basic(driver, resource):
    resource.buffer = [
        "Rohde&Schwarz,SMA100B,1419.8888K02/120399,5.00.122.24 SP1",
        "1",
        "1",
    ]
    assert (
        driver.identify() == "Rohde&Schwarz,SMA100B,1419.8888K02/120399,5.00.122.24 SP1"
    )
    assert driver.reset() is None
    assert driver.clear() is None
    assert resource.buffer == ["*IDN?", "*RST", "*OPC?", "*CLS", "*OPC?"]


def test_errors(driver, resource):
    resource.buffer = ['0,"No error"']
    assert driver.next_error() is None
    assert resource.buffer == [":SYST:ERR:NEXT?"]

    resource.buffer = ['-113,"Undefined header"']
    err = driver.next_error()
    assert err.code == -113
    assert err.message == "Undefined header"
    assert resource.buffer == [":SYST:ERR:NEXT?"]


def test_frequency_mode(driver, resource):
    resource.buffer = ["FIXed"]
    assert driver.frequency_mode == "FIXed"
    assert resource.buffer == ["SOUR1:FREQ:MODE?"]

    resource.buffer = ["1"]
    driver.frequency_mode = "FIXed"
    assert resource.buffer == ["SOUR1:FREQ:MODE FIXed", "*OPC?"]


def test_frequency(driver, resource):
    resource.buffer = ["1000000000"]
    assert driver.frequency == 1e9
    assert resource.buffer == ["SOUR1:FREQuency:FIXed?"]

    resource.buffer = ["1"]
    driver.frequency = 1e10
    assert resource.buffer == ["SOUR1:FREQuency:FIXed 10000000000.0000", "*OPC?"]

    with pytest.raises(ValueError):
        driver.frequency = 1e11

    with pytest.raises(ValueError):
        driver.frequency = 1e3


def test_power(driver, resource):
    resource.buffer = ["-30"]
    assert driver.output_power == -30
    assert resource.buffer == ["SOUR1:POWer:POWer?"]

    resource.buffer = ["1"]
    driver.output_power = -20
    assert resource.buffer == ["SOUR1:POWer:POWer -20", "*OPC?"]


def test_output(driver, resource):
    resource.buffer = ["1"]
    assert driver.output is True
    assert resource.buffer == ["OUTPut:STATe?"]

    resource.buffer = ["1"]
    driver.output = True
    assert resource.buffer == ["OUTPut:STATe ON", "*OPC?"]
