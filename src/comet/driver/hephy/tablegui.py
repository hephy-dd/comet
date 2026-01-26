"""
HEPHY Table Control GUI

PO? - Get Table Position and Status
MA=x.xxx,x.xxx,x.xxx - Move absolute [X,Y,Z]
MR=x.xxx,x - Move relative [StepWidth,Axis]
"""

from typing import Optional

from comet.driver.generic import InstrumentError
from comet.driver.generic.motion_controller import (
    Position,
    MotionControllerAxis,
    MotionController,
)

__all__ = ["TableGui"]


def get_position(resource) -> tuple[float, float, float]:
    reply = resource.query("PO?")
    try:
        x, y, z = reply.split(",")[:3]
        return float(x), float(y), float(z)
    except Exception as exc:
        raise InstrumentError(f"Failed to parse PO? reply: {reply!r}") from exc


def move_absolute(resource, x: float, y: float, z: float) -> None:
    resource.write(f"MA={x:.3f},{y:.3f},{z:.3f}")


def move_relative(resource, value: float, axis: int) -> None:
    resource.write(f"MR={value:.3f},{axis:d}")


class TableGuiAxis(MotionControllerAxis):
    def calibrate(self) -> None: ...  # Not supported

    def range_measure(self) -> None: ...  # Not supported

    @property
    def is_calibrated(self) -> bool:
        return True  # Not supported

    def move_absolute(self, value: float) -> None:
        x, y, z = get_position(self.resource)
        if self.index == 1:
            x = value
        if self.index == 2:
            y = value
        if self.index == 3:
            z = value
        move_absolute(self.resource, x, y, z)

    def move_relative(self, value: float) -> None:
        move_relative(self.resource, value, self.index)

    @property
    def position(self) -> float:
        pos = get_position(self.resource)
        return float(pos[self.index - 1])

    @property
    def is_moving(self) -> bool:
        return False  # Not supported


class TableGui(MotionController):
    MOTION_AXES = [1, 2, 3]

    def identify(self) -> str:
        self.resource.query("???")  # test connection
        return "Table Control GUI"  # Not supported

    def reset(self) -> None: ...  # Not supported

    def clear(self) -> None: ...  # Not supported

    def next_error(self) -> Optional[InstrumentError]:
        return None  # Not supported

    def __getitem__(self, index: int) -> TableGuiAxis:
        if index not in self.MOTION_AXES:
            raise ValueError(f"Invalid axis: {index}")
        return TableGuiAxis(self.resource, index)

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
        x, y, z = get_position(self.resource)
        return x, y, z

    @property
    def is_moving(self) -> bool:
        return False  # Not supported

    @property
    def joystick_enabled(self) -> bool:
        return False  # Not supported

    @joystick_enabled.setter
    def joystick_enabled(self, value: bool) -> None: ...  # Not supported
