import random
import time

from comet.emulator import IEC60488Emulator, message, run


class K6517BEmulator(IEC60488Emulator):

    IDENTITY = "Keithley Inc., Model 6517B, 43768438, v1.0 (Emulator)"

    def __init__(self):
        super().__init__()
        self.error_queue = []
        self.zero_check = False
        self.zero_correction = False
        self.sense_function = 'VOLT'
        self.sense_average_tcontrol = {'VOLT': 'REP', 'CURR': 'REP'}
        self.sense_average_count = {'VOLT': 10, 'CURR': 10}
        self.sense_average_state = {'VOLT': False, 'CURR': False}

    @message(r'\*RST')
    def set_reset(self):
        self.error_queue.clear()
        self.zero_check = False
        self.zero_correction = False
        self.sense_function = 'VOLT'
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

    @message(r':?FORM:ELEM (READ)')
    def set_format_elements(self, value):
        pass

    @message(r':?FORM:ELEM\?')
    def get_format_elements(self):
        return "READ"

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

    @message(r':?SYST:ZCOR(?:STAT)?\s+(0|1|ON|OFF)')
    def set_zero_correction(self, value):
        self.zero_correction = {'0': False, '1': True, 'OFF': False, 'ON': True}[value]

    @message(r':?SYST:ZCOR(?:STAT)\?')
    def get_zero_correction(self):
        return {False: '0', True: '1'}[self.zero_correction]

    @message(r':?SENS:FUNC \'(VOLT|CURR|RES|CHAR)(?:\:DC)?\'')
    def set_sense_function(self, value: str):
        self.sense_function = value

    @message(r':?SENS:FUNC\?')
    def get_sense_function(self):
        return f"\"{self.sense_function}:DC\""

    @message(r':?INIT')
    def set_init(self):
        pass

    def _reading(self):
        if self.sense_function == 'CURR':
            curr_min = float(self.options.get("curr.min", 2.5e-10))
            curr_max = float(self.options.get("curr.max", 2.5e-9))
            return random.uniform(curr_min, curr_max)
        elif self.sense_function == 'VOLT':
            volt_min = float(self.options.get("volt.min", -5))
            volt_max = float(self.options.get("volt.max", +5))
            return random.uniform(volt_min, volt_max)
        return 0

    @message(r':?READ\?')
    def get_read(self):
        time.sleep(.25)
        return format(self._reading(), 'E')

    @message(r':?FETC[H]?\?')
    def get_fetch(self):
        return format(self._reading(), 'E')

    @message(r':?MEAS:CURR\?')
    def get_measure_current(self):
        time.sleep(random.uniform(.25, 1.0))
        vdc = random.uniform(.000025, .0001)
        return format(vdc, 'E')

    @message(r':?MEAS:VOLT\?')
    def get_measure_voltage(self):
        time.sleep(random.uniform(.25, 1.0))
        vdc = random.uniform(10., 100.)
        return format(vdc, 'E')

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
    run(K6517BEmulator())
