from abc import ABC, abstractmethod
from typing import List, Iterable, Optional, Tuple

from ..driver import Driver

__all__ = [
    "InstrumentError",
    "BeeperMixin",
    "ErrorQueueMixin",
    "RouteTerminalMixin",
    "Instrument",
]


class InstrumentError:

    def __init__(self, code: int, message: str) -> None:
        self.code: int = code
        self.message: str = message

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}({self.code}, {self.message!r})"


class BeeperMixin(ABC):

    BEEPER_ON: bool = True
    BEEPER_OFF: bool = False

    @property  # type: ignore
    @abstractmethod
    def beeper(self) -> bool:
        ...

    @beeper.setter  # type: ignore
    @abstractmethod
    def beeper(self, value: bool) -> None:
        ...


class ErrorQueueMixin(ABC):

    @abstractmethod
    def next_error(self) -> Optional[InstrumentError]:
        ...


class RouteTerminalMixin(ABC):

    ROUTE_TERMINAL_FRONT: str = "front"
    ROUTE_TERMINAL_REAR: str = "rear"

    @property  # type: ignore
    @abstractmethod
    def route_terminal(self) -> str:
        ...

    @route_terminal.setter  # type: ignore
    @abstractmethod
    def route_terminal(self, route_terminal: str) -> None:
        ...


class Instrument(ErrorQueueMixin, Driver):

    @abstractmethod
    def identify(self) -> str:
        ...

    @abstractmethod
    def reset(self) -> None:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...