from typing import Optional

from comet.driver.generic import SourceMeterUnit
from comet.driver.generic import InstrumentError

from .k2400 import parse_error

__all__ = ['K2470']


class K2470(SourceMeterUnit):

    def identify(self) -> str:
        return self.query('*IDN?')

    def reset(self) -> None:
        self.write('*RST')
        self.waitcomplete()

    def clear(self) -> None:
        self.write('*CLS')
        self.waitcomplete()

    def next_error(self) -> Optional[InstrumentError]:
        code, message = parse_error(self.query(':SYST:ERR:NEXT?'))
        if code:
            return InstrumentError(code, message)
        return None

    def get_terminal(self) -> str:
        value = self.query(':ROUT:TERM?')
        return {
            'FRON': self.TERMINAL_FRONT,
            'REAR': self.TERMINAL_REAR
        }[value]

    def set_terminal(self, terminal: str) -> None:
        value = {
            self.TERMINAL_FRONT: 'FRON',
            self.TERMINAL_REAR: 'REAR'
        }[terminal]
        self.write(f':ROUT:TERM {value}')
        self.waitcomplete()

    def get_output(self) -> bool:
        value = int(float(self.query(':OUTP:STAT?')))
        return {
            0: self.OUTPUT_OFF,
            1: self.OUTPUT_ON
        }[value]

    def set_output(self, state: bool) -> None:
        value = {
            self.OUTPUT_OFF: 0,
            self.OUTPUT_ON: 1
        }[state]
        self.write(f':OUTP:STAT {value:d}')
        self.waitcomplete()

    def get_function(self) -> str:
        value = self.query(':SOUR:FUNC:MODE?')
        return {
            'VOLT': self.FUNCTION_VOLTAGE,
            'CURR': self.FUNCTION_CURRENT
        }[value]

    def set_function(self, function: str) -> None:
        value = {
            self.FUNCTION_VOLTAGE: 'VOLT',
            self.FUNCTION_CURRENT: 'CURR'
        }[function]
        self.write(f':SOUR:FUNC:MODE {value}')
        self.waitcomplete()
        sense_function = {
            self.FUNCTION_VOLTAGE: 'CURR',
            self.FUNCTION_CURRENT: 'VOLT'
        }[function]
        self.write(f':SENS:FUNC \'{sense_function}\'')
        self.waitcomplete()

    def get_voltage(self) -> float:
        return float(self.query(':SOUR:VOLT:LEV?'))

    def set_voltage(self, level: float) -> None:
        self.write(f':SOUR:VOLT:LEV {level:E}')
        self.waitcomplete()

    def get_voltage_range(self) -> float:
        return float(self.query(':SOUR:VOLT:RANG?'))

    def set_voltage_range(self, level: float) -> None:
        self.write(f':SOUR:VOLT:RANG {level:E}')
        self.waitcomplete()

    def get_current(self) -> float:
        return float(self.query(':SOUR:CURR:LEV?'))

    def set_current(self, level: float) -> None:
        self.write(f':SOUR:CURR:LEV {level:E}')
        self.waitcomplete()

    def get_current_range(self) -> float:
        return float(self.query(':SOUR:CURR:RANG?'))

    def set_current_range(self, level: float) -> None:
        self.write(f':SOUR:CURR:RANG {level:E}')
        self.waitcomplete()

    def read_voltage(self) -> float:
        return float(self.query(':MEAS:VOLT?'))

    def read_current(self) -> float:
        return float(self.query(':MEAS:CURR?'))

    # Helper

    def query(self, message: str) -> str:
        return self.resource.query(message).strip()

    def write(self, message: str) -> None:
        self.resource.write(message)

    def waitcomplete(self) -> None:
        self.query('*OPC?')

