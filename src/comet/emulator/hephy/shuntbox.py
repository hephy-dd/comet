"""HEPHY Shunt Box emulator."""

import random
import time

from comet.emulator import Emulator
from comet.emulator import message, run

__all__ = ["ShuntBoxEmulator"]


def format_error(code: int) -> str:
    return f"Err{abs(code):d}"


class ShuntBoxEmulator(Emulator):

    IDENTITY: str = "ShuntBox, v1.0 (Emulator)"
    MEMORY_BYTES: int = 4200
    CHANNELS: int = 10
    SUCCESS: str = "OK"

    def __init__(self) -> None:
        super().__init__()
        self.start_time: float = time.time()

    @property
    def uptime(self) -> int:
        return int(round(time.time() - self.start_time))

    @message(r'\*IDN\?')
    def get_idn(self) -> str:
        return self.options.get("identity", self.IDENTITY)

    @message(r'GET:UP \?')
    def get_up(self) -> str:
        return format(self.uptime)

    @message(r'GET:RAM \?')
    def get_ram(self) -> str:
        return format(self.MEMORY_BYTES)

    @message(r'GET:TEMP ALL')
    def get_temp_all(self) -> str:
        values = []
        for i in range(self.CHANNELS):
            values.append(format(random.uniform(22.0, 26.0), ".1f"))
        return ",".join(values)

    @message(r'GET:TEMP (\d+)')
    def get_temp(self, value) -> str:
        return format(random.uniform(22.0, 26.0), ".1f")

    @message(r'SET:REL_(ON|OFF) (\d+|ALL)')
    def set_rel(self, state, value) -> str:
        return self.SUCCESS

    @message(r'GET:REL (\d+)')
    def get_rel(self, value) -> str:
        return "0"

    @message(r'GET:REL ALL')
    def get_rel_all(self) -> str:
        return ",".join(["0"] * (self.CHANNELS + 4))

    @message(r'.*')
    def unknown_message(self) -> str:
        return format_error(99)


if __name__ == "__main__":
    run(ShuntBoxEmulator())
