from abc import ABC, abstractmethod
from typing import Any, Mapping, Optional

from ..driver import Driver

__all__ = [
    "InstrumentError",
    "InitializeMixin",
    "IdentifyMixin",
    "ResetMixin",
    "ClearMixin",
    "ErrorQueueMixin",
    "ConfigureMixin",
    "BeeperMixin",
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


class InitializeMixin(ABC):
    @abstractmethod
    def initialize(self) -> None: ...


class IdentifyMixin(ABC):
    @abstractmethod
    def identify(self) -> str: ...


class ResetMixin(ABC):
    @abstractmethod
    def reset(self) -> None: ...


class ClearMixin(ABC):
    @abstractmethod
    def clear(self) -> None: ...


class ErrorQueueMixin(ABC):
    @abstractmethod
    def next_error(self) -> Optional[InstrumentError]: ...


class BeeperMixin(ABC):
    BEEPER_ON: bool = True
    BEEPER_OFF: bool = False

    @property
    @abstractmethod
    def beeper(self) -> bool: ...

    @beeper.setter
    @abstractmethod
    def beeper(self, value: bool) -> None: ...


class RouteTerminalMixin(ABC):
    ROUTE_TERMINAL_FRONT: str = "front"
    ROUTE_TERMINAL_REAR: str = "rear"

    @property
    @abstractmethod
    def route_terminal(self) -> str: ...

    @route_terminal.setter
    @abstractmethod
    def route_terminal(self, route_terminal: str) -> None: ...


class Instrument(IdentifyMixin, ResetMixin, ClearMixin, ErrorQueueMixin, Driver): ...
