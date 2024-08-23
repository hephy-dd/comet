import pytest

from comet.driver.nkt_photonics.pilas import PILAS

from .test_driver import resource


@pytest.fixture
def driver(resource):
    return PILAS(resource)


def test_identify(driver, resource):
    resource.buffer = [
        r"controller serial: PLC1060CW0F00000715\nlaser head serial: PLH1060CW0F00000715\ncenter wavelength: 1060 nm\nCW laser option: no\nCW laser power: fixed\nsoftware version: SW.PiLas.V1.1.AEb\ncontroller hardware version: PiLas_Control_PCB_Rev.2.1\nlaser head hardware version: PiLas_Laser_Head_PCB_Rev.2.0"
    ]
    assert (
        driver.identify()
        == r"controller serial: PLC1060CW0F00000715\nlaser head serial: PLH1060CW0F00000715\ncenter wavelength: 1060 nm\nCW laser option: no\nCW laser power: fixed\nsoftware version: SW.PiLas.V1.1.AEb\ncontroller hardware version: PiLas_Control_PCB_Rev.2.1\nlaser head hardware version: PiLas_Laser_Head_PCB_Rev.2.0"
    )
    assert resource.buffer == ["version?"]


def test_output(driver, resource):
    resource.buffer = ["0"]
    assert driver.output == driver.OUTPUT_OFF
    assert resource.buffer == ["ld?"]

    resource.buffer = ["1"]
    assert driver.output == driver.OUTPUT_ON
    assert resource.buffer == ["ld?"]

    resource.buffer = []
    driver.output = driver.OUTPUT_ON
    assert resource.buffer == ["ld=1"]

    resource.buffer = []
    driver.output = driver.OUTPUT_OFF
    assert resource.buffer == ["ld=0"]


def test_tune_mode(driver, resource):
    resource.buffer = ["0"]
    assert driver.tune_mode == driver.TUNE_MANUAL
    assert resource.buffer == ["tm?"]

    resource.buffer = ["1"]
    assert driver.tune_mode == driver.TUNE_AUTO
    assert resource.buffer == ["tm?"]

    resource.buffer = []
    driver.tune_mode = driver.TUNE_AUTO
    assert resource.buffer == ["tm=1"]

    resource.buffer = []
    driver.tune_mode = driver.TUNE_MANUAL
    assert resource.buffer == ["tm=0"]


def test_tune(driver, resource):
    resource.buffer = ["1000"]
    assert driver.tune == 100.0
    assert resource.buffer == ["tune?"]

    resource.buffer = ["0"]
    driver.tune = 50.0
    assert resource.buffer == ["tm?", "tune=500"]

    resource.buffer = ["0"]
    with pytest.raises(ValueError):
        driver.tune = -1

    resource.buffer = ["0"]
    with pytest.raises(ValueError):
        driver.tune = 101


def test_frequency(driver, resource):
    resource.buffer = ["1000"]
    assert driver.frequency == 1000
    assert resource.buffer == ["f?"]

    resource.buffer = []
    driver.frequency = 1000
    assert resource.buffer == ["f=1000"]

    with pytest.raises(ValueError):
        driver.frequency = 24

    with pytest.raises(ValueError):
        driver.frequency = 40e6 + 1


def test_laser_diode_temperature(driver, resource):
    resource.buffer = ["2501"]
    assert driver.laser_diode_temperature == 25.01
    assert resource.buffer == ["ldtemp?"]


def test_laser_head_temperature(driver, resource):
    resource.buffer = ["2490"]
    assert driver.laser_head_temperature == 24.9
    assert resource.buffer == ["lht?"]
