import random
import time

from comet.emulator import IEC60488Emulator, message, run
from comet.emulator.utils import Error


class K6514Emulator(IEC60488Emulator):

    IDENTITY: str = "Keithley Inc., Model 5614, 43768438, v1.0 (Emulator)"

    def __init__(self) -> None:
        super().__init__()
        self.error_queue: list[Error] = []
        self.zero_check: bool = False
        self.zero_correction: bool = False
        self.sense_function: str = "VOLT"
        self.sense_average_tcontrol: str = "REP"
        self.sense_average_count: int = 10
        self.sense_average_state: int = 0
        self.sense_current_range: float = 2.1e-4
        self.sense_current_range_auto: int = 1
        self.sense_nplc: float = 5.0

    @message(r'^\*RST$')
    def set_rst(self) -> None:
        self.error_queue.clear()
        self.zero_check = False
        self.zero_correction = False
        self.sense_function = "VOLT"
        self.sense_average_tcontrol = "REP"
        self.sense_average_count = 10
        self.sense_average_state = 0
        self.sense_current_range = 2.1e-4
        self.sense_current_range_auto = 1
        self.sense_nplc = 5.0

    @message(r'^\*CLS$')
    def set_cls(self) -> None:
        self.error_queue.clear()

    @message(r'^:?SYST:ERR:COUN\?$')
    def get_system_error_count(self) -> str:
        return format(len(self.error_queue), "d")

    @message(r'^:?SYST:ERR(?::NEXT)?\?$')
    def get_system_error_next(self) -> str:
        if self.error_queue:
            error = self.error_queue.pop(0)
        else:
            error = Error(0, "no error")
        return f'{error.code}, "{error.message}"'

    @message(r'^:?FORM:ELEM (READ)$')
    def set_format_elements(self, value) -> None: ...

    @message(r'^:?FORM:ELEM\?$')
    def get_format_elements(self) -> str:
        return "READ"

    @message(r'^:?INIT$')
    def set_init(self) -> None:
        time.sleep(random.uniform(.5, 1.0))

    def _reading(self) -> float:
        if self.sense_function == "CURR":
            curr_min = float(self.options.get("curr.min", 2.5e-10))
            curr_max = float(self.options.get("curr.max", 2.5e-9))
            return random.uniform(curr_min, curr_max)
        elif self.sense_function == "VOLT":
            volt_min = float(self.options.get("volt.min", -5))
            volt_max = float(self.options.get("volt.max", +5))
            return random.uniform(volt_min, volt_max)
        return 0

    @message(r'^:?FETC[H]?\?$')
    def get_fetch(self) -> str:
        return format(self._reading(), "E")

    @message(r'^:?READ\?$')
    def get_read(self) -> str:
        time.sleep(random.uniform(.25, 1.0))
        return format(self._reading(), "E")

    @message(r'^:?SYST:ZCH\s+(0|1|ON|OFF)$')
    def set_zero_check(self, value) -> None:
        self.zero_check = {"0": False, "1": True, "OFF": False, "ON": True}[value]

    @message(r'^:?SYST:ZCH\?$')
    def get_zero_check(self) -> str:
        return {False: "0", True: "1"}[self.zero_check]

    @message(r'^:?SYST:ZCOR\s+(0|1|ON|OFF)$')
    def set_zero_correction(self, value) -> None:
        self.zero_correction = {"0": False, "1": True, "OFF": False, "ON": True}[value]

    @message(r'^:?SYST:ZCOR\?$')
    def get_zero_correction(self) -> str:
        return {False: "0", True: "1"}[self.zero_correction]

    @message(r'^:?SENS:FUNC \'(VOLT|CURR|RES|CHAR)(?:\:DC)?\'$')
    def set_sense_function(self, value: str) -> None:
        self.sense_function = value

    @message(r'^:?SENS:FUNC\?$')
    def get_sense_function(self) -> str:
        return f"\"{self.sense_function}:DC\""

    # Average

    @message(r'^(?::?SENS)?:AVER:TCON\?$')
    def get_sense_average_tcontrol(self) -> str:
        return self.sense_average_tcontrol

    @message(r'^(?::?SENS)?:AVER:TCON (REP|MOV)$')
    def set_sense_average_tcontrol(self, state: str) -> None:
        self.sense_average_tcontrol = state

    @message(r'^(?::?SENS)?:AVER:COUN\?$')
    def get_sense_average_count(self) -> int:
        return self.sense_average_count

    @message(r'^(?::?SENS)?:AVER:COUN (\d+)$')
    def set_sense_average_count(self, count: str) -> None:
        self.sense_average_count = int(count)

    @message(r'^(?::?SENS)?:AVER(?::STAT)?\?$')
    def get_sense_average_state(self) -> int:
        return int(self.sense_average_state)

    @message(r'^(?::?SENS)?:AVER(?::STAT)? (OFF|ON|0|1)$')
    def set_sense_average_state(self, state: str) -> None:
        self.sense_average_state = {"OFF": 0, "ON": 1, "0": 0, "1": 1}[state]

    # Current range

    @message(r'^(?::?SENS)?:CURR:RANG\?$')
    def get_sense_current_range(self) -> str:
        return format(self.sense_current_range, "E")

    @message(r'^(?::?SENS)?:CURR:RANG(?::UPP)?\s+(.+)$')
    def set_sense_current_range(self, value: str) -> None:
        try:
            self.sense_current_range = float(value)
        except Exception:
            self.error_queue.append(Error(102, "invalid header"))

    @message(r'^(?::?SENS)?:CURR:RANG:AUTO\?$')
    def get_sense_current_range_auto(self) -> int:
        return self.sense_current_range_auto

    @message(r'^(?::?SENS)?:CURR:RANG:AUTO\s+(OFF|ON|0|1)$')
    def set_sense_current_range_auto(self, state: str) -> None:
        self.sense_current_range_auto = {"OFF": 0, "ON": 1, "0": 0, "1": 1}[state]

    @message(r'^(?::?SENS)?:CURR:RANG:AUTO:ULIM\s+(.+)$')
    def set_sense_current_range_auto_ulimit(self, value: str) -> None:
        ...  # TODO

    @message(r'^(?::?SENS)?:CURR:RANG:AUTO:LLIM\s+(.+)$')
    def set_sense_current_range_auto_llimit(self, value: str) -> None:
        ...  # TODO

    # NPLC (coupled commands)

    @message(r'^(?::?SENS)?:(:?CURR|VOLT|RES|CHAR):NPLC\?$')
    def get_sense_nplc(self) -> str:
        return format(self.sense_nplc, "f")  # TODO precision?

    @message(r'^(?::?SENS)?:(:?CURR|VOLT|RES|CHAR):NPLC\s+(.+)$')
    def set_sense_nplc(self, mode: str, value: str) -> None:
        try:
            self.sense_nplc = max(0.01, min(10.0, float(value)))
        except Exception:
            self.error_queue.append(Error(102, "invalid header"))

    @message(r'^(.*)$')
    def unknown_message(self, request) -> None:
        self.error_queue.append(Error(101, "malformed command"))


if __name__ == "__main__":
    run(K6514Emulator())
