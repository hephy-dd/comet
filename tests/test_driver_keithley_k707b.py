import pytest

from comet.driver.keithley import K707B


@pytest.fixture
def driver(resource):
    return K707B(resource)


def test_basic(driver, resource):
    resource.buffer = ["Keithley Model 707B", "1", "1"]
    assert driver.identify() == "Keithley Model 707B"
    assert driver.reset() is None
    assert driver.clear() is None
    assert resource.buffer == ["*IDN?", "*RST", "*OPC?", "*CLS", "*OPC?"]


def test_errors(driver, resource):
    resource.buffer = ["0\t\"Queue is Empty\"\t0\t0"]
    assert driver.next_error() is None
    assert resource.buffer == ["print(errorqueue.next())"]

    resource.buffer = ["42\t\"test error\"\t0\t0"]
    error = driver.next_error()
    assert error.code == 42
    assert error.message == "test error"


def test_channels(driver, resource):
    resource.buffer = [""]
    assert driver.closed_channels == []
    assert resource.buffer == ["print(channel.getclose(\"allslots\"))"]

    resource.buffer = ["1B01"]
    assert driver.closed_channels == ["1B01"]
    assert resource.buffer == ["print(channel.getclose(\"allslots\"))"]

    resource.buffer = ["1B01;1A02"]
    assert driver.closed_channels == ["1A02", "1B01"]
    assert resource.buffer == ["print(channel.getclose(\"allslots\"))"]

    resource.buffer = ["1"]
    assert driver.close_channels(["1A02"]) is None
    assert resource.buffer == ["channel.close(\"1A02\")", "*OPC?"]

    resource.buffer = ["1"]
    assert driver.close_channels(["1A02", "1B01"]) is None
    assert resource.buffer == ["channel.close(\"1A02,1B01\")", "*OPC?"]

    resource.buffer = ["1"]
    assert driver.open_channels(["1A02", "1B01"]) is None
    assert resource.buffer == ["channel.open(\"1A02,1B01\")", "*OPC?"]

    resource.buffer = ["1"]
    assert driver.open_all_channels() is None
    assert resource.buffer == ["channel.open(\"allslots\")", "*OPC?"]
