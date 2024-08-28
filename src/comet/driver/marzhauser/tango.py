from typing import Dict, Optional

from comet.driver.generic import InstrumentError
from comet.driver.generic.motion_controller import Position, MotionControllerAxis, MotionController

__all__ = ["Tango"]

ERROR_MESSAGES: Dict[int, str] = {
    1: "no valid axis name",
    2: "no executable instruction",
    3: "too many characters in command line",
    4: "invalid instruction",
    5: "number is not inside allowed range",
    6: "wrong number of parameters",
    7: "! or ? is missing or not allowed",
    8: "no TVR possible, while axis active",
    9: "no ON or OFF of axis possible, while TVR active",
    10: "function not configured",
    11: "no move instruction possible, while joystick enabled",
    12: "limit switch actuated",
    13: "function not executable, because encoder detected",
    14: "error during calibration (limit switch not released",
    15: "error during calibration (opposing limit switch actuated)",
    21: "multiple axis moves are forbidden (e.g. during initialization)",
    22: "automatic or manual move is not allowed (e.g. door open or initialization)",
    27: "emergency STOP is active",
    29: "servo amplifiers are disabled (switched OFF)",
    30: "safety circuit out of order",
    32: "move discarded target outside limit",
    70: "wrong CPLD data",
    71: "ETS error",
    72: "parameter is write protected (check lock bits)",
    73: "internal error, e.g. eeprom data corruption",
    74: "closed loop switched off due to parameter change, deviation or enc. error",
    75: "could not enable axis correction, or axis correction was disabled",
    76: "io extension error (output overload on IO1 or Multi-IO connector)",
    77: "io/xPos internal bus communication error",
    78: "HDI input device error",
    79: "xPos module error",
    80: "internal error: HDI ISR not running",
    81: "internal error: Encoder ISR not running",
    82: "overload on motor connector +5V (PCI-E/DT-E: also on +5V of AUX I/O)",
    83: "overload on AUX I/O +5V supply",
    84: "overload on encoder +5V supply",
    85: "overload on AUX I/O +12V supply or AUX mini +24V supply",
    86: "low brake output voltage",
    87: "overload on motor 4 connector +5V",
    88: "overload on a supply output pin (latched overload state), clear by \"!err\"",
    89: "not executable while in standby mode",
    90: "temperature error",
    91: "encoder error",
}


def parse_error(response: str) -> Optional[InstrumentError]:
    code = int(response)
    if code:
        message = ERROR_MESSAGES.get(code, "unknown error")
        return InstrumentError(code, message)
    return None


class TangoAxis(MotionControllerAxis):

    @property
    def name(self) -> str:
        return "xyza"[self.index]

    def calibrate(self) -> None:
        self.resource.write("!autostatus 0")
        self.resource.write(f"!cal {self.name}")

    def range_measure(self) -> None:
        self.resource.write("!autostatus 0")
        self.resource.write(f"!rm {self.name}")

    @property
    def is_calibrated(self) -> bool:
        """Return True if axis is calibrated and range measured."""
        result = self.resource.query(f"?calst {self.name}")
        return (int(result) & 0x3) == 0x3

    def move_absolute(self, value: float) -> None:
        self.resource.write("!autostatus 0")
        self.resource.write(f"!moa {self.name} {value:.3f}")

    def move_relative(self, value: float) -> None:
        self.resource.write("!autostatus 0")
        self.resource.write(f"!mor {self.name} {value:.3f}")

    @property
    def position(self) -> float:
        result = self.resource.query(f"?pos {self.name}")
        return float(result)

    @property
    def is_moving(self) -> bool:
        result = self.resource.query(f"?statusaxis {self.name}")
        return "M" in result


class Tango(MotionController):

    def identify(self) -> str:
        return self.resource.query("?version").strip()

    def reset(self) -> None:
        ...

    def clear(self) -> None:
        self.resource.write("!err")  # clear error state

    def next_error(self) -> Optional[InstrumentError]:
        return parse_error(self.resource.query("?err"))

    def __getitem__(self, index: int) -> TangoAxis:
        return TangoAxis(self.resource, index)

    def calibrate(self) -> None:
        self.resource.write("!autostatus 0")
        self.resource.write("!cal")

    def range_measure(self) -> None:
        self.resource.write("!autostatus 0")
        self.resource.write("!rm")

    @property
    def is_calibrated(self) -> bool:
        """Return True if all active axes are calibrated and range measured."""
        values = self.resource.query("?calst").split()
        return [(int(value) & 0x3) for value in values].count(0x3) == len(values)

    def move_absolute(self, position: Position) -> None:
        values = " ".join([format(value, '.3f') for value in position])
        self.resource.write("!autostatus 0")
        self.resource.write(f"!moa {values}")

    def move_relative(self, position: Position) -> None:
        values = " ".join([format(value, '.3f') for value in position])
        self.resource.write("!autostatus 0")
        self.resource.write(f"!mor {values}")

    def abort(self) -> None:
        self.resource.write("!a")

    def force_abort(self) -> None:
        self.resource.write(chr(0x03))  # Ctrl+C

    @property
    def position(self) -> Position:
        result = self.resource.query("?pos")
        return [float(value) for value in result.split()]

    @property
    def is_moving(self) -> bool:
        result = self.resource.query("?statusaxis")
        return "M" in result

    @property
    def joystick_enabled(self) -> bool:
        result = self.resource.query("?joy")
        return bool(int(result))

    @joystick_enabled.setter
    def joystick_enabled(self, value: bool) -> None:
        enabled = {False: 0, True: 2}[value]
        self.resource.write("!autostatus 0")
        self.resource.write(f"!joy {enabled:d}")
