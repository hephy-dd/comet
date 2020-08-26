"""Keithley 6517B emulator."""

import random
import time
import re
import logging

from comet.emulator.emulator import message, run
from comet.emulator.iec60488 import IEC60488Handler

__all__ = ['K6517BHandler']

class K6517BHandler(IEC60488Handler):

    identification = "Spanish Inquisition Inc., Model 6517B, 12345678, v1.0"

    zero_check = False

    @message(r'\*ESR\?')
    def query_esr(self):
        return format(random.randint(0, 1))

    @message(r':?SYST:ERR\?')
    def query_system_error(self):
        return '0, "no error"'

    @message(r':?SYST:ZCH\?')
    def query_system_zerocheck(self):
        return format(type(self).zero_check, 'd')

    @message(r':?SYST:ZCH\s+(OFF|ON)')
    def write_system_zerocheck(self, value):
        type(self).zero_check = {'OFF': False, 'ON': True}[value]

    @message(r':?SENS:FUNC\?')
    def query_sense_function(self):
        return '"CURR:DC"'

    @message(r':?INIT')
    def write_init(self):
        pass

    @message(r':?READ\?')
    def query_read(self):
        return format(random.uniform(0.000001, 0.0001))

    @message(r':?FETC[H]\?')
    def query_fetch(self):
        return format(random.uniform(0.000001, 0.0001))

if __name__ == "__main__":
    run(K6517BHandler)
