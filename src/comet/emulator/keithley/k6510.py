import random

from comet.emulator import Context, IEC60488Emulator, message, run
from comet.emulator.utils import Error

__all__ = ["K6510Emulator"]


class K6510Emulator(IEC60488Emulator):
    IDENTITY: str = "Keithley Inc., Model DAQ6510, 54313645, v1.0 (Emulator)"

    def __init__(self, context: Context) -> None:
        super().__init__(context)

        options = context.options

        self.error_queue: list[Error] = []

        self.route_terminals = options.get("route.terminals", "front")
        self.curr_min = float(options.get("curr.min", 1e-6))
        self.curr_max = float(options.get("curr.max", 1e-7))
        self.volt_min = float(options.get("volt.min", 1e3))
        self.volt_max = float(options.get("volt.max", 1e2))

    @message(r"\*RST$")
    def set_rst(self) -> None:
        self.error_queue.clear()

    @message(r"\*CLS$")
    def set_cls(self) -> None:
        self.error_queue.clear()

    @message(r":?SYST:ERR(?:or)?:COUN[T]?\?$")
    def get_system_error_count(self) -> str:
        return format(len(self.error_queue), "d")

    @message(r":?SYST:ERR(?:or)?(?::NEXT)?\?$")
    def get_system_error_next(self) -> str:
        if self.error_queue:
            error = self.error_queue.pop(0)
        else:
            error = Error(0, "no error")
        return f'{error.code}, "{error.message}"'

    # Route terminal

    @message(r":?ROUT(?:e)?:TERM(?:inal(?:s)?)?\?$")
    def get_route_terminals(self) -> str:
        if self.route_terminals.lower().startswith("rear"):
            return "REAR"
        return "FRON"

    # Measure

    @message(r":?MEAS(?:ure)?:VOLT(?:age)?\?$")
    def get_measure_voltage(self) -> str:
        return format(random.uniform(self.volt_min, self.volt_max), "E")

    @message(r":?MEAS(?:ure)?:CURR(?:ent)?\?$")
    def get_measure_current(self) -> str:
        return format(random.uniform(self.curr_min, self.curr_max), "E")

    @message(r".*")
    def unknown_message(self) -> None:
        self.error_queue.append(Error(101, "malformed command"))


if __name__ == "__main__":
    run(K6510Emulator)
