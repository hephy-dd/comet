import pytest

from comet.driver.rohde_schwarz.nge100 import NGE100

from .test_driver import resource


@pytest.fixture
def driver(resource):
    return NGE100(resource)


def test_identify(driver, resource):
    resource.buffer = ["Rohde&Schwarz,NGE103B,5601.3800k03/101863,1.54"]
    assert driver.identify() == "Rohde&Schwarz,NGE103B,5601.3800k03/101863,1.54"
    assert resource.buffer == ["*IDN?"]


def test_reset(driver, resource):
    resource.buffer = [""]
    driver.reset()
    assert resource.buffer == ["*RST", "*OPC?"]


def test_clear(driver, resource):
    resource.buffer = [""]
    driver.clear()
    assert resource.buffer == ["*CLS", "*OPC?"]


def test_error(driver, resource):
    resource.buffer = ["0, 'No error'"]
    assert driver.next_error() == None
    assert resource.buffer == ["SYSTem:ERRor?"]

    resource.buffer = ["-222, 'Data out of range;INSTrument 5'"]
    error = driver.next_error()
    assert error.code == -222

    assert error.message == "Data out of range;INSTrument 5"
    assert resource.buffer == ["SYSTem:ERRor?"]


def test_get_channel(driver, resource):
    assert len(driver) == 3
    for i in range(3):
        assert driver[i].channel == i

    with pytest.raises(IndexError):
        driver[3]

    with pytest.raises(IndexError):
        driver[-1]


def test_read_voltage_level(driver, resource):
    resource.buffer = ["0"]
    assert driver[0].voltage_level == 0.0
    assert resource.buffer == [
        "INSTrument 1",
        "SOURce:VOLTage:LEVel:IMMediate:AMPLitude?",
    ]


def test_set_voltage_level(driver, resource):
    resource.buffer = ["1"]
    driver[0].voltage_level = 0.0
    assert resource.buffer == [
        "INSTrument 1",
        "SOURce:VOLTage:LEVel:IMMediate:AMPLitude 0.0",
        "*OPC?",
    ]

    with pytest.raises(ValueError):
        driver[0].voltage_level = -1

    with pytest.raises(ValueError):
        driver[0].voltage_level = 33


def test_read_current_limit(driver, resource):
    resource.buffer = ["0.0"]
    assert driver[0].current_limit == 0.0
    assert resource.buffer == [
        "INSTrument 1",
        "SOURce:CURRent:LEVel:IMMediate:AMPLitude?",
    ]


def test_set_current_limit(driver, resource):
    resource.buffer = ["1"]
    driver[0].current_limit = 0.0
    assert resource.buffer == [
        "INSTrument 1",
        "SOURce:CURRent:LEVel:IMMediate:AMPLitude 0.0",
        "*OPC?",
    ]

    with pytest.raises(ValueError):
        driver[0].current_limit = -1

    with pytest.raises(ValueError):
        driver[0].current_limit = 3.1


def test_measure_voltage(driver, resource):
    resource.buffer = ["1.0"]
    assert driver[0].measure_voltage() == 1.0
    assert resource.buffer == ["INSTrument 1", "MEASure:SCALar:VOLTage:DC?"]


def test_measure_current(driver, resource):
    resource.buffer = ["1.0"]
    assert driver[0].measure_current() == 1.0
    assert resource.buffer == ["INSTrument 1", "MEASure:SCALar:CURRent:DC?"]


def test_measure_power(driver, resource):
    resource.buffer = ["10.0"]
    assert driver[0].measure_power() == 10.0
    assert resource.buffer == ["INSTrument 1", "MEASure:SCALar:POWer?"]
