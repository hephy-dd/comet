import random
import time

from comet.emulator.emulator import message, run
from comet.emulator.emulator import RequestHandler

__all__ = ['Venus1Handler']

class Venus1Handler(RequestHandler):
    """Corvus TT Venus-1 request handler."""

    macadr = '00:00:00:00:00:00'
    identify = "Corvus 0 0 0 0"
    version = "1.0"
    serialno = "01011234"

    @message(r'getmacadr')
    def query_getmacadr(self, message):
        return self.macadr

    @message(r'identify')
    def query_identify(self, message):
        return self.identify

    @message(r'version')
    def query_version(self, message):
        return self.version

    @message(r'getserialno')
    def query_getserialno(self, message):
        return self.serialno

if __name__ == "__main__":
    run(Venus1Handler)
