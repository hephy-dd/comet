"""ITK Andromeda emulator."""

import random
from enum import IntEnum

from comet.emulator import Context, Emulator, message, run

__all__ = ["AndromedaEmulator"]


class ErrorType(IntEnum):
    NO_ERROR = 0
    INTERNAL_ERROR = 4
    DEVICE_OUT_OF_RANGE = 100
    UNDEFINED_SYMBOL = 102
    WRONG_PARAMETER_TYPE = 1001
    NOT_ENOUGH_PARAMETERS = 1002
    PARAMETER_OUT_OF_RANGE = 1003
    UNDEFINED_COMMAND = 2000


class AndromedaEmulator(Emulator):
    def __init__(self, context: Context) -> None:
        super().__init__(context)

        options = context.options

        self.identity: str = options.get("identity", "Andromeda 0 0 0 0")
        self.version: float = options.get("version", 1.0)
        self.mac_address: str = options.get("mac_address", "00:00:00:00:00:00")
        self.serial_no: str = options.get("serial_no", "00770031")

        position: dict[str, float] = options.get("position", {})

        self.position: dict[str, float] = {
            "1": position.get("x", 0.0),
            "2": position.get("y", 0.0),
            "3": position.get("z", 0.0),
            "4": position.get("a", 0.0),
            "5": position.get("b", 0.0),
            "6": position.get("c", 0.0),
        }
        self.calibrate: dict[str, int] = {
            "1": 0x3,
            "2": 0x3,
            "3": 0x3,
            "4": 0x3,
            "5": 0x3,
            "6": 0x3,
        }

        self.axes_moving: bool = False
        self.manual_move: bool = False
        self.errors: list[ErrorType] = []

    @message(r"identify$")
    def get_identify(self) -> str:
        return self.identity

    @message(r"getversion|version$")
    def get_version(self) -> str:
        return str(self.version)  # double!

    @message(r"getmacadr$")
    def get_macadr(self) -> str:
        return self.mac_address

    @message(r"getserialno$")
    def get_serialno(self) -> str:
        return self.serial_no

    @message(r"getproductid$")
    def get_productid(self) -> str:
        return "andromeda"

    @message(r"reset$")
    def set_reset(self) -> None:
        self.errors.clear()

    @message(r"status|st$")
    def get_status(self) -> str:
        status: int = 0
        all_cal = int(all(value & 0x1 for value in self.calibrate.values()))
        all_rm = int(all(value & 0x2 for value in self.calibrate.values()))
        status |= int(self.axes_moving) << 0
        status |= int(self.manual_move) << 1
        status |= (all_cal & 0x1) << 3
        status |= (all_rm & 0x1) << 4
        return str(status)

    @message(r"(\S+)\s+(?:nstatus|nst|est|ast)$")
    def get_nstatus(self, axis: str) -> str | None:
        if self._parse_axis(axis) is None:
            return None

        status: int = 0
        cal = int(self.calibrate[axis] & 0x1 == 0x1)
        rm = int(self.calibrate[axis] & 0x2 == 0x2)
        status |= int(self.axes_moving) << 0
        status |= int(self.manual_move) << 1
        status |= (cal & 0x1) << 3
        status |= (rm & 0x1) << 4
        return str(status)

    @message(r"(\S+)\s+np$")
    def get_np(self, axis: str) -> str | None:
        if self._parse_axis(axis) is None:
            return None

        return format(self.position[axis], ".6f")

    @message(r"(.+)\s+m$")
    def set_move(self, values: str) -> None:
        vector = self._parse_vector(values)
        if vector is None:
            return

        for i, value in enumerate(vector, start=1):
            self.position[str(i)] = value

    @message(r"(.+)\s+r$")
    def set_rmove(self, values: str) -> None:
        vector = self._parse_vector(values)
        if vector is None:
            return

        for i, value in enumerate(vector, start=1):
            self.position[str(i)] += value

    @message(r"(\S+)\s+nrandmove$")
    def set_nrandmove(self, axis: str) -> None:
        if self._parse_axis(axis) is None:
            return

        self.position[axis] = random.uniform(0, 100)

    @message(r"(\S+)\s+(?:ncalibrate|ncal)$")
    def set_ncalibrate(self, axis: str) -> None:
        if self._parse_axis(axis) is None:
            return

        self.calibrate[axis] = 0x1

    @message(r"(\S+)\s+(?:nrangemeasure|nrm)$")
    def set_nrangemeasure(self, axis: str) -> None:
        if self._parse_axis(axis) is None:
            return

        self.calibrate[axis] |= 0x2

    @message(r"ge$")
    def get_error(self) -> str:
        error = self.errors.pop() if self.errors else ErrorType.NO_ERROR
        return str(error)

    def _parse_axis(self, axis: str) -> str | None:
        try:
            axis_num = int(axis)
        except ValueError:
            self.errors.append(ErrorType.WRONG_PARAMETER_TYPE)
            return None

        if not 1 <= axis_num <= 6:
            self.errors.append(ErrorType.DEVICE_OUT_OF_RANGE)
            return None

        return str(axis_num)

    def _parse_vector(self, values: str) -> list[float] | None:
        values_str = values.split()

        if not values_str:
            self.errors.append(ErrorType.NOT_ENOUGH_PARAMETERS)
            return None

        if len(values_str) > 6:
            self.errors.append(ErrorType.PARAMETER_OUT_OF_RANGE)
            return None

        try:
            return [float(value) for value in values_str]
        except ValueError:
            self.errors.append(ErrorType.WRONG_PARAMETER_TYPE)
            return None


if __name__ == "__main__":
    run(AndromedaEmulator)
