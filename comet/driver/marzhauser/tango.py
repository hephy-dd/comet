from typing import Iterable, Optional

from comet.driver.generic import InstrumentError
from comet.driver.generic import StepperMotorAxis, StepperMotorController

Position = Iterable[float]


class TangoAxis(StepperMotorAxis):

    @property
    def name(self) -> str:
        return "xyza"[self.index]

    def calibrate(self) -> None:
        self.resource.write("!autostatus 0")
        self.resource.write(f"!cal {self.name}")

    def range_measure(self) -> None:
        self.resource.write("!autostatus 0")
        self.resource.write(f"!rm {self.name}")

    def move_absolute(self, value: float) -> None:
        self.resource.write("!autostatus 0")
        self.resource.write(f"!moa {self.name} {value:.3f}")

    def move_relative(self, value: float) -> None:
        self.resource.write("!autostatus 0")
        self.resource.write(f"!mor {self.name} {value:.3f}")

    @property
    def position(self) -> float:
        result = self.resource.query(f"?pos {self.name}")
        return float(result)

    @property
    def is_moving(self) -> bool:
        result = self.resource.query(f"?statusaxis {self.name}")
        return "M" in result


class Tango(StepperMotorController):

    def identify(self) -> str:
        return self.resource.query("?version").strip()

    def reset(self) -> None:
        ...

    def clear(self) -> None:
        ...

    def next_error(self) -> Optional[InstrumentError]:
        ...

    def __getitem__(self, index: int) -> TangoAxis:
        return TangoAxis(self.resource, index)

    def calibrate(self) -> None:
        self.resource.write("!autostatus 0")
        self.resource.write("!cal")

    def range_measure(self) -> None:
        self.resource.write("!autostatus 0")
        self.resource.write("!rm")

    def move_absolute(self, position: Position) -> None:
        values = " ".join([format(value, '.3f') for value in position])
        self.resource.write("!autostatus 0")
        self.resource.write(f"!moa {values}")

    def move_relative(self, position: Position) -> None:
        values = " ".join([format(value, '.3f') for value in position])
        self.resource.write("!autostatus 0")
        self.resource.write(f"!mor {values}")

    def abort(self) -> None:
        self.resource.write("!a")

    def force_abort(self) -> None:
        self.resource.write(chr(0x03))  # Ctrl+C

    @property
    def position(self) -> Position:
        result = self.resource.query("?pos")
        return [float(value) for value in result.split()]

    @property
    def is_moving(self) -> bool:
        result = self.resource.query("?statusaxis")
        return "M" in result

    @property
    def joystick_enabled(self) -> bool:
        result = self.resource.query(f"?joy")
        return bool(int(result))

    @joystick_enabled.setter
    def joystick_enabled(self, value: bool) -> None:
        enabled = {False: 0, True: 2}[value]
        self.resource.write("!autostatus 0")
        self.resource.write(f"!joy {enabled:d}")
