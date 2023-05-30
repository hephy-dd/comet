import pytest

from comet.emulator.keithley.k2657a import K2657AEmulator


@pytest.fixture
def emulator():
    return K2657AEmulator()


def test_basic(emulator):
    assert emulator("*IDN?") == "Keithley Inc., Model 2657A, 43768438, v1.0 (Emulator)"
    assert emulator("*RST") is None
    assert emulator("*CLS") is None
    assert emulator("*OPC?") == "1"
    assert emulator("*WAI") is None


def test_source_output(emulator):
    assert float(emulator("print(smua.source.output)")) == 0
    assert emulator("smua.source.output = 1") is None
    assert float(emulator("print(smua.source.output)")) == 1
    assert emulator("smua.source.output = 0") is None
    assert float(emulator("print(smua.source.output)")) == 0
    assert emulator("smua.source.output = smua.OUTPUT_ON") is None
    assert float(emulator("print(smua.source.output)")) == 1
    assert emulator("smua.source.output = smua.OUTPUT_OFF") is None
    assert float(emulator("print(smua.source.output)")) == 0


def test_source_function(emulator):
    assert float(emulator("print(smua.source.func)")) == 1
    assert emulator("smua.source.func = 0") is None
    assert float(emulator("print(smua.source.func)")) == 0
    assert emulator("smua.source.func = 1") is None
    assert float(emulator("print(smua.source.func)")) == 1
    assert emulator("smua.source.func = smua.OUTPUT_DCAMPS") is None
    assert float(emulator("print(smua.source.output)")) == 0
    assert emulator("smua.source.func = smua.OUTPUT_DCVOLTS") is None
    assert float(emulator("print(smua.source.func)")) == 1


def test_source_levelv(emulator):
    assert float(emulator(f"print(smua.source.levelv)")) == 0
    assert emulator("smua.source.levelv = 420") is None
    assert float(emulator(f"print(smua.source.levelv)")) == 420
    assert emulator("smua.source.levelv = 0") is None
    assert float(emulator(f"print(smua.source.levelv)")) == 0


def test_source_leveli(emulator):
    assert float(emulator(f"print(smua.source.leveli)")) == 0
    assert emulator("smua.source.leveli = 2.5E-6") is None
    assert float(emulator(f"print(smua.source.leveli)")) == 2.5E-6
    assert emulator("smua.source.leveli = 0") is None
    assert float(emulator(f"print(smua.source.leveli)")) == 0


def test_source_rangev(emulator):
    assert float(emulator("print(smua.source.rangev)")) == 0
    assert emulator("smua.source.rangev = 300") is None
    assert float(emulator("print(smua.source.rangev)")) == 300
    assert emulator("smua.source.rangev = 0") is None
    assert float(emulator("print(smua.source.rangev)")) == 0


def test_source_rangei(emulator):
    assert float(emulator("print(smua.source.rangei)")) == 0
    assert emulator("smua.source.rangei = 2.0E-3") is None
    assert float(emulator("print(smua.source.rangei)")) == 2.0E-3
    assert emulator("smua.source.rangei = 0") is None
    assert float(emulator("print(smua.source.rangei)")) == 0


def test_source_autorangev(emulator):
    assert float(emulator("print(smua.source.autorangev)")) == 1
    assert emulator("smua.source.autorangev = 0") is None
    assert float(emulator("print(smua.source.autorangev)")) == 0
    assert emulator("smua.source.autorangev = 1") is None
    assert float(emulator("print(smua.source.autorangev)")) == 1
    assert emulator("smua.source.autorangev = smua.AUTORANGE_OFF") is None
    assert float(emulator("print(smua.source.autorangev)")) == 0
    assert emulator("smua.source.autorangev = smua.AUTORANGE_ON") is None
    assert float(emulator("print(smua.source.autorangev)")) == 1


def test_source_autorangei(emulator):
    assert float(emulator("print(smua.source.autorangei)")) == 1
    assert emulator("smua.source.autorangei = 0") is None
    assert float(emulator("print(smua.source.autorangei)")) == 0
    assert emulator("smua.source.autorangei = 1") is None
    assert float(emulator("print(smua.source.autorangei)")) == 1
    assert emulator("smua.source.autorangei = smua.AUTORANGE_OFF") is None
    assert float(emulator("print(smua.source.autorangei)")) == 0
    assert emulator("smua.source.autorangei = smua.AUTORANGE_ON") is None
    assert float(emulator("print(smua.source.autorangei)")) == 1


def test_source_protectv(emulator):
    assert float(emulator("print(smua.source.protectv)")) == 0
    assert emulator("smua.source.protectv = 300") is None
    assert float(emulator("print(smua.source.protectv)")) == 300
    assert emulator("smua.source.protectv = 0") is None
    assert float(emulator("print(smua.source.protectv)")) == 0
