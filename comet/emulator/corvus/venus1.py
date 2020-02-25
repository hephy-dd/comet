import random
import time

from comet.emulator.emulator import message, run
from comet.emulator.emulator import RequestHandler

__all__ = ['Venus1Handler']

class Venus1Handler(RequestHandler):
    """Corvus TT Venus-1 request handler."""

    identification = "Spanish Inquisition Inc., Corvus"
    version = "1.0"
    serialno = "01011234"

    @message(r'identify')
    def query_get_idn(self, message):
        return self.identification

    @message(r'getversion')
    def query_get_idn(self, message):
        return self.version

    @message(r'getserialno')
    def query_get_idn(self, message):
        return self.serialno

if __name__ == "__main__":
    run(ShuntBoxHandler)
