"""Hydra (Venus-3) emulator."""

import random

from comet.emulator import Emulator, message, run

__all__ = ["HydraEmulator"]


class HydraEmulator(Emulator):
    """Hydra (Venus-3) emulator."""

    IDENTITY: str = "Hydra 0 0 0 0"
    VERSION: str = "1.0"
    MAC_ADDR: str = "00:00:00:00:00:00"
    SERIAL_NO: str = "01010042"

    def __init__(self) -> None:
        super().__init__()

        self.pos = {"1": 0.0, "2": 0.0}
        self.calibrate = {"1": 3, "2": 3}

        self.axes_moving: int = 0
        self.manual_move: int = 0

    @message(r'^identify$')
    def get_identify(self) -> str:
        return self.options.get("identity", self.IDENTITY)

    @message(r'^getversion|version$')
    def get_version(self) -> float:
        return float(self.options.get("version", self.VERSION))  # double!

    @message(r'^getmacadr$')
    def get_macadr(self) -> str:
        return self.options.get("macaddr", self.MAC_ADDR)

    @message(r'^getserialno$')
    def get_serialno(self) -> str:
        return self.options.get("serialno", self.SERIAL_NO)

    @message(r'^getproductid$')
    def get_productid(self) -> str:
        return "hydra"

    @message(r'^getcputemp$')
    def get_cputemp(self) -> float:
        return float(self.options.get("cputemp", 40.0))

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
    def get_nstatus(self, device) -> int:
        status = 0
        cal = int(self.calibrate[device] & 0x1 == 0x1)
        rm = int(self.calibrate[device] & 0x2 == 0x2)
        status |= ((self.axes_moving & 0x1) << 0)
        status |= ((self.manual_move & 0x1) << 1)
        status |= ((cal & 0x1) << 3)
        status |= ((rm & 0x1) << 4)
        return status

    @message(r'^(1|2)\s+np$')
    def get_np(self, device) -> float:
        return self.pos[device]

    @message(r'^([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+m$')
    def set_move(self, x, y) -> None:
        self.pos.update({"1": float(x), "2": float(y)})

    @message(r'^([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+r$')
    def set_rmove(self, x, y) -> None:
        self.pos["1"] += float(x)
        self.pos["2"] += float(y)

    @message(r'^(1|2)\s+nrandmove$')
    def set_nrandmove(self, device) -> None:
        self.pos[device] = random.uniform(0, 100)

    @message(r'^(1|2)\s+(?:ncalibrate|ncal)$')
    def set_ncalibrate(self, device) -> None:
        self.calibrate[device] = 0x1

    @message(r'^(1|2)\s+(?:nrangemeasure|nrm)$')
    def set_nrangemeasure(self, device) -> None:
        self.calibrate[device] |= 0x2


if __name__ == "__main__":
    run(HydraEmulator())
