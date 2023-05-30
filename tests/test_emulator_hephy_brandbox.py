import pytest

from comet.emulator.hephy.brandbox import BrandBoxEmulator


@pytest.fixture
def emulator():
    return BrandBoxEmulator()


def test_basic(emulator):
    assert emulator("*IDN?") == "BrandBox, v2.0 (Emulator)"
    assert emulator("*RST") == "OK"
    assert emulator("*CLS") == "OK"
    assert emulator("*STB?") == "0,0,0,0,0,0"
    assert emulator("*STR?") == "0"
    assert emulator("*OPC?") == "1"


def test_debug(emulator):
    assert emulator("DEBUG?") == "Err99"


def test_channels(emulator):
    assert emulator(":CLOS:STAT?") == ""
    assert emulator(":OPEN:STAT?") == "A1,A2,B1,B2,C1,C2"
    assert emulator(":CLOS C1,A1") == "OK"
    assert emulator(":CLOS:STAT?") == "A1,C1"
    assert emulator(":OPEN:STAT?") == "A2,B1,B2,C2"
    assert emulator(":OPEN C1") == "OK"
    assert emulator(":CLOS:STAT?") == "A1"
    assert emulator(":OPEN:STAT?") == "A2,B1,B2,C1,C2"

    assert emulator(":OPEN A1,A2,B1") == "OK"
    assert emulator(":OPEN B2,C1,C2") == "OK"

    assert emulator("GET:A ?") == "OFF,OFF"
    assert emulator("GET:A1 ?") == "OFF"
    assert emulator("GET:A2 ?") == "OFF"
    assert emulator("GET:B ?") == "OFF,OFF"
    assert emulator("GET:B1 ?") == "OFF"
    assert emulator("GET:B2 ?") == "OFF"
    assert emulator("GET:C ?") == "OFF,OFF"
    assert emulator("GET:C1 ?") == "OFF"
    assert emulator("GET:C2 ?") == "OFF"

    assert emulator("SET:A2_ON") == "OK"
    assert emulator("SET:B1_ON") == "OK"
    assert emulator("SET:C_ON") == "OK"

    assert emulator("GET:A ?") == "OFF,ON"
    assert emulator("GET:A1 ?") == "OFF"
    assert emulator("GET:A2 ?") == "ON"
    assert emulator("GET:B ?") == "ON,OFF"
    assert emulator("GET:B1 ?") == "ON"
    assert emulator("GET:B2 ?") == "OFF"
    assert emulator("GET:C ?") == "ON,ON"
    assert emulator("GET:C1 ?") == "ON"
    assert emulator("GET:C2 ?") == "ON"

    assert emulator("SET:A_OFF") == "OK"
    assert emulator("SET:B_OFF") == "OK"
    assert emulator("SET:C1_OFF") == "OK"
    assert emulator("SET:C2_OFF") == "OK"

    assert emulator("GET:A ?") == "OFF,OFF"
    assert emulator("GET:A1 ?") == "OFF"
    assert emulator("GET:A2 ?") == "OFF"
    assert emulator("GET:B ?") == "OFF,OFF"
    assert emulator("GET:B1 ?") == "OFF"
    assert emulator("GET:B2 ?") == "OFF"
    assert emulator("GET:C ?") == "OFF,OFF"
    assert emulator("GET:C1 ?") == "OFF"
    assert emulator("GET:C2 ?") == "OFF"

    assert emulator(":CLOS:STAT?") == ""
    assert emulator("*STB?") == "0,0,0,0,0,0"


def test_mod(emulator):
    assert emulator("GET:MOD ?") == "N/A"
    assert emulator("SET:MOD IV") == "OK"
    assert emulator("GET:MOD ?") == "IV"
    assert emulator("SET:MOD CV") == "OK"
    assert emulator("GET:MOD ?") == "CV"
    assert emulator("SET:MOD CC") == "Err99"
    assert emulator("GET:MOD ?") == "CV"


def test_test_state(emulator):
    assert emulator("GET:TST ?") == "OFF"
    assert emulator("SET:TST ON") == "OK"
    assert emulator("GET:TST ?") == "ON"
    assert emulator("SET:TST OFF") == "OK"
    assert emulator("GET:TST ?") == "OFF"
