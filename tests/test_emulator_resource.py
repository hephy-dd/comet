import pytest

from comet.emulator import open_emulator


def test_resource():
    with open_emulator("keithley.k2410") as res:
        assert res.encoding == "ascii"
        assert res.query("*IDN?") == "Keithley Inc., Model 2410, 43768438, v1.0 (Emulator)"


def test_resource_latin1():
    with open_emulator("nkt_photonics.pilas") as res:
        res.encoding = "latin-1"
        assert res.query("lht?") == "laser head temp.:\t     25.0 °C"
