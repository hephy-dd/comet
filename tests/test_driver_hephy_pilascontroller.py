import pytest

from comet.driver.hephy.pilascontroller import PilasController


@pytest.fixture
def driver(resource):
    return PilasController(resource)


def test_identify(driver, resource):
    resource.buffer = ["0"]
    assert driver.identify() == "Picosecond Laser System"
    assert resource.buffer == ["LS?"]


def test_output(driver, resource):
    resource.buffer = ["0"]
    assert driver.output == driver.OUTPUT_OFF
    assert resource.buffer == ["LS?"]

    resource.buffer = ["1"]
    assert driver.output == driver.OUTPUT_ON
    assert resource.buffer == ["LS?"]

    resource.buffer = []
    driver.output = driver.OUTPUT_ON
    assert resource.buffer == ["LS=1"]

    resource.buffer = []
    driver.output = driver.OUTPUT_OFF
    assert resource.buffer == ["LS=0"]


def test_interlock(driver, resource):
    resource.buffer = ["1"]
    assert driver.interlock
    assert resource.buffer == ["IL?"]

    resource.buffer = ["0"]
    assert not driver.interlock
    assert resource.buffer == ["IL?"]


def test_tune_mode(driver, resource):
    resource.buffer = ["0"]
    assert driver.tune_mode == driver.TUNE_MANUAL
    assert resource.buffer == ["TM?"]

    resource.buffer = ["1"]
    assert driver.tune_mode == driver.TUNE_AUTO
    assert resource.buffer == ["TM?"]

    resource.buffer = []
    driver.tune_mode = driver.TUNE_AUTO
    assert resource.buffer == ["TM=1"]

    resource.buffer = []
    driver.tune_mode = driver.TUNE_MANUAL
    assert resource.buffer == ["TM=0"]


def test_tune(driver, resource):
    resource.buffer = ["37.00%"]
    assert driver.tune == 37.0
    assert resource.buffer == ["TV?"]

    resource.buffer = []
    driver.tune = 50.0
    assert resource.buffer == ["TM=0", "TV=50.0"]

    resource.buffer = []
    with pytest.raises(ValueError):
        driver.tune = -1

    resource.buffer = []
    with pytest.raises(ValueError):
        driver.tune = 101


def test_frequency(driver, resource):
    resource.buffer = ["100000Hz"]
    assert driver.frequency == 100_000
    assert resource.buffer == ["IF?"]

    resource.buffer = []
    driver.frequency = 42000
    assert resource.buffer == ["IF=42000"]

    resource.buffer = []
    with pytest.raises(ValueError):
        driver.frequency = 24

    resource.buffer = []
    with pytest.raises(ValueError):
        driver.frequency = 40e6 + 1


def test_laser_head_temperature(driver, resource):
    resource.buffer = [b"26.12\xb0C"]
    assert driver.laser_head_temperature == 26.12
    assert resource.buffer == ["LT?"]
