import pytest

from comet.emulator.nkt_photonics.pilas import PILASEmulator


@pytest.fixture
def emulator():
    return PILASEmulator()


def test_identify(emulator):

    assert (
        emulator("version?")
        == "controller serial: PLC1060CW0F00000715\nlaser head serial: PLH1060CW0F00000715\ncenter wavelength: 1060 nm\nCW laser option: no\nCW laser power: fixed\nsoftware version: SW.PiLas.V1.1.AEb\ncontroller hardware version: PiLas_Control_PCB_Rev.2.1\nlaser head hardware version: PiLas_Laser_Head_PCB_Rev.2.0"
    )


def test_output(emulator):
    assert emulator("ld?") == "pulsed laser emission: off"
    assert emulator("ld=1") == "done"
    assert emulator("ld?") == "pulsed laser emission: on"
    assert emulator("ld=0") == "done"
    assert emulator("ld?") == "pulsed laser emission: off"


def test_tune_mode(emulator):
    assert emulator("tm?") == "tune mode:\tmanual"
    assert emulator("tm=1") == "done"
    assert emulator("tm?") == "tune mode:\tauto"
    assert emulator("tm=0") == "done"
    assert emulator("tm?") == "tune mode:\tmanual"


def test_tune(emulator):
    assert emulator("tune?") == "tune value:\t\t     0.00 %"
    assert emulator("tune=500") == "done"
    assert emulator("tune?") == "tune value:\t\t     50.00 %"
    assert emulator("tune=1000") == "done"
    assert emulator("tune?") == "tune value:\t\t     100.00 %"
    assert emulator("tune=0") == "done"
    assert emulator("tune?") == "tune value:\t\t     0.00 %"


def test_frequency(emulator):
    assert emulator("f?") == "int. frequency:\t       1000000 Hz"
    assert emulator("f=1000") == "done"
    assert emulator("f?") == "int. frequency:\t       1000 Hz"
    assert emulator("f=40000000") == "done"
    assert emulator("f?") == "int. frequency:\t       40000000 Hz"


def test_laser_diode_temperature(emulator):
    assert emulator("ldtemp?") == "LD temp.:\t\tgood"
    emulator.laser_diode_temperature = False

    assert emulator("ldtemp?") == "LD temp.:\t\tbad"
