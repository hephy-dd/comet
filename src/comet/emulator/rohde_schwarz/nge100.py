"""Rohde&Schwarz NGE100 power supply emulator"""

import math

from comet.emulator import Emulator
from comet.emulator import message, run


__all__ = ["NGE100Emulator"]


class NGE100Emulator(Emulator):
    IDENTITY: str = "Rohde&Schwarz,NGE103B,5601.3800k03/101863,1.54"

    def __init__(self) -> None:
        super().__init__()

        self.voltage_levels: list[float] = [0.0, 0.0, 0.0]
        self.current_limits: list[float] = [0.0, 00.0, 0.0]
        self.enabled_channels: list[bool] = [False, False, False]

        self.selected_channel: int = 0

        self.resistances: list[float] = [1, 1e3, math.inf]  # 1 Ohm, 1 kOhm, infinite

    def get_voltage(self) -> float:
        voltage_from_current_limit = (
            self.current_limits[self.selected_channel]
            * self.resistances[self.selected_channel]
        )
        voltage_from_voltage_level = self.voltage_levels[self.selected_channel]
        return min(voltage_from_current_limit, voltage_from_voltage_level)

    def get_current(self) -> float:
        current_from_voltage_level = (
            self.voltage_levels[self.selected_channel]
            / self.resistances[self.selected_channel]
        )
        current_from_current_limit = self.current_limits[self.selected_channel]
        return min(current_from_voltage_level, current_from_current_limit)

    @message(r"^\*IDN\?$")
    def identify(self) -> str:
        return self.IDENTITY

    @message(r"^INST(?:rument)? (\d)$")
    def set_channel(self, channel: int) -> None:
        self.selected_channel = int(channel) - 1

    @message(r"^INST(?:rument)?\?$")
    def get_channel(self) -> str:
        return str(self.selected_channel + 1)

    @message(r"^OUTP(?:ut)? (\d)$")
    def set_enabled(self, enabled: int) -> None:
        self.enabled_channels[self.selected_channel] = bool(int(enabled))

    @message(r"^OUTP(?:ut)?\?$")
    def get_enabled(self) -> str:
        return str(int(self.enabled_channels[self.selected_channel]))

    @message(r"(?:SOUR(?:ce)?:)?VOLT(?:age)?(?::LEV(?:el)?)?(?::IMM(?:ediate)?)?(?::AMPL(?:itude)?)? (\d+\.?\d*)$")
    def set_voltage_level(self, voltage_level: float) -> None:
        voltage_level = min(max(0, float(voltage_level)), 32)
        self.voltage_levels[self.selected_channel] = voltage_level

    @message(r"(?:SOUR(?:ce)?:)?VOLT(?:age)?(?::LEV(?:el)?)?(?::IMM(?:ediate)?)?(?::AMPL(?:itude)?)?\?$")
    def get_voltage_level(self) -> str:
        return str(self.voltage_levels[self.selected_channel])

    @message(r"(?:SOUR(?:ce)?:)?CURR(?:ent)?(?::LEV(?:el)?)?(?::IMM(?:ediate)?)?(?::AMPL(?:itude)?)? (\d+\.?\d*)$")
    def set_current_limit(self, current_limit: float) -> None:
        current_limit = min(max(0, float(current_limit)), 3)
        self.current_limits[self.selected_channel] = current_limit

    @message(r"(?:SOUR(?:ce)?:)?CURR(?:ent)?(?::LEV(?:el)?)?(?::IMM(?:ediate)?)?(?::AMPL(?:itude)?)?\?$")
    def get_current_limit(self) -> str:
        return str(self.current_limits[self.selected_channel])

    @message(r"MEAS(?:ure)?(?::SCAL(?:ar)?)?:VOLT(?:age)?(?::DC)?\?$")
    def measure_voltage(self) -> str:
        return str(self.get_voltage())

    @message(r"MEAS(?:ure)?(?::SCAL(?:ar)?)?:CURR(?:ent)?(?::DC)?\?$")
    def measure_current(self) -> str:
        return str(self.get_current())

    @message(r"MEAS(?:ure)?(?::SCAL(?:ar)?)?:POW(?:er)?(?::DC)?\?$")
    def measure_power(self) -> str:
        return str(self.get_voltage() * self.get_current())


if __name__ == "__main__":
    run(NGE100Emulator())
