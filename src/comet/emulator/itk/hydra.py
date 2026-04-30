"""Hydra (Venus-3) emulator."""

import random
from collections.abc import Mapping
from typing import Any

from comet.emulator import Emulator, message, run

__all__ = ["HydraEmulator"]


class HydraEmulator(Emulator):
    """Hydra (Venus-3) emulator."""

    def __init__(self) -> None:
        super().__init__()

        self.identity: str = "Hydra 0 0 0 0"
        self.version: float = 1.0
        self.mac_address: str = "00:00:00:00:00:00"
        self.serial_no: str = "01010042"

        self.x_pos: float = 0.0
        self.y_pos: float = 0.0

        self.calibrate: dict[str, int] = {"1": 3, "2": 3}

        self.axes_moving: int = 0
        self.manual_move: int = 0

        self.cpu_temperature: float = 40.0

    def load_options(self, options: Mapping[str, Any]) -> None:
        if isinstance(identity := options.get("identity"), str):
            self.identity = identity
        if isinstance(version := options.get("version"), float):
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

        if isinstance(cpu_temperature := options.get("cpu_temperature"), float):
            self.cpu_temperature = cpu_temperature

    @message(r'^identify$')
    def get_identify(self) -> str:
        return self.identity

    @message(r'^getversion|version$')
    def get_version(self) -> float:
        return self.version  # double!

    @message(r'^getmacadr$')
    def get_macadr(self) -> str:
        return self.mac_address

    @message(r'^getserialno$')
    def get_serialno(self) -> str:
        return self.serial_no

    @message(r'^getproductid$')
    def get_productid(self) -> str:
        return "hydra"

    @message(r'^getcputemp$')
    def get_cputemp(self) -> float:
        return self.cpu_temperature

    @message(r'^reset$')
    def set_reset(self) -> None: ...

    @message(r'^status|st$')
    def get_status(self) -> int:
        status = 0
        all_cal = int(all([value & 0x1 for value in self.calibrate.values()]))
        all_rm = int(all([value & 0x2 for value in self.calibrate.values()]))
        status |= ((self.axes_moving & 0x1) << 0)
        status |= ((self.manual_move & 0x1) << 1)
        status |= ((all_cal & 0x1) << 3)
        status |= ((all_rm & 0x1) << 4)
        return status

    @message(r'^(1|2)\s+(?:nstatus|nst|est|ast)$')
    def get_nstatus(self, axis) -> int:
        status = 0
        cal = int(self.calibrate[axis] & 0x1 == 0x1)
        rm = int(self.calibrate[axis] & 0x2 == 0x2)
        status |= ((self.axes_moving & 0x1) << 0)
        status |= ((self.manual_move & 0x1) << 1)
        status |= ((cal & 0x1) << 3)
        status |= ((rm & 0x1) << 4)
        return status

    @message(r'^(1|2)\s+np$')
    def get_np(self, axis) -> float:
        if axis == "1":
            return self.x_pos
        else:
            return self.y_pos

    @message(r'^([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+m$')
    def set_move(self, x, y) -> None:
        self.x_pos = float(x)
        self.y_pos = float(y)

    @message(r'^([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+r$')
    def set_rmove(self, x, y) -> None:
        self.x_pos += float(x)
        self.y_pos += float(y)

    @message(r'^(1|2)\s+nrandmove$')
    def set_nrandmove(self, axis) -> None:
        pos = random.uniform(0, 100)
        if axis == "1":
            self.x_pos = pos
        elif axis == "2":
            self.y_pos = pos

    @message(r'^(1|2)\s+(?:ncalibrate|ncal)$')
    def set_ncalibrate(self, axis) -> None:
        self.calibrate[axis] = 0x1

    @message(r'^(1|2)\s+(?:nrangemeasure|nrm)$')
    def set_nrangemeasure(self, axis) -> None:
        self.calibrate[axis] |= 0x2


if __name__ == "__main__":
    run(HydraEmulator())
