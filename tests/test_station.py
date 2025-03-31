from comet.station import Station


def test_station():
    station = Station()
    assert station.instruments_config == {}


def test_station_from_config():
    station = Station.from_config({})
    assert station.instruments_config == {}
    station = Station.from_config({"instruments": {}})
    assert station.instruments_config == {}
    station = Station.from_config({"instruments": {"smu": {"resource_name": "GPIB::16::INSTR"}}})
    assert station.instruments_config == {"smu": {"resource_name": "GPIB::16::INSTR"}}


def test_station_context():
    with Station.from_config({}) as station:
        assert station.instruments == {}
