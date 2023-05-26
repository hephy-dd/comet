import pytest

from comet.driver.hephy import BrandBox

from .test_driver import resource, buffer


@pytest.fixture
def driver(resource):
    return BrandBox(resource)


def test_basic(driver, buffer):
    buffer.extend(['BrandBox V1.0', 'OK', 'OK'])
    assert driver.identify() == 'BrandBox V1.0'
    assert driver.reset() is None
    assert driver.clear() is None
    assert buffer == ['*IDN?', '*RST', '*CLS']


def test_errors(driver, buffer):
    assert driver.next_error() is None

    buffer.append('Err99')
    driver.clear()
    error = driver.next_error()
    assert error.code == 99
    assert error.message == 'Invalid command'
    assert driver.next_error() is None


def test_channels(driver, buffer):
    buffer.append('')
    assert driver.closed_channels == []
    assert buffer == [':CLOS:STAT?']

    buffer.clear()
    buffer.append('A1')
    assert driver.closed_channels == ['A1']
    assert buffer == [':CLOS:STAT?']

    buffer.clear()
    buffer.append('B1,B2,C2')
    assert driver.closed_channels == ['B1', 'B2', 'C2']
    assert buffer == [':CLOS:STAT?']

    buffer.clear()
    buffer.append('OK')
    assert driver.close_channels(['B1']) is None
    assert buffer == [':CLOS B1']

    buffer.clear()
    buffer.append('OK')
    assert driver.close_channels(['A2', 'B2', 'C1']) is None
    assert buffer == [':CLOS A2,B2,C1']

    buffer.clear()
    buffer.append('OK')
    assert driver.open_channels(['B2']) is None
    assert buffer == [':OPEN B2']

    buffer.clear()
    buffer.append('OK')
    assert driver.open_channels(['B2', 'A1']) is None
    assert buffer == [':OPEN A1,B2']

    buffer.clear()
    buffer.append('OK')
    assert driver.open_all_channels() is None
    assert buffer == [':OPEN A1,A2,B1,B2,C1,C2']
