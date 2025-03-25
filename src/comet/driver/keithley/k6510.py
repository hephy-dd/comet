import warnings
from typing import Optional

from comet.driver.generic import InstrumentError, RouteTerminalMixin
from comet.driver.generic.dmm import DigitalMultiMeter

__all__ = ["K6510"]


def parse_error(response: str) -> tuple[int, str]:
    code, message = [token.strip() for token in response.split(",")][:2]
    return int(code), message.strip('"')


class K6510(RouteTerminalMixin, DigitalMultiMeter):
    def identify(self) -> str:
        return self.query("*IDN?")

    def reset(self) -> None:
        self.write("*RST")
        self.query("*OPC?")

    def clear(self) -> None:
        self.write("*CLS")
        self.query("*OPC?")

    # Error queue

    def next_error(self) -> Optional[InstrumentError]:
        code, message = parse_error(self.query(":SYST:ERR:NEXT?"))
        if code:
            return InstrumentError(code, message)
        return None

    # Route Terminal

    @property
    def route_terminal(self) -> str:
        value = self.query(":ROUT:TERM?")
        return {
            "FRON": self.ROUTE_TERMINAL_FRONT,
            "REAR": self.ROUTE_TERMINAL_REAR,
        }[value]

    @route_terminal.setter
    def route_terminal(self, route_terminal: str) -> None:
        warnings.warn("DAQ6510 does not support setting terminals.", UserWarning)

    # DigitalMultiMeter

    def measure_voltage(self) -> float:
        return float(self.query(":MEAS:VOLT?"))

    def measure_current(self) -> float:
        return float(self.query(":MEAS:CURR?"))

    # Helper

    def query(self, message: str) -> str:
        return self.resource.query(message).strip()

    def write(self, message: str) -> None:
        self.resource.write(message)
