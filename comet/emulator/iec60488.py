import random

from comet.emulator.emulator import message, run
from comet.emulator.emulator import RequestHandler

__all__ = ['IEC60488Handler']

class IEC60488Handler(RequestHandler):
    """Generic IEC60488 compliant instrument request handler."""

    identification = "Generic IEC60488 Instrument, Spanish Inquisition Inc."

    @message(r'\*IDN\?')
    def query_idn(self):
        return type(self).identification

    @message(r'\*CLS')
    def write_cls(self):
        pass

    @message(r'\*OPC\?')
    def query_opc(self):
        return "1"

    @message(r'\*OPC')
    def write_opc(self):
        pass

    @message(r'\*ESR\?')
    def query_esr(self):
        return format(random.randint(0, 1))

if __name__ == "__main__":
    run(IEC60488Handler)
