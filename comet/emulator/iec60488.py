from comet.emulator import Emulator
from comet.emulator import message, run

__all__ = ['IEC60488Emulator']


class IEC60488Emulator(Emulator):

    IDENTITY = "Generic IEC60488 Instrument (Emulator)"

    @message(r'\*IDN\?')
    def get_idn(self):
        return self.IDENTITY

    @message(r'\*ESR\?')
    def get_esr(self):
        return 0

    @message(r'\*ESE\?')
    def get_ese(self):
        return 0

    @message(r'\*ESE (\d+)')
    def set_ese(self, value):
        pass

    @message(r'\*STB\?')
    def get_stb(self):
        return 0

    @message(r'\*OPC\?')
    def get_opc(self):
        return 1

    @message(r'\*OPC (\d+)')
    def set_opc(self, value):
        pass

    @message(r'\*RST')
    def set_rst(self):
        pass

    @message(r'\*CLS')
    def set_cls(self):
        pass

    @message(r'\*TST?')
    def get_tst(self):
        return 0

    @message(r'\*WAI')
    def set_wai(self):
        pass


if __name__ == '__main__':
    run(IEC60488Emulator())
