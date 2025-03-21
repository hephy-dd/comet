"""Emulator drop in replacement for PyVISA resources.

>>> with open_emulator("keithley.k2410") as res:
...     print(res.query("*IDN?"))
...

"""

import time
from typing import Optional, TypeVar

from .emulator import Emulator, emulator_factory

T = TypeVar("T")


def open_emulator(module_name: str, options: Optional[dict] = None) -> "EmulatorResource":
    emulator = emulator_factory(module_name)()
    if options:
        emulator.options.update(options)
    return EmulatorResource(emulator)


class EmptyBufferError(Exception): ...


class EmulatorResource:
    def __init__(self, emulator: Emulator) -> None:
        self.emulator: Emulator = emulator
        self.buffer: list[str] = []

    def __enter__(self: T) -> T:
        return self

    def __exit__(self, *args) -> None:
        ...

    def write(self, message: str, *args, **kwargs) -> int:
        response = self.emulator(message)
        if response:
            self.buffer.append(str(response))
        return len(message)

    def read(self, *args, **kwargs) -> str:
        if not self.buffer:
            raise EmptyBufferError()
        return self.buffer.pop(0)

    def query(self, message: str, delay: Optional[float] = None) -> str:
        self.write(message)
        if delay:
            time.sleep(delay)
        return self.read()
