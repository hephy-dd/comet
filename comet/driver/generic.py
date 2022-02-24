from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from .driver import Driver

__all__ = [
    'InstrumentError',
    'BeeperMixin',
    'ErrorQueueMixin',
    'RouteTerminalMixin',
    'Instrument',
    'SourceMeterUnit',
    'Electrometer',
    'LCRMeter',
    'SwitchingMatrix'
]


class InstrumentError:

    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message


class BeeperMixin(ABC):

    BEEPER_ON: bool = True
    BEEPER_OFF: bool = False

    @property
    @abstractmethod
    def beeper(self) -> bool:
        ...

    @beeper.setter
    @abstractmethod
    def beeper(self, value: bool) -> None:
        ...


class ErrorQueueMixin(ABC):

    @abstractmethod
    def next_error(self) -> Optional[InstrumentError]:
        ...


class RouteTerminalMixin(ABC):

    ROUTE_TERMINAL_FRONT: str = 'front'
    ROUTE_TERMINAL_REAR: str = 'rear'

    @property
    @abstractmethod
    def route_terminal(self) -> str:
        ...

    @route_terminal.setter
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


class SourceMeterUnit(Instrument):

    OUTPUT_ON: bool = True
    OUTPUT_OFF: bool = False

    @property
    @abstractmethod
    def output(self) -> bool:
        ...

    @output.setter
    @abstractmethod
    def output(self, state: bool) -> None:
        ...

    FUNCTION_VOLTAGE: str = 'voltage'
    FUNCTION_CURRENT: str = 'current'

    @property
    @abstractmethod
    def function(self) -> str:
        ...

    @function.setter
    @abstractmethod
    def function(self, function: str) -> None:
        ...

    # Voltage source

    @property
    @abstractmethod
    def voltage_level(self) -> float:
        ...

    @voltage_level.setter
    @abstractmethod
    def voltage_level(self, level: float) -> None:
        ...

    @property
    @abstractmethod
    def voltage_range(self) -> float:
        ...

    @voltage_range.setter
    @abstractmethod
    def voltage_range(self, level: float) -> None:
        ...

    @property
    @abstractmethod
    def voltage_compliance(self) -> float:
        ...

    @voltage_compliance.setter
    @abstractmethod
    def voltage_compliance(self, level: float) -> None:
        ...

    # Current source

    @property
    @abstractmethod
    def current_level(self) -> float:
        ...

    @current_level.setter
    @abstractmethod
    def current_level(self, level: float) -> None:
        ...

    @property
    @abstractmethod
    def current_range(self) -> float:
        ...

    @current_range.setter
    @abstractmethod
    def current_range(self, level: float) -> None:
        ...

    @property
    def current_compliance(self) -> float:
        ...

    @current_compliance.setter
    @abstractmethod
    def current_compliance(self, level: float) -> None:
        ...

    @property
    @abstractmethod
    def compliance_tripped(self) -> bool:
        ...

    # Measurements

    @abstractmethod
    def measure_voltage(self) -> float:
        ...

    @abstractmethod
    def measure_current(self) -> float:
        ...


class Electrometer(Instrument):

    # Measurements

    @abstractmethod
    def measure_voltage(self) -> float:
        ...

    @abstractmethod
    def measure_current(self) -> float:
        ...

    @abstractmethod
    def measure_resistance(self) -> float:
        ...

    @abstractmethod
    def measure_charge(self) -> float:
        ...


class LCRMeter(Instrument):

    @property
    @abstractmethod
    def function(self) -> str:
        ...

    @function.setter
    @abstractmethod
    def function(self, function: str) -> None:
        ...

    @property
    @abstractmethod
    def amplitude(self) -> float:
        ...

    @amplitude.setter
    @abstractmethod
    def amplitude(self, level: float) -> None:
        ...

    @property
    @abstractmethod
    def frequency(self) -> float:
        ...

    @frequency.setter
    @abstractmethod
    def frequency(self, frequency: float) -> None:
        ...

    @abstractmethod
    def measure_pair(self) -> Tuple[float, float]:
        ...


class SwitchingMatrix(Instrument):

    CHANNELS: List[str] = []

    @property
    @abstractmethod
    def closed_channels(self) -> List[str]:
        ...

    @abstractmethod
    def close_channels(self, channels: List[str]) -> None:
        ...

    @abstractmethod
    def open_channels(self, channels: List[str]) -> None:
        ...

    @abstractmethod
    def open_all_channels(self) -> None:
        ...