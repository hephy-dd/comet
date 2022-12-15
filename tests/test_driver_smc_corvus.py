from comet.driver.smc import Corvus

from .test_driver import Resource


def test_corvus():
    resource = Resource()
    instr = Corvus(resource)

    resource.buffer = ["Corvus 1 312 1 10F"]
    assert instr.identify() == "Corvus 1 312 1 10F"
    assert resource.buffer == ["identify"]

    resource.buffer = []
    assert instr.calibrate() is None
    assert resource.buffer == ["cal"]

    resource.buffer = []
    assert instr.range_measure() is None
    assert resource.buffer == ["rm"]

    resource.buffer = ["3 3 3"]
    assert instr.is_calibrated
    assert resource.buffer == ["getcaldone"]

    resource.buffer = ["3 2"]
    assert not instr.is_calibrated
    assert resource.buffer == ["getcaldone"]

    resource.buffer = []
    assert instr.move_absolute([0, 4.2]) is None
    assert resource.buffer == ["0.000 4.200 move"]

    resource.buffer = []
    assert instr.move_relative([0, 2.1]) is None
    assert resource.buffer == ["0.000 2.100 rmove"]

    resource.buffer = []
    assert instr.abort() is None
    assert resource.buffer == ["abort"]

    resource.buffer = []
    assert instr.force_abort() is None
    assert resource.buffer == ["\x03"]

    resource.buffer = ["2.100 4.200"]
    assert instr.position == [2.1, 4.2]
    assert resource.buffer == ["pos"]

    resource.buffer = ["3"]
    assert instr.is_moving
    assert resource.buffer == ["status"]

    resource.buffer = ["2"]
    assert not instr.is_moving
    assert resource.buffer == ["status"]

    resource.buffer = ["1"]
    assert instr.joystick_enabled
    assert resource.buffer == ["getjoystick"]

    resource.buffer = ["0"]
    assert not instr.joystick_enabled
    assert resource.buffer == ["getjoystick"]

    resource.buffer = []
    instr.joystick_enabled = True
    assert resource.buffer == ["1 joystick"]


def test_corvus_axes():
    resource = Resource()
    instr = Corvus(resource)

    resource.buffer = []
    assert instr[0].calibrate() is None
    assert resource.buffer == ["0 ncal"]

    resource.buffer = []
    assert instr[1].range_measure() is None
    assert resource.buffer == ["1 nrm"]

    resource.buffer = []
    assert instr[2].move_absolute(2.4) is None
    assert resource.buffer == ["2.400 2 nmove"]

    resource.buffer = []
    assert instr[0].move_relative(1.2) is None
    assert resource.buffer == ["1.200 0 nrmove"]

    resource.buffer = ["4.200"]
    assert instr[1].position == 4.2
    assert resource.buffer == ["1 npos"]

    resource.buffer = ["3"]
    assert instr[2].is_moving
    assert resource.buffer == ["status"]

    resource.buffer = ["2"]
    assert not instr[0].is_moving
    assert resource.buffer == ["status"]