"""Driver for ECR AC3 thermal chuck"""

import time
from dataclasses import dataclass
from enum import IntEnum


from comet.emulator import Emulator
from comet.emulator import message, run

__all__ = ["AC3Emulator"]


class Mode(IntEnum):
    NORMAL = 1
    STANDBY = 2
    DEFROST = 3
    PURGE = 4


class Status(IntEnum):
    TEMPERATURE_REACHED = 0
    HEATING = 1
    COOLING = 2
    ERROR = 8


@dataclass
class State:
    temperature: float = 25.0
    target_temperature: float = 25.0
    mode: Mode = Mode.NORMAL
    control_status: Status = Status.TEMPERATURE_REACHED
    hold_mode: int = 11
    dewpoint_control_status: bool = True
    dewpoint: float = -20.0


class Logic:
    def __init__(self, state: State) -> None:
        self.state = state
        self.ramp_rate_c_per_s: float = 1.0
        self.temperature_tolerance: float = 0.2
        self._last_update_monotonic: float = time.monotonic()

    def update_state(self) -> None:
        now = time.monotonic()
        dt = now - self._last_update_monotonic

        state = self.state
        active = state.mode in (Mode.NORMAL, Mode.STANDBY)

        if active:
            delta = state.target_temperature - state.temperature
            max_step = self.ramp_rate_c_per_s * dt

            if abs(delta) <= self.temperature_tolerance:
                state.temperature = state.target_temperature
                state.control_status = Status.TEMPERATURE_REACHED
            else:
                step = min(abs(delta), max_step)
                if delta > 0:
                    state.temperature += step
                    state.control_status = Status.HEATING
                else:
                    state.temperature -= step
                    state.control_status = Status.COOLING

                # snap if close enough
                if (
                    abs(state.target_temperature - state.temperature)
                    <= self.temperature_tolerance
                ):
                    state.temperature = state.target_temperature
                    state.control_status = Status.TEMPERATURE_REACHED
        else:
            state.control_status = Status.TEMPERATURE_REACHED

        self._last_update_monotonic = now


class AC3Emulator(Emulator):
    def __init__(self) -> None:
        super().__init__()
        self.state = State()
        self.logic = Logic(self.state)

    @message(r"^RC$")
    def get_temperature(self) -> str:
        self.logic.update_state()
        return f"C{int(self.state.temperature * 10):+05d}"

    @message(r"^RT$")
    def get_target_temperature(self) -> str:
        return f"T{int(self.state.target_temperature * 10):+05d}"

    @message(r"^ST([+-]\d{4})$")
    def set_target_temperature(self, value: str) -> str:
        self.state.target_temperature = float(value) / 10
        return "OK"

    @message(r"^RO$")
    def get_mode(self) -> str:
        return f"O{self.state.mode:d}"

    @message(r"^SO([1234])$")
    def set_mode(self, value: str) -> str:
        self.state.mode = Mode(int(value))
        return "OK"

    @message(r"^RF$")
    def get_dewpoint(self) -> str:
        return f"F{int(self.state.dewpoint * 10):+05d}"

    @message(r"^RD$")
    def get_dewpoint_control_status(self) -> str:
        return f"D{int(self.state.dewpoint_control_status)}"

    @message(r"^SD([01])$")
    def set_dewpoint_control_status(self, value: str) -> str:
        self.state.dewpoint_control_status = bool(int(value))
        return "OK"

    @message(r"^RH$")
    def get_hold_mode(self) -> str:
        return f"H{self.state.hold_mode:02d}"

    @message(r"^SH([01])$")
    def set_hold_mode(self, value: str) -> str:
        val = int(value)
        if val == 0:
            self.state.hold_mode = 0
        else:
            self.state.hold_mode = 11
        return "OK"

    @message(r"^RI$")
    def get_control_status(self) -> str:
        self.logic.update_state()
        return f"I{self.state.control_status:d}"

    @message(r"^RE$")
    def get_error(self) -> str:
        return "E000"


if __name__ == "__main__":
    run(AC3Emulator())
