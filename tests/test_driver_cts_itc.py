from datetime import datetime

import pytest
from comet.driver.cts import ITC

from .test_driver import resource


def to_bytes(s: str) -> bytes:
    return s.encode("ascii")


@pytest.fixture
def driver(resource):
    return ITC(resource)


def test_identify(driver):
    driver.resource.buffer = [to_bytes("T010120010000")]
    assert driver.identify() == "ITC climate chamber"
    assert driver.resource.buffer == [to_bytes("T")]


def test_get_time(driver):
    driver.resource.buffer = [to_bytes("T010120010000")]
    assert driver.time == datetime(2020, 1, 1, 1, 0)
    assert driver.resource.buffer == [to_bytes("T")]


def test_set_time(driver):
    driver.resource.buffer = [to_bytes("t010120010000")]
    driver.time = datetime(2020, 1, 1, 1, 0)
    assert driver.resource.buffer == [to_bytes("t010120010000")]


@pytest.mark.parametrize("running", [0, 1])
@pytest.mark.parametrize("error", [
    (0, "0", None),
    (1, "\x3a", "Feuchtesensor 08-B2"),
])
def test_status(driver, running, error):
    is_error, error_code, error_msg = error
    driver.resource.buffer = [to_bytes(f"S{running}{is_error}000101{error_code}")]
    st = driver.status
    assert st.running == bool(running)
    assert st.error == error_msg
    assert st.warning is None
    assert st.channels == {0: False, 1: False, 2: False, 3: True, 4: False, 5: True}  # TODO refactor?
    assert driver.resource.buffer == [to_bytes("S")]


@pytest.mark.parametrize("error_message", [
    "",
    "Feuchtesensor 08-B2",
])
def test_error_message(driver, error_message):
    driver.resource.buffer = [to_bytes(f"F{error_message:<32}")]
    assert driver.error_message == error_message
    assert driver.resource.buffer == [to_bytes("F")]


@pytest.mark.parametrize("program", [0, 42])
def test_get_program(driver, program):
    driver.resource.buffer = [to_bytes(f"P{program:03d}")]
    assert driver.program == program
    assert driver.resource.buffer == [to_bytes("P")]


@pytest.mark.parametrize("program", [0, 42])
def test_set_program(driver, program):
    driver.resource.buffer = [to_bytes(f"p{program:03d}")]
    driver.program = program
    assert driver.resource.buffer == [to_bytes(f"p{program:03d}")]


def test_start(driver):
    driver.resource.buffer = [to_bytes("s1")]
    driver.start()
    assert driver.resource.buffer == [to_bytes("s1 1")]


def test_stop(driver):
    driver.resource.buffer = [to_bytes("s1")]
    driver.stop()
    assert driver.resource.buffer == [to_bytes("s1 0")]
