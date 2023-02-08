import random
from comet.emulator import IEC60488Emulator, message, run


class K2400Emulator(IEC60488Emulator):

    IDENTITY = "Keithley Inc., Model 2400, 43768438, v1.0 (Emulator)"

    DEFAULT_VOLTAGE_PROTECTION_LEVEL = 210.

    def __init__(self):
        super().__init__()
        self.error_queue = []
        self.system_beeper_state = True
        self.route_terminals = 'FRON'
        self.output_state = False
        self.source_function_mode = 'VOLT'
        self.source_level = {'VOLT': 0., 'CURR': 0.}
        self.source_range = {'VOLT': 0., 'CURR': 0.}
        self.source_range_auto = {'VOLT': True, 'CURR': True}
        self.source_voltage_protection_level = self.DEFAULT_VOLTAGE_PROTECTION_LEVEL
        self.sense_voltage_protection_level = 2.1e+1
        self.sense_current_protection_level = 1.05e-5
        self.sense_function = 'CURR'
        self.sense_function_concurrent = False
        self.sense_average_tcontrol = 'REP'
        self.sense_average_count = 10
        self.sense_average_state = False
        self.sense_nplc = 1.0
        self.system_rsense = False
        self.format_elements = ['VOLT', 'CURR', 'RES', 'TIME', 'STAT']

    @message(r'\*RST')
    def set_rst(self):
        self.error_queue.clear()
        self.system_beeper_state = True
        self.route_terminals = 'FRON'
        self.output_state = False
        self.source_function_mode = 'VOLT'
        self.source_level.update({'VOLT': 0., 'CURR': 0.})
        self.source_range.update({'VOLT': 0., 'CURR': 0.})
        self.source_range_auto.update({'VOLT': True, 'CURR': True})
        self.source_voltage_protection_level = self.DEFAULT_VOLTAGE_PROTECTION_LEVEL
        self.sense_function = 'CURR'
        self.sense_function_concurrent = False
        self.sense_average_tcontrol = 'REP'
        self.sense_average_count = 10
        self.sense_average_state = False
        self.sense_nplc = 1.0
        self.system_rsense = False
        self.format_elements = ['VOLT', 'CURR', 'RES', 'TIME', 'STAT']

    @message(r'\*CLS')
    def set_cls(self):
        self.error_queue.clear()

    @message(r':?SYST(?:em)?:ERR(?:or)?:COUN(?:t)?\?')
    def get_system_error_count(self):
        return len(self.error_queue)

    @message(r':?SYST(?:em)?:ERR(?:or)?(?::NEXT)?\?')
    def get_system_error_next(self):
        if self.error_queue:
            code, message = self.error_queue.pop(0)
            return f'{code}, "{message}"'
        return '0, "no error"'

    # Beeper

    @message(r':?SYST(?:em)?:BEEP(?:er)?(?::STAT(?:e)?)?\?')
    def get_system_beeper_state(self):
        return int(self.system_beeper_state)

    @message(r':?SYST(?:em)?:BEEP(?:er)?(?::STAT(?:e)?)? (OFF|ON|0|1)')
    def set_system_beeper_state(self, state):
        self.system_beeper_state = {'OFF': False, 'ON': True, '0': False, '1': True}[state]

    # Route terminal

    @message(r':?ROUT(?:e)?:TERM(?:inal)?\?')
    def get_route_terminals(self):
        return self.route_terminals

    @message(r':?ROUT(?:e)?:TERM(?:inal)? (FRON|REAR)')
    def set_route_terminals(self, terminal):
        self.route_terminals = terminal

    # Output state

    @message(r':?OUTP(?:ut)?(?::STAT(?:e)?)?\?')
    def get_output_state(self):
        return {False: '0', True: '1'}[self.output_state]

    @message(r':?OUTP(?:ut)?(?::STAT(?:e)?)? (.+)')
    def set_output_state(self, state):
        try:
            self.output_state = {'ON': True, 'OFF': False, '0': False, '1': True}[state]
        except KeyError:
            self.error_queue.append((101, "malformed command"))

    # Source function mode

    @message(r':?SOUR:FUNC(?::MODE)?\?')
    def get_source_function_mode(self):
        return self.source_function_mode

    @message(r':?SOUR:FUNC(?::MODE)? (VOLT|CURR)$')
    def set_source_function_mode(self, function):
        try:
            self.source_function_mode = function
        except KeyError:
            self.error_queue.append((101, "malformed command"))

    # Source levels

    @message(r':?SOUR:(VOLT|CURR)(?::LEV)?\?')
    def get_source_level(self, function):
        return format(self.source_level[function], 'E')

    @message(r':?SOUR:(VOLT|CURR)(?::LEV)? (.+)')
    def set_source_level(self, function, level):
        try:
            self.source_level[function] = float(level)
        except ValueError:
            self.error_queue.append((101, "malformed command"))

    # Source range levels

    @message(r':?SOUR:(VOLT|CURR):RANG\?')
    def get_source_range_level(self, function):
        return format(self.source_range[function], 'E')

    @message(r':?SOUR:(VOLT|CURR):RANG (.+)')
    def set_source_range_level(self, function, level):
        try:
            self.source_range[function] = float(level)
            self.source_range_auto[function] = False
        except ValueError:
            self.error_queue.append((101, "malformed command"))

    # Source auto ranges

    @message(r':?SOUR:(VOLT|CURR):RANG:AUTO\?')
    def get_source_range_auto(self, function):
        return int(self.source_range_auto[function])

    @message(r':?SOUR:(VOLT|CURR):RANG:AUTO (.+)')
    def set_source_range_auto(self, function, state):
        try:
            self.source_range_auto[function] = {'ON': True, 'OFF': False, '0': False, '1': True}[state]
        except ValueError:
            self.error_queue.append((101, "malformed command"))

    # Source voltage limit

    @message(r':?SOUR:VOLT:PROT(?::LEV)?\?')
    def get_source_voltage_protection_level(self):
        return format(self.source_voltage_protection_level, 'E')

    @message(r':?SOUR:VOLT:PROT(?::LEV)? (.+)')
    def set_source_voltage_protection_level(self, level):
        try:
            self.source_voltage_protection_level = float(level)
        except ValueError:
            self.error_queue.append((101, "malformed command"))

    # Source compliance

    @message(r'(?::?SENS)?:VOLT:PROT(?::LEV)?\?')
    def get_sense_voltage_protection_level(self):
        return format(self.sense_voltage_protection_level, 'E')

    @message(r'(?::?SENS)?:VOLT:PROT(?::LEV)? (.+)')
    def set_sense_voltage_protection_level(self, level):
        try:
            self.sense_voltage_protection_level = float(level)
        except ValueError:
            self.error_queue.append((101, "malformed command"))

    @message(r'(?::?SENS)?:VOLT:PROT:TRIP\?')
    def get_sense_voltage_protection_tripped(self):
        return format(False, 'd')  # TODO

    @message(r'(?::?SENS)?:CURR:PROT(?::LEV)?\?')
    def get_sense_current_protection_level(self):
        return format(self.sense_current_protection_level, 'E')

    @message(r'(?::?SENS)?:CURR:PROT(?::LEV)? (.+)')
    def set_sense_current_protection_level(self, level):
        try:
            self.sense_current_protection_level = float(level)
        except ValueError:
            self.error_queue.append((101, "malformed command"))

    @message(r'(?::?SENS)?:CURR:PROT:TRIP\?')
    def get_sense_current_protection_tripped(self):
        return format(False, 'd')  # TODO

    # Sense function

    @message(r'(?::?SENS)?:FUNC(?::ON)?\?')
    def get_sense_function_on(self):
        return f'\'{self.sense_function}:DC\''

    @message(r'(?::?SENS)?:FUNC(?::ON)? \'(VOLT|CURR)\'')
    def set_sense_function_on(self, function):
        self.sense_function = function

    # Concurrent function

    @message(r'^(?::?SENS)?:FUNC:CONC\?$')
    def get_sense_function_concurrent(self):
        return int(self.sense_function_concurrent)

    @message(r'^(?::?SENS)?:FUNC:CONC (OFF|ON|0|1)$')
    def set_sense_function_concurrent(self, state):
        self.sense_function_concurrent = {'OFF': False, 'ON': True, '0': False, '1': True}[state]

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
    def set_sense_average_state(self, state):
        self.sense_average_state = {'OFF': False, 'ON': True, '0': False, '1': True}[state]

    # Integration time

    @message(r'(?::?SENS)?:(?:VOLT|CURR|RES):NPLC\?')
    def get_sense_nplc(self):
        return format(self.sense_nplc, 'E')

    @message(r'(?::?SENS)?:(?:VOLT|CURR|RES):NPLC (.+)')
    def set_sense_nplc(self, nplc: str):
        self.sense_nplc = round(float(nplc), 2)

    # 2/4-wire remote sense

    @message(r'(?::?SYST):RSEN\?')
    def get_system_rsense(self):
        return int(self.system_rsense)

    @message(r'(?::?SYST):RSEN (OFF|ON|0|1)')
    def set_system_rsense(self, state: str):
        self.system_rsense = {'OFF': False, 'ON': True, '0': False, '1': True}[state]

    # Format

    @message(r':?FORM:ELEM\?')
    def get_format_elements(self):
        return ','.join(self.format_elements)

    @message(r':?FORM:ELEM (.+)')
    def set_format_elements(self, elements):
        elements = [element.strip() for element in elements.split(',') if element.strip()]
        self.format_elements = elements

    # Measure

    @message(r':?INIT(?:iate)?')
    def set_initiate(self):
        ...

    @message(r':?READ\?')
    def get_read(self):
        curr_min = float(self.options.get("curr.min", 1e6))
        curr_max = float(self.options.get("curr.max", 1e7))
        return format(random.uniform(curr_min, curr_max), 'E')

    @message(r':?FETC[H]?\?')
    def get_fetch(self):
        curr_min = float(self.options.get("curr.min", 1e6))
        curr_max = float(self.options.get("curr.max", 1e7))
        return format(random.uniform(curr_min, curr_max), 'E')

    @message(r'(.*)')
    def unknown_message(self, request):
        self.error_queue.append((101, "malformed command"))


if __name__ == '__main__':
    run(K2400Emulator())
