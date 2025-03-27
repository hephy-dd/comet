from typing import Optional

from comet.driver.generic import BeeperMixin
from comet.driver.generic import InstrumentError
from comet.driver.generic.dmm import DigitalMultiMeter

__all__ = ["K2700"]


def parse_error(response: str) -> tuple[int, str]:
    code, message = [token.strip() for token in response.split(",")][:2]
    return int(code), message.strip('"')


class K2700(BeeperMixin, DigitalMultiMeter):
    """Driver for Keithley 2700 digital multimeter."""
    def __init__(self, resource) -> None:
        super().__init__(resource)
        self._sense_function: Optional[str] = None
        self._format_elements: Optional[str] = None

    def identify(self) -> str:
        return self._query("*IDN?")

    def reset(self) -> None:
        self._write("*RST")
        self._query("*OPC?")
        self._sense_function = None
        self._format_elements = None

    def clear(self) -> None:
        self._write("*CLS")
        self._query("*OPC?")

    # Beeper

    @property
    def beeper(self) -> bool:
        return bool(int(self._query(":SYST:BEEP:STAT?")))

    @beeper.setter
    def beeper(self, value: bool) -> None:
        self._write(f":SYST:BEEP:STAT {value:d}")
        self._query("*OPC?")

    # Error queue

    def next_error(self) -> Optional[InstrumentError]:
        code, message = parse_error(self._query(":SYST:ERR:NEXT?"))
        if code:
            return InstrumentError(code, message)
        return None

    # Measurements

    def measure_voltage(self) -> float:
        self._ensure_sense_function("VOLT:DC")
        self._ensure_format_elements("READ")
        return float(self._query(":READ?"))

    def measure_current(self) -> float:
        self._ensure_sense_function("CURR:DC")
        self._ensure_format_elements("READ")
        return float(self._query(":READ?"))

    # Helper

    def _query(self, message: str) -> str:
        return self.resource.query(message).strip()

    def _write(self, message: str) -> None:
        self.resource.write(message)

    def _ensure_sense_function(self, function: str) -> None:
        if self._sense_function != function:
            self._write(f":SENS:FUNC '{function}'")
            self._sense_function = function

    def _ensure_format_elements(self, elements: str) -> None:
        if self._format_elements != elements:
            self._write(f":FORM:ELEM {elements}")
            self._format_elements = elements
