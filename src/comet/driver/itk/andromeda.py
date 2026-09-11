from typing import Final

from comet.driver.generic import InstrumentError
from comet.driver.generic.motion_controller import (
    MotionController,
    MotionControllerAxis,
    Position,
)

__all__ = ["Andromeda"]

ERROR_MESSAGES: dict[int, str] = {
    0: "no error",
    4: "internal error",
    100: "device number out of range",
    102: "undefined symbol",
    1001: "wrong parameter type",
    1002: "stack underflow: too few parameters on stack",
    1003: "parameter out of range",
    1004: "move out of limits requested",
    1009: "parameter stack overflow",
    2000: "undefined command",
    3000: "no configuration file available",
    3001: "error in configuration file",
    3100: "most recent valid parameter set restored due to file corruption",
}


def format_position_arg(value: float) -> str:
    return format(value, ".4f")


def format_position_args(position: Position) -> str:
    values = [format_position_arg(value) for value in position]

    if not 1 <= len(values) <= 6:
        raise ValueError(f"Expected 1-6 axis values, got {len(values)}")

    return " ".join(values)


def parse_error(response: str) -> InstrumentError | None:
    code = int(response)
    if code:
        message = ERROR_MESSAGES.get(code, "unknown error")
        return InstrumentError(code, message)
    return None


class AndromedaAxis(MotionControllerAxis):
    def calibrate(self) -> None:
        self.resource.write(f"{self.index:d} ncal")

    def range_measure(self) -> None:
        self.resource.write(f"{self.index:d} nrm")

    @property
    def is_calibrated(self) -> bool:
        """Return True if axis is calibrated and range measured."""
        result = self.resource.query(f"{self.index:d} nst")
        return bool(int(result) & 0x18)

    def move_absolute(self, value: float) -> None:
        self.resource.write(f"{format_position_arg(value)} {self.index:d} nm")

    def move_relative(self, value: float) -> None:
        self.resource.write(f"{format_position_arg(value)} {self.index:d} nr")

    @property
    def position(self) -> float:
        result = self.resource.query(f"{self.index:d} np")
        return float(result)

    @property
    def is_moving(self) -> bool:
        result = self.resource.query(f"{self.index:d} nst")
        return bool(int(result) & 0x1)


class Andromeda(MotionController):
    AXES: Final[list[int]] = [1, 2, 3, 4, 5, 6]

    def identify(self) -> str:
        return self.resource.query("identify").strip()

    def reset(self) -> None: ...

    def clear(self) -> None: ...

    def next_error(self) -> InstrumentError | None:
        response = self.resource.query("ge")
        return parse_error(response)

    def __getitem__(self, index: int) -> AndromedaAxis:
        if index not in type(self).AXES:
            raise IndexError(index)
        return AndromedaAxis(self.resource, index)

    def calibrate(self) -> None:
        for index in type(self).AXES:
            self.resource.write(f"{index:d} ncal")

    def range_measure(self) -> None:
        for index in type(self).AXES:
            self.resource.write(f"{index:d} nrm")

    @property
    def is_calibrated(self) -> bool:
        """Return True if all active axes are calibrated and range measured."""
        status = int(self.resource.query("st"))
        return bool(int(status & 0x18))

    def move_absolute(self, position: Position) -> None:
        self.resource.write(f"{format_position_args(position)} m")

    def move_relative(self, position: Position) -> None:
        self.resource.write(f"{format_position_args(position)} r")

    def abort(self) -> None:
        for index in type(self).AXES:
            self.resource.write(f"{index:d} nabort")

    def force_abort(self) -> None:
        self.resource.write(chr(0x03))  # Ctrl+C

    @property
    def position(self) -> Position:
        x, y, z, a, b, c = self.resource.query("p").split()
        return [float(x), float(y), float(z), float(a), float(b), float(c)]

    @property
    def is_moving(self) -> bool:
        result = self.resource.query("st")
        return bool(int(result) & 0x1)

    @property
    def joystick_enabled(self) -> bool:
        results = []
        for index in type(self).AXES:
            result = self.resource.query(f"{index:d} getmanctrl")
            results.append(int(result))
        return any(results)

    @joystick_enabled.setter
    def joystick_enabled(self, value: bool) -> None:
        states = 0xF if value else 0x0
        for index in type(self).AXES:
            self.resource.write(f"{states:d} {index:d} setmanctrl")
