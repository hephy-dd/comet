import random
import time
from typing import Optional

from comet.emulator import IEC60488Emulator, message, run
from comet.emulator.utils import Error


class Reading:
    def __init__(self, reading: float, unit: str) -> None:
        self.reading: float = reading
        self.unit: str = unit
        self.channel: int = 0
        self.reading_number: int = 0
        self.timestamp: float = 0.0
        self.limits: int = 0


class FormatElements:
    VALID_ELEMENTS: list[str] = ["READ", "CHAN", "UNIT", "RNUM", "TST", "LIM"]
    DEFAULT_ELEMENTS: list[str] = ["READ", "UNIT", "RNUM", "TST"]

    def __init__(self) -> None:
        self.elements: set[str] = set(self.DEFAULT_ELEMENTS)

    def __str__(self) -> str:
        elements = []
        for element in self.VALID_ELEMENTS:
            elements.append(element if element in self.elements else "")
        return ",".join(elements)

    def from_text(self, text: str) -> Optional[Error]:
        elements = set([element.strip() for element in text.split(",") if element.strip()])
        for element in elements:
            if element not in self.VALID_ELEMENTS:
                return Error(-201, "Syntax error")
        if elements == set(["UNIT"]):
            return Error(-101, "Invalid character")
        self.elements = elements
        return None

    def format_reading(self, reading: Reading) -> str:
        values = []
        if "READ" in self.elements:
            value = f"{reading.reading:+.8E}"
            if "UNIT" in self.elements:
                value += reading.unit
            values.append(value)
        if "TST" in self.elements:
            value = f"{reading.timestamp:+.3f}"
            if "UNIT" in self.elements:
                value += "SECS"
            values.append(value)
        if "RNUM" in self.elements:
            value = f"{reading.reading_number:+05d}"
            if "UNIT" in self.elements:
                value += "RDNG#"
            values.append(value)
        if "CHAN" in self.elements:
            value = f"{reading.channel:03d}"
            values.append(value)
        if "LIM" in self.elements:
            value = f"{reading.limits:04d}"
            if "UNIT" in self.elements:
                value += "LIMITS"
            values.append(value)
        return ",".join(values)


