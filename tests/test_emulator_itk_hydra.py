import pytest

from comet.emulator.itk.hydra import HydraEmulator


@pytest.fixture
def emulator():
    return HydraEmulator()


def test_basic(emulator):
    assert emulator("identify") == "Hydra 0 0 0 0"
    assert emulator("getversion") == "1.0"
    assert emulator("version") == "1.0"
    assert emulator("getmacadr") == "00:00:00:00:00:00"
    assert emulator("getserialno") == "01010042"
    assert emulator("getproductid") == "hydra"
    assert emulator("getcputemp") == "40.0"
    assert emulator("reset") is None


def test_status(emulator):
    assert emulator("status") == "24"
    assert emulator("st") == "24"

    assert emulator("1 nstatus") == "24"
    assert emulator("1 nst") == "24"
    assert emulator("1 est") == "24"
    assert emulator("1 ast") == "24"

    assert emulator("2 nstatus") == "24"
    assert emulator("2 nst") == "24"
    assert emulator("2 est") == "24"
    assert emulator("2 ast") == "24"


def test_position(emulator):
    assert float(emulator("1 np")) == 0.0
    assert float(emulator("2 np")) == 0.0
    assert emulator("10 20 m") is None
    assert float(emulator("1 np")) == 10.0
    assert float(emulator("2 np")) == 20.0
    assert emulator("10 -10 r") is None
    assert float(emulator("1 np")) == 20.0
    assert float(emulator("2 np")) == 10.0
    assert emulator("1 nrandmove") is None
    assert float(emulator("1 np")) != 20.0
    assert float(emulator("2 np")) == 10.0
    assert emulator("2 nrandmove") is None
    assert float(emulator("1 np")) != 20.0
    assert float(emulator("2 np")) != 10.0


def test_calibration(emulator):
    assert emulator("1 ncalibrate") is None
    assert emulator("2 ncal") is None
    assert emulator("1 nrangemeasure") is None
    assert emulator("2 nrm") is None
