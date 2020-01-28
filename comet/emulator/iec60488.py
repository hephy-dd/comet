from comet.emulator.emulator import message, run
from comet.emulator.emulator import RequestHandler

__all__ = ['IEC60488Handler']

class IEC60488Handler(RequestHandler):
    """Generic IEC60488 compliant instrument request handler."""

    @message(r'\*(IDN)\?')
    def query_idn(self, message):
        return "Generic Instrument, Spanish Inquisition Inc."

    @message(r'\*(CLS)')
    def write_cls(self, message):
        pass

    @message(r'\*(OPC)\?')
    def query_opc(self, message):
        return "1"

    @message(r'\*(OPC)')
    def write_opc(self, message):
        pass

    @message(r'\*(ESR)\?')
    def query_esr(self, message):
        return format(random.randint(0, 1))

    @message(r':?(INIT)')
    def write_init(self, message):
        pass

if __name__ == "__main__":
    run(IEC60488Handler)
