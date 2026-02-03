import pytest

from comet.driver.mbi.tablecontrol import TableControl


@pytest.fixture
def driver(resource):
    return TableControl(resource)


def test_table_control(driver, resource):
    resource.buffer = ["table-control v0.8.0"]
    assert driver.identify() == "table-control v0.8.0"
    assert resource.buffer == ["*IDN?"]

    resource.buffer = []
    assert driver.calibrate() is None
    assert resource.buffer == []

    resource.buffer = []
    assert driver.range_measure() is None
    assert resource.buffer == []

    resource.buffer = ["3,3,3"]
    assert driver.is_calibrated
    assert resource.buffer == ["CAL?"]

    resource.buffer = ["3,1,3"]
    assert not driver.is_calibrated
    assert resource.buffer == ["CAL?"]

    resource.buffer = []
    assert driver.move_absolute((1.0, 2.0, 3.0)) is None
    assert resource.buffer == ["MOVE:ABS 1.000000,2.000000,3.000000"]

    resource.buffer = []
    assert driver.move_relative((0, -1.0, 0)) is None
    assert resource.buffer == ["MOVE:REL 0.000000,-1.000000,0.000000"]

    resource.buffer = []
    assert driver.abort() is None
    assert resource.buffer == ["MOVE:ABORT"]

    resource.buffer = []
    assert driver.force_abort() is None
    assert resource.buffer == ["MOVE:ABORT"]

    resource.buffer = ["2.100000,4.200000,0.100000"]
    assert driver.position == (2.1, 4.2, 0.1)
    assert resource.buffer == ["POS?"]

    resource.buffer = ["1"]
    assert driver.is_moving
    assert resource.buffer == ["MOVE?"]

    resource.buffer = ["0"]
    assert not driver.is_moving
    assert resource.buffer == ["MOVE?"]

    resource.buffer = []
    assert not driver.joystick_enabled
    assert resource.buffer == []

    resource.buffer = []
    driver.joystick_enabled = True
    assert resource.buffer == []


def test_table_control_axes(driver, resource):
    resource.buffer = []
    assert driver[1].calibrate() is None
    assert resource.buffer == []

    resource.buffer = []
    assert driver[2].range_measure() is None
    assert resource.buffer == []

    resource.buffer = ["1.000000,2.000000,3.000000"]
    assert driver[2].move_absolute(4.0) is None
    assert resource.buffer == ["POS?", "MOVE:ABS 1.000000,4.000000,3.000000"]

    resource.buffer = []
    assert driver[1].move_relative(1.2) is None
    assert resource.buffer == ["MOVE:REL 1.200000,0.000000,0.000000"]

    resource.buffer = ["1.000001,2.000001,3.000001"]
    assert driver[2].position == 2.000001
    assert resource.buffer == ["POS?"]

    resource.buffer = ["1"]
    assert driver[3].is_moving
    assert resource.buffer == ["MOVE?"]

    resource.buffer = ["0"]
    assert not driver[1].is_moving
    assert resource.buffer == ["MOVE?"]
