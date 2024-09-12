from typing import Optional

from comet.driver.generic import InstrumentError
from comet.driver.generic import RouteTerminalMixin
from comet.driver.generic.source_meter_unit import SourceMeterUnit

from .k2400 import parse_error

__all__ = ["K2470"]


class K2470(RouteTerminalMixin, SourceMeterUnit):
    def identify(self) -> str:
        return self.query("*IDN?")

    def reset(self) -> None:
        self.write("*RST")

    def clear(self) -> None:
        self.write("*CLS")

    # Error queue

    def next_error(self) -> Optional[InstrumentError]:
        code, message = parse_error(self.query(":SYST:ERR:NEXT?"))
        if code:
            return InstrumentError(code, message)
        return None

    # Route terminal

    @property
    def route_terminal(self) -> str:
        value = self.query(":ROUT:TERM?")
        return {
            "FRON": self.ROUTE_TERMINAL_FRONT,
            "REAR": self.ROUTE_TERMINAL_REAR,
        }[value]

    @route_terminal.setter
    def route_terminal(self, route_terminal: str) -> None:
        value = {
            self.ROUTE_TERMINAL_FRONT: "FRON",
            self.ROUTE_TERMINAL_REAR: "REAR",
        }[route_terminal]
        self.write(f":ROUT:TERM {value}")

    # Source meter unit

    @property
    def output(self) -> bool:
        value = int(float(self.query(":OUTP:STAT?")))
        return {
            0: self.OUTPUT_OFF,
            1: self.OUTPUT_ON,
        }[value]

    @output.setter
    def output(self, state: bool) -> None:
        value = {
            self.OUTPUT_OFF: "OFF",
            self.OUTPUT_ON: "ON",
        }[state]
        self.write(f":OUTP:STAT {value}")

    @property
    def function(self) -> str:
        value = self.query(":SOUR:FUNC:MODE?")
        return {
            "VOLT": self.FUNCTION_VOLTAGE,
            "CURR": self.FUNCTION_CURRENT,
        }[value]

    @function.setter
    def function(self, function: str) -> None:
        function_mode = {
            self.FUNCTION_VOLTAGE: "VOLT",
            self.FUNCTION_CURRENT: "CURR",
        }[function]
        self.write(f":SOUR:FUNC:MODE {function_mode}")
        sense_function = {
            self.FUNCTION_VOLTAGE: "CURR",
            self.FUNCTION_CURRENT: "VOLT",
        }[function]
        self.write(f":SENS:FUNC '{sense_function}'")

    # Voltage source

    @property
    def voltage_level(self) -> float:
        return float(self.query(":SOUR:VOLT:LEV?"))

    @voltage_level.setter
    def voltage_level(self, level: float) -> None:
        self.write(f":SOUR:VOLT:LEV {level:E}")

    @property
    def voltage_range(self) -> float:
        return float(self.query(":SOUR:VOLT:RANG?"))

    @voltage_range.setter
    def voltage_range(self, level: float) -> None:
        self.write(f":SOUR:VOLT:RANG {level:E}")

    @property
    def voltage_compliance(self) -> float:
        return float(self.query(":SOUR:CURR:VLIM:LEV?"))

    @voltage_compliance.setter
    def voltage_compliance(self, level: float) -> None:
        self.write(f":SOUR:CURR:VLIM:LEV {level:.3E}")

    @property
    def voltage_compliance_tripped(self) -> bool:
        return bool(int(self.query(":SOUR:VOLT:ILIM:LEV:TRIP?")))

    # Current source

    @property
    def current_level(self) -> float:
        return float(self.query(":SOUR:CURR:LEV?"))

    @current_level.setter
    def current_level(self, level: float) -> None:
        self.write(f":SOUR:CURR:LEV {level:E}")

    @property
    def current_range(self) -> float:
        return float(self.query(":SOUR:CURR:RANG?"))

    @current_range.setter
    def current_range(self, level: float) -> None:
        self.write(f":SOUR:CURR:RANG {level:E}")

    @property
    def current_compliance(self) -> float:
        return float(self.query(":SOUR:VOLT:ILIM:LEV?"))

    @current_compliance.setter
    def current_compliance(self, level: float) -> None:
        self.write(f":SOUR:VOLT:ILIM:LEV {level:.3E}")

    @property
    def current_compliance_tripped(self) -> bool:
        return bool(int(self.query(":SOUR:CURR:VLIM:LEV:TRIP?")))

    @property
    def compliance_tripped(self) -> bool:
        return bool(int(self.query(":SOUR:CURR:VLIM:LEV:TRIP?"))) or (
            bool(int(self.query(":SOUR:VOLT:ILIM:LEV:TRIP?")))
        )

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
        self.query("*OPC?")
