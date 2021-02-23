"""Keithley 2400 emulator."""

import random
import time

from comet.emulator.emulator import message, run
from comet.emulator.iec60488 import IEC60488Handler

__all__ = ['K2400Handler']

class FormatMixin:

    elements = ['VOLT', 'TIME']

    @message(r':?FORM:ELEM\?')
    def query_format_elements(self):
        return ','.join((type(self).elements))

    @message(r':?FORM:ELEM\s+(?:(VOLT|CURR|RES|TIME|\,)+)')
    def write_format_elements(self, values):
        type(self).elements = [value.strip() for value in values.split(',')]

class RouteMixin:

    terminals = 0

    @message(r':?ROUT:TERM\?')
    def query_format_elements(self):
        return ','.join((type(self).elements))

    @message(r':?ROUT:TERM\s+(?:(VOLT|CURR|RES|TIME|\,)+)')
    def write_format_elements(self, values):
        type(self).elements = [value.strip() for value in values.split(',')]

class SystemMixin:

    beeper_state = False

    @message(r':?SYST:BEEP:STAT\?')
    def query_beeper_state(self):
        return int(type(self).beeper_state)

    @message(r':?SYST:BEEP:STAT\s+(0|1|OFF|ON)')
    def write_beeper_state(self, value):
        type(self).beeper_state = {'0': False, '1': True, 'OFF': False, 'ON': True}[value]

class MeasureMixin:

    readings = 10

    @message(r':?INIT')
    def write_init(self):
        pass

    @message(r':?READ\?')
    @message(r':?FETC[H]?\?')
    def query_read(self):
        vdc = random.uniform(.00025, .001)
        time.sleep(random.uniform(.5, 1.0))  # rev B10 ;)
        return "{:E},+0.000,+0.000,+0.000,+0.000".format(vdc)

class SourceMixin:

    source_function = 'VOLT'
    source_voltage_level = 0.0
    source_current_level = 0.0

    @message(r':?SOUR:FUNC:MODE\?')
    def query_source_function_mode(self):
        return type(self).source_function

    @message(r':?SOUR:FUNC:MODE\s+(CURR|VOLT|MEM)')
    def write_source_function_mode(self, mode):
        type(self).source_function = mode

    @message(r':?SOUR:VOLT:LEV\?')
    def query_source_voltage_level(self):
        return format(type(self).source_voltage_level, 'E')

    @message(r':?SOUR:VOLT:LEV\s+(.*)')
    def write_source_voltage_level(self, value):
        type(self).source_voltage_level = float(value)

    @message(r':?SOUR:CURR:LEV\?')
    def query_source_current_level(self):
        return format(type(self).source_current_level, 'E')

    @message(r':?SOUR:CURR:LEV\s+(.*)')
    def write_source_current_level(self, value):
        type(self).source_current_level = float(value)

class SenseMixin:

    @message(r':?SENS:CURR:PROT:LEV\?')
    def query_current_protection_level(self):
        return format(0.0, 'E')

    @message(r':?SENS:CURR:PROT:TRIP\?')
    def query_current_protection_tripped(self):
        return 0

    @message(r':?SENS:CURR:PROT:RSYN\?')
    def query_current_protection_rsyncronized(self):
        return 0

    @message(r':?SENS:VOLT:PROT:LEV\?')
    def query_voltage_protection_level(self):
        return format(0.0, 'E')

    @message(r':?SENS:VOLT:PROT:TRIP\?')
    def query_voltage_protection_tripped(self):
        return 0

    @message(r':?SENS:VOLT:PROT:RSYN\?')
    def query_voltage_protection_rsyncronized(self):
        return 0

class K2400Handler(IEC60488Handler, SystemMixin, MeasureMixin, SourceMixin,
                   SenseMixin):
    """Generic Keithley 2400 series compliant request handler."""

    identification = "Spanish Inquisition Inc., Model 2400, 12345678, v1.0"

    format_elements = 'VOLT', 'CURR', 'FOO', 'STAT', 'TIME'

    output_state = 0

    @message(r':?SYST:ERR\?')
    def query_system_error(self):
        return '0,"no error"'

    @message(r':?OUTP\?')
    @message(r':?OUTP:STAT\?')
    def query_output(self):
        return type(self).output_state

    @message(r':?OUTP\s+(0|1|OFF|ON)')
    @message(r':?OUTP:STAT\s+(0|1|OFF|ON)')
    def query_output(self, state):
        type(self).output_state = {'0': 0, '1': 1, 'OFF': 0, 'ON': 1}.get(state, 0)

    @message(r':?FORM:ELEM\?')
    def query_format_elements(self):
        return ','.join(type(self).format_elements)

if __name__ == "__main__":
    run(K2400Handler)
