import random

from comet.emulator import Emulator
from comet.emulator.router import scpi

__all__ = ["IEC60488Emulator"]


class IEC60488Emulator(Emulator):
    IDENTITY: str = "Generic IEC60488 Instrument (Emulator)"

    @scpi("*IDN?")
    def get_idn(self) -> str:
        return self.context.options.get("identity", self.IDENTITY)

    @scpi("*ESR?")
    def get_esr(self) -> int:
        return random.choice((0, 1))  # emulate operation complete

    @scpi("*ESE?")
    def get_ese(self) -> int:
        return 0

    @scpi("*ESE")
    def set_ese(self, value) -> None: ...

    @scpi("*STB?")
    def get_stb(self) -> int:
        return 0

    @scpi("*OPC?")
    def get_opc(self) -> int:
        return 1

    @scpi("*OPC")
    def set_opc(self) -> None: ...

    @scpi("*RST")
    def set_rst(self) -> None: ...

    @scpi("*CLS")
    def set_cls(self) -> None: ...

    @scpi("*TST?")
    def get_tst(self) -> int:
        return 0

    @scpi("*WAI")
    def set_wai(self) -> None: ...
