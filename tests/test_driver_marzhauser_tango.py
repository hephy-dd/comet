from comet.driver.marzhauser import Tango

from .test_driver import Resource


def test_tango():
    resource = Resource()
    instr = Tango(resource)

    resource.buffer = ["TANGO-MINI3"]
    assert instr.identify() == "TANGO-MINI3"
    assert resource.buffer == ["?version"]

    resource.buffer = []
    assert instr.calibrate() is None
    assert resource.buffer == ["!autostatus 0", "!cal"]

    resource.buffer = []
    assert instr.range_measure() is None
    assert resource.buffer == ["!autostatus 0", "!rm"]

    resource.buffer = ["3 3 3"]
    assert instr.is_calibrated
    assert resource.buffer == ["?calst"]

    resource.buffer = ["3 2"]
    assert not instr.is_calibrated
    assert resource.buffer == ["?calst"]

    resource.buffer = []
    assert instr.move_absolute([2.1, 4.2]) is None
    assert resource.buffer == ["!autostatus 0", "!moa 2.100 4.200"]

    resource.buffer = []
    assert instr.move_relative([0, 2.1]) is None
    assert resource.buffer == ["!autostatus 0", "!mor 0.000 2.100"]

    resource.buffer = []
    assert instr.abort() is None
    assert resource.buffer == ["!a"]

    resource.buffer = []
    assert instr.force_abort() is None
    assert resource.buffer == ["\x03"]

    resource.buffer = ["2.100 4.200"]
    assert instr.position == [2.1, 4.2]
    assert resource.buffer == ["?pos"]

    resource.buffer = ["@@M-."]
    assert instr.is_moving
    assert resource.buffer == ["?statusaxis"]

    resource.buffer = ["@@@-."]
    assert not instr.is_moving
    assert resource.buffer == ["?statusaxis"]

    resource.buffer = ["2"]
    assert instr.joystick_enabled
    assert resource.buffer == ["?joy"]

    resource.buffer = ["0"]
    assert not instr.joystick_enabled
    assert resource.buffer == ["?joy"]

    resource.buffer = []
    instr.joystick_enabled = True
    assert resource.buffer == ["!autostatus 0", "!joy 2"]


def test_tango_axes():
    resource = Resource()
    instr = Tango(resource)

    resource.buffer = []
    assert instr[0].calibrate() is None
    assert resource.buffer == ["!autostatus 0", "!cal x"]

    resource.buffer = []
    assert instr[1].range_measure() is None
    assert resource.buffer == ["!autostatus 0", "!rm y"]

    resource.buffer = []
    assert instr[2].move_absolute(2.4) is None
    assert resource.buffer == ["!autostatus 0", "!moa z 2.400"]

    resource.buffer = []
    assert instr[0].move_relative(1.2) is None
    assert resource.buffer == ["!autostatus 0", "!mor x 1.200"]

    resource.buffer = ["4.200"]
    assert instr[1].position == 4.2
    assert resource.buffer == ["?pos y"]

    resource.buffer = ["M"]
    assert instr[2].is_moving
    assert resource.buffer == ["?statusaxis z"]

    resource.buffer = ["@"]
    assert not instr[0].is_moving
    assert resource.buffer == ["?statusaxis x"]
