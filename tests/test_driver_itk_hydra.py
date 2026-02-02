import pytest

from comet.driver.itk import Hydra


@pytest.fixture
def driver(resource):
    return Hydra(resource)


def test_hydra(driver, resource):
    resource.buffer = ["Hydra 1 312 1 10F"]
    assert driver.identify() == "Hydra 1 312 1 10F"
    assert resource.buffer == ["identify"]

    resource.buffer = []
    assert driver.calibrate() is None
    assert resource.buffer == ["1 ncal", "2 ncal"]

    resource.buffer = []
    assert driver.range_measure() is None
    assert resource.buffer == ["1 nrm", "2 nrm"]

    resource.buffer = []
    assert driver.move_absolute([0, 4.2]) is None
    assert resource.buffer == ["0.000 4.200 m"]

    resource.buffer = []
    assert driver.move_relative([0, 2.1]) is None
    assert resource.buffer == ["0.000 2.100 r"]

    resource.buffer = []
    assert driver.abort() is None
    assert resource.buffer == ["1 nabort", "2 nabort"]

    resource.buffer = []
    assert driver.force_abort() is None
    assert resource.buffer == ["\x03"]

    resource.buffer = ["2.100 4.200"]
    assert driver.position == [2.1, 4.2]
    assert resource.buffer == ["p"]

    resource.buffer = ["3"]
    assert driver.is_moving
    assert resource.buffer == ["st"]

    resource.buffer = ["2"]
    assert not driver.is_moving
    assert resource.buffer == ["st"]

    resource.buffer = ["1", "0"]
    assert driver.joystick_enabled
    assert resource.buffer == ["1 getmanctrl", "2 getmanctrl"]

    resource.buffer = ["0", "0"]
    assert not driver.joystick_enabled
    assert resource.buffer == ["1 getmanctrl", "2 getmanctrl"]

    resource.buffer = []
    driver.joystick_enabled = True
    assert resource.buffer == ["15 1 setmanctrl", "15 2 setmanctrl"]


def test_hydra_axes(driver, resource):
    resource.buffer = []
    assert driver[1].calibrate() is None
    assert resource.buffer == ["1 ncal"]

    resource.buffer = []
    assert driver[2].range_measure() is None
    assert resource.buffer == ["2 nrm"]

    resource.buffer = []
    assert driver[2].move_relative(1.2) is None
    assert resource.buffer == ["1.200 2 nr"]

    resource.buffer = []
    assert driver[1].move_absolute(2.2) is None
    assert resource.buffer == ["2.200 1 nm"]

    resource.buffer = ["4.200"]
    assert driver[1].position == 4.2
    assert resource.buffer == ["1 np"]

    resource.buffer = ["2"]
    assert not driver[1].is_moving
    assert resource.buffer == ["1 nst"]
