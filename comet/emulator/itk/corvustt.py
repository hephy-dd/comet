"""Corvus TT (Venus-1) emulator."""

import random
import time

from comet.emulator import Emulator, message, run

__all__ = ["CorvusTTEmulator"]


class CorvusTTEmulator(Emulator):
    """Corvus TT (Venus-1) emulator."""

    IDENTITY = "Corvus 0 0 0 0"
    VERSION = "1.0"
    MAC_ADDR = "00:00:00:00:00:00"
    SERIAL_NO = "01011234"

    def __init__(self):
        super().__init__()

        self.x_pos = 0.0
        self.y_pos = 0.0
        self.z_pos = 0.0

        self.x_unit = 1
        self.y_unit = 1
        self.z_unit = 1

        self.table_limits = [0.0, 0.0, 0.0, 1000000.0, 100000.0, 25000.0]

        self.getcaldone = [3, 3, 3]
        self.getaxis = [1, 1, 1]
        self.geterror = 0
        self.getmerror = 0

        self.joystick = False

        self.status = 0

        self.ticks_t0 = time.monotonic()

    @message(r'^identify$')
    def get_identify(self):
        return self.options.get("identity", self.IDENTITY)

    @message(r'^version$')
    def get_version(self):
        return self.options.get("version", self.VERSION)

    @message(r'^getmacadr$')
    def get_macadr(self):
        return self.options.get("macaddr", self.MAC_ADDR)

    @message(r'^getserialno$')
    def get_serialno(self):
        return self.options.get("serialno", self.SERIAL_NO)

    @message(r'^getoptions$')
    def get_options(self):
        return 0x3

    @message(r'^getticks|gt$')
    def get_ticks(self):
        return int((time.monotonic() - self.ticks_t0) * (1 / 250e-6))  # 250us ticks

    @message(r'^(\d)\s+beep$')
    def set_beep(self, millisec):
        ...

    @message(r'^reset$')
    def set_reset(self):
        self.getcaldone = [0, 0, 0]
        self.status = 0

    @message(r'^status|st$')
    def get_status(self):
        return self.status

    @message(r'^pos|p$')
    def get_pos(self):
        return f'{self.x_pos:.6f} {self.y_pos:.6f} {self.z_pos:.6f}'

    @message(r'^(.+)\s+setlimit$')
    def set_limit(self, value):
        a1, b1, c1, a2, b2, c2 = map(float, value.split())
        self.table_limits = a1, b1, c1, a2, b2, c2

    @message(r'^getlimit$')
    def get_limit(self):
        a1, b1, c1, a2, b2, c2 = self.table_limits
        return f"{a1:.6f} {b1:.6f}", f"{c1:.6f} {a2:.6f}", f"{b2:.6f} {c2:.6f}"

    @message(r'^([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+(?:move|m)$')
    def set_move(self, x, y, z):
        self.x_pos = max(0.0, float(x))
        self.y_pos = max(0.0, float(y))
        self.z_pos = max(0.0, float(z))

    @message(r'^([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+(?:rmove|r)$')
    def set_rmove(self, x, y, z):
        self.x_pos = max(0.0, self.x_pos + float(x))
        self.y_pos = max(0.0, self.y_pos + float(y))
        self.z_pos = max(0.0, self.z_pos + float(z))

    @message(r'^randmove$')
    def set_randmove(self):
        a1, b1, c1, a2, b2, c2 = self.table_limits
        self.x_pos = random.uniform(a1, a2)
        self.y_pos = random.uniform(b1, b2)
        self.z_pos = random.uniform(c1, c2)

    @message(r'^(-1|1|2|3)\s+getcaldone$')
    def get_caldone(self, axis):
        if axis == "-1":
            a1, a2, a3 = self.getcaldone
            return f"{a1} {a2} {a3}"
        if axis == "1":
            self.getcaldone[0]
        if axis == "2":
            self.getcaldone[0]
        if axis == "3":
            self.getcaldone[0]

    @message(r'^(-1|1|2|3)\s+getaxis$')
    def get_axis(self, axis):
        if axis == "-1":
            a1, a2, a3 = self.getaxis
            return f"{a1} {a2} {a3}"
        if axis == "1":
            return self.getaxis[0]
        if axis == "2":
            return self.getaxis[1]
        if axis == "3":
            return self.getaxis[2]

    @message(r'^geterror|ge$')
    def get_error(self):
        return self.geterror

    @message(r'^getmerror|gme$')
    def get_merror(self):
        return self.getmerror

    @message(r'^(0|1)\s+(?:joystick|j)$')
    def set_joystick(self, value):
        self.joystick = bool(int(value))

    @message(r'^getjoystick|gj$')
    def get_joystick(self):
        return int(self.joystick)

    @message(r'^(-1|1|2|3)\s+getunit$')
    def get_unit(self, axis):
        if axis == "-1":
            return f'{self.x_unit} {self.y_unit} {self.z_unit} 1'
        if axis == "1":
            return f'{self.x_unit}'
        if axis == "2":
            return f'{self.y_unit}'
        if axis == "3":
            return f'{self.z_unit}'

    @message(r'^(\d)\s+(1|2|3)\s+setunit$')
    def set_unit(self, value, axis):
        if axis == "1":
            self.x_unit = int(value)
        if axis == "2":
            self.y_unit = int(value)
        if axis == "3":
            self.z_unit = int(value)

    @message(r'^(1|2|3)\s+ncal$')
    def set_ncal(self, axis):
        if axis == "1":
            self.getcaldone[0] = 0x1
        if axis == "2":
            self.getcaldone[1] = 0x1
        if axis == "3":
            self.getcaldone[2] = 0x1

    @message(r'^(1|2|3)\s+nrm$')
    def set_nrm(self, axis):
        if axis == "1":
            self.getcaldone[0] |= 0x2
        if axis == "2":
            self.getcaldone[1] |= 0x2
        if axis == "3":
            self.getcaldone[2] |= 0x2


if __name__ == "__main__":
    run(CorvusTTEmulator())
