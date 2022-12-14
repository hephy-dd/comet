from abc import ABC, abstractmethod
from typing import Iterable

from .instrument import Instrument

__all__ = ["StepperMotorAxis", "StepperMotorController"]

Position = Iterable[float]


class StepperMotorAxis(ABC):

    def __init__(self, resource, index: int) -> None:
        super().__init__()
        self.resource = resource
        self.index: int = index

    @abstractmethod
    def calibrate(self) -> None:
        ...

    @abstractmethod
    def range_measure(self) -> None:
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


class StepperMotorController(Instrument):

    @abstractmethod
    def __getitem__(self, index: int) -> StepperMotorAxis:
        ...

    @abstractmethod
    def calibrate(self) -> None:
        ...

    @abstractmethod
    def range_measure(self) -> None:
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