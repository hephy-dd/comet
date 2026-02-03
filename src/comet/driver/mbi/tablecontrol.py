from typing import Final, Optional

from comet.driver.generic import InstrumentError
from comet.driver.generic.motion_controller import (
    Position,
    MotionControllerAxis,
    MotionController,
)

__all__ = ["TableControl"]


def split_tokens(text: str) -> list[str]:
    return [token.strip() for token in text.split(",")]


def parse_error(response: str) -> tuple[int, str]:
    code, message = [token.strip() for token in response.split(",")][:2]
    return int(code), message.strip('"')


class TableControlAxis(MotionControllerAxis):
    def calibrate(self) -> None: ...  # Not Implemented

    def range_measure(self) -> None: ...  # Not Implemented

    @property
    def is_calibrated(self) -> bool:
        """Return True if axis is calibrated and range measured."""
        result = split_tokens(self.resource.query("CAL?"))
        return int(result[self.index - 1]) == 3

    def move_absolute(self, value: float) -> None:
        x, y, z = [float(token) for token in split_tokens(self.resource.query("POS?"))]
        if self.index == 1:
            x = value
        elif self.index == 2:
            y = value
        elif self.index == 3:
            z = value
        self.resource.write(f"MOVE:ABS {x:.6f},{y:.6f},{z:.6f}")

    def move_relative(self, value: float) -> None:
        x, y, z = 0.0, 0.0, 0.0
        if self.index == 1:
            x = value
        elif self.index == 2:
            y = value
        elif self.index == 3:
            z = value
        self.resource.write(f"MOVE:REL {x:.6f},{y:.6f},{z:.6f}")

    @property
    def position(self) -> float:
        result = split_tokens(self.resource.query("POS?"))
        return float(result[self.index - 1])

    @property
    def is_moving(self) -> bool:
        return self.resource.query("MOVE?").strip() == "1"


class TableControl(MotionController):
    AXIS_IDS: Final = (1, 2, 3)

    def identify(self) -> str:
        return self.resource.query("*IDN?").strip()

    def reset(self) -> None: ...

    def clear(self) -> None:
        self.resource.query("*CLS")

    def next_error(self) -> Optional[InstrumentError]:
        response = self.resource.query("SYS:ERR?").strip()
        code, message = parse_error(response)
        if code:
            return InstrumentError(code, message)
        return None

    def __getitem__(self, index: int) -> TableControlAxis:
        if index not in self.AXIS_IDS:
            raise IndexError(f"invalid axis index {index}; valid: {self.AXIS_IDS}")
        return TableControlAxis(self.resource, index)

    def calibrate(self) -> None: ...  # Not Implemented

    def range_measure(self) -> None: ...  # Not Implemented

    @property
    def is_calibrated(self) -> bool:
        """Return True if all active axes are calibrated and range measured."""
        return self.resource.query("CAL?").strip() == "3,3,3"

    def move_absolute(self, position: Position) -> None:
        x, y, z = position
        self.resource.write(f"MOVE:ABS {x:.6f},{y:.6f},{z:.6f}")

    def move_relative(self, position: Position) -> None:
        x, y, z = position
        self.resource.write(f"MOVE:REL {x:.6f},{y:.6f},{z:.6f}")

    def abort(self) -> None:
        self.resource.write("MOVE:ABORT")

    def force_abort(self) -> None:
        self.resource.write("MOVE:ABORT")

    @property
    def position(self) -> Position:
        x, y, z = split_tokens(self.resource.query("POS?"))
        return float(x), float(y), float(z)

    @property
    def is_moving(self) -> bool:
        return self.resource.query("MOVE?").strip() == "1"

    @property
    def joystick_enabled(self) -> bool:
        return False  # Not Implemented

    @joystick_enabled.setter
    def joystick_enabled(self, value: bool) -> None: ...  # Not Implemented
