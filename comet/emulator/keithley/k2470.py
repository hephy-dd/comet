import random
from typing import Dict, List, Tuple

from comet.emulator import IEC60488Emulator, message, run
from comet.emulator.utils import tsp_print, tsp_assign, Error


class K2470Emulator(IEC60488Emulator):

    IDENTITY: str = "Keithley Inc., Model 2470, 43768438, v1.0 (Emulator)"
    LANGUAGE: str = "SCPI"

    DEFAULT_VOLTAGE_PROTECTION_LEVEL: float = 1050.

    def __init__(self) -> None:
        super().__init__()
        self.language: str = str(self.options.get("language", self.LANGUAGE))
        self.error_queue: List[Error] = []
        self.route_terminals: str = "FRON"
        self.output_state: bool = False
        self.source_function_mode: str = "VOLT"
        self.source_level: Dict = {"VOLT": 0., "CURR": 0.}
        self.source_range: Dict = {"VOLT": 0., "CURR": 0.}
        self.source_range_auto: Dict = {"VOLT": True, "CURR": True}
        self.source_voltage_protection_level: float = self.DEFAULT_VOLTAGE_PROTECTION_LEVEL
        self.source_voltage_ilimit_level: float = 1.05e-4
        self.source_current_vlimit_level: float = 2.1e-1
        self.sense_average_tcontrol: Dict = {"VOLT": "REP", "CURR": "REP"}
        self.sense_average_count: Dict = {"VOLT": 10, "CURR": 10}
        self.sense_average_state: Dict = {"VOLT": False, "CURR": False}
        self.sense_nplc: float = 1.0
        self.system_breakdown_protection: str = "OFF"

    @property
    def output_interlock_tripped(self):
        return bool(self.options.get("interlock.tripped", True))

    @message(r'^\*LANG\?$')
    def get_lang(self):
        return self.language

    @message(r'^\*RST$')
    def set_rst(self):
        self.error_queue.clear()
        self.route_terminals = "FRON"
        self.output_state = False
        self.source_function_mode = "VOLT"
        self.source_level.update({"VOLT": 0., "CURR": 0.})
        self.source_range.update({"VOLT": 0., "CURR": 0.})
        self.source_range_auto.update({"VOLT": True, "CURR": True})
        self.source_voltage_protection_level = self.DEFAULT_VOLTAGE_PROTECTION_LEVEL
        self.source_voltage_ilimit_level = 1.05e-4
        self.source_current_vlimit_level = 2.1e-1
        self.sense_average_tcontrol.update({"VOLT": "REP", "CURR": "REP"})
        self.sense_average_count.update({"VOLT": 10, "CURR": 10})
        self.sense_average_state.update({"VOLT": False, "CURR": False})
        self.sense_nplc = 1.0
        self.system_breakdown_protection = "OFF"

    @message(r'^\*CLS$')
    def set_cls(self):
        self.error_queue.clear()

    @message(r'^:?SYST:ERR(?::NEXT)?\?$')
    def get_system_error_next(self):
        if self.error_queue:
            error = self.error_queue.pop(0)
        else:
            error = Error(0, "no error")
        return f'{error.code}, "{error.message}"'

    @message(r'^:?SYST:BRE:PROT\?$')
    def get_system_breakdown_protection(self):
        return self.system_breakdown_protection

    @message(r'^:?SYST:BRE:PROT (AUTO|OFF|ON)$')
    def set_system_breakdown_protection(self, state):
        self.system_breakdown_protection = state

    # Route terminal

    @message(r'^:?ROUT:TERM\?$')
    def get_route_terminals(self):
        return self.route_terminals

    @message(r'^:?ROUT:TERM (FRON|REAR)$')
    def set_route_terminals(self, terminal):
        self.route_terminals = terminal

    # Output state

    @message(r'^:?OUTP(?::STAT)?\?$')
    def get_output_state(self):
        return {False: "0", True: "1"}[self.output_state]

    @message(r'^:?OUTP(?::STAT)? (.+)$')
    def set_output_state(self, state):
        try:
            self.output_state = {"ON": True, "OFF": False, "0": False, "1": True}[state]
        except KeyError:
            self.error_queue.append(Error(101, "malformed command"))

    @message(r'^:?OUTP:INT:TRIP\?$')
    def get_output_interlock_tripped(self):
        return {False: "0", True: "1"}[self.output_interlock_tripped]

    # Source function mode

    @message(r'^:?SOUR:FUNC(?::MODE)?\?$')
    def get_source_function_mode(self):
        return self.source_function_mode

    @message(r'^:?SOUR:FUNC(?::MODE)? (VOLT|CURR)$')
    def set_source_function_mode(self, function):
        try:
            self.source_function_mode = function
        except KeyError:
            self.error_queue.append(Error(101, "malformed command"))

    # Source levels

    @message(r'^:?SOUR:(VOLT|CURR)(?::LEV)?\?$')
    def get_source_level(self, function):
        return format(self.source_level[function], "E")

    @message(r'^:?SOUR:(VOLT|CURR)(?::LEV)? (.+)$')
    def set_source_level(self, function, level):
        try:
            self.source_level[function] = float(level)
        except ValueError:
            self.error_queue.append(Error(101, "malformed command"))

    # Source range levels

    @message(r'^:?SOUR:(VOLT|CURR):RANG\?$')
    def get_source_range_level(self, function):
        return format(self.source_range[function], "E")

    @message(r'^:?SOUR:(VOLT|CURR):RANG (.+)$')
    def set_source_range_level(self, function, level):
        try:
            self.source_range[function] = float(level)
            self.source_range_auto[function] = False
        except ValueError:
            self.error_queue.append(Error(101, "malformed command"))

    # Source auto ranges

    @message(r'^:?SOUR:(VOLT|CURR):RANG:AUTO\?$')
    def get_source_range_auto(self, function):
        return int(self.source_range_auto[function])

    @message(r'^:?SOUR:(VOLT|CURR):RANG:AUTO (.+)$')
    def set_source_range_auto(self, function, state):
        try:
            self.source_range_auto[function] = {"ON": True, "OFF": False, "0": False, "1": True}[state]
        except ValueError:
            self.error_queue.append(Error(101, "malformed command"))

    # Source voltage limit

    @message(r'^:?SOUR:VOLT:PROT(?::LEV)?\?$')
    def get_source_voltage_protection_level(self):
        return format(self.source_voltage_protection_level, "E")

    @message(r'^:?SOUR:VOLT:PROT(?::LEV)? (.+)$')
    def set_source_voltage_protection_level(self, level):
        try:
            self.source_voltage_protection_level = float(level)
        except ValueError:
            self.error_queue.append(Error(101, "malformed command"))

    # Source compliance

    @message(r'^:?SOUR:VOLT:ILIM(?::LEV)?\?$')
    def get_source_voltage_ilimit_level(self):
        return format(self.source_voltage_ilimit_level, "E")

    @message(r'^:?SOUR:VOLT:ILIM(?::LEV)? (.+)$')
    def set_source_voltage_ilimit_level(self, level):
        try:
            self.source_voltage_ilimit_level = float(level)
        except ValueError:
            self.error_queue.append(Error(101, "malformed command"))

    @message(r'^:?SOUR:VOLT:ILIM(?::LEV)?:TRIP\?$')
    def get_source_voltage_ilimit_level_tripped(self):
        return format(False, "E")  # TODO

    @message(r'^:?SOUR:CURR:VLIM(?::LEV)?\?$')
    def get_source_current_vlimit_level(self):
        return format(self.source_current_vlimit_level, "E")

    @message(r'^:?SOUR:CURR:VLIM(?::LEV)? (.+)$')
    def set_source_current_vlimit_level(self, level):
        try:
            self.source_current_vlimit_level = float(level)
        except ValueError:
            self.error_queue.append(Error(101, "malformed command"))

    @message(r'^:?SOUR:CURR:VLIM(?::LEV)?:TRIP\?$')
    def get_source_current_vlimit_level_tripped(self):
        return format(False, "E")  # TODO

    # Average

    @message(r'^:?SENS:(VOLT|CURR):AVER:TCON\?$')
    def get_sense_average_tcontrol(self, function: str):
        return format(self.sense_average_tcontrol[function], "E")

    @message(r'^:?SENS:(VOLT|CURR):AVER:TCON (MOV|REP)$')
    def set_sense_average_tcontrol(self, function: str, tcontrol: str):
        self.sense_average_tcontrol[function] = tcontrol

    @message(r'^:?SENS:(VOLT|CURR):AVER:COUN[T]?\?$')
    def get_sense_average_count(self, function: str):
        return format(self.sense_average_count[function], "E")

    @message(r':?SENS:(VOLT|CURR):AVER:COUN[T]? (\d+)$')
    def set_sense_average_count(self, function: str, count: str):
        self.sense_average_count[function] = int(count)

    @message(r'^:?SENS:(VOLT|CURR):AVER:STAT[E]?\?$')
    def get_sense_average_state(self, function: str):
        return format(self.sense_average_state[function], "E")

    @message(r'^:?SENS:(VOLT|CURR):AVER:STAT[E]? (OFF|ON|0|1)$')
    def set_sense_average_state(self, function: str, state: str):
        self.sense_average_state[function] = {"OFF": False, "ON": True, "0": False, "1": True}[state]

    # Integration time

    @message(r'^(?::?SENS)?:(?:VOLT|CURR|RES):NPLC\?$')
    def get_sense_nplc(self):
        return format(self.sense_nplc, "E")

    @message(r'^(?::?SENS)?:(?:VOLT|CURR|RES):NPLC (.+)$')
    def set_sense_nplc(self, nplc: str):
        self.sense_nplc = round(float(nplc), 2)

    # Measure

    @message(r'^:?MEAS:VOLT\?$')
    def get_measure_voltage(self):
        volt_min = float(self.options.get("curr.min", 0))
        volt_max = float(self.options.get("curr.max", 10))
        return format(random.uniform(volt_min, volt_max), "E")

    @message(r'^:?MEAS:CURR\?$')
    def get_measure_current(self):
        curr_min = float(self.options.get("curr.min", 1e6))
        curr_max = float(self.options.get("curr.max", 1e7))
        return format(random.uniform(curr_min, curr_max), "E")

    # TSP

    @message(r'^reset\(\)$')
    def write_reset(self):
        self.error_queue.clear()

    @message(r'^clear\(\)$')
    def write_clear(self):
        self.error_queue.clear()

    @message(r'^errorqueue\.clear\(\)$')
    def set_errorqueue_clear(self):
        self.error_queue.clear()

    @message(tsp_print(r'errorqueue\.count'))
    def get_errorqueue_count(self):
        return len(self.error_queue)

    @message(tsp_print(r'errorqueue\.next\(\)'))
    def get_errorqueue_next(self):
        if self.error_queue:
            code, message = self.error_queue.pop(0)
            return f"{code}, \"{message}\", 0, 0"
        return "0, \"Queue is Empty\", 0, 0"

    @message(tsp_print(r'smu\.source\.output'))
    def get_tsp_source_output(self):
        return {False: 0, True: 1}[self.smu_source_output]

    @message(tsp_assign(r'smu\.source\.output'))
    def set_tsp_source_output(self, value):
        try:
            self.smu_source_output = {
                "smu.ON": True, "smu.OFF": False,
                "0": False, "1": True
            }[value]
        except KeyError:
            self.error_queue.append(Error(101, "malformed command"))

    @message(r'^.*$')
    def unknown_message(self):
        self.error_queue.append(Error(101, "malformed command"))


if __name__ == "__main__":
    run(K2470Emulator())
