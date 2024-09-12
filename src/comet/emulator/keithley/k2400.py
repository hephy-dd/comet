import random

from comet.emulator import IEC60488Emulator, message, run
from comet.emulator.utils import Error


class K2400Emulator(IEC60488Emulator):

    IDENTITY: str = "Keithley Inc., Model 2400, 43768438, v1.0 (Emulator)"

    DEFAULT_VOLTAGE_PROTECTION_LEVEL: float = 210.

    def __init__(self) -> None:
        super().__init__()
        self.error_queue: list[Error] = []
        self.system_beeper_state: bool = True
        self.system_rsense: bool = False
        self.route_terminals: str = "FRON"
        self.output_state: bool = False
        self.source_function_mode: str = "VOLT"
        self.source_level: dict[str, float] = {"VOLT": 0., "CURR": 0.}
        self.source_range: dict[str, float] = {"VOLT": 0., "CURR": 0.}
        self.source_range_auto: dict[str, bool] = {"VOLT": True, "CURR": True}
        self.source_voltage_protection_level: float = self.DEFAULT_VOLTAGE_PROTECTION_LEVEL
        self.sense_voltage_protection_level: float = 2.1e+1
        self.sense_current_protection_level: float = 1.05e-5
        self.sense_function = SenseFunction()
        self.sense_function.add("CURR")
        self.sense_function_concurrent: bool = False
        self.sense_average_tcontrol: str = "REP"
        self.sense_average_count: int = 10
        self.sense_average_state: bool = False
        self.sense_nplc: float = 1.0
        self.format_elements = FormatElements()
        self.format_elements.update(["VOLT", "CURR", "RES", "TIME", "STAT"])

    @message(r'^\*RST$')
    def set_rst(self) -> None:
        self.error_queue.clear()
        self.system_beeper_state = True
        self.system_rsense = False
        self.route_terminals = "FRON"
        self.output_state = False
        self.source_function_mode = "VOLT"
        self.source_level.update({"VOLT": 0., "CURR": 0.})
        self.source_range.update({"VOLT": 0., "CURR": 0.})
        self.source_range_auto.update({"VOLT": True, "CURR": True})
        self.source_voltage_protection_level = self.DEFAULT_VOLTAGE_PROTECTION_LEVEL
        self.sense_function.clear()
        self.sense_function.add("CURR")
        self.sense_function_concurrent = False
        self.sense_average_tcontrol = "REP"
        self.sense_average_count = 10
        self.sense_average_state = False
        self.sense_nplc = 1.0
        self.format_elements.clear()
        self.format_elements.update(["VOLT", "CURR", "RES", "TIME", "STAT"])

    @message(r'^\*CLS$')
    def set_cls(self) -> None:
        self.error_queue.clear()

    @message(r'^:?SYST(?:em)?:ERR(?:or)?:COUN(?:t)?\?$')
    def get_system_error_count(self) -> str:
        return format(len(self.error_queue), "d")

    @message(r'^:?SYST(?:em)?:ERR(?:or)?(?::NEXT)?\?$')
    def get_system_error_next(self) -> str:
        if self.error_queue:
            error = self.error_queue.pop(0)
        else:
            error = Error(0, "no error")
        return f'{error.code}, "{error.message}"'

    # Beeper

    @message(r'^:?SYST(?:em)?:BEEP(?:er)?(?::STAT(?:e)?)?\?$')
    def get_system_beeper_state(self) -> str:
        return format(self.system_beeper_state, "d")

    @message(r'^:?SYST(?:em)?:BEEP(?:er)?(?::STAT(?:e)?)? (OFF|ON|0|1)$')
    def set_system_beeper_state(self, state) -> None:
        self.system_beeper_state = {"OFF": False, "ON": True, "0": False, "1": True}[state]

    # Remote sensing

    @message(r'^:?SYST(?:em)?:RSEN(?:se)?\?$')
    def get_system_rsense(self) -> str:
        return format(self.system_rsense, "d")

    @message(r'^:?SYST(?:em)?:RSEN(?:se)?\s+(OFF|ON|0|1)$')
    def set_system_rsense(self, enabled) -> None:
        self.system_rsense = {'OFF': False, 'ON': True, '0': False, '1': True}[enabled]

    # Route terminal

    @message(r'^:?ROUT(?:e)?:TERM(?:inal)?\?$')
    def get_route_terminals(self) -> str:
        return self.route_terminals

    @message(r'^:?ROUT(?:e)?:TERM(?:inal)? (FRON|REAR)$')
    def set_route_terminals(self, terminal) -> None:
        self.route_terminals = terminal

    # Output state

    @message(r'^:?OUTP(?:ut)?(?::STAT(?:e)?)?\?$')
    def get_output_state(self) -> str:
        return {False: '0', True: '1'}[self.output_state]

    @message(r'^:?OUTP(?:ut)?(?::STAT(?:e)?)? (.+)$')
    def set_output_state(self, state) -> None:
        try:
            self.output_state = {"ON": True, "OFF": False, "0": False, "1": True}[state]
        except KeyError:
            self.error_queue.append(Error(101, "malformed command"))

    # Source function mode

    @message(r'^:?SOUR:FUNC(?::MODE)?\?$')
    def get_source_function_mode(self) -> str:
        return self.source_function_mode

    @message(r'^:?SOUR:FUNC(?::MODE)? (VOLT|CURR)$')
    def set_source_function_mode(self, function) -> None:
        try:
            self.source_function_mode = function
        except KeyError:
            self.error_queue.append(Error(101, "malformed command"))

    # Source levels

    @message(r'^:?SOUR:(VOLT|CURR)(?::LEV)?\?$')
    def get_source_level(self, function) -> str:
        return format(self.source_level[function], 'E')

    @message(r'^:?SOUR:(VOLT|CURR)(?::LEV)? (.+)$')
    def set_source_level(self, function, level) -> None:
        try:
            self.source_level[function] = float(level)
        except ValueError:
            self.error_queue.append(Error(101, "malformed command"))

    # Source range levels

    @message(r'^:?SOUR:(VOLT|CURR):RANG\?$')
    def get_source_range_level(self, function) -> str:
        return format(self.source_range[function], "E")

    @message(r'^:?SOUR:(VOLT|CURR):RANG (.+)$')
    def set_source_range_level(self, function, level) -> None:
        try:
            self.source_range[function] = float(level)
            self.source_range_auto[function] = False
        except ValueError:
            self.error_queue.append(Error(101, "malformed command"))

    # Source auto ranges

    @message(r'^:?SOUR:(VOLT|CURR):RANG:AUTO\?$')
    def get_source_range_auto(self, function) -> str:
        return format(self.source_range_auto[function], "d")

    @message(r'^:?SOUR:(VOLT|CURR):RANG:AUTO (.+)$')
    def set_source_range_auto(self, function, state) -> None:
        try:
            self.source_range_auto[function] = {"ON": True, "OFF": False, "0": False, "1": True}[state]
        except ValueError:
            self.error_queue.append(Error(101, "malformed command"))

    # Source voltage limit

    @message(r'^:?SOUR:VOLT:PROT(?::LEV)?\?$')
    def get_source_voltage_protection_level(self) -> str:
        return format(self.source_voltage_protection_level, "E")

    @message(r'^:?SOUR:VOLT:PROT(?::LEV)? (.+)$')
    def set_source_voltage_protection_level(self, level) -> None:
        try:
            self.source_voltage_protection_level = float(level)
        except ValueError:
            self.error_queue.append(Error(101, "malformed command"))

    # Source compliance

    @message(r'^(?::?SENS)?:VOLT:PROT(?::LEV)?\?$')
    def get_sense_voltage_protection_level(self) -> str:
        return format(self.sense_voltage_protection_level, "E")

    @message(r'^(?::?SENS)?:VOLT:PROT(?::LEV)? (.+)$')
    def set_sense_voltage_protection_level(self, level) -> None:
        try:
            self.sense_voltage_protection_level = float(level)
        except ValueError:
            self.error_queue.append(Error(101, "malformed command"))

    @message(r'^(?::?SENS)?:VOLT:PROT:TRIP\?$')
    def get_sense_voltage_protection_tripped(self) -> str:
        return format(False, "d")  # TODO

    @message(r'^(?::?SENS)?:CURR:PROT(?::LEV)?\?$')
    def get_sense_current_protection_level(self) -> str:
        return format(self.sense_current_protection_level, "E")

    @message(r'^(?::?SENS)?:CURR:PROT(?::LEV)? (.+)$')
    def set_sense_current_protection_level(self, level) -> None:
        try:
            self.sense_current_protection_level = float(level)
        except ValueError:
            self.error_queue.append(Error(101, "malformed command"))

    @message(r'^(?::?SENS)?:CURR:PROT:TRIP\?$')
    def get_sense_current_protection_tripped(self) -> str:
        return format(False, "d")  # TODO

    # Sense function

    @message(r'^(?::?SENS)?:FUNC(?::ON)?\?$')
    def get_sense_function_on(self) -> str:
        return format(self.sense_function)

    @message(r'^(?::?SENS)?:FUNC(?::ON)? \'(VOLT|CURR|RES|TIME|STAT)\'$')
    def set_sense_function_on(self, value) -> None:
        self.sense_function.add(value)

    # TODO
    @message(r'^(?::?SENS)?:FUNC(?::ON)? \'VOLT\',\s*\'CURR\'$')
    def set_sense_function_on_2(self) -> None:
        self.sense_function.add("VOLT")
        self.sense_function.add("CURR")

    # Concurrent function

    @message(r'^(?::?SENS)?:FUNC:CONC\?$')
    def get_sense_function_concurrent(self) -> int:
        return int(self.sense_function_concurrent)

    @message(r'^(?::?SENS)?:FUNC:CONC (OFF|ON|0|1)$')
    def set_sense_function_concurrent(self, state) -> None:
        self.sense_function_concurrent = {"OFF": False, "ON": True, "0": False, "1": True}[state]

    # Average

    @message(r'^(?::?SENS)?:AVER:TCON\?$')
    def get_sense_average_tcontrol(self) -> str:
        return self.sense_average_tcontrol

    @message(r'^(?::?SENS)?:AVER:TCON (REP|MOV)$')
    def set_sense_average_tcontrol(self, state: str) -> None:
        self.sense_average_tcontrol = state

    @message(r'^(?::?SENS)?:AVER:COUN\?$')
    def get_sense_average_count(self) -> int:
        return self.sense_average_count

    @message(r'^(?::?SENS)?:AVER:COUN (\d+)$')
    def set_sense_average_count(self, count: str) -> None:
        self.sense_average_count = int(count)

    @message(r'^(?::?SENS)?:AVER(?::STAT)?\?$')
    def get_sense_average_state(self) -> int:
        return int(self.sense_average_state)

    @message(r'^(?::?SENS)?:AVER(?::STAT)? (OFF|ON|0|1)$')
    def set_sense_average_state(self, state) -> None:
        self.sense_average_state = {"OFF": False, "ON": True, "0": False, "1": True}[state]

    # Integration time

    @message(r'^(?::?SENS)?:(?:VOLT|CURR|RES):NPLC\?$')
    def get_sense_nplc(self) -> str:
        return format(self.sense_nplc, "E")

    @message(r'^(?::?SENS)?:(?:VOLT|CURR|RES):NPLC (.+)$')
    def set_sense_nplc(self, nplc: str) -> None:
        self.sense_nplc = round(float(nplc), 2)

    # Format

    @message(r'^:?FORM:ELEM\?$')
    def get_format_elements(self) -> str:
        return format(self.format_elements)

    @message(r'^:?FORM:ELEM (.+)$')
    def set_format_elements(self, elements) -> None:
        elements = [element.strip() for element in elements.split(",") if element.strip()]
        self.format_elements.clear()
        self.format_elements.update(elements)

    # Measure

    @message(r'^:?INIT(?:iate)?$')
    def set_initiate(self) -> None: ...

    @message(r'^:?READ\?$')
    def get_read(self) -> str:
        result = []
        if "VOLT" in self.format_elements._values:
            curr_min = float(self.options.get("volt.min", self.source_level.get("VOLT")))
            curr_max = float(self.options.get("volt.max", self.source_level.get("VOLT")))
            result.append(format(random.uniform(curr_min, curr_max), "E"))
        if "CURR" in self.format_elements._values:
            curr_min = float(self.options.get("curr.min", 1e6))
            curr_max = float(self.options.get("curr.max", 1e7))
            result.append(format(random.uniform(curr_min, curr_max), "E"))
        if "RES" in self.format_elements._values:
            result.append(format(float("nan")))
        if "TIME" in self.format_elements._values:
            result.append(format(float("nan")))
        if "STAT" in self.format_elements._values:
            result.append(format(0))
        return ",".join(result)

    @message(r'^:?FETC[H]?\?$')
    def get_fetch(self) -> str:
        curr_min = float(self.options.get("curr.min", 1e6))
        curr_max = float(self.options.get("curr.max", 1e7))
        return format(random.uniform(curr_min, curr_max), "E")

    @message(r'^(.*)$')
    def unknown_message(self, request) -> None:
        self.error_queue.append(Error(101, "malformed command"))


