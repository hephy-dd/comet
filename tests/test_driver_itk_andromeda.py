import pytest

from comet.driver.itk.andromeda import Andromeda


@pytest.fixture
def driver(resource) -> Andromeda:
    return Andromeda(resource)


def test_andromeda(driver, resource):
    resource.buffer = ["Andromeda 1 312 1 10F"]
    assert driver.identify() == "Andromeda 1 312 1 10F"
    assert resource.buffer == ["identify"]

    resource.buffer = []
    assert driver.calibrate() is None
    assert resource.buffer == [
        "1 ncal",
        "2 ncal",
        "3 ncal",
    ]

    resource.buffer = []
    assert driver.range_measure() is None
    assert resource.buffer == ["1 nrm", "2 nrm", "3 nrm"]

    resource.buffer = []
    assert driver.move_absolute([0, 4.2, 1.0]) is None
    assert resource.buffer == ["0.0000 4.2000 1.0000 m"]

    resource.buffer = []
    assert driver.move_relative([0, 2.1, -0.1]) is None
    assert resource.buffer == ["0.0000 2.1000 -0.1000 r"]

    resource.buffer = []
    assert driver.abort() is None
    assert resource.buffer == [
        "1 nabort",
        "2 nabort",
        "3 nabort",
    ]

    resource.buffer = []
    assert driver.force_abort() is None
    assert resource.buffer == ["\x03"]

    resource.buffer = ["2.1000 4.2000 0.1000"]
    assert driver.position == [2.1, 4.2, 0.1]
    assert resource.buffer == ["p"]

    resource.buffer = ["3"]
    assert driver.is_moving
    assert resource.buffer == ["st"]

    resource.buffer = ["2"]
    assert not driver.is_moving
    assert resource.buffer == ["st"]

    resource.buffer = [
        "1",
        "0",
        "0",
    ]
    assert driver.joystick_enabled
    assert resource.buffer == [
        "1 getmanctrl",
        "2 getmanctrl",
        "3 getmanctrl",
    ]

    resource.buffer = ["0", "0", "0"]
    assert not driver.joystick_enabled
    assert resource.buffer == [
        "1 getmanctrl",
        "2 getmanctrl",
        "3 getmanctrl",
    ]

    resource.buffer = []
    driver.joystick_enabled = True
    assert resource.buffer == [
        "15 1 setmanctrl",
        "15 2 setmanctrl",
        "15 3 setmanctrl",
    ]


def test_andromeda_axes(driver, resource):
    resource.buffer = []
    assert driver[1].calibrate() is None
    assert resource.buffer == ["1 ncal"]

    resource.buffer = []
    assert driver[2].range_measure() is None
    assert resource.buffer == ["2 nrm"]

    resource.buffer = []
    assert driver[2].move_relative(1.2) is None
    assert resource.buffer == ["1.2000 2 nr"]

    resource.buffer = []
    assert driver[1].move_absolute(2.2) is None
    assert resource.buffer == ["2.2000 1 nm"]

    resource.buffer = ["4.200"]
    assert driver[1].position == 4.2
    assert resource.buffer == ["1 np"]

    resource.buffer = ["2"]
    assert not driver[1].is_moving
    assert resource.buffer == ["1 nst"]
