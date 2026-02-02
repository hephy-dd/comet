import pytest

from comet.driver.marzhauser import Tango


@pytest.fixture
def driver(resource):
    return Tango(resource)


def test_tango(driver, resource):
    resource.buffer = ["TANGO-MINI3"]
    assert driver.identify() == "TANGO-MINI3"
    assert resource.buffer == ["?version"]

    resource.buffer = []
    assert driver.calibrate() is None
    assert resource.buffer == ["!autostatus 0", "!cal"]

    resource.buffer = []
    assert driver.range_measure() is None
    assert resource.buffer == ["!autostatus 0", "!rm"]

    resource.buffer = ["3 3 3"]
    assert driver.is_calibrated
    assert resource.buffer == ["?calst"]

    resource.buffer = ["3 2"]
    assert not driver.is_calibrated
    assert resource.buffer == ["?calst"]

    resource.buffer = []
    assert driver.move_absolute([2.1, 4.2]) is None
    assert resource.buffer == ["!autostatus 0", "!moa 2.100 4.200"]

    resource.buffer = []
    assert driver.move_relative([0, 2.1]) is None
    assert resource.buffer == ["!autostatus 0", "!mor 0.000 2.100"]

    resource.buffer = []
    assert driver.abort() is None
    assert resource.buffer == ["!a"]

    resource.buffer = []
    assert driver.force_abort() is None
    assert resource.buffer == ["\x03"]

    resource.buffer = ["2.100 4.200"]
    assert driver.position == [2.1, 4.2]
    assert resource.buffer == ["?pos"]

    resource.buffer = ["@@M-."]
    assert driver.is_moving
    assert resource.buffer == ["?statusaxis"]

    resource.buffer = ["@@@-."]
    assert not driver.is_moving
    assert resource.buffer == ["?statusaxis"]

    resource.buffer = ["2"]
    assert driver.joystick_enabled
    assert resource.buffer == ["?joy"]

    resource.buffer = ["0"]
    assert not driver.joystick_enabled
    assert resource.buffer == ["?joy"]

    resource.buffer = []
    driver.joystick_enabled = True
    assert resource.buffer == ["!autostatus 0", "!joy 2"]


def test_tango_axes(driver, resource):
    resource.buffer = []
    assert driver[0].calibrate() is None
    assert resource.buffer == ["!autostatus 0", "!cal x"]

    resource.buffer = []
    assert driver[1].range_measure() is None
    assert resource.buffer == ["!autostatus 0", "!rm y"]

    resource.buffer = []
    assert driver[2].move_absolute(2.4) is None
    assert resource.buffer == ["!autostatus 0", "!moa z 2.400"]

    resource.buffer = []
    assert driver[0].move_relative(1.2) is None
    assert resource.buffer == ["!autostatus 0", "!mor x 1.200"]

    resource.buffer = ["4.200"]
    assert driver[1].position == 4.2
    assert resource.buffer == ["?pos y"]

    resource.buffer = ["M"]
    assert driver[2].is_moving
    assert resource.buffer == ["?statusaxis z"]

    resource.buffer = ["@"]
    assert not driver[0].is_moving
    assert resource.buffer == ["?statusaxis x"]
