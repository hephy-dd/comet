import pytest

from comet.driver.photonic import F3000


@pytest.fixture
def driver(resource):
    return F3000(resource)


def test_identify(driver, resource):
    resource.buffer = ["F3000 v2.09, Emulator"]
    assert driver.identify() == "F3000 v2.09, Emulator"
    assert resource.buffer == ["V?"]


def test_read_brightness(driver, resource):
    resource.buffer = ["B50"]
    assert driver.brightness == 50
    assert resource.buffer == ["B?"]


def test_set_brightness(driver, resource):
    resource.buffer = [""]
    driver.brightness = 0
    assert resource.buffer == ["B0"]

    resource.buffer = [""]
    driver.brightness = 50
    assert resource.buffer == ["B50"]

    resource.buffer = [""]
    driver.brightness = 100
    assert resource.buffer == ["B100"]

    resource.buffer = [""]
    driver.brightness = 101
    assert resource.buffer == ["B100"]


def test_read_light_enabled(driver, resource):
    resource.buffer = ["S1"]
    assert driver.light_enabled == 0
    assert resource.buffer == ["S?"]

    resource.buffer = ["S0"]
    assert driver.light_enabled == 1
    assert resource.buffer == ["S?"]


def test_set_light_enabled(driver, resource):
    resource.buffer = [""]
    driver.light_enabled = True
    assert resource.buffer == ["S0"]

    resource.buffer = [""]
    driver.light_enabled = False
    assert resource.buffer == ["S1"]
