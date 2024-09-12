"""Thorlabs PM100 USB power meter Emulator"""

import random

from comet.emulator import Emulator
from comet.emulator import message, run
from comet.emulator.utils import Error


__all__ = ["PM100Emulator"]


class PM100Emulator(Emulator):
    IDENTITY: str = "Thorlabs,PM100USB,P2004525,1.4.0"

    def __init__(self) -> None:
        super().__init__()

        self.error_queue: list[Error] = []

        self.average_count: int = 100
        self.wavelength: int = 370

    @message(r"^\*IDN\?$")
    def identify(self) -> str:
        return self.IDENTITY

    @message(r"^\*RST$")
    def set_reset(self) -> None:
        self.average_count = 100
        self.wavelength = 370

    @message(r"^\*CLS$")
    def set_clear(self) -> None:
        self.error_queue.clear()

    @message(r"^:?SYST:ERR(?::NEXT)?\?$")
    def get_system_error_next(self) -> str:
        if self.error_queue:
            error = self.error_queue.pop(0)
        else:
            error = Error(0, "no error")
        return f'{error.code}, "{error.message}"'

    @message(r"^(?:SENS(?:e)?)?:AVER(?:age)?:COUN(?:t)?\?$")
    def get_average_count(self) -> int:
        return self.average_count

    @message(r"^(?:SENS(?:e)?)?:AVER(?:age)?:COUN(?:t)? (\d+)$")
    def set_average_count(self, average_count) -> None:
        self.average_count = average_count

    @message(r"^(?:SENS(?:e)?)?:CORR(?:ection)?:WAV(?:elength)?\?$")
    def get_wavelength(self) -> int:
        return self.wavelength

    @message(r"^(?:SENS(?:e)?)?:CORR(?:ection)?:WAV(?:elength)? (\d+)$")
    def set_wavelength(self, wavelength) -> None:
        self.wavelength = wavelength

    @message(r"^MEAS(?:ure)?(?::SCAL(?:ar)?)?(?::POW(?:er)?)?")
    def measure_power(self) -> str:
        power = random.uniform(1e-9, 2e-9)
        return format(power, "E")


if __name__ == "__main__":
    run(PM100Emulator())
