from typing import Dict, Optional

from comet.driver.generic import InstrumentError
from comet.driver.generic.motion_controller import Position, MotionControllerAxis, MotionController

__all__ = ["Corvus"]

ERROR_MESSAGES: Dict[int, str] = {
    1: "internal error",
    2: "internal error",
    3: "internal error",
    4: "internal error",
    1001: "wrong parameter",
    1002: "not enough parameter on the stack",
    1003: "not enough parameter on the stack",
    1007: "range of parameter is exceeded",
    1004: "move stopped working range should run over",
    1008: "not enough parameter on the stack",
    1009: "not enough space on the stack",
    1010: "not enough space on parameter memory",
    1015: "parameters outside the working range",
    2000: "unknown command",
}


def parse_error(response: str) -> Optional[InstrumentError]:
    code = int(response)
    if code:
        message = ERROR_MESSAGES.get(code, "unknown error")
        return InstrumentError(code, message)
    return None


class CorvusAxis(MotionControllerAxis):

    def calibrate(self) -> None:
        self.resource.write(f"{self.index:d} ncal")

    def range_measure(self) -> None:
        self.resource.write(f"{self.index:d} nrm")

    @property
    def is_calibrated(self) -> bool:
        """Return True if axis is calibrated and range measured."""
        result = self.resource.query(f"{self.index:d} getcaldone")
        return int(result) == 0x3

    def move_absolute(self, value: float) -> None:
        self.resource.write(f"{value:.3f} {self.index:d} nmove")

    def move_relative(self, value: float) -> None:
        self.resource.write(f"{value:.3f} {self.index:d} nrmove")

    @property
    def position(self) -> float:
        result = self.resource.query(f"{self.index:d} npos")
        return float(result)

    @property
    def is_moving(self) -> bool:
        result = self.resource.query("status")
        return bool(int(result) & 0x1)


class Corvus(MotionController):

    def identify(self) -> str:
        return self.resource.query("identify").strip()

    def reset(self) -> None:
        ...

    def clear(self) -> None:
        ...

    def next_error(self) -> Optional[InstrumentError]:
        response = self.resource.query("geterror")
        return parse_error(response)

    def __getitem__(self, index: int) -> CorvusAxis:
        return CorvusAxis(self.resource, index)

    def calibrate(self) -> None:
        self.resource.write("cal")

    def range_measure(self) -> None:
        self.resource.write("rm")

    @property
    def is_calibrated(self) -> bool:
        """Return True if all active axes are calibrated and range measured."""
        values = self.resource.query(f"getcaldone").split()
        return [int(value) for value in values].count(0x3) == len(values)

    def move_absolute(self, position: Position) -> None:
        values = " ".join([format(value, '.3f') for value in position])
        self.resource.write(f"{values} move")

    def move_relative(self, position: Position) -> None:
        values = " ".join([format(value, '.3f') for value in position])
        self.resource.write(f"{values} rmove")

    def abort(self):
        self.resource.write("abort")

    def force_abort(self):
        self.resource.write(chr(0x03))  # Ctrl+C

    @property
    def position(self) -> Position:
        result = self.resource.query("pos")
        return [float(value) for value in result.split()]

    @property
    def is_moving(self) -> bool:
        result = self.resource.query("status")
        return bool(int(result) & 0x1)

    @property
    def joystick_enabled(self) -> bool:
        result = self.resource.query("getjoystick")
        return bool(int(result))

    @joystick_enabled.setter
    def joystick_enabled(self, value: bool) -> None:
        self.resource.write(f"{value:d} joystick")
