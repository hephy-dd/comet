import time
from typing import Optional

from comet.driver.generic import SourceMeterUnit
from comet.driver.generic import InstrumentError

__all__ = ['K237']

ERROR_MESSAGES = {
    0: "Trigger Overrun",
    1: "IDDC",
    2: "IDDCO",
    3: "Interlock Present",
    4: "Illegal Measure Range",
    5: "Illegal Source Range",
    6: "Invalid Sweep Mix",
    7: "Log Cannot Cross Zero",
    8: "Autoranging Source With Pulse Sweep",
    9: "In Calibration",
    10: "In Standby",
    11: "Unit is a 236",
    12: "IOU DPRAM Failed",
    13: "IOU EEPROM Failed",
    14: "IOU Cal Checksum Error",
    15: "DPRAM Lockup",
    16: "DPRAM Link Error",
    17: "Cal ADC Zero Error",
    18: "Cal ADC Gain Error",
    19: "Cal SRC Zero Error",
    20: "Cal SRC Gain Error",
    21: "Cal Common Mode Error",
    22: "Cal Compliance Error",
    23: "Cal Value Error",
    24: "Cal Constants Error",
    25: "Cal Invalid Error"
}


def select_range_index(values: dict, level: float) -> int:
    level = abs(level)
    for index, value in sorted(values.items()):
        if level <= value:
            return index
    return 0  # auto


class K237(SourceMeterUnit):

    WRITE_DELAY = 0.250

    VOLTAGE_RANGES = {
        0: 0.,
        1: 1.1,
        2: 11.,
        3: 110.,
        4: 1100.,
    }

    CURRENT_RANGES = {
        0: 0.,
        1: 1e-09,
        2: 1e-08,
        3: 1e-07,
        4: 1e-06,
        5: 1e-05,
        6: 1e-04,
        7: 1e-03,
        8: 1e-02,
        9: 1e-01,
        10: 1e-00
    }

    def identify(self) -> str:
        value = self.query('U0X')
        model = value[0:3]
        revision = value[3:6]
        return f'Keithley Inc., Model {model}, rev. {revision}'

    def reset(self) -> None:
        self.resource.clear()

    def clear(self) -> None:
        self.resource.clear()

    def next_error(self) -> Optional[InstrumentError]:
        values = self.query('U1X')[3:]
        for index, value in enumerate(values):
            if value == '1':
                message = ERROR_MESSAGES.get(index, "Unknown Error")
                return InstrumentError(index, message)
        return None

    # Source meter unit

    @property
    def output(self) -> bool:
        return self.query('U3X')[18:20] == 'N1'

    @output.setter
    def output(self, state: bool) -> None:
        value = {False: 'N0X', True: 'N1X'}[state]
        self.write(value)

    @property
    def function(self) -> str:
        return {
            0: self.FUNCTION_VOLTAGE,
            1: self.FUNCTION_CURRENT
        }[int(self.query('U4X')[8])]

    @function.setter
    def function(self, function: str) -> None:
        value = {
            self.FUNCTION_VOLTAGE: 0,
            self.FUNCTION_CURRENT: 1
        }[function]
        self.write(f'F{value:d},0X')

    # Voltage source

    @property
    def voltage_level(self) -> float:
        self.write('G1,2,0X')  # set output format
        return float(self.query('X'))

    @voltage_level.setter
    def voltage_level(self, level: float) -> None:
        self.write(f'B{level:.3E},,X')

    @property
    def voltage_range(self) -> float:
        index = int(self.query('U4X')[5:7])
        return type(self).VOLTAGE_RANGES[index]

    @voltage_range.setter
    def voltage_range(self, level: float) -> None:
        index = select_range_index(type(self).VOLTAGE_RANGES, level)
        self.write(f'B,{index:d},X')

    @property
    def voltage_compliance(self) -> float:
        raise AttributeError("Property not readable: voltage_compliance")

    @voltage_compliance.setter
    def voltage_compliance(self, level: float) -> None:
        self.write(f'L{level:.3E},0X')

    # Current source

    @property
    def current_level(self) -> float:
        self.write('G1,2,0X')  # set output format
        return float(self.query('X'))

    @current_level.setter
    def current_level(self, level: float) -> None:
        self.write(f'B{level:.3E},,X')

    @property
    def current_range(self) -> float:
        index = int(self.query('U4X')[5:7])
        return type(self).CURRENT_RANGES[index]

    @current_range.setter
    def current_range(self, level: float) -> None:
        index = select_range_index(type(self).CURRENT_RANGES, level)
        self.write(f'B,{index:d},X')

    @property
    def current_compliance(self) -> float:
        raise AttributeError("Property not readable: current_compliance")

    @current_compliance.setter
    def current_compliance(self, level: float) -> None:
        self.write(f'L{level:.3E},0X')

    @property
    def compliance_tripped(self) -> bool:
        self.write('G1,0,0X')  # set output format
        return self.query('X')[0:2] == 'OS'

    # Measurements

    def measure_voltage(self) -> float:
        self.write('G4,2,0X')  # set output format
        return float(self.query('X'))

    def measure_current(self) -> float:
        self.write('G4,2,0X')  # set output format
        return float(self.query('X'))

    # Helper

    def write(self, message):
        self.resource.write(message)
        # throttle consecutive writes
        time.sleep(self.WRITE_DELAY)

    def query(self, message: str) -> str:
        return self.resource.query(message).strip()
