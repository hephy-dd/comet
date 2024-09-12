from typing import Optional

from comet.driver.generic import InstrumentError
from comet.driver.generic.motion_controller import (
    Position,
    MotionControllerAxis,
    MotionController,
)

__all__ = ["Hydra"]

ERROR_MESSAGES: dict[int, str] = {
    0: "no error",
    4: "internal error",
    100: "devicenumber out of range",
    101: "stack underflow or cmd not found at 0",
    102: "undefined symbol",
    1001: "wrong parameter type",
    1002: "stack underflow: too few parameters on stack",
    1003: "parameter out of range",
    1004: "move out of limits requested",
    2000: "undefined command",
    3000: "no configuration file available",
    3001: "error in configuration file",
    3100: "most recent valid parameter set restored due to file corruption",
}


def parse_error(response: str) -> Optional[InstrumentError]:
    code = int(response)
    if code:
        message = ERROR_MESSAGES.get(code, "unknown error")
        return InstrumentError(code, message)
    return None


class HydraAxis(MotionControllerAxis):
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
        self.resource.write(f"{value:.3f} {self.index:d} nm")

    def move_relative(self, value: float) -> None:
        self.resource.write(f"{value:.3f} {self.index:d} nr")

    @property
    def position(self) -> float:
        result = self.resource.query(f"{self.index:d} np")
        return float(result)

    @property
    def is_moving(self) -> bool:
        result = self.resource.query(f"{self.index:d} nst")
        return bool(int(result) & 0x1)


class Hydra(MotionController):
    AXES: list[int] = [1, 2]

    def identify(self) -> str:
        return self.resource.query("identify").strip()

    def reset(self) -> None: ...

    def clear(self) -> None: ...

    def next_error(self) -> Optional[InstrumentError]:
        response = self.resource.query("ge")
        return parse_error(response)

    def __getitem__(self, index: int) -> HydraAxis:
        if index not in type(self).AXES:
            raise IndexError(index)
        return HydraAxis(self.resource, index)

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
        values = [format(value, ".3f") for value in position]
        self.resource.write(f"{values[0]} {values[1]} m")

    def move_relative(self, position: Position) -> None:
        values = [format(value, ".3f") for value in position]
        self.resource.write(f"{values[0]} {values[1]} r")

    def abort(self) -> None:
        for index in type(self).AXES:
            self.resource.write(f"{index:d} nabort")

    def force_abort(self) -> None:
        self.resource.write(chr(0x03))  # Ctrl+C

    @property
    def position(self) -> Position:
        x, y = self.resource.query("p").split()
        return [float(x), float(y)]

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
