from typing import Optional, Tuple

from comet.driver.generic import LCRMeter
from comet.driver.generic import InstrumentError

__all__ = ['E4980A']


class E4980A(LCRMeter):

    FUNCTION_CPD = 'CPD'
    FUNCTION_CPRP = 'CPRP'

    def identify(self) -> str:
        return self.query('*IDN?')

    def reset(self) -> None:
        self.write('*RST')
        self.waitcomplete()

    def clear(self) -> None:
        self.write('*CLS')
        self.waitcomplete()

    def next_error(self) -> Optional[InstrumentError]:
        code, message = self.query(':SYST:ERR:NEXT?').split(',')[:2]
        if int(code):
            return InstrumentError(int(code), message.strip('\"\' '))
        return None

    def set_mute(self, state: bool) -> None:
        self.write(f':SYST:BEEP:STAT {state:d}')
        self.waitcomplete()

    def get_function(self) -> str:
        value = self.query(':FUNC:IMP:TYPE?')
        return {
            'CPD': self.FUNCTION_CPD,
            'CPRP': self.FUNCTION_CPRP
        }[value]

    def set_function(self, function: str) -> None:
        value = {
            self.FUNCTION_CPD: 'CPD',
            self.FUNCTION_CPRP: 'CPRP'
        }[function]
        self.write(f':FUNC:IMP:TYPE {value}')
        self.waitcomplete()

    def get_amplitude(self) -> str:
        return float(self.query(':VOLT:LEV?'))

    def set_amplitude(self, level: float) -> None:
        self.write(f':VOLT:LEV {level:E}')
        self.waitcomplete()

    def get_frequency(self) -> str:
        return float(self.query(':FREQ:CW?'))

    def set_frequency(self, frequency: float) -> None:
        self.write(f':FREQ:CW {frequency:E}')
        self.waitcomplete()

    def set_measurement_time(self, apterture: str) -> None:
        self.write(f':APER {apterture}')
        self.waitcomplete()

    def set_correction_length(self, meters: int) -> None:
        self.write(f':CORR:LENG {meters:d}')
        self.waitcomplete()

    def read(self) -> Tuple[float, float]:
        values = self.query(':FETC:IMP:FORM?').split(',')[:2]
        return tuple(map(float, values))

    # Helper

    def query(self, message: str) -> str:
        return self.resource.query(message).strip()

    def write(self, message: str) -> None:
        self.resource.write(message)

    def waitcomplete(self) -> None:
        self.query('*OPC?')
