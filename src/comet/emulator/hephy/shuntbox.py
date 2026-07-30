"""HEPHY Shunt Box emulator."""

import random
import time

from comet.emulator import Context, Emulator, message, run

__all__ = ["ShuntBoxEmulator"]


def format_error(code: int) -> str:
    return f"Err{abs(code):d}"


class ShuntBoxEmulator(Emulator):
    MEMORY_BYTES: int = 4200
    CHANNELS: int = 10
    SUCCESS: str = "OK"

    def __init__(self, context: Context) -> None:
        super().__init__(context)

        options = context.options

        self._identity = options.get("identity", "ShuntBox, v1.0 (Emulator)")
        self._start_time: float = float(options.get("start_time", time.monotonic()))
        self._temp_min: float = float(options.get("temp.min", 22.0))
        self._temp_max: float = float(options.get("temp.max", 26.0))

    @property
    def _uptime(self) -> int:
        return round(time.monotonic() - self._start_time)

    @message(r"\*IDN\?$")
    def get_idn(self) -> str:
        return self._identity

    @message(r"GET:UP \?$")
    def get_up(self) -> str:
        return format(self._uptime)

    @message(r"GET:RAM \?$")
    def get_ram(self) -> str:
        return format(self.MEMORY_BYTES)

    @message(r"GET:TEMP ALL$")
    def get_temp_all(self) -> str:
        values = []
        for i in range(self.CHANNELS):
            values.append(format(random.uniform(self._temp_min, self._temp_max), ".1f"))
        return ",".join(values)

    @message(r"GET:TEMP (\d+)$")
    def get_temp(self, value) -> str:
        return format(random.uniform(self._temp_min, self._temp_max), ".1f")

    @message(r"SET:REL_(ON|OFF) (\d+|ALL)$")
    def set_rel(self, state, value) -> str:
        return self.SUCCESS

    @message(r"GET:REL (\d+)$")
    def get_rel(self, value) -> str:
        return "0"

    @message(r"GET:REL ALL$")
    def get_rel_all(self) -> str:
        return ",".join(["0"] * (self.CHANNELS + 4))

    @message(r".*")
    def unknown_message(self) -> str:
        return format_error(99)


if __name__ == "__main__":
    run(ShuntBoxEmulator)
