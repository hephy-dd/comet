import random

from comet.emulator.emulator import message, run
from comet.emulator.emulator import RequestHandler

__all__ = ['TSPHandler']

class TSPHandler(RequestHandler):
    """Generic TSP compliant instrument request handler."""

    localnode_model = "Generic TSP Instrument"
    localnode_serialno = "12345678"
    localnode_version = "v 1.0"

    @message(r'\*IDN\?')
    def query_idn(self):
        return ', '.join((
            type(self).localnode_model,
            type(self).localnode_serialno,
            type(self).localnode_version
        ))

    @message(r'print\(localnode.model\)')
    def query_localnode_model(self):
        return type(self).localnode_model

    @message(r'print\(localnode.serialno\)')
    def query_localnode_serialno(self):
        return type(self).localnode_serialno

    @message(r'print\(localnode.version\)')
    def query_localnode_version(self):
        return type(self).localnode_version

    @message(r'reset\(\)')
    @message(r'\*RST')
    def write_reset(self):
        pass

    @message(r'eventlog.clear\(\)')
    @message(r'status.clear\(\)')
    @message(r'\*CLS')
    def write_cls(self):
        pass

    @message(r'waitcomplete\(\)')
    def query_waitcomplete(self):
        pass

    @message(r'print\(\[\[1\]\]\)')
    @message(r'\*OPC\?')
    def query_opc(self):
        return "1"

    @message(r'opc\(\)')
    @message(r'\*OPC')
    def write_opc(self):
        pass

    @message(r'print\(status\.standard\.event\)')
    @message(r'\*ESR\?')
    def query_esr(self):
        return format(random.randint(0, 1))

if __name__ == "__main__":
    run(TSPHandler)
