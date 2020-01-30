import random
import time

from comet.emulator.emulator import message, run
from comet.emulator.iec60488 import IEC60488Handler

__all__ = ['K2400Handler']

class SystemMixin:

    @message(r':?(SYST):(BEEP):(STAT)\?')
    def query_syst_err(self, message):
        return "0"

class MeasureMixin:

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

class K2400Handler(IEC60488Handler, SystemMixin, MeasureMixin):
    """Generic Keithley 2400 series compliant request handler."""

    identification = "Spanish Inquisition Inc., Model 2400, 12345678, v1.0"

    @message(r':?(SYST):(ERR)\?')
    def query_syst_err(self, message):
        return '0,"no error"'

    @message(r':?(OUTP)\?')
    def query_outp(self, message):
        return "1"

if __name__ == "__main__":
    run(K2400Handler)
