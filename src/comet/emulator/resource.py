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
    termination: str = "\n"
    encoding: str = "ascii"

    def __init__(self, emulator: Emulator) -> None:
        self.emulator: Emulator = emulator
        self.buffer: list = []

    def __enter__(self: T) -> T:
        return self

    def __exit__(self, *args) -> None:
        ...

    def write(self, message: str, termination: Optional[str] = None, encoding: Optional[str] = None) -> int:
        termination = self.termination if termination is None else termination
        response = self.emulator(message)
        if response:
            if isinstance(response, (list, tuple)):
                for res in response:
                    self.buffer.append(response)
            else:
                self.buffer.append(response)
        return len(message + termination)

    def read(self, termination: Optional[str] = None, encoding: Optional[str] = None,) -> str:
        encoding = self.encoding if encoding is None else encoding
        if not self.buffer:
            raise EmptyBufferError("Read buffer is empty.")
        return bytes(self.buffer.pop(0)).decode(encoding)

    def query(self, message: str, delay: Optional[float] = None) -> str:
        self.write(message)
        if delay:
            time.sleep(delay)
        return self.read()
