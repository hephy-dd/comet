import pytest
from io import StringIO
from unittest.mock import patch, MagicMock

from comet.station import default_resource_factory, Station


@pytest.fixture
def mock_resource_factory():
    def factory(config):
        mock_resource = MagicMock()
        mock_resource.__enter__.return_value = mock_resource
        mock_resource.query.return_value = "Keithley Model 2410"
        return mock_resource
    return factory


@patch("pyvisa.ResourceManager")
def test_default_resource_factory(mock_rm_cls):
    mock_rm = MagicMock()
    mock_resource = MagicMock()

    mock_rm_cls.return_value = mock_rm
    mock_rm.open_resource.return_value = mock_resource

    result = default_resource_factory({
        "visa_library": "@sim",
        "resource_name": "GPIB::1::INSTR",
        "termination": "\n",
        "timeout": 5.0
    })

    mock_rm_cls.assert_called_once_with("@sim")
    mock_rm.open_resource.assert_called_once_with(
        "GPIB::1::INSTR",
        read_termination="\n",
        write_termination="\n",
        timeout=5000  # 5.0 * 1000
    )
    assert result is mock_resource


def test_station():
    station = Station()
    assert station.instruments_config == {}


def test_station_from_config():
    station = Station.from_config({})
    assert station.instruments_config == {}
    station = Station.from_config({"instruments": {}})
    assert station.instruments_config == {}
    station = Station.from_config({"instruments": {"smu": {"resource_name": "GPIB::16::INSTR", "model": "keithley.k2410"}}})
    assert station.instruments_config == {"smu": {"resource_name": "GPIB::16::INSTR", "model": "keithley.k2410"}}


def test_station_from_file_json():
    station = Station.from_file(StringIO("\n"))
    assert station.instruments_config == {}
    station = Station.from_file(StringIO("{\"instruments\": {}}\n"))
    assert station.instruments_config == {}
    station = Station.from_file(StringIO("{\"instruments\": {\"smu\": {\"resource_name\": \"GPIB::16::INSTR\", \"model\": \"keithley.k2410\"}}}\n"))
    assert station.instruments_config == {"smu": {"resource_name": "GPIB::16::INSTR", "model": "keithley.k2410"}}


def test_station_from_file_yaml():
    station = Station.from_file(StringIO("\n"))
    assert station.instruments_config == {}
    station = Station.from_file(StringIO("instruments: {}\n"))
    assert station.instruments_config == {}
    station = Station.from_file(StringIO("instruments:\n  smu:\n    resource_name: GPIB::16::INSTR\n    model: keithley.k2410\n"))
    assert station.instruments_config == {"smu": {"resource_name": "GPIB::16::INSTR", "model": "keithley.k2410"}}


def test_station_context(mock_resource_factory):
    with Station(resource_factory=mock_resource_factory) as station:
        assert station._instruments == {}
    config = {"instruments": {"smu": {"resource_name": "GPIB::16::INSTR", "model": "keithley.k2410"}}}
    with Station.from_config(config, resource_factory=mock_resource_factory) as station:
        assert "smu" in station._instruments
        assert station.smu is station._instruments["smu"]
        assert station.smu.identify() == "Keithley Model 2410"


def test_instrument_attribute_is_readonly(mock_resource_factory):
    config = {"instruments": {"smu": {"resource_name": "GPIB::16::INSTR", "model": "keithley.k2410"}}}
    station = Station.from_config(config, resource_factory=mock_resource_factory)
    with pytest.raises(AttributeError):
        station.smu
    with station as st:
        with pytest.raises(AttributeError):
            st.smu = 42


def test_add_and_update_instrument(mock_resource_factory):
    station = Station(resource_factory=mock_resource_factory)
    station.add_instrument("smu", resource_name="GPIB::2::INSTR")
    assert "smu" in station.instruments_config
    station.update_instrument("smu", termination="\n", timeout=3.0)
    assert station.instruments_config["smu"]["timeout"] == 3.0
