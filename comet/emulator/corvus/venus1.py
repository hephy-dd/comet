"""Corvus TT Venus-1 emulator."""

from comet.emulator.emulator import message, run
from comet.emulator.emulator import RequestHandler

__all__ = ['Venus1Handler']

class Venus1Handler(RequestHandler):
    """Corvus TT Venus-1 request handler."""

    macadr = '00:00:00:00:00:00'
    identify = "Corvus 0 0 0 0"
    version = "1.0"
    serialno = "01011234"

    x_pos = 0.0
    y_pos = 0.0
    z_pos = 0.0

    x_unit = 1
    y_unit = 1
    z_unit = 1

    getcaldone = 3
    getaxis = 3
    geterror = 0
    getmerror = 0

    joystick = False

    @message(r'getmacadr')
    def query_getmacadr(self):
        return self.macadr

    @message(r'identify')
    def query_identify(self):
        return self.identify

    @message(r'version')
    def query_version(self):
        return self.version

    @message(r'getserialno')
    def query_getserialno(self):
        return self.serialno

    @message(r'pos')
    def query_pos(self):
        cls = type(self)
        return f'{cls.x_pos:.6f} {cls.y_pos:.6f} {cls.z_pos:.6f}'

    @message(r'([+-]?\d+(?:\.\d+)?) ([+-]?\d+(?:\.\d+)?) ([+-]?\d+(?:\.\d+)?) move')
    def write_move(self, x, y, z):
        type(self).x_pos = max(0.0, float(x))
        type(self).y_pos = max(0.0, float(y))
        type(self).z_pos = max(0.0, float(z))

    @message(r'([+-]?\d+(?:\.\d+)?) ([+-]?\d+(?:\.\d+)?) ([+-]?\d+(?:\.\d+)?) rmove')
    def write_rmove(self, x, y, z):
        type(self).x_pos = max(0.0, type(self).x_pos + float(x))
        type(self).y_pos = max(0.0, type(self).y_pos + float(y))
        type(self).z_pos = max(0.0, type(self).z_pos + float(z))

    @message(r'\d\s+getcaldone')
    def query_getcaldone(self):
        return type(self).getcaldone

    @message(r'\d\s+getaxis')
    def query_getaxis(self):
        return type(self).getaxis

    @message(r'geterror')
    def query_geterror(self):
        return type(self).geterror

    @message(r'getmerror')
    def query_getmerror(self):
        return type(self).getmerror

    @message(r'(\d) joystick')
    def write_joystick(self, value):
        type(self).joystick = bool(int(value))

    @message(r'getjoystick')
    def query_getjoystick(self):
        return int(type(self).joystick)

    @message(r'-1 getunit')
    def query_getunit_all(self):
        cls = type(self)
        return f'{cls.x_unit} {cls.y_unit} {cls.z_unit} 1'

    @message(r'1 getunit')
    def query_getunit_x(self):
        cls = type(self)
        return f'{cls.x_unit}'

    @message(r'2 getunit')
    def query_getunit_y(self):
        cls = type(self)
        return f'{cls.y_unit}'

    @message(r'3 getunit')
    def query_getunit_z(self):
        cls = type(self)
        return f'{cls.z_unit}'

    @message(r'(\d) 1 setunit')
    def write_setunit_x(self, value):
        cls = type(self)
        cls.x_unit = int(value)

    @message(r'(\d) 2 setunit')
    def write_setunit_y(self, value):
        cls = type(self)
        cls.y_unit = int(value)

    @message(r'(\d) 3 setunit')
    def write_setunit_z(self, value):
        cls = type(self)
        cls.z_unit = int(value)


if __name__ == "__main__":
    run(Venus1Handler)
