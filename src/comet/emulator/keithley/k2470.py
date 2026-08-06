import random

from comet.emulator import Context, IEC60488Emulator, message, run
from comet.emulator.utils import Error, tsp_assign, tsp_print


class K2470Emulator(IEC60488Emulator):
    IDENTITY: str = "Keithley Inc., Model 2470, 43768438, v1.0 (Emulator)"
    LANGUAGE: str = "SCPI"

    DEFAULT_VOLTAGE_PROTECTION_LEVEL: float = 1050.0

    def __init__(self, context: Context) -> None:
        super().__init__(context)

        options = context.options

        self.language: str = str(options.get("language", self.LANGUAGE))
        self.error_queue: list[Error] = []
        self.route_terminals: str = "FRON"
        self.output_state: bool = False
        self.source_function_mode: str = "VOLT"
        self.source_level: dict[str, float] = {"VOLT": 0.0, "CURR": 0.0}
        self.source_range: dict[str, float] = {"VOLT": 0.0, "CURR": 0.0}
        self.source_range_auto: dict[str, bool] = {"VOLT": True, "CURR": True}
        self.source_voltage_protection_level: float = (
            self.DEFAULT_VOLTAGE_PROTECTION_LEVEL
        )
        self.source_voltage_ilimit_level: float = 1.05e-4
        self.source_current_vlimit_level: float = 2.1e-1
        self.sense_function_on: str = "CURR"
        self.source_voltage_delay_auto: bool = True
        self.sense_curr_azero: bool = True
        self.sense_curr_range: float = 1.0e-08
        self.sense_curr_range_auto: bool = True
        self.sense_curr_range_auto_llimit: float = 1.0e-08
        self.sense_curr_range_auto_ulimit: float = 1.0  # read only
        self.sense_average_tcontrol: dict[str, str] = {"VOLT": "REP", "CURR": "REP"}
        self.sense_average_count: dict[str, int] = {"VOLT": 10, "CURR": 10}
        self.sense_average_state: dict[str, bool] = {"VOLT": False, "CURR": False}
        self.sense_nplc: float = 1.0
        self.system_breakdown_protection: str = "OFF"
        self.output_interlock_tripped = bool(options.get("interlock.tripped", True))

        self.volt_min = float(options.get("volt.min", 0))
        self.volt_max = float(options.get("volt.max", 10))
        self.curr_min = float(options.get("curr.min", 1e-6))
        self.curr_max = float(options.get("curr.max", 1e-7))

    @message(r"\*LANG\?$")
    def get_lang(self) -> str:
        return self.language

    @message(r"\*RST$")
    def set_rst(self) -> None:
        self.error_queue.clear()
        self.route_terminals = "FRON"
        self.output_state = False
        self.source_function_mode = "VOLT"
        self.source_level.update({"VOLT": 0.0, "CURR": 0.0})
        self.source_range.update({"VOLT": 0.0, "CURR": 0.0})
        self.source_range_auto.update({"VOLT": True, "CURR": True})
        self.source_voltage_protection_level = self.DEFAULT_VOLTAGE_PROTECTION_LEVEL
        self.source_voltage_ilimit_level = 1.05e-4
        self.source_current_vlimit_level = 2.1e-1
        self.sense_function_on = "CURR"
        self.source_voltage_delay_auto = True
        self.sense_curr_azero = True
        self.sense_curr_range = 1.0e-08
        self.sense_curr_range_auto = True
        self.sense_curr_range_auto_llimit = 1.0e-08
        self.sense_curr_range_auto_ulimit = 1.0  # read only
        self.sense_average_tcontrol.update({"VOLT": "REP", "CURR": "REP"})
        self.sense_average_count.update({"VOLT": 10, "CURR": 10})
        self.sense_average_state.update({"VOLT": False, "CURR": False})
        self.sense_nplc = 1.0
        self.system_breakdown_protection = "OFF"

    @message(r"\*CLS$")
    def set_cls(self) -> None:
        self.error_queue.clear()

    @message(r":?SYST:ERR(?::NEXT)?\?$")
    def get_system_error_next(self) -> str:
        if self.error_queue:
            error = self.error_queue.pop(0)
        else:
            error = Error(0, "no error")
        return f'{error.code}, "{error.message}"'

    @message(r":?SYST:BRE:PROT\?$")
    def get_system_breakdown_protection(self) -> str:
        return self.system_breakdown_protection

    @message(r":?SYST:BRE:PROT\s+(AUTO|OFF|ON)$")
    def set_system_breakdown_protection(self, state) -> None:
        self.system_breakdown_protection = state

    # Route terminal

    @message(r":?ROUT:TERM\?$")
    def get_route_terminals(self) -> str:
        return self.route_terminals

    @message(r":?ROUT:TERM\s+(FRON|REAR)$")
    def set_route_terminals(self, terminal) -> None:
        self.route_terminals = terminal

    # Output state

    @message(r":?OUTP(?::STAT)?\?$")
    def get_output_state(self) -> str:
        return {False: "0", True: "1"}[self.output_state]

    @message(r":?OUTP(?::STAT)?\s+(.+)$")
    def set_output_state(self, state) -> None:
        try:
            self.output_state = {"ON": True, "OFF": False, "0": False, "1": True}[state]
        except KeyError:
            self.error_queue.append(Error(101, "malformed command"))

    @message(r":?OUTP:INT:TRIP\?$")
    def get_output_interlock_tripped(self) -> str:
        return {False: "0", True: "1"}[self.output_interlock_tripped]

    # Source function mode

    @message(r":?SOUR:FUNC(?::MODE)?\?$")
    def get_source_function_mode(self) -> str:
        return self.source_function_mode

    @message(r":?SOUR:FUNC(?::MODE)?\s+(VOLT|CURR)$")
    def set_source_function_mode(self, function) -> None:
        try:
            self.source_function_mode = function
        except KeyError:
            self.error_queue.append(Error(101, "malformed command"))

    @message(r":?SOUR:VOLT:DEL:AUTO\?$")
    def get_source_voltage_delay_auto(self) -> str:
        return format(self.source_voltage_delay_auto, "E")

    @message(r":?SOUR:VOLT:DEL:AUTO\s+(OFF|ON|0|1)$")
    def set_source_voltage_delay_auto(self, enable) -> None:
        self.source_voltage_delay_auto = {
            "ON": True,
            "OFF": False,
            "0": False,
            "1": True,
        }[enable]

    # Source levels

    @message(r":?SOUR:(VOLT|CURR)(?::LEV)?\?$")
    def get_source_level(self, function) -> str:
        return format(self.source_level[function], "E")

    @message(r":?SOUR:(VOLT|CURR)(?::LEV)?\s+(.+)$")
    def set_source_level(self, function, level) -> None:
        try:
            self.source_level[function] = float(level)
        except ValueError:
            self.error_queue.append(Error(101, "malformed command"))

    # Source range levels

    @message(r":?SOUR:(VOLT|CURR):RANG\?$")
    def get_source_range_level(self, function) -> str:
        return format(self.source_range[function], "E")

    @message(r":?SOUR:(VOLT|CURR):RANG\s+(.+)$")
    def set_source_range_level(self, function, level) -> None:
        try:
            self.source_range[function] = float(level)
            self.source_range_auto[function] = False
        except ValueError:
            self.error_queue.append(Error(101, "malformed command"))

    # Source auto ranges

    @message(r":?SOUR:(VOLT|CURR):RANG:AUTO\?$")
    def get_source_range_auto(self, function) -> int:
        return int(self.source_range_auto[function])

    @message(r":?SOUR:(VOLT|CURR):RANG:AUTO\s+(.+)$")
    def set_source_range_auto(self, function, state) -> None:
        try:
            self.source_range_auto[function] = {
                "ON": True,
                "OFF": False,
                "0": False,
                "1": True,
            }[state]
        except ValueError:
            self.error_queue.append(Error(101, "malformed command"))

    # Source voltage limit

    @message(r":?SOUR:VOLT:PROT(?::LEV)?\?$")
    def get_source_voltage_protection_level(self) -> str:
        return format(self.source_voltage_protection_level, "E")

    @message(r":?SOUR:VOLT:PROT(?::LEV)?\s+(.+)$")
    def set_source_voltage_protection_level(self, level) -> None:
        try:
            self.source_voltage_protection_level = float(level)
        except ValueError:
            self.error_queue.append(Error(101, "malformed command"))

    # Source compliance

    @message(r":?SOUR:VOLT:ILIM(?::LEV)?\?$")
    def get_source_voltage_ilimit_level(self) -> str:
        return format(self.source_voltage_ilimit_level, "E")

    @message(r":?SOUR:VOLT:ILIM(?::LEV)?\s+(.+)$")
    def set_source_voltage_ilimit_level(self, level) -> None:
        try:
            self.source_voltage_ilimit_level = float(level)
        except ValueError:
            self.error_queue.append(Error(101, "malformed command"))

    @message(r":?SOUR:VOLT:ILIM(?::LEV)?:TRIP\?$")
    def get_source_voltage_ilimit_level_tripped(self) -> str:
        return format(False, "E")  # TODO

    @message(r":?SOUR:CURR:VLIM(?::LEV)?\?$")
    def get_source_current_vlimit_level(self) -> str:
        return format(self.source_current_vlimit_level, "E")

    @message(r":?SOUR:CURR:VLIM(?::LEV)?\s+(.+)$")
    def set_source_current_vlimit_level(self, level) -> None:
        try:
            self.source_current_vlimit_level = float(level)
        except ValueError:
            self.error_queue.append(Error(101, "malformed command"))

    @message(r":?SOUR:CURR:VLIM(?::LEV)?:TRIP\?$")
    def get_source_current_vlimit_level_tripped(self) -> str:
        return format(False, "E")  # TODO

    @message(r":?SENS:FUNC(?::ON)?\s+\"(CURR|RES|VOLT)\"$")
    def set_sense_function_on(self, function: str) -> None:
        self.sense_function_on = function

    # Sense range

    @message(r":?SENS:CURR:AZER\?$")
    def get_sense_curr_azero(self) -> str:
        return format(self.sense_curr_azero, "E")

    @message(r":?SENS:CURR:AZER\s+(OFF|ON|0|1)$")
    def set_sense_curr_azero(self, enable) -> None:
        self.sense_curr_azero = {
            "ON": True,
            "OFF": False,
            "0": False,
            "1": True,
        }[enable]

    @message(r":?SENS:CURR:RANG\?$")
    def get_sense_curr_range(self) -> str:
        return format(self.sense_curr_range, "E")

    @message(r":?SENS:CURR:RANG\s+(.+)$")
    def set_sense_curr_range(self, level: str) -> None:
        self.sense_curr_range = float(level)

    @message(r":?SENS:CURR:RANG:AUTO\?$")
    def get_sense_curr_range_auto(self) -> str:
        return format(self.sense_curr_range_auto, "E")

    @message(r":?SENS:CURR:RANG:AUTO\s+(OFF|ON|0|1)$")
    def set_sense_curr_range_auto(self, enabled: str) -> None:
        self.sense_curr_range_auto = {
            "OFF": False,
            "ON": True,
            "0": False,
            "1": True,
        }[enabled]

    @message(r":?SENS:CURR:RANG:AUTO:LLIM\?$")
    def get_sense_curr_range_auto_llimit(self) -> str:
        return format(self.sense_curr_range_auto_llimit, "E")

    @message(r":?SENS:CURR:RANG:AUTO:LLIM\s+(.+)$")
    def set_sense_curr_range_auto_llimit(self, level: str) -> None:
        self.sense_curr_range_auto_llimit = float(level)

    @message(r":?SENS:CURR:RANG:AUTO:ULIM\?$")
    def get_sense_curr_range_auto_ulimit(self) -> str:
        return format(self.sense_curr_range_auto_ulimit, "E")

    # Average

    @message(r":?SENS:(VOLT|CURR):AVER:TCON\?$")
    def get_sense_average_tcontrol(self, function: str) -> str:
        return format(self.sense_average_tcontrol[function], "E")

    @message(r":?SENS:(VOLT|CURR):AVER:TCON\s+(MOV|REP)$")
    def set_sense_average_tcontrol(self, function: str, tcontrol: str) -> None:
        self.sense_average_tcontrol[function] = tcontrol

    @message(r":?SENS:(VOLT|CURR):AVER:COUN[T]?\?$")
    def get_sense_average_count(self, function: str) -> str:
        return format(self.sense_average_count[function], "E")

    @message(r":?SENS:(VOLT|CURR):AVER:COUN[T]?\s+(\d+)$")
    def set_sense_average_count(self, function: str, count: str) -> None:
        self.sense_average_count[function] = int(count)

    @message(r":?SENS:(VOLT|CURR):AVER:STAT[E]?\?$")
    def get_sense_average_state(self, function: str) -> str:
        return format(self.sense_average_state[function], "E")

    @message(r":?SENS:(VOLT|CURR):AVER:STAT[E]?\s+(OFF|ON|0|1)$")
    def set_sense_average_state(self, function: str, state: str) -> None:
        self.sense_average_state[function] = {
            "OFF": False,
            "ON": True,
            "0": False,
            "1": True,
        }[state]

    # Integration time

    @message(r"(?::?SENS)?:(?:VOLT|CURR|RES):NPLC\?$")
    def get_sense_nplc(self) -> str:
        return format(self.sense_nplc, "E")

    @message(r"(?::?SENS)?:(?:VOLT|CURR|RES):NPLC\s+(.+)$")
    def set_sense_nplc(self, nplc: str) -> None:
        self.sense_nplc = round(float(nplc), 2)

    # Measure

    @message(r":?READ\?$")
    def get_read(self) -> str:
        read = self._read_current()
        return format(read, "E")

    @message(r":?READ\?\s+\"([a-zA-Z0-9_]+)\",\s+SOUR,\s+READ$")
    def get_read_elements(self, _buffer: str) -> str:
        sour = self._read_voltage()
        read = self._read_current()
        return f"{sour:E},{read:E}"

    @message(r":?INIT(?::IMM)?$")
    def set_init(self) -> None: ...

    @message(r":?MEAS:VOLT\?$")
    def get_measure_voltage(self) -> str:
        volt = self._read_voltage()
        return format(volt, "E")

    @message(r":?MEAS:CURR\?$")
    def get_measure_current(self) -> str:
        curr = self._read_current()
        return format(curr, "E")

    @message(r":?TRAC[E]?:CLE\s+\"([a-zA-Z0-9_]+)\"$")
    def set_trace_clear(self, _buffer: str) -> None: ...

    @message(r":?TRAC[E]?:TRIG\s+\"([a-zA-Z0-9_]+)\"$")
    def set_trace_trigger(self, _buffer: str) -> None: ...

    @message(r":?TRAC[E]?:DATA\?\s+1,\s+1,\s+\"([a-zA-Z0-9_]+)\",\s+SOUR,\s+READ$")
    def get_trace_data(self, _buffer: str) -> str:
        sour = self._read_voltage()
        read = self._read_current()
        return f"{sour:E},{read:E}"

    # TSP

    @message(r"reset\(\)$")
    def write_reset(self) -> None:
        self.error_queue.clear()

    @message(r"clear\(\)$")
    def write_clear(self) -> None:
        self.error_queue.clear()

    @message(r"errorqueue\.clear\(\)$")
    def set_errorqueue_clear(self) -> None:
        self.error_queue.clear()

    @message(tsp_print(r"errorqueue\.count"))
    def get_errorqueue_count(self) -> int:
        return len(self.error_queue)

    @message(tsp_print(r"errorqueue\.next\(\)"))
    def get_errorqueue_next(self) -> str:
        if self.error_queue:
            error = self.error_queue.pop(0)
            return f'{error.code}, "{error.message}", 0, 0'
        return '0, "Queue is Empty", 0, 0'

    @message(tsp_print(r"smu\.source\.output"))
    def get_tsp_source_output(self) -> int:
        return {False: 0, True: 1}[self.smu_source_output]

    @message(tsp_assign(r"smu\.source\.output"))
    def set_tsp_source_output(self, value) -> None:
        try:
            self.smu_source_output = {
                "smu.ON": True,
                "smu.OFF": False,
                "0": False,
                "1": True,
            }[value]
        except KeyError:
            self.error_queue.append(Error(101, "malformed command"))

    @message(r".*")
    def unknown_message(self) -> None:
        self.error_queue.append(Error(101, "malformed command"))

    def _read_voltage(self) -> float:
        return random.uniform(self.volt_min, self.volt_max)

    def _read_current(self) -> float:
        return random.uniform(self.curr_min, self.curr_max)


if __name__ == "__main__":
    run(K2470Emulator)
