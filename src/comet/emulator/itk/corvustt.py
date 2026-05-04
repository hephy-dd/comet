"""Corvus TT (Venus-1) emulator."""

import random
import time
from dataclasses import dataclass, astuple
from collections.abc import Mapping
from typing import Any, Optional

from comet.emulator import Emulator, message, run

__all__ = ["CorvusTTEmulator"]


@dataclass
class TableLimits:
    a1: float
    b1: float
    c1: float
    a2: float
    b2: float
    c2: float


class CorvusTTEmulator(Emulator):
    """Corvus TT (Venus-1) emulator."""

    def __init__(self) -> None:
        super().__init__()

        self.identity: str = "Corvus 0 0 0 0"
        self.version: str = "1.0"
        self.mac_address: str = "00:00:00:00:00:00"
        self.serial_no: str = "01011234"

        self.x_pos: float = 0.0
        self.y_pos: float = 0.0
        self.z_pos: float = 0.0

        self.x_unit: int = 1
        self.y_unit: int = 1
        self.z_unit: int = 1

        self.table_limits = TableLimits(0.0, 0.0, 0.0, 1000000.0, 100000.0, 25000.0)

        self.getcaldone: list[int] = [3, 3, 3]
        self.getaxis: list[int] = [1, 1, 1]
        self.geterror: int = 0
        self.getmerror: int = 0

        self.joystick: bool = False

        self.status: int = 0

        self.ticks_t0: float = time.monotonic()

    def load_options(self, options: Mapping[str, Any]) -> None:
        if isinstance(identity := options.get("identity"), str):
            self.identity = identity
        if isinstance(version := options.get("version"), str):
            self.version = version
        if isinstance(mac_address := options.get("mac_address"), str):
            self.mac_address = mac_address
        if isinstance(serial_no := options.get("serial_no"), str):
            self.serial_no = serial_no

        if isinstance(position := options.get("position"), dict):
            if isinstance(x := position.get("x"), (int, float)):
                self.x_pos = float(x)
            if isinstance(y := position.get("y"), (int, float)):
                self.y_pos = float(y)
            if isinstance(z := position.get("z"), (int, float)):
                self.z_pos = float(z)

        if isinstance(unit := options.get("unit"), dict):
            if isinstance(x := unit.get("x"), int):
                self.x_unit = int(max(1, min(3, x)))
            if isinstance(y := unit.get("y"), int):
                self.y_unit = int(max(1, min(3, y)))
            if isinstance(z := unit.get("z"), int):
                self.z_unit = int(max(1, min(3, z)))

    @message(r"identify$")
    def get_identify(self) -> str:
        return self.identity

    @message(r"version$")
    def get_version(self) -> str:
        return self.version

    @message(r"getmacadr$")
    def get_macadr(self) -> str:
        return self.mac_address

    @message(r"getserialno$")
    def get_serialno(self) -> str:
        return self.serial_no

    @message(r"getoptions$")
    def get_options(self) -> int:
        return 0x3

    @message(r"getticks|gt$")
    def get_ticks(self) -> str:
        dt = time.monotonic() - self.ticks_t0
        ticks = int(dt * (1 / 250e-6))  # 250us ticks
        return f"{ticks:d}"

    @message(r"(\d)\s+beep$")
    def set_beep(self, millisec) -> None: ...

    @message(r"reset$")
    def set_reset(self) -> None:
        self.getcaldone = [0, 0, 0]
        self.status = 0

    @message(r"status|st$")
    def get_status(self) -> str:
        return f"{self.status:d}"

    @message(r"pos|p$")
    def get_pos(self) -> str:
        return f'{self.x_pos:.6f} {self.y_pos:.6f} {self.z_pos:.6f}'

    @message(r"(.+)\s+setlimit$")
    def set_limit(self, value) -> None:
        a1, b1, c1, a2, b2, c2 = map(float, value.split())
        self.table_limits = TableLimits(a1, b1, c1, a2, b2, c2)

    @message(r"getlimit$")
    def get_limit(self) -> tuple[str, str, str]:
        a1, b1, c1, a2, b2, c2 = astuple(self.table_limits)
        return f"{a1:.6f} {b1:.6f}", f"{c1:.6f} {a2:.6f}", f"{b2:.6f} {c2:.6f}"

    @message(r"([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+(?:move|m)$")
    def set_move(self, x, y, z) -> None:
        self.x_pos = max(0.0, float(x))
        self.y_pos = max(0.0, float(y))
        self.z_pos = max(0.0, float(z))

    @message(r"([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+(?:rmove|r)$")
    def set_rmove(self, x, y, z) -> None:
        self.x_pos = max(0.0, self.x_pos + float(x))
        self.y_pos = max(0.0, self.y_pos + float(y))
        self.z_pos = max(0.0, self.z_pos + float(z))

    @message(r"randmove$")
    def set_randmove(self) -> None:
        a1, b1, c1, a2, b2, c2 = astuple(self.table_limits)
        self.x_pos = random.uniform(a1, a2)
        self.y_pos = random.uniform(b1, b2)
        self.z_pos = random.uniform(c1, c2)

    @message(r"(1|2|3)\s+getcaldone$")
    def get_caldone(self, axis) -> Optional[str]:
        if axis == "1":
            return f"{self.getcaldone[0]}"
        if axis == "2":
            return f"{self.getcaldone[1]}"
        if axis == "3":
            return f"{self.getcaldone[2]}"
        return None

    @message(r"(-1|1|2|3)\s+getaxis$")
    def get_axis(self, axis) -> Optional[str]:
        if axis == "-1":
            a1, a2, a3 = self.getaxis
            return f"{a1} {a2} {a3}"
        if axis == "1":
            return f"{self.getaxis[0]}"
        if axis == "2":
            return f"{self.getaxis[1]}"
        if axis == "3":
            return f"{self.getaxis[2]}"
        return None

    @message(r"geterror|ge$")
    def get_error(self) -> int:
        return self.geterror

    @message(r"getmerror|gme$")
    def get_merror(self) -> int:
        return self.getmerror

    @message(r"(0|1)\s+(?:joystick|j)$")
    def set_joystick(self, value) -> None:
        self.joystick = bool(int(value))

    @message(r"getjoystick|gj$")
    def get_joystick(self) -> str:
        return f"{self.joystick:d}"

    @message(r"(-1|1|2|3)\s+getunit$")
    def get_unit(self, axis) -> Optional[str]:
        if axis == "-1":
            return f"{self.x_unit} {self.y_unit} {self.z_unit} 1"
        if axis == "1":
            return f"{self.x_unit}"
        if axis == "2":
            return f"{self.y_unit}"
        if axis == "3":
            return f"{self.z_unit}"
        return None

    @message(r"(\d)\s+(1|2|3)\s+setunit$")
    def set_unit(self, value, axis) -> None:
        if axis == "1":
            self.x_unit = int(value)
        if axis == "2":
            self.y_unit = int(value)
        if axis == "3":
            self.z_unit = int(value)

    @message(r"(1|2|3)\s+ncal$")
    def set_ncal(self, axis) -> None:
        if axis == "1":
            self.getcaldone[0] = 0x1
        if axis == "2":
            self.getcaldone[1] = 0x1
        if axis == "3":
            self.getcaldone[2] = 0x1

    @message(r"(1|2|3)\s+nrm$")
    def set_nrm(self, axis) -> None:
        if axis == "1":
            self.getcaldone[0] |= 0x2
        if axis == "2":
            self.getcaldone[1] |= 0x2
        if axis == "3":
            self.getcaldone[2] |= 0x2


if __name__ == "__main__":
    run(CorvusTTEmulator())
