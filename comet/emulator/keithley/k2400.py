import random
import time

from comet.emulator.emulator import message, run
from comet.emulator.iec60488 import IEC60488Handler

__all__ = ['K2400Handler']

class K2400Handler(IEC60488Handler):
    """Generic Keithley 2400 series compliant request handler."""

    @message(r'\*(IDN)\?')
    def query_idn(self, message):
        return "Keithley Model 2400, Spanish Inquisition Inc."

    @message(r':?(FETC[H]?)\?')
    def query_read(self, message):
        values = []
        for i in range(10):
            vdc = random.uniform(.00025,.001)
            values.append("{:E}VDC,+0.000SECS,+0.0000RDNG#".format(vdc))
        time.sleep(random.uniform(.5, 1.0)) # rev B10 ;)
        return ",".join(values)

if __name__ == "__main__":
    run(K2400Handler)
