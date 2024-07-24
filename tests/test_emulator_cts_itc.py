import re

import pytest

from comet.emulator.cts.itc import ITCEmulator


@pytest.fixture
def emulator():
    return ITCEmulator()


def test_basic(emulator):
    assert emulator("S") == "S11110100\x06"


def test_time(emulator):
    assert re.match(r"^T\d{6}\d{6}$", emulator("T"))
    assert re.match(r"^T\d{6}\d{6}$", emulator("t010203010203"))


def test_channels(emulator):
    assert re.match(r"A0 \-?\d+\.\d \-?\d+\.\d", emulator("A0"))
    assert re.match(r"A1 \-?\d+\.\d \-?\d+\.\d", emulator("A1"))
    assert re.match(r"A2 \-?\d+\.\d \-?\d+\.\d", emulator("A2"))
    assert re.match(r"A3 \-?\d+\.\d \-?\d+\.\d", emulator("A3"))
    assert re.match(r"A4 \-?\d+\.\d \-?\d+\.\d", emulator("A4"))
    assert re.match(r"A5 \-?\d+\.\d \-?\d+\.\d", emulator("A5"))
    assert re.match(r"A6 \-?\d+\.\d \-?\d+\.\d", emulator("A6"))
    assert re.match(r"A7 \-?\d+\.\d \-?\d+\.\d", emulator("A7"))
    assert re.match(r"A8 \-?\d+\.\d \-?\d+\.\d", emulator("A8"))
    assert re.match(r"A9 \-?\d+\.\d \-?\d+\.\d", emulator("A9"))
    assert re.match(r"A\: \-?\d+\.\d \-?\d+\.\d", emulator("A:"))
    assert re.match(r"A\; \-?\d+\.\d \-?\d+\.\d", emulator("A;"))
    assert re.match(r"A\< \-?\d+\.\d \-?\d+\.\d", emulator("A<"))
    assert re.match(r"A\= \-?\d+\.\d \-?\d+\.\d", emulator("A="))
    assert re.match(r"A\> \-?\d+\.\d \-?\d+\.\d", emulator("A>"))
    assert re.match(r"A\? \-?\d+\.\d \-?\d+\.\d", emulator("A?"))


def test_digital_channels(emulator):
    assert emulator("O") == "O1000000000000"  # TODO


def test_program(emulator):
    assert emulator("P") == "P000"
    assert emulator("P004") == "P004"
    assert emulator("P") == "P004"
    assert emulator("P000") == "P000"
    assert emulator("P") == "P000"
