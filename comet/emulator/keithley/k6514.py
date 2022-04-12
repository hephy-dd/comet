import random
import time

from comet.emulator import IEC60488Emulator, message, run


class K6514Emulator(IEC60488Emulator):

    IDENTITY = "Keithley Inc., Model 5614, 43768438, v1.0 (Emulator)"

    def __init__(self):
        super().__init__()
        self.error_queue = []
        self.zero_check = False
        self.sense_function = 'VOLT'
        self.sense_average_tcontrol = 'REP'
        self.sense_average_count = 10
        self.sense_average_state = 0
        self.sense_current_range = 2.1e-4
        self.sense_current_range_auto = 1
        self.sense_nplc = 5.

    @message(r'\*RST')
    def set_rst(self):
        self.error_queue.clear()
        self.zero_check = False
        self.sense_function = 'VOLT'
        self.sense_average_tcontrol = 'REP'
        self.sense_average_count = 10
        self.sense_average_state = 0
        self.sense_current_range = 2.1e-4
        self.sense_current_range_auto = 1
        self.sense_nplc = 5.

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

    @message(r':?FORM:ELEM (READ)')
    def set_format_elements(self, value):
        pass

    @message(r':?FORM:ELEM\?')
    def get_format_elements(self):
        return "READ"

    @message(r':?INIT')
    def set_init(self):
        time.sleep(random.uniform(.5, 1.0))

    @message(r':?FETC[H]?\?')
    def get_fetch(self):
        vdc = random.uniform(.00025, .001)
        return format(vdc, 'E')

    @message(r':?READ\?')
    def get_read(self):
        time.sleep(random.uniform(.25, 1.0))
        vdc = random.uniform(.00025, .001)
        return format(vdc, 'E')

    @message(r':?SYST:ZCH\s+(0|1|ON|OFF)')
    def set_zero_check(self, value):
        self.zero_check = {'0': False, '1': True, 'OFF': False, 'ON': True}[value]

    @message(r':?SYST:ZCH\?')
    def get_zero_check(self):
        return {False: '0', True: '1'}[self.zero_check]

    @message(r':?SENS:FUNC \'(VOLT|CURR|RES|CHAR)(?:\:DC)?\'')
    def set_sense_function(self, value: str):
        self.sense_function = value

    @message(r':?SENS:FUNC\?')
    def get_sense_function(self):
        return f"\"{self.sense_function}:DC\""

    # Average

    @message(r'(?::?SENS)?:AVER:TCON\?')
    def get_sense_average_tcontrol(self):
        return self.sense_average_tcontrol

    @message(r'(?::?SENS)?:AVER:TCON (REP|MOV)')
    def set_sense_average_tcontrol(self, state: str):
        self.sense_average_tcontrol = state

    @message(r'(?::?SENS)?:AVER:COUN\?')
    def get_sense_average_count(self):
        return self.sense_average_count

    @message(r'(?::?SENS)?:AVER:COUN (\d+)')
    def set_sense_average_count(self, count: str):
        self.sense_average_count = int(count)

    @message(r'(?::?SENS)?:AVER(?::STAT)?\?')
    def get_sense_average_state(self):
        return int(self.sense_average_state)

    @message(r'(?::?SENS)?:AVER(?::STAT)? (OFF|ON|0|1)')
    def set_sense_average_state(self, state: str):
        self.sense_average_state = {'OFF': 0, 'ON': 1, '0': 0, '1': 1}[state]

    # Current range

    @message(r'(?::?SENS)?:CURR:RANG\?')
    def get_sense_current_range(self):
        return format(self.sense_current_range, 'E')

    @message(r'(?::?SENS)?:CURR:RANG(?::UPP)?\s+(.+)')
    def set_sense_current_range(self, value: str):
        try:
            self.sense_current_range = float(value)
        except Exception:
            self.error_queue.append((102, "invalid header"))

    @message(r'(?::?SENS)?:CURR:RANG:AUTO\?')
    def get_sense_current_range_auto(self):
        return self.sense_current_range_auto

    @message(r'(?::?SENS)?:CURR:RANG:AUTO\s+(OFF|ON|0|1)')
    def set_sense_current_range_auto(self, state: str):
        self.sense_current_range_auto = {'OFF': 0, 'ON': 1, '0': 0, '1': 1}[state]

    @message(r'(?::?SENS)?:CURR:RANG:AUTO:ULIM\s+(.+)')
    def set_sense_current_range_auto_ulimit(self, value: str):
        pass  # TODO

    @message(r'(?::?SENS)?:CURR:RANG:AUTO:LLIM\s+(.+)')
    def set_sense_current_range_auto_llimit(self, value: str):
        pass  # TODO

    # NPLC (coupled commands)

    @message(r'(?::?SENS)?:(:?CURR|VOLT|RES|CHAR):NPLC\?')
    def get_sense_nplc(self):
        return self.sense_nplc

    @message(r'(?::?SENS)?:(:?CURR|VOLT|RES|CHAR):NPLC\s+(.+)')
    def set_sense_nplc(self, mode: str, value: str):
        try:
            self.sense_nplc = max(0.01, min(10.0, float(value)))
        except Exception:
            self.error_queue.append((102, "invalid header"))

    @message(r'(.*)')
    def unknown_message(self, request):
        self.error_queue.append((101, "malformed command"))


if __name__ == '__main__':
    run(K6514Emulator())
