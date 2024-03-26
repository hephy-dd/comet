from typing import Optional, Tuple

from comet.driver.generic import InstrumentError
from comet.driver.generic.lcr_meter import LCRMeter

__all__ = ['E4980A']


class E4980A(LCRMeter):

    FUNCTION_CPD = 'CPD'
    FUNCTION_CPQ = 'CPQ'
    FUNCTION_CPG = 'CPG'
    FUNCTION_CPRP = 'CPRP'
    FUNCTION_CSD = 'CSD'
    FUNCTION_CSQ = 'CSQ'
    FUNCTION_CSRS = 'CSRS'
    FUNCTION_LPD = 'LPD'
    FUNCTION_LPQ = 'LPQ'
    FUNCTION_LPG = 'LPG'
    FUNCTION_LPRP = 'LPRP'
    FUNCTION_LPRD = 'LPRD'
    FUNCTION_LSD = 'LSD'
    FUNCTION_LSQ = 'LSQ'
    FUNCTION_LSRS = 'LSRS'
    FUNCTION_LS = 'LS'
    FUNCTION_RD = 'RD'
    FUNCTION_RX = 'RX'
    FUNCTION_ZTD = 'ZTD'
    FUNCTION_ZTR = 'ZTR'
    FUNCTION_GB = 'GB'
    FUNCTION_YTD = 'YTD'
    FUNCTION_YTR = 'YTR'
    FUNCTION_VDID = 'VDID'

    def identify(self) -> str:
        return self.query('*IDN?')

    def reset(self) -> None:
        self.write('*RST')

    def clear(self) -> None:
        self.write('*CLS')

    # Beeper

    @property
    def beeper(self) -> bool:
        return bool(int(self.query(':SYST:BEEP:STAT?')))

    @beeper.setter
    def beeper(self, value: bool) -> None:
        self.write(f':SYST:BEEP:STAT {value:d}')

    # Error Queue

    def next_error(self) -> Optional[InstrumentError]:
        code, message = self.query(':SYST:ERR:NEXT?').split(',')[:2]
        if int(code):
            return InstrumentError(int(code), message.strip('\"\' '))
        return None

    # LCR Meter

    @property
    def function(self) -> str:
        return self.query(':FUNC:IMP:TYPE?')

    @function.setter
    def function(self, function: str) -> None:
        self.write(f':FUNC:IMP:TYPE {function}')

    @property
    def amplitude(self) -> float:
        return float(self.query(':VOLT:LEV?'))

    @amplitude.setter
    def amplitude(self, level: float) -> None:
        self.write(f':VOLT:LEV {level:E}')

    @property
    def frequency(self) -> float:
        return float(self.query(':FREQ:CW?'))

    @frequency.setter
    def frequency(self, frequency: float) -> None:
        self.write(f':FREQ:CW {frequency:E}')

    # TODO
    def set_measurement_time(self, apterture: str) -> None:
        self.write(f':APER {apterture}')

    @property
    def correction_length(self) -> int:
        return int(float(self.query(':CORR:LENG?')))

    @correction_length.setter
    def correction_length(self, meters: int) -> None:
        self.write(f':CORR:LENG {meters:d}')

    # Measurements

    def measure_impedance(self) -> Tuple[float, float]:
        first, second = self.query(':FETC:IMP:FORM?').split(',')[:2]
        return float(first), float(second)

    # Helper

    def query(self, message: str) -> str:
        return self.resource.query(message).strip()

    def write(self, message: str) -> None:
        self.resource.write(message)
        self.query('*OPC?')
