from comet.driver.generic import InstrumentError

MESSAGE = "Nobody expects the Spanish Inquisition!"


def test_instrument_error():
    err = InstrumentError(42, MESSAGE)
    assert err.code == 42
    assert err.message == MESSAGE
    assert repr(err) == f"InstrumentError(42, '{MESSAGE}')"
