import pytest

from comet.driver.hephy.corvuscontroller import CorvusController


@pytest.fixture
def driver(resource):
    return CorvusController(resource)


def test_basic(driver, resource):
    resource.buffer = ["0.000000,0.000000,0.000000,0"]
    assert driver.identify() == "Corvus Controller"
    assert resource.buffer == ["PO?"]


def test_move_absolute(driver, resource):
    resource.buffer = []
    driver.move_absolute((1.0, 2.0, 3.0))
    assert resource.buffer == ["MA=1.000000,2.000000,3.000000"]


def test_move_relative(driver, resource):
    resource.buffer = []
    driver.move_relative((0, 0.042, -0.1))
    assert resource.buffer == ["MR=0.042000,2", "MR=-0.100000,3"]


def test_is_moving(driver, resource):
    resource.buffer = ["0.0000000,0.000000,0.000000,0"]
    assert not driver.is_moving
    assert resource.buffer == ["PO?"]

    resource.buffer = ["0.0000000,0.000000,0.000000,1"]
    assert driver.is_moving
    assert resource.buffer == ["PO?"]


def test_axis_move_absolute(driver, resource):
    resource.buffer = ["1.0000000,2.000000,3.000000,0"]
    driver[2].move_absolute(0.420)
    assert resource.buffer == ["PO?", "MA=1.000000,0.420000,3.000000"]


def test_axis_move_relative(driver, resource):
    resource.buffer = []
    driver[1].move_relative(0.042)
    driver[2].move_relative(0.420)
    driver[3].move_relative(4.200)
    assert resource.buffer == ["MR=0.042000,1", "MR=0.420000,2", "MR=4.200000,3"]


def test_axis_is_moving(driver, resource):
    resource.buffer = ["0.0000000,0.000000,0.000000,0"]
    assert not driver[1].is_moving
    assert resource.buffer == ["PO?"]

    resource.buffer = ["0.0000000,0.000000,0.000000,1"]
    assert driver[2].is_moving
    assert resource.buffer == ["PO?"]
