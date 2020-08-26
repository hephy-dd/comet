"""Keysight E4980A emulator."""

import random
import time
import re
import logging

from comet.emulator.emulator import message, run
from comet.emulator.iec60488 import IEC60488Handler

__all__ = ['E4980AHandler']

class E4980AHandler(IEC60488Handler):

    identification = "Spanish Inquisition Inc., Model 4980A, 12345678, v1.0"

    correction_method = 0
    correction_channel = 0

    @message(r':SYST:ERR\?')
    def query_system_error(self):
        return '0, "no error"'

    @message(r':?FETC[H]?\?')
    def query_fetch(self):
        return '{:E},{:E}'.format(random.random(), random.random())

    @message(r':CORR:METH\?')
    def query_correction_method(self):
        return type(self).correction_method

    @message(r':CORR:METH\s+SING')
    def write_correction_method_single(self):
        type(self).correction_method = 0

    @message(r':CORR:METH\s+MULT')
    def write_correction_method_multi(self):
        type(self).correction_method = 1

    @message(r':CORR:USE:CHAN\?')
    def query_correction_channel(self):
        return type(self).correction_channel

    @message(r':CORR:USE:CHAN\s+(\d+)')
    def write_correction_channel(self, value):
        type(self).correction_channel = int(value)

if __name__ == "__main__":
    run(E4980AHandler)
