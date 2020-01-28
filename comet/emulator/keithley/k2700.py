import random
import time

from comet.emulator.emulator import message, run
from comet.emulator.iec60488 import IEC60488Handler

__all__ = ['K2700Handler']

class K2700Handler(IEC60488Handler):
    """Generic Keithley 2700 series compliant request handler."""

    identification = "Spanish Inquisition Inc., Model 2700, 12345678, v1.0"
    readings = 10

    @message(r':?(INIT)')
    def write_init(self, message):
        pass

    @message(r':?(READ)\?')
    @message(r':?(FETC[H]?)\?')
    def query_read(self, message):
        values = []
        for i in range(self.readings):
            vdc = random.uniform(.00025,.001)
            values.append("{:E}VDC,+0.000SECS,+0.0000RDNG#".format(vdc))
        time.sleep(random.uniform(.5, 1.0)) # rev B10 ;)
        return ",".join(values)

if __name__ == "__main__":
    run(K2700Handler)
