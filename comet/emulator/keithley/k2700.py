import random
import time

from comet.emulator import IEC60488Emulator, message, run


class K2700Emulator(IEC60488Emulator):

    IDENTITY = "Keithley Inc., Model 2700, 43768438, v1.0 (Emulator)"

    def __init__(self):
        super().__init__()
        self.error_queue = []
        self.system_beeper_state = True

    @message(r'\*RST')
    def set_rst(self):
        self.error_queue.clear()
        self.system_beeper_state = True

    @message(r'\*CLS')
    def set_cls(self):
        self.error_queue.clear()

    @message(r':?SYST:ERR:COUN\?')
    def get_system_error_count(self):
        return len(self.error_queue)

    @message(r':?SYST:ERR(?::NEXT)?\?')
    def get_system_error_next(self):
        if self.error_queue:
            code, message = self.error_queue.pop(0)
            return f'{code}, "{message}"'
        return '0, "no error"'

    @message(r':?SYST:BEEP(?::STAT)?\?')
    def get_beeper_state(self):
        return int(self.system_beeper_state)

    @message(r':?SYST:BEEP(?::STAT)? (OFF|ON|0|1)')
    def set_beeper_state(self, value):
        self.system_beeper_state = {'0': False, '1': True, 'OFF': False, 'ON': True}[value]

    @message(r':?INIT')
    def set_init(self):
        pass

    @message(r':?READ\?')
    def get_read(self):
        self.get_fetch()

    @message(r':?FETC[H]?\?')
    def get_fetch(self):
        vdc = random.uniform(.00025, .001)
        time.sleep(random.uniform(.5, 1.0))  # rev B10 ;)
        return "{:E},+0.000,+0.000,+0.000,+0.000".format(vdc)

    @message(r'(.*)')
    def unknown_message(self, request):
        self.error_queue.append((101, "malformed command"))


if __name__ == "__main__":
    run(K2700Emulator())

