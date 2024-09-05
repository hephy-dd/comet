import pytest

from comet.driver.nkt_photonics.pilas import PILAS

from .test_driver import MockResource


class PILASMock(MockResource):
    def read(self, encoding=None):
        return self.buffer.pop(0)


@pytest.fixture
def resource():

    return PILASMock()


@pytest.fixture
def driver(resource):
    return PILAS(resource)


def test_identify(driver, resource):
    resource.buffer = [
        "controller serial: PLC1060CW0F00000715",
        "laser head serial: PLH1060CW0F00000715",
        "center wavelength: 1060 nm",
        "CW laser option: no",
        "CW laser power: fixed",
        "software version: SW.PiLas.V1.1.AEb",
        "controller hardware version: PiLas_Control_PCB_Rev.2.1",
        "laser head hardware version: PiLas_Laser_Head_PCB_Rev.2.0",
    ]
    assert (
        driver.identify()
        == "controller serial: PLC1060CW0F00000715\nlaser head serial: PLH1060CW0F00000715\ncenter wavelength: 1060 nm\nCW laser option: no\nCW laser power: fixed\nsoftware version: SW.PiLas.V1.1.AEb\ncontroller hardware version: PiLas_Control_PCB_Rev.2.1\nlaser head hardware version: PiLas_Laser_Head_PCB_Rev.2.0"
    )
    assert resource.buffer == ["version?"]


def test_output(driver, resource):
    resource.buffer = ["pulsed laser emission: off"]
    assert driver.output == driver.OUTPUT_OFF
    assert resource.buffer == ["ld?"]

    resource.buffer = ["pulsed laser emission: on"]
    assert driver.output == driver.OUTPUT_ON
    assert resource.buffer == ["ld?"]

    resource.buffer = ["done"]
    driver.output = driver.OUTPUT_ON
    assert resource.buffer == ["ld=1"]

    resource.buffer = ["done"]
    driver.output = driver.OUTPUT_OFF
    assert resource.buffer == ["ld=0"]


def test_tune_mode(driver, resource):
    resource.buffer = ["tune mode:\tmanual"]
    assert driver.tune_mode == driver.TUNE_MANUAL
    assert resource.buffer == ["tm?"]

    resource.buffer = ["tune mode:\tauto"]
    assert driver.tune_mode == driver.TUNE_AUTO
    assert resource.buffer == ["tm?"]

    resource.buffer = ["done"]
    driver.tune_mode = driver.TUNE_AUTO
    assert resource.buffer == ["tm=1"]

    resource.buffer = ["done"]
    driver.tune_mode = driver.TUNE_MANUAL
    assert resource.buffer == ["tm=0"]


def test_tune(driver, resource):
    resource.buffer = [
        "tune value:\t\t     37.00 %",
    ]
    assert driver.tune == 37.0
    assert resource.buffer == ["tune?"]

    resource.buffer = ["done", "done"]
    driver.tune = 50.0
    assert resource.buffer == ["tm=0", "tune=500"]

    resource.buffer = ["done", "done"]
    with pytest.raises(ValueError):
        driver.tune = -1

    resource.buffer = ["done", "done"]
    with pytest.raises(ValueError):

        driver.tune = 101


def test_frequency(driver, resource):
    resource.buffer = ["int. frequency:\t       100 Hz"]
    assert driver.frequency == 100
    assert resource.buffer == ["f?"]

    resource.buffer = ["done"]
    driver.frequency = 1000
    assert resource.buffer == ["f=1000"]

    with pytest.raises(ValueError):
        resource.buffer = ["done"]
        driver.frequency = 24

    with pytest.raises(ValueError):
        resource.buffer = ["done"]

        driver.frequency = 40e6 + 1


def test_laser_diode_temperature(driver, resource):
    resource.buffer = ["LD temp.:\t\tgood"]
    assert driver.get_laser_diode_temperature() == driver.DIODE_TEMPERATURE_GOOD
    assert resource.buffer == ["ldtemp?"]

    resource.buffer = ["LD temp.:\t\tbad"]
    assert driver.get_laser_diode_temperature() == driver.DIODE_TEMPERATURE_BAD
    assert resource.buffer == ["ldtemp?"]


def test_laser_head_temperature(driver, resource):
    resource.buffer = ["laser head temp.:\t     26.12 °C"]
    assert driver.get_laser_head_temperature() == 26.12
    assert resource.buffer == ["lht?"]
