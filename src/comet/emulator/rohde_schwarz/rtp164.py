"""Rohde Schwarz SMA100B signal generator emulator"""

from comet.emulator import IEC60488Emulator
from comet.emulator import message, run
from comet.emulator.utils import Error


__all__ = ["RTP164Emulator"]


class RTP164Emulator(IEC60488Emulator):
    IDENTITY: str = "Rohde&Schwarz,RTP,1320.5007k16/123456,5.50.2.0"

    def __init__(self) -> None:
        super().__init__()

        self.error_queue: list[Error] = []

    @message(r"\*IDN\?$")
    def identify(self) -> str:
        return self.IDENTITY

    @message(r"\*RST$")
    def set_reset(self) -> None:
        self.error_queue.clear()

    @message(r"\*CLS$")
    def set_clear(self) -> None:
        self.error_queue.clear()

    @message(r":?SYST(?:em)?:ERR(?::NEXT)?\?$")
    def get_system_error_next(self) -> str:
        if self.error_queue:
            error = self.error_queue.pop(0)
        else:
            error = Error(0, "No error")
        return f'{error.code},"{error.message}"'

    @message(r"(.*)$")
    def undefined_header(self, command) -> None:
        self.error_queue.append(Error(-113, "Undefined header"))
