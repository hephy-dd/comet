from abc import abstractmethod
from typing import Iterable

from .instrument import Driver, Instrument

__all__ = ["MotionControllerAxis", "MotionController"]

Position = Iterable[float]


class MotionControllerAxis(Driver):

    def __init__(self, resource, index: int) -> None:
        super().__init__(resource)
        self.index: int = index

    @abstractmethod
    def calibrate(self) -> None:
        ...

    @abstractmethod
    def range_measure(self) -> None:
        ...

    @property
    @abstractmethod
    def is_calibrated(self) -> bool:
        ...

    @abstractmethod
    def move_absolute(self, value: float) -> None:
        ...

    @abstractmethod
    def move_relative(self, value: float) -> None:
        ...

    @property
    @abstractmethod
    def position(self) -> float:
        ...

    @property
    @abstractmethod
    def is_moving(self) -> bool:
        ...


class MotionController(Instrument):

    @abstractmethod
    def __getitem__(self, index: int) -> MotionControllerAxis:
        ...

    @abstractmethod
    def calibrate(self) -> None:
        ...

    @abstractmethod
    def range_measure(self) -> None:
        ...

    @property
    @abstractmethod
    def is_calibrated(self) -> bool:
        ...

    @abstractmethod
    def move_absolute(self, position: Position) -> None:
        ...

    @abstractmethod
    def move_relative(self, position: Position) -> None:
        ...

    @abstractmethod
    def abort(self) -> None:
        ...

    @abstractmethod
    def force_abort(self) -> None:
        ...

    @property
    @abstractmethod
    def position(self) -> Position:
        ...

    @property
    @abstractmethod
    def is_moving(self) -> bool:
        ...

    @property  # type: ignore
    @abstractmethod
    def joystick_enabled(self) -> bool:
        ...

    @joystick_enabled.setter  # type: ignore
    @abstractmethod
    def joystick_enabled(self, value: bool) -> None:
        ...
