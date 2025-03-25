from typing import Optional

from comet.driver.generic import BeeperMixin
from comet.driver.generic import InstrumentError
from comet.driver.generic.dmm import DigitalMultiMeter

__all__ = ["K2700"]


def parse_error(response: str) -> tuple[int, str]:
    code, message = [token.strip() for token in response.split(",")][:2]
    return int(code), message.strip('"')


class K2700(BeeperMixin, DigitalMultiMeter):
    def identify(self) -> str:
        return self.query("*IDN?")

    def reset(self) -> None:
        self.write("*RST")
        self.query("*OPC?")

    def clear(self) -> None:
        self.write("*CLS")
        self.query("*OPC?")

    # Beeper

    @property
    def beeper(self) -> bool:
        return bool(int(self.query(":SYST:BEEP:STAT?")))

    @beeper.setter
    def beeper(self, value: bool) -> None:
        self.write(f":SYST:BEEP:STAT {value:d}")
        self.query("*OPC?")

    # Error queue

    def next_error(self) -> Optional[InstrumentError]:
        code, message = parse_error(self.query(":SYST:ERR:NEXT?"))
        if code:
            return InstrumentError(code, message)
        return None

    # Measurements

    def measure_voltage(self) -> float:
        return float(self.query(":MEAS:VOLT?"))

    def measure_current(self) -> float:
        return float(self.query(":MEAS:CURR?"))

    # Helper

    def query(self, message: str) -> str:
        return self.resource.query(message).strip()

    def write(self, message: str) -> None:
        self.resource.write(message)
