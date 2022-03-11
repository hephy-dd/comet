import random
import time

from comet.emulator import IEC60488Emulator, message, run


class K6517BEmulator(IEC60488Emulator):

    IDENTITY = "Keithley Inc., Model 6517B, 43768438, v1.0 (Emulator)"

    def __init__(self):
        super().__init__()
        self.error_queue = []
        self.zero_check = False
        self.sense_average_tcontrol = {'VOLT': 'REP', 'CURR': 'REP'}
        self.sense_average_count = {'VOLT': 10, 'CURR': 10}
        self.sense_average_state = {'VOLT': False, 'CURR': False}

    @message(r'\*RST')
    def set_reset(self):
        self.error_queue.clear()
        self.zero_check = False
        self.sense_average_tcontrol.update({'VOLT': 'REP', 'CURR': 'REP'})
        self.sense_average_count.update({'VOLT': 10, 'CURR': 10})
        self.sense_average_state.update({'VOLT': False, 'CURR': False})

    @message(r'\*CLS')
    def set_clear(self):
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

    @message(r'\*ESR\?')
    def get_esr(self):
        return format(random.randint(0, 1))

    @message(r':?SYST:ERR\?')
    def get_system_error(self):
        return '0, "no error"'

    @message(r':?SYST:ZCH\?')
    def get_system_zerocheck(self):
        return format(self.zero_check, 'd')

    @message(r':?SYST:ZCH\s+(OFF|ON)')
    def set_system_zerocheck(self, value):
        self.zero_check = {'OFF': False, 'ON': True}[value]

    @message(r':?SENS:FUNC\?')
    def get_sense_function(self):
        return '"CURR:DC"'

    @message(r':?INIT')
    def set_init(self):
        pass

    @message(r':?READ\?')
    def get_read(self):
        time.sleep(.25)
        return format(random.uniform(0.000001, 0.0001))

    @message(r':?FETC[H]?\?')
    def get_fetch(self):
        time.sleep(.25)
        return format(random.uniform(0.000001, 0.0001))

    # Average

    @message(r':?SENS:(VOLT|CURR):AVER:TCON\?')
    def get_sense_average_tcontrol(self, function: str):
        return format(self.sense_average_tcontrol[function], 'E')

    @message(r':?SENS:(VOLT|CURR):AVER:TCON (MOV|REP)')
    def set_sense_average_tcontrol(self, function: str, tcontrol: str):
        self.sense_average_tcontrol[function] = tcontrol

    @message(r':?SENS:(VOLT|CURR):AVER:COUN[T]?\?')
    def get_sense_average_count(self, function: str):
        return format(self.sense_average_count[function], 'E')

    @message(r':?SENS:(VOLT|CURR):AVER:COUN[T]? (\d+)')
    def set_sense_average_count(self, function: str, count: str):
        self.sense_average_count[function] = int(count)

    @message(r':?SENS:(VOLT|CURR):AVER:STAT[E]?\?')
    def get_sense_average_state(self, function: str):
        return format(self.sense_average_state[function], 'E')

    @message(r':?SENS:(VOLT|CURR):AVER:STAT[E]? (OFF|ON|0|1)')
    def set_sense_average_state(self, function: str, state: str):
        self.sense_average_state[function] = {'OFF': 0, 'ON': 1, '0': 0, '1': 1}[state]

    @message(r'(.*)')
    def unknown_message(self, request):
        self.error_queue.append((101, "malformed command"))


if __name__ == '__main__':
    run(K6517BEmulator())
