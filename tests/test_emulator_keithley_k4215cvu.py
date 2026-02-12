import math
import pytest

from comet.emulator.keithley.k4215cvu import K4215CVUEmulator


@pytest.fixture
def emulator():
    return K4215CVUEmulator()


def assert_two_floats_csv(s: str):
    parts = s.split(",")
    assert len(parts) == 2
    a = float(parts[0])
    b = float(parts[1])
    assert math.isfinite(a)
    assert math.isfinite(b)
    return a, b


def test_basic_ieee488(emulator):
    # *IDN? should return identity string
    assert emulator("*IDN?") == "KEITHLEY INSTRUMENTS,KI4200A,1489223,V1.14 (Emulator)"

    # *RST/*CLS/*BC should not return anything
    assert emulator("*RST") is None
    assert emulator("*CLS") is None
    assert emulator("*BC") is None


def test_unknown_command_pushes_scpi_error(emulator):
    # Send something invalid
    assert emulator(":CVU:NOPE 1") is None

    # Typical SCPI: -113 Undefined header
    assert emulator(":ERROR:LAST:GET") == '-113, "Undefined header"'

    # Clearing last error should pop it
    assert emulator(":ERROR:LAST:CLEAR") is None
    assert emulator(":ERROR:LAST:GET") == '0, "No error"'


def test_measz_returns_two_floats_output_off(emulator):
    # Ensure output is off (default or explicitly)
    assert emulator(":CVU:OUTPUT 0") is None
    s = str(emulator(":CVU:MEASZ?"))
    a, b = assert_two_floats_csv(s)
    # Off state should be near-zero-ish but not necessarily exactly zero
    assert abs(a) < 1e-2
    assert abs(b) < 1e-2


def test_measz_returns_two_floats_output_on(emulator):
    assert emulator(":CVU:OUTPUT 1") is None
    s = str(emulator(":CVU:MEASZ?"))
    assert_two_floats_csv(s)


@pytest.mark.parametrize("cmd,val,query,default", [
    (":CVU:ACV {}", "1.000000E-01", ":CVU:ACV?", 0.1),
    (":CVU:FREQ {}", "100000", ":CVU:FREQ?", 100000),
    (":CVU:DCV {}", "0.000E+00", ":CVU:DCV?", 0.0),
    (":CVU:DCV:OFFSET {}", "0.000E+00", ":CVU:DCV:OFFSET?", 0.0),
])
def test_getters_setters_roundtrip_common(emulator, cmd, val, query, default):
    # check getter exists and returns something parseable
    assert emulator(query) == val
    # set
    assert emulator(cmd.format(val)) is None
    assert emulator(query) == val


def test_speed_roundtrip(emulator):
    assert emulator(":CVU:SPEED 3,1.000E+00,1.000E+00,1.000E-01") is None
    s = str(emulator(":CVU:SPEED?"))
    parts = s.split(",")
    assert len(parts) == 4
    assert int(parts[0]) in (0, 1, 2, 3)
    assert float(parts[1])
    assert float(parts[2])
    assert float(parts[3])


@pytest.mark.parametrize("val", ["1", "2"])
def test_config_acvhi_roundtrip(emulator, val):
    assert emulator(f":CVU:CONFIG:ACVHI {val}") is None
    assert emulator(":CVU:CONFIG:ACVHI?") == val


@pytest.mark.parametrize("val", ["1", "2"])
def test_config_dcvhi_roundtrip(emulator, val):
    assert emulator(f":CVU:CONFIG:DCVHI {val}") is None
    assert emulator(":CVU:CONFIG:DCVHI?") == val


def test_data_type_error(emulator):
    # Provide non-numeric where numeric is expected
    assert emulator(":CVU:ACV bananas") is None
    err = emulator(":ERROR:LAST:GET")
    assert err == '-104, "Data type error"'


def test_data_out_of_range_error(emulator):
    # ACV out of range (valid is 0.01..1.0)
    assert emulator(":CVU:ACV 10") is None
    err = emulator(":ERROR:LAST:GET")
    assert err == '-222, "Data out of range"'


def test_correction_roundtrip(emulator):
    assert emulator(":CVU:CORRECT 1,0,1") is None
    assert emulator(":CVU:CORRECT?") == "1,0,1"


def test_length_roundtrip(emulator):
    assert emulator(":CVU:LENGTH 1.5") is None
    assert emulator(":CVU:LENGTH?") == "1.5"
