import pytest

from comet.driver.itk.corvustt import CorvusTT


@pytest.fixture
def driver(resource) -> CorvusTT:
    return CorvusTT(resource)


def test_corvus(driver, resource):
    resource.buffer = ["Corvus 1 312 1 10F"]
    assert driver.identify() == "Corvus 1 312 1 10F"
    assert resource.buffer == ["identify"]

    resource.buffer = []
    assert driver.calibrate() is None
    assert resource.buffer == ["cal"]

    resource.buffer = []
    assert driver.range_measure() is None
    assert resource.buffer == ["rm"]

    resource.buffer = ["3", "3", "3"]
    assert driver.is_calibrated
    assert resource.buffer == ["1 getcaldone", "2 getcaldone", "3 getcaldone"]

    resource.buffer = ["3", "1"]
    assert not driver.is_calibrated
    assert resource.buffer == ["1 getcaldone", "2 getcaldone"]

    resource.buffer = []
    assert driver.move_absolute([0, 4.2, 1.0]) is None
    assert resource.buffer == ["0.0000 4.2000 1.0000 move"]

    resource.buffer = []
    assert driver.move_relative([0, 2.1, -0.1]) is None
    assert resource.buffer == ["0.0000 2.1000 -0.1000 rmove"]

    resource.buffer = []
    assert driver.abort() is None
    assert resource.buffer == ["abort"]

    resource.buffer = []
    assert driver.force_abort() is None
    assert resource.buffer == ["\x03"]

    resource.buffer = ["2.1000 4.2000 0.000"]
    assert driver.position == [2.1, 4.2, 0.0]
    assert resource.buffer == ["pos"]

    resource.buffer = ["3"]
    assert driver.is_moving
    assert resource.buffer == ["status"]

    resource.buffer = ["2"]
    assert not driver.is_moving
    assert resource.buffer == ["status"]

    resource.buffer = ["1"]
    assert driver.joystick_enabled
    assert resource.buffer == ["getjoystick"]

    resource.buffer = ["0"]
    assert not driver.joystick_enabled
    assert resource.buffer == ["getjoystick"]

    resource.buffer = []
    driver.joystick_enabled = True
    assert resource.buffer == ["1 joystick"]


def test_corvus_axes(driver, resource):
    resource.buffer = []
    assert driver[1].calibrate() is None
    assert resource.buffer == ["1 ncal"]

    resource.buffer = []
    assert driver[2].range_measure() is None
    assert resource.buffer == ["2 nrm"]

    resource.buffer = []
    assert driver[3].move_absolute(2.4) is None
    assert resource.buffer == ["2.4000 3 nmove"]

    resource.buffer = []
    assert driver[1].move_relative(1.2) is None
    assert resource.buffer == ["1.2000 1 nrmove"]

    resource.buffer = ["4.200"]
    assert driver[2].position == 4.2
    assert resource.buffer == ["2 npos"]

    resource.buffer = ["3"]
    assert driver[3].is_moving
    assert resource.buffer == ["status"]

    resource.buffer = ["2"]
    assert not driver[1].is_moving
    assert resource.buffer == ["status"]
