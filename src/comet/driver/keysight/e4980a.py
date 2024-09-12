from typing import Optional

from comet.driver.generic import InstrumentError
from comet.driver.generic.lcr_meter import LCRMeter

__all__ = ["E4980A"]


class E4980A(LCRMeter):
    FUNCTION_CPD: str = "CPD"
    FUNCTION_CPQ: str = "CPQ"
    FUNCTION_CPG: str = "CPG"
    FUNCTION_CPRP: str = "CPRP"
    FUNCTION_CSD: str = "CSD"
    FUNCTION_CSQ: str = "CSQ"
    FUNCTION_CSRS: str = "CSRS"
    FUNCTION_LPD: str = "LPD"
    FUNCTION_LPQ: str = "LPQ"
    FUNCTION_LPG: str = "LPG"
    FUNCTION_LPRP: str = "LPRP"
    FUNCTION_LPRD: str = "LPRD"
    FUNCTION_LSD: str = "LSD"
    FUNCTION_LSQ: str = "LSQ"
    FUNCTION_LSRS: str = "LSRS"
    FUNCTION_LS: str = "LS"
    FUNCTION_RD: str = "RD"
    FUNCTION_RX: str = "RX"
    FUNCTION_ZTD: str = "ZTD"
    FUNCTION_ZTR: str = "ZTR"
    FUNCTION_GB: str = "GB"
    FUNCTION_YTD: str = "YTD"
    FUNCTION_YTR: str = "YTR"
    FUNCTION_VDID: str = "VDID"

    def identify(self) -> str:
        return self.query("*IDN?")

    def reset(self) -> None:
        self.write("*RST")

    def clear(self) -> None:
        self.write("*CLS")

    # Beeper

    @property
    def beeper(self) -> bool:
        return bool(int(self.query(":SYST:BEEP:STAT?")))

    @beeper.setter
    def beeper(self, value: bool) -> None:
        self.write(f":SYST:BEEP:STAT {value:d}")

    # Error Queue

    def next_error(self) -> Optional[InstrumentError]:
        code, message = self.query(":SYST:ERR:NEXT?").split(",")[:2]
        if int(code):
            return InstrumentError(int(code), message.strip("\"' "))
        return None

    # LCR Meter

    @property
    def function(self) -> str:
        return self.query(":FUNC:IMP:TYPE?")

    @function.setter
    def function(self, function: str) -> None:
        self.write(f":FUNC:IMP:TYPE {function}")

    @property
    def amplitude(self) -> float:
        return float(self.query(":VOLT:LEV?"))

    @amplitude.setter
    def amplitude(self, level: float) -> None:
        self.write(f":VOLT:LEV {level:E}")

    @property
    def frequency(self) -> float:
        return float(self.query(":FREQ:CW?"))

    @frequency.setter
    def frequency(self, frequency: float) -> None:
        self.write(f":FREQ:CW {frequency:E}")

    # TODO
    def set_measurement_time(self, apterture: str) -> None:
        self.write(f":APER {apterture}")

    @property
    def correction_length(self) -> int:
        return int(float(self.query(":CORR:LENG?")))

    @correction_length.setter
    def correction_length(self, meters: int) -> None:
        self.write(f":CORR:LENG {meters:d}")

    # Measurements

    def measure_impedance(self) -> tuple[float, float]:
        first, second = self.query(":FETC:IMP:FORM?").split(",")[:2]
        return float(first), float(second)

    # Helper

    def query(self, message: str) -> str:
        return self.resource.query(message).strip()

    def write(self, message: str) -> None:
        self.resource.write(message)
        self.query("*OPC?")
