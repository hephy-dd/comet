from typing import Iterable, Optional

from comet.driver.generic import InstrumentError
from comet.driver.generic import StepperMotorAxis, StepperMotorController

Position = Iterable[float]


class Venus2Axis(StepperMotorAxis):

    def calibrate(self) -> None:
        self.resource.write(f"{self.index:d} ncal")

    def range_measure(self) -> None:
        self.resource.write(f"{self.index:d} nrm")

    def move_absolute(self, value: float) -> None:
        self.resource.write(f"{value:.3f} {self.index:d} nmove")

    def move_relative(self, value: float) -> None:
        self.resource.write(f"{value:.3f} {self.index:d} nrmove")

    @property
    def position(self) -> float:
        result = self.resource.query(f"{self.index:d} npos")
        return float(result)

    @property
    def is_moving(self) -> bool:
        result = self.resource.query("status")
        return bool(int(result) & 0x1)


class Venus2(StepperMotorController):

    def identify(self) -> str:
        return self.resource.query("identify").strip()

    def reset(self) -> None:
        ...

    def clear(self) -> None:
        ...

    def next_error(self) -> Optional[InstrumentError]:
        ...

    def __getitem__(self, index: int) -> Venus2Axis:
        return Venus2Axis(self.resource, index)

    def calibrate(self) -> None:
        self.resource.write("cal")

    def range_measure(self) -> None:
        self.resource.write("rm")

    def move_absolute(self, position: Position) -> None:
        values = " ".join([format(value, '.3f') for value in position])
        self.resource.write(f"{values} move")

    def move_relative(self, position: Position) -> None:
        values = " ".join([format(value, '.3f') for value in position])
        self.resource.write(f"{values} rmove")

    def abort(self):
        self.resource.write("abort")

    def force_abort(self):
        self.resource.write(chr(0x03))  # Ctrl+C

    @property
    def position(self) -> Position:
        result = self.resource.query("pos")
        return [float(value) for value in result.split()]

    @property
    def is_moving(self) -> bool:
        result = self.resource.query("status")
        return bool(int(result) & 0x1)

    @property
    def joystick_enabled(self) -> bool:
        result = self.resource.query("getjoystick")
        return bool(int(result))

    @joystick_enabled.setter
    def joystick_enabled(self, value: bool) -> None:
        self.resource.write(f"{value:d} joystick")