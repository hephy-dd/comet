from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from .driver import Driver


class InstrumentError:

    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message


class ErrorQueueMixin(ABC):

    @abstractmethod
    def next_error(self) -> Optional[InstrumentError]:
        ...


class RouteTerminalMixin(ABC):

    ROUTE_TERMINAL_FRONT = 'front'
    ROUTE_TERMINAL_REAR = 'rear'

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
        pass

    @abstractmethod
    def reset(self) -> None:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...

    def set_mute(self, state: bool) -> None:
        pass


class SourceMeterUnit(Instrument):

    OUTPUT_ON = True
    OUTPUT_OFF = False

    @property
    @abstractmethod
    def output(self) -> bool:
        ...

    @output.setter
    @abstractmethod
    def output(self, state: bool) -> None:
        ...

    FUNCTION_VOLTAGE = 'voltage'
    FUNCTION_CURRENT = 'current'

    @property
    @abstractmethod
    def function(self) -> str:
        ...

    @function.setter
    @abstractmethod
    def function(self, function: str) -> None:
        ...

    @abstractmethod
    def get_voltage(self) -> float:
        pass

    @abstractmethod
    def set_voltage(self, level: float) -> None:
        pass

    @abstractmethod
    def get_voltage_range(self) -> float:
        pass

    @abstractmethod
    def set_voltage_range(self, level: float) -> None:
        pass

    @abstractmethod
    def set_voltage_compliance(self, level: float) -> None:
        pass

    @abstractmethod
    def get_current(self) -> float:
        pass

    @abstractmethod
    def set_current(self, level: float) -> None:
        pass

    @abstractmethod
    def get_current_range(self) -> float:
        pass

    @abstractmethod
    def set_current_range(self, level: float) -> None:
        pass

    @abstractmethod
    def set_current_compliance(self, level: float) -> None:
        pass

    @abstractmethod
    def compliance_tripped(self) -> bool:
        pass

    @abstractmethod
    def measure_voltage(self) -> float:
        ...

    @abstractmethod
    def measure_current(self) -> float:
        ...


class Electrometer(Instrument):

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
    def measure(self) -> Tuple[float, float]:
        pass


class SwitchingMatrix(Instrument):

    CHANNELS: List[str] = []

    @abstractmethod
    def closed_channels(self) -> List[str]:
        pass

    @abstractmethod
    def close_channels(self, channels: List[str]) -> None:
        pass

    @abstractmethod
    def open_channels(self, channels: List[str]) -> None:
        pass

    @abstractmethod
    def open_all_channels(self) -> None:
        pass
