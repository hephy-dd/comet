"""Keithley 6514 Electrometer emulator."""

import random
import time

from comet.emulator.emulator import message, run
from comet.emulator.iec60488 import IEC60488Handler
from comet.emulator.keithley.k2400 import SystemMixin

__all__ = ['K6514Handler']

class MeasureMixin:

    readings = 10

    @message(r':?FORM:ELEM (READ)')
    def write_format_elements(self, value):
        pass

    @message(r':?FORM:ELEM\?')
    def query_format_elements(self):
        return "READ"

    @message(r':?INIT')
    def write_init(self):
        time.sleep(random.uniform(.5, 1.0))

    @message(r':?FETC[H]?\?')
    def query_fetch(self):
        vdc = random.uniform(.00025, .001)
        return format(vdc, 'E')

    @message(r':?READ\?')
    def query_read(self):
        time.sleep(random.uniform(.5, 1.0))
        vdc = random.uniform(.00025, .001)
        return format(vdc, 'E')

class K6514Handler(IEC60488Handler, SystemMixin, MeasureMixin):
    """Generic Keithley 6514 series compliant request handler."""

    identification = "Spanish Inquisition Inc., Model 6514, 12345678, v1.0"

    zero_check = False
    sense_function = 'VOLT'

    @message(r':?SYST:ZCH\s+(0|1|ON|OFF)')
    def write_zero_check(self, value):
        type(self).zero_check = {'0': False, '1': True, 'OFF': False, 'ON': True}[value]

    @message(r':?SYST:ZCH\?')
    def query_zero_check(self):
        return {False: '0', True: '1'}[type(self).zero_check]

    @message(r':?SENS:FUNC [\'\"](VOLT|CURR)(?:\:DC)?[\'\"]')
    def write_sense_function(self, value):
        type(self).sense_function = value

    @message(r':?SENS:FUNC\?')
    def query_sense_function(self):
        return f"\"{type(self).sense_function}:DC\""

if __name__ == "__main__":
    run(K6514Handler)
