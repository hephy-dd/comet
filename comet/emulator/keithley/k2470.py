"""Keithley 2470 emulator."""

from comet.emulator.emulator import message, run
from comet.emulator.iec60488 import IEC60488Handler

__all__ = ['K2470Handler']

class K2470Handler(IEC60488Handler):
    """Generic Keithley 2470 series compliant request handler."""

    identification = "Spanish Inquisition Inc., Model 2470, 12345678, v1.0"

    beeper_state = False

    @message(r'print\(beeper\)')
    def query_beeper_state(self):
        return int(type(self).beeper_state)

    @message(r'beeper\s+=\s+(0|1|false|true)')
    def write_beeper_state(self, value):
        type(self).beeper_state = {'0': False, '1': True, 'false': False, 'true': True}[value]

if __name__ == "__main__":
    run(K2470Handler)
