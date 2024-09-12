"""Rohde Schwarz SMA100B signal generator emulator"""

from comet.emulator import Emulator
from comet.emulator import message, run
from comet.emulator.utils import Error


__all__ = ["SMA100BEmulator"]


class SMA100BEmulator(Emulator):
    IDENTITY: str = "Rohde&Schwarz,SMA100B,1419.8888K02/120399,5.00.122.24 SP1"

    def __init__(self) -> None:
        super().__init__()

        self.error_queue: list[Error] = []

        self.frequency_mode: str = "FIXed"
        self.frequency: float = 1e10
        self.power: float = 0
        self.output: bool = False

    @message(r"^\*IDN\?$")
    def identify(self) -> str:
        return self.IDENTITY

    @message(r"^\*RST$")
    def set_reset(self) -> None:
        self.average_count = 100
        self.wavelength = 370

    @message(r"^\*CLS$")
    def set_clear(self) -> None:
        self.error_queue.clear()

    @message(r"^:?SYST(?:em)?:ERR(?::NEXT)?\?$")
    def get_system_error_next(self) -> str:
        if self.error_queue:
            error = self.error_queue.pop(0)
        else:
            error = Error(0, "no error")
        return f'{error.code}, "{error.message}"'

    @message(r"^(?:SOUR(?:ce)?1)?:FREQ(?:uency)?:MODE\?$")
    def get_frequency_mode(self) -> str:
        return self.frequency_mode

    @message(r"^(?:SOUR(?:ce)?1)?:FREQ(?:uency)?:MODE (\w+)$")
    def set_frequency_mode(self, mode) -> None:
        self.frequency_mode = mode

    @message(r"^(?:SOUR(?:ce)?1)?:FREQuency:(?:CW|FIX(?:ed)?)\?$")
    def get_frequency(self) -> float:
        return self.frequency

    @message(r"^(?:SOUR(?:ce)?1)?:FREQuency:(?:CW|FIX(?:ed)?) ([\d.]+(?:[eE][+-]?\d+)?)$")
    def set_frequency(self, frequency) -> None:
        frequency = float(frequency)
        if frequency < 8e3 or frequency > 12.75e9:
            self.error_queue.append(Error(222, "Parameter Data Out of Range"))
        else:
            self.frequency = frequency

    @message(r"^(?:SOUR(?:ce)?1)?:POW(?:er)?:POW(?:er)?\?$")
    def get_power(self) -> float:
        return self.power

    @message(r"^(?:SOUR(?:ce)?1)?:POW(?:er)?:POW(?:er)? ([+-]?[\d.]+(?:[eE][+-]?\d+)?)$")
    def set_power(self, power) -> None:
        power = float(power)
        if power < -145 or power > 40:
            self.error_queue.append(Error(222, "Parameter Data Out of Range"))
        else:
            self.power = power

    @message(r"^(?:SOUR(?:ce)?1:)?OUTP(?:ut)?:STAT(?:e)?\?$")
    def get_output(self) -> str:
        return "1" if self.output else "0"

    @message(r"^(?:SOUR(?:ce)?1:)?OUTP(?:ut)?:STAT(?:e)? (ON|OFF)$")
    def set_output(self, state) -> None:
        self.output = True if state == "ON" else False


if __name__ == "__main__":
    run(SMA100BEmulator())
