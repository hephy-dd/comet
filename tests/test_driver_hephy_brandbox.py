import pytest

from comet.driver.hephy import BrandBox


@pytest.fixture
def driver(resource):
    return BrandBox(resource)


def test_basic(driver, resource):
    resource.buffer = ["BrandBox V1.0", "OK", "OK"]
    assert driver.identify() == "BrandBox V1.0"
    assert driver.reset() is None
    assert driver.clear() is None
    assert resource.buffer == ["*IDN?", "*RST", "*CLS"]


def test_errors(driver, resource):
    assert driver.next_error() is None

    resource.buffer = ["Err99"]
    driver.clear()
    error = driver.next_error()
    assert error.code == 99
    assert error.message == "Invalid command"
    assert driver.next_error() is None


def test_channels(driver, resource):
    resource.buffer = [""]
    assert driver.closed_channels == []
    assert resource.buffer == [":CLOS:STAT?"]

    resource.buffer = ["A1"]
    assert driver.closed_channels == ["A1"]
    assert resource.buffer == [":CLOS:STAT?"]

    resource.buffer = ["B1,B2,C2"]
    assert driver.closed_channels == ["B1", "B2", "C2"]
    assert resource.buffer == [":CLOS:STAT?"]

    resource.buffer = ["OK"]
    assert driver.close_channels(["B1"]) is None
    assert resource.buffer == [":CLOS B1"]

    resource.buffer = ["OK"]
    assert driver.close_channels(["A2", "B2", "C1"]) is None
    assert resource.buffer == [":CLOS A2,B2,C1"]

    resource.buffer = ["OK"]
    assert driver.open_channels(["B2"]) is None
    assert resource.buffer == [":OPEN B2"]

    resource.buffer.clear()
    resource.buffer = ["OK"]
    assert driver.open_channels(["B2", "A1"]) is None
    assert resource.buffer == [":OPEN A1,B2"]

    resource.buffer = ["OK"]
    assert driver.open_all_channels() is None
    assert resource.buffer == [":OPEN A1,A2,B1,B2,C1,C2"]