class K2700Emulator(IEC60488Emulator):

    IDENTITY: str = "Keithley Inc., Model 2700, 43768438, v1.0 (Emulator)"

    def __init__(self) -> None:
        super().__init__()
        self.reading_number: int = 0
        self.format_elements: FormatElements = FormatElements()
        self.sense_function: str = "VOLT:DC"
        self.sense_voltage_average_tcontrol: str = "MOV"
        self.sense_voltage_average_count: int = 10
        self.sense_voltage_average_state: bool = False
        self.error_queue: list[Error] = []
        self.system_beeper_state: bool = True
        self.trigger_delay_auto: bool = True
        self.trigger_delay: float = 0.001

    @message(r'^\*RST$')
    def set_rst(self) -> None:
        self.reading_number = 0
        self.format_elements = FormatElements()
        self.sense_function = "VOLT:DC"
        self.sense_voltage_average_tcontrol = "MOV"
        self.sense_voltage_average_count = 10
        self.sense_voltage_average_state = False
        self.system_beeper_state = True
        self.trigger_delay_auto = True
        self.trigger_delay = 0.001
        self.error_queue.clear()

    @message(r'^\*CLS$')
    def set_cls(self) -> None:
        self.error_queue.clear()

    # Format

    @message(r'^:?FORM(?:AT)?:ELEM(?:ENTS)?\?$')
    def get_format_elements(self) -> str:
        return str(self.format_elements)

    @message(r'^:?FORM(?:AT)?:ELEM(?:ENTS)?\s+(.*)$')
    def set_format_elements(self, elements) -> None:
        error = self.format_elements.from_text(elements)
        if error:
            self.error_queue.append(error)

    # Sense

    @message(r'^:?SENS(?:E)?:FUNC(?:TION)?\?$')
    def get_sense_function(self) -> str:
        return f"\"{self.sense_function}\""

    @message(r'^:?SENS(?:E)?:FUNC(?:TION)\s+\"(VOLT|CURR|VOLT:DC|CURR:DC|TEMP)\"$')
    def set_sense_function(self, function: str) -> None:
        self.sense_function = {"VOLT": "VOLT:DC", "CURR": "CURR:DC"}.get(function, function)

    @message(r'^:?SENS(?:E)?:VOLT:AVER:TCON\?$')
    def get_sense_average_tcontrol(self) -> str:
        return self.sense_voltage_average_tcontrol

    @message(r'^:?SENS(?:E)?:VOLT:AVER:TCON\s+(REP|MOV)$')
    def set_sense_average_tcontrol(self, name: str) -> None:
        self.sense_voltage_average_tcontrol = name

    @message(r'^:?SENS(?:E)?:VOLT:AVER:COUN[T]?\?$')
    def get_sense_average_count(self) -> str:
        return format(self.sense_voltage_average_count, "d")

    @message(r'^:?SENS(?:E)?:VOLT:AVER:COUN[T]?\s+(\d+)$')
    def set_sense_average_count(self, count: str) -> None:
        self.sense_voltage_average_count = int(count)

    @message(r'^:?SENS(?:E)?:VOLT:AVER(?::STAT[E]?)?\?$')
    def get_sense_voltage_average_state(self) -> str:
        return format(self.sense_voltage_average_state, "d")

    @message(r'^:?SENS(?:E)?:VOLT:AVER(?::STAT[E]?)?\s+(OFF|ON|0|1)$')
    def set_sense_voltage_average_state(self, value) -> None:
        self.sense_voltage_average_state = {"0": False, "1": True, "OFF": False, "ON": True}[value]

    @message(r'^:?SYST:ERR\?$')
    def get_system_error(self) -> str:
        if self.error_queue:
            error = self.error_queue.pop(0)
        else:
            error = Error(0, "no error")
        return f'{error.code}, "{error.message}"'

    @message(r'^:?SYST:BEEP(?::STAT)?\?$')
    def get_beeper_state(self) -> str:
        return format(self.system_beeper_state, "d")

    @message(r'^:?SYST:BEEP(?::STAT)? (OFF|ON|0|1)$')
    def set_beeper_state(self, value) -> None:
        self.system_beeper_state = {'0': False, '1': True, 'OFF': False, 'ON': True}[value]

    @message(r'^:?INIT(?::IMM)$')
    def set_init(self) -> None: ...

    @message(r'^:?READ\?$')
    def get_read(self) -> None:
        return self._read()

    @message(r'^:?FETC[H]?\?$')
    def get_fetch(self) -> str:
        return self._read()

    # Measure

    @message(r'^:?MEAS:VOLT\?$')
    def get_measure_voltage(self) -> str:
        self.sense_function = "VOLT:DC"
        return self._read()

    @message(r'^:?MEAS:CURR\?$')
    def get_measure_current(self) -> str:
        self.sense_function = "CURR:DC"
        return self._read()

    @message(r'^:?MEAS:TEMP\?$')
    def get_measure_temperature(self) -> str:
        self.sense_function = "TEMP"
        return self._read()

    # Trigger

    @message(r':?TRIG:DEL:AUTO\?$')
    def get_trigger_delay_auto(self) -> str:
        return format(self.trigger_delay_auto, "d")

    @message(r':?TRIG:DEL:AUTO\s+(OFF|ON|0|1)$')
    def set_trigger_delay_auto(self, value) -> None:
        self.trigger_delay_auto = {'0': False, '1': True, 'OFF': False, 'ON': True}[value]

    @message(r':?TRIG:DEL\?$')
    def get_trigger_delay(self) -> str:
        return format(self.trigger_delay, "E")

    @message(r':?TRIG:DEL\s+(.+)$')
    def set_trigger_delay(self, value) -> None:
        try:
            self.trigger_delay = min(999999.999, max(0.001, float(value)))
        except ValueError:
            self.error_queue.append(Error(-113, "undefined header"))

    @message(r'^(.*)$')
    def unknown_message(self, request) -> None:
        self.error_queue.append(Error(101, "malformed command"))

    def _read(self):
        """Returns formatted reading."""
        if self.sense_function == "VOLT:DC":
            volt_min = float(self.options.get("volt.min", 0))
            volt_max = float(self.options.get("volt.max", 10))
            reading = Reading(random.uniform(volt_min, volt_max), "VDC")
        elif self.sense_function == "CURR:DC":
            curr_min = float(self.options.get("curr.min", 1e6))
            curr_max = float(self.options.get("curr.max", 1e7))
            reading = Reading(random.uniform(curr_min, curr_max), "ADC")
        else:
            temp_min = float(self.options.get("temp.min", 24))
            temp_max = float(self.options.get("temp.max", 25))
            reading = Reading(random.uniform(temp_min, temp_max), "")  # TEMP
        time.sleep(random.uniform(.5, 1.0))  # rev B10 ;)
        reading.reading_number = self.reading_number
        self.reading_number += 1
        return self.format_elements.format_reading(reading)


if __name__ == '__main__':
    run(K2700Emulator())
