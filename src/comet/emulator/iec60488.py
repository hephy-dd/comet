import random

from comet.emulator import Emulator
from comet.emulator import message

__all__ = ["IEC60488Emulator"]


class IEC60488Emulator(Emulator):
    IDENTITY: str = "Generic IEC60488 Instrument (Emulator)"

    @message(r"\*IDN\?")
    def get_idn(self):
        return self.options.get("identity", self.IDENTITY)

    @message(r"\*ESR\?")
    def get_esr(self):
        return random.choice((0, 1))  # emulate operation complete

    @message(r"\*ESE\?")
    def get_ese(self):
        return 0

    @message(r"\*ESE (\d+)")
    def set_ese(self, value): ...

    @message(r"\*STB\?")
    def get_stb(self):
        return 0

    @message(r"\*OPC\?")
    def get_opc(self):
        return 1

    @message(r"\*OPC")
    def set_opc(self): ...

    @message(r"\*RST")
    def set_rst(self): ...

    @message(r"\*CLS")
    def set_cls(self): ...

    @message(r"\*TST?")
    def get_tst(self):
        return 0

    @message(r"\*WAI")
    def set_wai(self): ...
