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
        vdc = random.uniform(.00025,.001)
        time.sleep(random.uniform(.5, 1.0)) # rev B10 ;)
        return "{:E},+0.000,+0.000,+0.000,+0.000".format(vdc)

class SourceMixin:

    @message(r':?(SOUR):(VOLT):(LEV)\?')
    def query_source_voltage_level(self, message):
        return format(0.0, 'E')

class SenseMixin:

    @message(r':?(SENS):(CURR):(PROT):(LEV)\?')
    def query_current_protection_level(self, message):
        return format(0.0, 'E')

    @message(r':?(SENS):(CURR):(PROT):(TRIP)\?')
    def query_current_protection_tripped(self, message):
        return "0"

    @message(r':?(SENS):(CURR):(PROT):(RSYN)\?')
    def query_current_protection_rsyncronized(self, message):
        return "0"

    @message(r':?(SENS):(VOLT):(PROT):(LEV)\?')
    def query_voltage_protection_level(self, message):
        return format(0.0, 'E')

    @message(r':?(SENS):(VOLT):(PROT):(TRIP)\?')
    def query_voltage_protection_tripped(self, message):
        return "0"

    @message(r':?(SENS):(VOLT):(PROT):(RSYN)\?')
    def query_voltage_protection_rsyncronized(self, message):
        return "0"

class K2400Handler(IEC60488Handler, SystemMixin, MeasureMixin, SourceMixin, SenseMixin):
    """Generic Keithley 2400 series compliant request handler."""

    identification = "Spanish Inquisition Inc., Model 2400, 12345678, v1.0"

    @message(r':?(SYST):(ERR)\?')
    def query_syst_err(self, message):
        return '0,"no error"'

    @message(r':?(OUTP)\?')
    @message(r':?(OUTP):(STAT)\?')
    def query_outp(self, message):
        return "1"

if __name__ == "__main__":
    run(K2400Handler)
