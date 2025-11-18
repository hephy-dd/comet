import pytest

from comet.driver.rohde_schwarz.rto6 import RTO6

from .test_driver import resource


@pytest.fixture
def driver(resource):
    return RTO6(resource)


def test_identify(driver, resource):
    resource.buffer = ["Rohde&Schwarz,RTO6,1802.0001k04/123456,5.50.2.0"]
    assert driver.identify() == "Rohde&Schwarz,RTO6,1802.0001k04/123456,5.50.2.0"
    assert resource.buffer == ["*IDN?"]
