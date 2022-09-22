import re
from typing import Any, Dict, List, Optional, Tuple

from comet.driver.generic import Instrument
from comet.driver.generic import InstrumentError

__all__ = ['EnvironBox']

ERROR_MESSAGES: Dict[int, str] = {
    1: "RTC not running",
    2: "RTC read error",
    80: "DAC not found",
    90: "I/O Port Expander parameter error",
    99: "Invalid command",
    100: "General SET command error",
    199: "GET command parameter not found",
    200: "General GET command error",
    999: "Unknown command"
}


def test_bit(value: int, index: int) -> bool:
    return bool((value >> index) & 1)


def parse_error(response: str) -> Optional[InstrumentError]:
    m = re.match(r'^err(\d+)', response.lower())
    if m:
        code = int(m.group(1))
        message = ERROR_MESSAGES.get(code, "")
        return InstrumentError(code, message)
    return None


def parse_pc_data(response: str) -> Dict[str, Any]:
    values = response.split(",")
    relay_status = int(values[23])
    return {
        "box_humidity": float(values[1]),
        "box_temperature": float(values[2]),
        "box_dewpoint": float(values[3]),
        "power_microscope_ctrl": test_bit(relay_status, 0),
        "power_box_light": test_bit(relay_status, 1),
        "power_probecard_light": test_bit(relay_status, 2),
        "power_laser_sensor": test_bit(relay_status, 3),
        "power_probecard_camera": test_bit(relay_status, 4),
        "power_microscope_camera": test_bit(relay_status, 5),
        "power_microscope_light": test_bit(relay_status, 6),
        "box_light": bool(int(values[24])),
        "box_door": bool(int(values[25])),
        "discharge_time": float(values[31]),
        "box_lux": float(values[32]),
        "pt100_1": float(values[33]),
        "pt100_2": float(values[34]),
    }


class EnvironBox(Instrument):

    _error_queue: List[InstrumentError] = []

    def identify(self) -> str:
        return self.query('*IDN?')

    def reset(self) -> None:
        self._error_queue.clear()
        self.write('*RST')

    def clear(self) -> None:
        self._error_queue.clear()
        self.write("*CLS")

    # Error queue

    def next_error(self) -> Optional[InstrumentError]:
        if self._error_queue:
            return self._error_queue.pop(0)
        return None

    DISCARGE_OFF: bool = False
    DISCARGE_ON: bool = True

    def set_discharge(self, state: bool) -> None:
        value = {
            self.DISCARGE_OFF: 'OFF',
            self.DISCARGE_ON: 'ON'
        }[state]
        self.write(f'SET:DISCHARGE {value}')

    def get_box_humidity(self) -> float:
        return float(self.query('GET:HUM ?'))

    def get_box_temperature(self) -> float:
        return float(self.query('GET:TEMP ?'))

    def get_box_lux(self) -> float:
        return float(self.query('GET:LUX ?'))

    BOX_DOOR_CLOSED: bool = False
    BOX_DOOR_OPEN: bool = True

    def get_box_door_state(self) -> bool:
        return bool(float(self.query('GET:DOOR ?')))

    def get_chuck_temperature(self) -> float:
        return float(self.query('GET:PT100_1 ?'))

    def get_chuck_block_temperature(self) -> float:
        return float(self.query('GET:PT100_2 ?'))

    BOX_LIGHT_OFF: bool = False
    BOX_LIGHT_ON: bool = True

    def get_box_light(self) -> bool:
        value = self.query('GET:LIGHT ?')
        return {
            '0': self.BOX_LIGHT_OFF,
            '1': self.BOX_LIGHT_ON
        }[value]

    def set_box_light(self, state: bool) -> None:
        value = {
            self.BOX_LIGHT_OFF: 'OFF',
            self.BOX_LIGHT_ON: 'ON'
        }[state]
        self.write(f'SET:BOX_LIGHT {value}')

    MICROSCOPE_LIGHT_OFF: bool = False
    MICROSCOPE_LIGHT_ON: bool = True

    def get_microscope_light(self) -> bool:
        value = self.get_data().get("power_microscope_light")
        return {
            '0': self.BOX_LIGHT_OFF,
            '1': self.BOX_LIGHT_ON
        }[value]

    def set_microscope_light(self, state: bool) -> None:
        value = {
            self.BOX_LIGHT_OFF: 'OFF',
            self.BOX_LIGHT_ON: 'ON'
        }[state]
        self.write(f'SET:MICROSCOPE_LIGHT {value}')

    PROBECARD_LIGHT_OFF: bool = False
    PROBECARD_LIGHT_ON: bool = True

    def get_probecard_light(self) -> bool:
        value = self.get_data().get("power_probecard_light")
        return {
            '0': self.BOX_LIGHT_OFF,
            '1': self.BOX_LIGHT_ON
        }[value]

    def set_probecard_light(self, state: bool) -> None:
        value = {
            self.BOX_LIGHT_OFF: 'OFF',
            self.BOX_LIGHT_ON: 'ON'
        }[state]
        self.write(f'SET:PROBCARD_LIGHT {value}')

    TEST_LED_OFF: bool = False
    TEST_LED_ON: bool = True

    def get_test_led(self) -> bool:
        value = self.query('GET:TEST_LED ?')
        return {
            '0': self.TEST_LED_OFF,
            '1': self.TEST_LED_ON
        }[value]

    def set_test_led(self, state: bool) -> None:
        value = {
            self.TEST_LED_OFF: 'OFF',
            self.TEST_LED_ON: 'ON'
        }[state]
        self.write(f'SET:TEST_LED {value}')

    def get_data(self):
        return parse_pc_data(self.query('GET:PC_DATA ?'))

    # Helper

    def query(self, message: str) -> str:
        response = self.resource.query(message).strip()
        error = parse_error(response)
        if error:
            self._error_queue.append(error)
            return ''
        return response

    def write(self, message: str) -> None:
        response = self.query(message)
        error = parse_error(response)
        if error:
            self._error_queue.append(error)