class SenseFunction:

    ALLOWED_VALUES = ["VOLT:DC", "CURR:DC", "RES"]
    ALIAS_VALUES = {"VOLT": "VOLT:DC", "CURR": "CURR:DC"}

    def __init__(self) -> None:
        self._values: set[str] = set()

    def add(self, value) -> None:
        if value in self.ALIAS_VALUES:
            value = self.ALIAS_VALUES.get(value)
        if value in self.ALLOWED_VALUES:
            self._values.add(value)

    def remove(self, value) -> None:
        if value in self.ALIAS_VALUES:
            value = self.ALIAS_VALUES.get(value)
        if value in self._values:
            self._values.remove(value)

    def clear(self) -> None:
        self._values.clear()

    def update(self, values) -> None:
        for value in values:
            self.add(value)

    def __str__(self) -> str:
        values = sorted(self._values, key=lambda value: self.ALLOWED_VALUES.index(value))
        return ",".join([f"'{value}'" for value in values])


class FormatElements:

    ALLOWED_VALUES = ["VOLT", "CURR", "RES", "TIME", "STAT"]

    def __init__(self) -> None:
        self._values: set[str] = set()

    def add(self, value) -> None:
        if value in self.ALLOWED_VALUES:
            self._values.add(value)

    def remove(self, value) -> None:
        if value in self._values:
            self._values.remove(value)

    def clear(self) -> None:
        self._values.clear()

    def update(self, values) -> None:
        for value in values:
            self.add(value)

    def __str__(self) -> str:
        values = sorted(self._values, key=lambda value: self.ALLOWED_VALUES.index(value))
        return ",".join(values)


if __name__ == "__main__":
    run(K2400Emulator())
