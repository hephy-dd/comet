from typing import Optional

from comet.driver.generic import InstrumentError
from comet.driver.generic.electrometer import Electrometer

__all__ = ['K6517B']


def parse_error(response: str):
    code, message = [token.strip() for token in response.split(',')][:2]
    return int(code), message.strip('\"')


class K6517B(Electrometer):

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

    # Electrometer

    def measure_voltage(self) -> float:
        return float(self.query(':MEAS:VOLT?'))

    def measure_current(self) -> float:
        return float(self.query(':MEAS:CURR?'))

    def measure_resistance(self) -> float:
        return float(self.query(':MEAS:RES?'))

    def measure_charge(self) -> float:
        return float(self.query(':MEAS:CHAR?'))

    # Helper

    def query(self, message: str) -> str:
        return self.resource.query(message).strip()

    def write(self, message: str) -> None:
        self.resource.write(message)
        self.query('*OPC?')
