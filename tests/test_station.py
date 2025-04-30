from io import StringIO

from comet.station import Station


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


def test_station_context():
    with Station.from_config({}) as station:
        assert station.instruments == {}
