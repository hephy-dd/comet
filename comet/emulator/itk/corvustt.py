"""Corvus TT (Venus-1) emulator."""

from comet.emulator import Emulator, message, run

__all__ = ['CorvusTTEmulator']


class CorvusTTEmulator(Emulator):
    """Corvus TT (Venus-1) emulator."""

    identity = "Corvus 0 0 0 0"
    macadr = '00:00:00:00:00:00'
    version = "1.0"
    serialno = "01011234"

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

    @message(r'^getmacadr$')
    def get_macadr(self):
        return self.macadr

    @message(r'^identify$')
    def get_identify(self):
        return self.identity

    @message(r'^version$')
    def get_version(self):
        return self.version

    @message(r'^getserialno$')
    def get_serialno(self):
        return self.serialno

    @message(r'^status$')
    def get_status(self):
        return self.status

    @message(r'^pos$')
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

    @message(r'^([+-]?\d+(?:\.\d+)?) ([+-]?\d+(?:\.\d+)?) ([+-]?\d+(?:\.\d+)?) move$')
    def set_move(self, x, y, z):
        self.x_pos = max(0.0, float(x))
        self.y_pos = max(0.0, float(y))
        self.z_pos = max(0.0, float(z))

    @message(r'^([+-]?\d+(?:\.\d+)?) ([+-]?\d+(?:\.\d+)?) ([+-]?\d+(?:\.\d+)?) rmove$')
    def set_rmove(self, x, y, z):
        self.x_pos = max(0.0, self.x_pos + float(x))
        self.y_pos = max(0.0, self.y_pos + float(y))
        self.z_pos = max(0.0, self.z_pos + float(z))

    @message(r'^-1\s+getcaldone$')
    def get_caldone(self):
        a1, a2, a3 = self.getcaldone
        return f"{a1} {a2} {a3}"

    @message(r'^1\s+getcaldone$')
    def get_caldone_x(self):
        return self.getcaldone[0]

    @message(r'^2\s+getcaldone$')
    def get_caldone_y(self):
        return self.getcaldone[1]

    @message(r'^3\s+getcaldone$')
    def get_caldone_z(self):
        return self.getcaldone[2]

    @message(r'^-1\s+getaxis$')
    def get_axis(self):
        a1, a2, a3 = self.getaxis
        return f"{a1} {a2} {a3}"

    @message(r'^1\s+getaxis$')
    def get_axis_x(self):
        return self.getaxis[0]

    @message(r'^2\s+getaxis$')
    def get_axis_y(self):
        return self.getaxis[1]

    @message(r'^3\s+getaxis$')
    def get_axis_z(self):
        return self.getaxis[2]

    @message(r'^geterror$')
    def get_error(self):
        return self.geterror

    @message(r'^getmerror$')
    def get_merror(self):
        return self.getmerror

    @message(r'^(\d) joystick$')
    def set_joystick(self, value):
        self.joystick = bool(int(value))

    @message(r'^getjoystick$')
    def get_joystick(self):
        return int(self.joystick)

    @message(r'^-1 getunit$')
    def get_unit_all(self):
        return f'{self.x_unit} {self.y_unit} {self.z_unit} 1'

    @message(r'^1 getunit$')
    def get_unit_x(self):
        return f'{self.x_unit}'

    @message(r'^2 getunit$')
    def get_unit_y(self):
        return f'{self.y_unit}'

    @message(r'^3 getunit$')
    def get_unit_z(self):
        return f'{self.z_unit}'

    @message(r'^(\d) 1 setunit$')
    def set_unit_x(self, value):
        self.x_unit = int(value)

    @message(r'^(\d) 2 setunit$')
    def set_unit_y(self, value):
        self.y_unit = int(value)

    @message(r'^(\d) 3 setunit$')
    def set_unit_z(self, value):
        self.z_unit = int(value)


if __name__ == "__main__":
    run(CorvusTTEmulator())
