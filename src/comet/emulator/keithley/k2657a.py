import random
from typing import Dict, List

from comet.emulator import IEC60488Emulator, message, run
from comet.emulator.utils import tsp_print, tsp_assign, Error


class K2657AEmulator(IEC60488Emulator):

    IDENTITY: str = "Keithley Inc., Model 2657A, 43768438, v1.0 (Emulator)"

    def __init__(self) -> None:
        super().__init__()
        self.error_queue: List[Error] = []
        self.beeper_enable: bool = True
        self.smua_source_output: bool = False
        self.smua_source_function = "DCVOLTS"
        self.smua_source_level: Dict = {"v": 0., "i": 0.}
        self.smua_source_range: Dict = {"v": 0., "i": 0.}
        self.smua_source_autorange: Dict = {"v": True, "i": True}
        self.smua_source_limit: Dict = {"v": 0., "i": 0.}
        self.smua_measure_filter_enable: bool = False
        self.smua_measure_filter_count: int = 1
        self.smua_measure_filter_type: int = 1
        self.smua_measure_nplc: float = 1.0
        self.source_protectv: float = 0.

    @message(r'^reset\(\)$')
    def set_reset(self):
        self.error_queue.clear()
        self.beeper_enable = True
        self.smua_source_output = False
        self.smua_source_function = "DCVOLTS"
        self.smua_source_level.update({"v": 0., "i": 0.})
        self.smua_source_range.update({"v": 0., "i": 0.})
        self.smua_source_autorange.update({"v": True, "i": True})
        self.smua_source_limit.update({"v": 0., "i": 0.})
        self.smua_measure_filter_enable = False
        self.smua_measure_filter_count = 1
        self.smua_measure_filter_type = 1
        self.smua_measure_nplc = 1.0
        self.source_protectv = 0.

    @message(r'^status.reset\(\)$')
    def set_status_reset(self):
        self.error_queue.clear()

    @message(r'^clear\(\)$')
    def set_clear(self):
        self.error_queue.clear()

    @message(r'^errorqueue\.clear\(\)$')
    def set_errorqueue_clear(self):
        self.error_queue.clear()

    @message(tsp_print(r'errorqueue\.count'))
    def get_errorqueue_count(self):
        return format(len(self.error_queue), "d")

    @message(tsp_print(r'errorqueue\.next\(\)'))
    def get_errorqueue_next(self):
        if self.error_queue:
            error = self.error_queue.pop(0)
        else:
            error = Error(0, "Queue Is Empty")
        return f"{error.code}\t\"{error.message}\"\t0\t0"

    # Beeper

    @message(tsp_print(r'beeper\.enabled'))
    def get_beeper_enabled(self):
        return format(self.beeper_enable, "d")

    @message(tsp_assign(r'beeper\.enable'))
    def set_beeper_enable(self, enable: str):
        try:
            self.beeper_enable = {
                "beeper.ON": True, "beeper.OFF": False,
                "0": False, "1": True
            }[enable]
        except KeyError:
            self.error_queue.append(Error(110, "malformed command"))

    # Source output

    @message(tsp_print(r'smua\.source\.output'))
    def get_source_output(self):
        return format(self.smua_source_output, "E")

    @message(tsp_assign(r'smua\.source\.output'))
    def set_source_output(self, state):
        try:
            self.smua_source_output = {
                "smua.OUTPUT_ON": True, "smua.OUTPUT_OFF": False,
                "0": False, "1": True
            }[state]
        except KeyError:
            self.error_queue.append(Error(111, "malformed command"))

    # Source function

    @message(tsp_print(r'smua\.source\.func'))
    def get_source_function(self):
        return format({"DCAMPS": 0, "DCVOLTS": 1}[self.smua_source_function], "E")

    @message(tsp_assign(r'smua\.source\.func'))
    def set_source_function(self, function):
        try:
            self.smua_source_function = {
                "0": "DCAMPS", "smua.OUTPUT_DCAMPS": "DCAMPS",
                "1": "DCVOLTS", "smua.OUTPUT_DCVOLTS": "DCVOLTS"
            }[function]
        except KeyError:
            self.error_queue.append(Error(112, "malformed command"))

    # Source levels

    @message(tsp_print(r'smua\.source\.level([iv])'))
    def get_source_level(self, function):
        return format(self.smua_source_level[function], "E")

    @message(tsp_assign(r'smua\.source\.level([iv])'))
    def set_source_level(self, function, level):
        try:
            self.smua_source_level[function] = float(level)
        except ValueError:
            self.error_queue.append(Error(113, "malformed command"))

    # Source ranges

    @message(tsp_print(r'smua\.source\.range([iv])'))
    def get_source_range(self, function):
        return format(self.smua_source_range[function], "E")

    @message(tsp_assign(r'smua\.source\.range([iv])'))
    def set_source_range(self, function, level):
        try:
            self.smua_source_range[function] = float(level)
        except ValueError:
            self.error_queue.append(Error(114, "malformed command"))

    # Source autoranges

    @message(tsp_print(r'smua\.source\.autorange([iv])'))
    def get_source_autorange(self, function):
        return format(self.smua_source_autorange[function], "E")

    @message(tsp_assign(r'smua\.source\.autorange([iv])'))
    def set_source_autorange(self, function, state):
        try:
            self.smua_source_autorange[function] = {
                "0": False, "smua.AUTORANGE_OFF": False,
                "1": True, "smua.AUTORANGE_ON": True
            }[state]
        except KeyError:
            self.error_queue.append(Error(115, "malformed command"))

    # Source voltage limit

    @message(tsp_print(r'smua\.source\.protectv'))
    def get_source_protectv(self):
        return format(self.source_protectv, "E")

    @message(tsp_assign(r'smua\.source\.protectv'))
    def set_source_protectv(self, level):
        try:
            self.source_protectv = float(level)
        except ValueError:
            self.error_queue.append(Error(116, "malformed command"))

    # Compliance

    @message(tsp_print(r'smua.source.compliance'))
    def get_source_compliance(self):
        return "false"

    @message(tsp_print(r'smua\.source\.limit([iv])'))
    def get_source_limit(self, function):
        return format(self.smua_source_limit[function], "E")

    @message(tsp_assign(r'smua\.source\.limit([iv])'))
    def set_source_limit(self, function, level):
        try:
            self.smua_source_limit[function] = float(level)
        except ValueError:
            self.error_queue.append(Error(117, "malformed command"))

    @message(tsp_print(r'smua\.measure\.i\(\)'))
    def get_measure_i(self):
        curr_min = float(self.options.get("curr.min", 1e6))
        curr_max = float(self.options.get("curr.max", 1e7))
        return format(random.uniform(curr_min, curr_max), "E")

    @message(tsp_print(r'smua\.measure\.v\(\)'))
    def get_measure_v(self):
        return format(self.smua_source_level.get("v", 0) + random.uniform(-.25, +.25), "E")

    # Average

    @message(tsp_print(r'smua\.measure\.filter\.enable'))
    def get_measure_filter_enable(self):
        return format(self.smua_measure_filter_enable, "d")

    @message(tsp_assign(r'smua\.measure\.filter\.enable'))
    def set_measure_filter_enable(self, enable: str):
        try:
            self.smua_measure_filter_enable = {
                "0": False, "smua.FILTER_OFF": False,
                "1": True, "smua.FILTER_ON": True
            }[enable]
        except KeyError:
            self.error_queue.append(Error(118, "malformed command"))

    @message(tsp_print(r'smua\.measure\.filter\.count'))
    def get_measure_filter_count(self):
        return format(self.smua_measure_filter_count, "d")

    @message(tsp_assign(r'smua\.measure\.filter\.count'))
    def set_measure_filter_count(self, count: str):
        try:
            self.smua_measure_filter_count = int(count)
        except KeyError:
            self.error_queue.append(Error(119, "malformed command"))

    @message(tsp_print(r'smua\.measure\.filter\.type'))
    def get_measure_filter_type(self):
        return format(self.smua_measure_filter_type, "d")

    @message(tsp_assign(r'smua\.measure\.filter\.type'))
    def set_measure_filter_type(self, enable: str):
        try:
            self.smua_measure_filter_type = {
                "0": 0, "smua.FILTER_MOVING_AVG": 0,
                "1": 1, "smua.FILTER_REPEAT_AVG": 1,
                "2": 2, "smua.FILTER_MEDIAN": 2
            }[enable]
        except KeyError:
            self.error_queue.append(Error(120, "malformed command"))

    # Integration time

    @message(tsp_print(r'smua\.measure\.nplc'))
    def get_measure_nplc(self):
        return format(self.smua_measure_nplc, "E")

    @message(tsp_assign(r'smua\.measure\.nplc'))
    def set_measure_nplc(self, nplc: str):
        try:
            self.smua_measure_nplc = round(float(nplc), 3)
        except KeyError:
            self.error_queue.append(Error(120, "malformed command"))

    @message(r'^.*$')
    def unknown_message(self):
        self.error_queue.append(Error(100, "malformed command"))


if __name__ == "__main__":
    run(K2657AEmulator())
