import pytest

from comet.emulator.router.router import NoRouteError, Router
from comet.emulator.router.scpi import scpi


def test_command():
    class Target:
        @scpi(":SOURce:VOLTage")
        def voltage(self, value):
            return value

    assert Router(Target()).dispatch(":SOURCE:VOLTAGE 10") == "10"


@pytest.mark.parametrize(
    "message",
    [
        ":SOURCE:VOLTAGE?",
        ":SOUR:VOLT?",
        ":SOURC:VOLTA?",
    ],
)
def test_abbreviations(message):
    class Target:
        @scpi(":SOURce:VOLTage?")
        def voltage(self):
            return "10"

    assert Router(Target()).dispatch(message) == "10"


def test_query_and_command_are_different():
    class Target:
        @scpi(":SOURce:VOLTage?")
        def voltage(self):
            return "10"

    with pytest.raises(NoRouteError):
        Router(Target()).dispatch(":SOURCE:VOLTAGE")


def test_arguments():
    class Target:
        @scpi(":CONFigure:VOLTage")
        def configure(self, range_, resolution):
            return range_, resolution

    result = Router(Target()).dispatch(":CONF:VOLT 10,0.001")

    assert result == ("10", "0.001")


def test_invalid_abbreviation():
    class Target:
        @scpi(":MEASure:VOLTage?")
        def measure(self):
            return "10"

    with pytest.raises(NoRouteError):
        Router(Target()).dispatch(":MEA:VOLT?")
