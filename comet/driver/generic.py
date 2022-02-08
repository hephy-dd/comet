from abc import abstractmethod
from typing import List, Optional, Tuple

from .driver import Driver


class InstrumentError:

    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message


class Instrument(Driver):

    @abstractmethod
    def identify(self) -> str:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def next_error(self) -> Optional[InstrumentError]:
        pass

    def set_mute(self, state: bool) -> None:
        pass


class SourceMeterUnit(Instrument):

    TERMINAL_FRONT = 'front'
    TERMINAL_REAR = 'rear'

    @abstractmethod
    def get_terminal(self) -> str:
        pass

    @abstractmethod
    def set_terminal(self, terminal: str) -> None:
        pass

    OUTPUT_ON = True
    OUTPUT_OFF = False

    @abstractmethod
    def get_output(self) -> bool:
        pass

    @abstractmethod
    def set_output(self, state: bool) -> None:
        pass

    FUNCTION_VOLTAGE = 'voltage'
    FUNCTION_CURRENT = 'current'

    @abstractmethod
    def get_function(self) -> str:
        pass

    @abstractmethod
    def set_function(self, function: str) -> None:
        pass

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
    def read_voltage(self) -> float:
        pass

    @abstractmethod
    def read_current(self) -> float:
        pass


class Electrometer(Instrument):

    pass


class LCRMeter(Instrument):

    @abstractmethod
    def get_function(self) -> str:
        pass

    @abstractmethod
    def set_function(self, function: str) -> None:
        pass

    @abstractmethod
    def get_amplitude(self) -> float:
        pass

    @abstractmethod
    def set_amplitude(self, level: float) -> None:
        pass

    @abstractmethod
    def get_frequency(self) -> float:
        pass

    @abstractmethod
    def set_frequency(self, frequency: float) -> None:
        pass

    @abstractmethod
    def read(self) -> Tuple[float, float]:
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
