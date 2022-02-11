from typing import Optional

from comet.driver.generic import SourceMeterUnit
from comet.driver.generic import InstrumentError
from comet.driver.generic import RouteTerminalMixin

from .k2400 import parse_error

__all__ = ['K2470']


class K2470(RouteTerminalMixin, SourceMeterUnit):

    def identify(self) -> str:
        return self.query('*IDN?')

    def reset(self) -> None:
        self.write('*RST')

    def clear(self) -> None:
        self.write('*CLS')

    # Error queue

    def next_error(self) -> Optional[InstrumentError]:
        code, message = parse_error(self.query(':SYST:ERR:NEXT?'))
        if code:
            return InstrumentError(code, message)
        return None

    # Route terminal

    @property
    def route_terminal(self) -> str:
        value = self.query(':ROUT:TERM?')
        return {
            'FRON': self.ROUTE_TERMINAL_FRONT,
            'REAR': self.ROUTE_TERMINAL_REAR
        }[value]

    @route_terminal.setter
    def route_terminal(self, route_terminal: str) -> None:
        value = {
            self.ROUTE_TERMINAL_FRONT: 'FRON',
            self.ROUTE_TERMINAL_REAR: 'REAR'
        }[route_terminal]
        self.write(f':ROUT:TERM {value}')

    # Source meter unit

    @property
    def output(self) -> bool:
        value = int(float(self.query(':OUTP:STAT?')))
        return {
            0: self.OUTPUT_OFF,
            1: self.OUTPUT_ON
        }[value]

    @output.setter
    def output(self, state: bool) -> None:
        value = {
            self.OUTPUT_OFF: 'OFF',
            self.OUTPUT_ON: 'ON'
        }[state]
        self.write(f':OUTP:STAT {value}')

    @property
    def function(self) -> str:
        value = self.query(':SOUR:FUNC:MODE?')
        return {
            'VOLT': self.FUNCTION_VOLTAGE,
            'CURR': self.FUNCTION_CURRENT
        }[value]

    @function.setter
    def function(self, function: str) -> None:
        function_mode = {
            self.FUNCTION_VOLTAGE: 'VOLT',
            self.FUNCTION_CURRENT: 'CURR'
        }[function]
        self.write(f':SOUR:FUNC:MODE {function_mode}')
        sense_function = {
            self.FUNCTION_VOLTAGE: 'CURR',
            self.FUNCTION_CURRENT: 'VOLT'
        }[function]
        self.write(f':SENS:FUNC \'{sense_function}\'')

    def get_voltage(self) -> float:
        return float(self.query(':SOUR:VOLT:LEV?'))

    def set_voltage(self, level: float) -> None:
        self.write(f':SOUR:VOLT:LEV {level:E}')

    def get_voltage_range(self) -> float:
        return float(self.query(':SOUR:VOLT:RANG?'))

    def set_voltage_range(self, level: float) -> None:
        self.write(f':SOUR:VOLT:RANG {level:E}')

    def set_voltage_compliance(self, level: float) -> None:
        self.write(f':SOUR:CURR:VLIM:LEV {level:.3E}')

    def get_current(self) -> float:
        return float(self.query(':SOUR:CURR:LEV?'))

    def set_current(self, level: float) -> None:
        self.write(f':SOUR:CURR:LEV {level:E}')

    def get_current_range(self) -> float:
        return float(self.query(':SOUR:CURR:RANG?'))

    def set_current_range(self, level: float) -> None:
        self.write(f':SOUR:CURR:RANG {level:E}')

    def set_current_compliance(self, level: float) -> None:
        self.write(f':SOUR:VOLT:ILIM:LEV {level:.3E}')

    def compliance_tripped(self) -> bool:
        return bool(int(self.query(':SOUR:CURR:VLIM:LEV:TRIP?'))) or \
            bool(int(self.query(':SOUR:VOLT:ILIM:LEV:TRIP?')))

    def measure_voltage(self) -> float:
        return float(self.query(':MEAS:VOLT?'))

    def measure_current(self) -> float:
        return float(self.query(':MEAS:CURR?'))

    # Helper

    def query(self, message: str) -> str:
        return self.resource.query(message).strip()

    def write(self, message: str) -> None:
        self.resource.write(message)
        self.query('*OPC?')
