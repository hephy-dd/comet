import random
import time

from comet.emulator import IEC60488Emulator, message, run
from comet.emulator.utils import Error

__all__ = ["K6510Emulator"]


class K6510Emulator(IEC60488Emulator):

    IDENTITY: str = "Keithley Inc., Model DAQ6510, 54313645, v1.0 (Emulator)"

    def __init__(self) -> None:
        super().__init__()
        self.error_queue: list[Error] = []

    @message(r'^\*RST$')
    def set_rst(self) -> None:
        self.error_queue.clear()

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

    # Route terminal

    @message(r'^:?ROUT(?:e)?:TERM(?:inal(?:s)?)?\?$')
    def get_route_terminals(self) -> str:
        value = self.options.get("route.terminals", "front")
        if value.lower().startswith("rear"):
            return "REAR"
        return "FRON"

    # Measure

    @message(r'^:?MEAS(?:ure)?:VOLT(?:age)?\?$')
    def get_measure_voltage(self) -> str:
        volt_min = float(self.options.get("volt.min", 1e3))
        volt_max = float(self.options.get("volt.max", 1e2))
        return format(random.uniform(volt_min, volt_max), "E")

    @message(r'^:?MEAS(?:ure)?:CURR(?:ent)?\?$')
    def get_measure_current(self) -> str:
        curr_min = float(self.options.get("curr.min", 1e6))
        curr_max = float(self.options.get("curr.max", 1e7))
        return format(random.uniform(curr_min, curr_max), "E")

    @message(r'^(.*)$')
    def unknown_message(self, request) -> None:
        self.error_queue.append(Error(101, "malformed command"))


if __name__ == "__main__":
    run(K6510Emulator())
