"""
HEPHY Corvus Controller GUI

PO? - Get Table Position and Status (moving)
MA=x.xxx,x.xxx,x.xxx - Move absolute [X,Y,Z]
MR=x.xxx,x - Move relative [StepWidth,Axis]
"""

from typing import Final, Optional, Protocol

from comet.driver.generic import InstrumentError
from comet.driver.generic.motion_controller import (
    Position,
    MotionControllerAxis,
    MotionController,
)

__all__ = ["CorvusController"]


class Resource(Protocol):
    def query(self, message: str) -> str: ...
    def write(self, message: str) -> None: ...


def split_tokens(text: str) -> list[str]:
    return [token.strip() for token in text.split(",")]


def get_position_status(resource: Resource) -> tuple[float, float, float, bool]:
    reply = resource.query("PO?")
    try:
        x, y, z, is_moving = split_tokens(reply)[:4]
        return float(x), float(y), float(z), int(is_moving) == 1
    except Exception as exc:
        raise RuntimeError(f"Failed to parse 'PO?' reply: {reply!r}") from exc


def move_absolute(resource: Resource, x: float, y: float, z: float) -> None:
    resource.write(f"MA={x:.6f},{y:.6f},{z:.6f}")


def move_relative(resource: Resource, value: float, axis: int) -> None:
    resource.write(f"MR={value:.6f},{axis:d}")


class CorvusControllerAxis(MotionControllerAxis):
    def calibrate(self) -> None: ...  # Not supported

    def range_measure(self) -> None: ...  # Not supported

    @property
    def is_calibrated(self) -> bool:
        return True  # Not supported

    def move_absolute(self, value: float) -> None:
        x, y, z = get_position_status(self.resource)[:3]
        if self.index == 1:
            x = value
        elif self.index == 2:
            y = value
        elif self.index == 3:
            z = value
        move_absolute(self.resource, x, y, z)

    def move_relative(self, value: float) -> None:
        move_relative(self.resource, value, self.index)

    @property
    def position(self) -> float:
        pos = get_position_status(self.resource)[:3]
        return float(pos[self.index - 1])

    @property
    def is_moving(self) -> bool:
        return get_position_status(self.resource)[3]


class CorvusController(MotionController):
    """Driver for HEPHY Corvus Controller GUI."""

    AXIS_IDS: Final = (1, 2, 3)

    def identify(self) -> str:
        self.resource.query("???")  # test connection
        return "Corvus Controller"  # Not supported

    def reset(self) -> None: ...  # Not supported

    def clear(self) -> None: ...  # Not supported

    def next_error(self) -> Optional[InstrumentError]:
        return None  # Not supported

    def __getitem__(self, index: int) -> CorvusControllerAxis:
        if index not in self.AXIS_IDS:
            raise ValueError(f"Invalid axis: {index}")
        return CorvusControllerAxis(self.resource, index)

    def calibrate(self) -> None: ...  # Not supported

    def range_measure(self) -> None: ...  # Not supported

    @property
    def is_calibrated(self) -> bool:
        return True  # Not supported

    def move_absolute(self, position: Position) -> None:
        x, y, z = position
        move_absolute(self.resource, x, y, z)

    def move_relative(self, position: Position) -> None:
        x, y, z = position
        if x != 0.0:
            move_relative(self.resource, x, 1)
        if y != 0.0:
            move_relative(self.resource, y, 2)
        if z != 0.0:
            move_relative(self.resource, z, 3)

    def abort(self) -> None: ...  # Not supported

    def force_abort(self) -> None: ...  # Not supported

    @property
    def position(self) -> Position:
        x, y, z, _ = get_position_status(self.resource)
        return x, y, z

    @property
    def is_moving(self) -> bool:
        return get_position_status(self.resource)[3]

    @property
    def joystick_enabled(self) -> bool:
        return False  # Not supported

    @joystick_enabled.setter
    def joystick_enabled(self, value: bool) -> None: ...  # Not supported
