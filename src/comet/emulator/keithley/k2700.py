import random
import time
from typing import List

from comet.emulator import IEC60488Emulator, message, run
from comet.emulator.utils import Error


class K2700Emulator(IEC60488Emulator):

    IDENTITY: str = "Keithley Inc., Model 2700, 43768438, v1.0 (Emulator)"

    def __init__(self) -> None:
        super().__init__()
        self.error_queue: List[Error] = []
        self.system_beeper_state: bool = True

    @message(r'^\*RST$')
    def set_rst(self):
        self.error_queue.clear()
        self.system_beeper_state = True

    @message(r'^\*CLS$')
    def set_cls(self):
        self.error_queue.clear()

    @message(r'^:?SYST:ERR:COUN\?$')
    def get_system_error_count(self):
        return format(len(self.error_queue), "d")

    @message(r'^:?SYST:ERR(?::NEXT)?\?$')
    def get_system_error_next(self):
        if self.error_queue:
            error = self.error_queue.pop(0)
        else:
            error = Error(0, "no error")
        return f'{error.code}, "{error.message}"'

    @message(r'^:?SYST:BEEP(?::STAT)?\?$')
    def get_beeper_state(self):
        return format(self.system_beeper_state, "d")

    @message(r'^:?SYST:BEEP(?::STAT)? (OFF|ON|0|1)$')
    def set_beeper_state(self, value):
        self.system_beeper_state = {'0': False, '1': True, 'OFF': False, 'ON': True}[value]

    @message(r'^:?INIT$')
    def set_init(self):
        ...

    @message(r'^:?READ\?$')
    def get_read(self):
        self.get_fetch()

    @message(r'^:?FETC[H]?\?$')
    def get_fetch(self):
        vdc = random.uniform(.00025, .001)
        time.sleep(random.uniform(.5, 1.0))  # rev B10 ;)
        return "{:E},+0.000,+0.000,+0.000,+0.000".format(vdc)

    @message(r'^(.*)$')
    def unknown_message(self, request):
        self.error_queue.append(Error(101, "malformed command"))


if __name__ == '__main__':
    run(K2700Emulator())
