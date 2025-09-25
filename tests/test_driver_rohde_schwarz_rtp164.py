import struct
import pytest

from comet.driver.rohde_schwarz.rtp164 import RTP164

from .test_driver import resource, pack_bianry_values


@pytest.fixture
def driver(resource):
    return RTP164(resource)


def test_identify(driver, resource):
    resource.buffer = ["Rohde&Schwarz,RTP,1320.5007k16/123456,5.50.2.0"]
    assert driver.identify() == "Rohde&Schwarz,RTP,1320.5007k16/123456,5.50.2.0"
    assert resource.buffer == ["*IDN?"]


def test_reset(driver, resource):
    with pytest.raises(NotImplementedError):
        driver.reset()


def test_clear(driver, resource):
    resource.buffer = ["1"]
    driver.clear()
    assert resource.buffer == ["*CLS", "*OPC?"]


def test_error(driver, resource):
    resource.buffer = ["0,\"No error\""]
    assert driver.next_error() == None
    assert resource.buffer == ["SYST:ERR?"]


def test_get_channel(driver, resource):
    assert len(driver) == 4
    for i in range(4):
        assert driver[i].channel == i

    with pytest.raises(IndexError):
        driver[5]

    with pytest.raises(IndexError):
        driver[-1]


def test_get_enabled(driver, resource):
    resource.buffer = ["0"]
    assert not driver[0].enabled
    assert resource.buffer == [":CHAN1:STAT?"]
    resource.buffer = ["1"]
    assert driver[1].enabled
    assert resource.buffer == [":CHAN2:STAT?"]


def test_set_channel_enabled(driver, resource):
    resource.buffer = []
    driver[0].enabled = True
    assert resource.buffer == [":CHAN1:STAT ON"]
    resource.buffer = []
    driver[1].enabled = False
    assert resource.buffer == [":CHAN2:STAT OFF"]


def test_channel_time_axis(driver, resource):
    resource.buffer = ["-0.1,0.1,3,1"]
    assert driver[0].time_axis() == [-0.1, 0.0, 0.1]
    assert resource.buffer == [":CHAN1:DATA:HEAD?"]


def test_channel_acquire_waveform(driver, resource):
    values = [2.0, 1.0, 1.5]
    resource.buffer = ["1", pack_bianry_values(values)]
    assert driver[0].acquire_waveform() == values
    assert resource.buffer == ["SING", "*OPC?", ":CHAN1:DATA?"]

    values = [0, -1.0, 1.0, -2.0, 2.0, -1.0, 1.0, 0]
    resource.buffer = ["1", pack_bianry_values(values)]
    assert driver[1].acquire_waveform() == values
    assert resource.buffer == ["SING", "*OPC?", ":CHAN2:DATA?"]
