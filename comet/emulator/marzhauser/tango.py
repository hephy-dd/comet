"""TANGO emulator."""

from typing import Dict

from comet.emulator import Emulator, message, run

__all__ = ["TangoEmulator"]


class TangoEmulator(Emulator):
    """TANGO emulator."""

    VERSION: str = "TANGO-MINI3-EMULATOR, Version 1.00, Mar 11 2022, 13:51:01"

    def __init__(self) -> None:
        super().__init__()
        self.position: Dict[str, float] = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.calst: Dict[str, int] = {"x": 3, "y": 3, "z": 3}
        self.statusaxis: Dict[str, str] = {"x": "@", "y": "@", "z": "@"}
        self.velocity: Dict[str, float] = {"x": 10.0, "y": 10.0, "z": 10.0}
        self.autostatus: bool = True

    # Controller informations

    @message(r'^\??version$')
    def get_version(self) -> str:
        return format(self.options.get("version", self.VERSION))

    @message(r'^\?autostatus$')
    def get_autostatus(self) -> str:
        return format(self.autostatus, "d")

    @message(r'^\!autostatus (0|1)$')
    def set_autostatus(self, value) -> None:
        self.autostatus = {"0": False, "1": True}[value]

    @message(r'^\??err$')
    def get_error(self) -> str:
        return "0"

    # Calibration

    @message(r'^\!?cal$')
    def set_cal(self):
        self.calst["x"] |= 0x1
        self.calst["y"] |= 0x1
        self.calst["z"] |= 0x1
        if self.autostatus:
            return "AAA-."

    @message(r'^\!?cal (x|y|z)$')
    def set_cal_xyz(self, axes):
        self.calst[axes] |= 0x1
        if self.autostatus:
            return "A"

    @message(r'^\!?rm$')
    def set_rm(self):
        self.calst["x"] |= 0x2
        self.calst["y"] |= 0x2
        self.calst["z"] |= 0x2
        if self.autostatus:
            return "DDD-."

    @message(r'^\!?rm (x|y|z)$')
    def set_rm_xyz(self, axes):
        self.calst[axes] &= 0x1
        if self.autostatus:
            return "D"

    @message(r'^\??calst$')
    def get_calst(self) -> str:
        x = self.calst.get("x", 0)
        y = self.calst.get("y", 0)
        z = self.calst.get("z", 0)
        return f"{x:d} {y:d} {z:d}"

    @message(r'^\?calst (x|y|z)$')
    def get_calst_xyz(self, axis) -> str:
        value = self.calst.get(axis, 0)
        return f"{value:d}"

    # Positioning

    @message(r'^\?pos$')
    def get_pos(self):
        x = self.position.get("x", 0)
        y = self.position.get("y", 0)
        z = self.position.get("z", 0)
        return f"{x:.3f} {y:.3f} {z:.3f}"

    @message(r'^\?pos (x|y|z)$')
    def get_pos_xyz(self, axis):
        value = self.position.get(axis)
        return f"{value:.3f}"

    @message(r'^\!?moa ([^\sxyza]+) ([^\s]+) ([^\s]+)$')
    def set_move_absolute(self, x, y, z):
        self.position["x"] = float(x)
        self.position["y"] = float(y)
        self.position["z"] = float(z)
        if self.autostatus:
            return "@@@-."

    @message(r'^\!?moa (x|y|z) ([^\s]+)$')
    def set_move_absolute_xyz(self, axis, value):
        self.position[axis] = float(value)
        if self.autostatus:
            return "@@@-."

    @message(r'^\!?mor ([^\sxyza]+) ([^\s]+) ([^\s]+)$')
    def set_move_relative(self, x, y, z):
        self.position["x"] = float(x)
        self.position["y"] = float(y)
        self.position["z"] = float(z)
        if self.autostatus:
            return "@@@-."

    @message(r'^\!?mor (x|y|z) ([^\s]+)$')
    def set_move_relative_xyz(self, axis, value):
        self.position[axis] = float(value)
        if self.autostatus:
            return "@@@-."

    @message(r'^\?statusaxis$')
    def get_statusaxis(self):
        x = self.statusaxis.get("x", "-")
        y = self.statusaxis.get("y", "-")
        z = self.statusaxis.get("z", "-")
        return f"{x}{y}{z}-.-"

    @message(r'^\?statusaxis (x|y|z)$')
    def get_statusaxis_xyz(self, axis):
        value = self.statusaxis.get(axis, "-")
        return f"{value}"

    @message(r'^\?vel$')
    def get_vel(self):
        x = self.velocity.get("x")
        y = self.velocity.get("y")
        z = self.velocity.get("z")
        return f"{x:.3f} {y:.3f} {z:.3f}"

    @message(r'^\?vel (x|y|z)$')
    def get_vel_xyz(self, axis):
        value = self.velocity.get(axis)
        return f"{value:.3f}"

    @message(r'^!vel (x|y|z) ([^\s]+)$')
    def set_vel_xyz(self, axis, value):
        self.velocity[axis]= float(value)
        return "@@@-."

    # System configuration

    @message(r'^save$')
    def action_save(self):
        ...

    @message(r'^restore$')
    def action_restore(self):
        ...

    @message(r'^reset$')
    def action_reset(self):
        ...


if __name__ == "__main__":
    run(TangoEmulator())
