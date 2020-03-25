"""Corvus TT Venus-1 emulator."""

import random
import time

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

    joystick = False

    @message(r'getmacadr')
    def query_getmacadr(self, message):
        return self.macadr

    @message(r'identify')
    def query_identify(self, message):
        return self.identify

    @message(r'version')
    def query_version(self, message):
        return self.version

    @message(r'getserialno')
    def query_getserialno(self, message):
        return self.serialno

    @message(r'pos')
    def query_pos(self, message):
        cls = self.__class__
        return f'{cls.x_pos:.6f} {cls.y_pos:.6f} {cls.z_pos:.6f}'

    @message(r'\d+(\.\d+)? \d+(\.\d+)? \d+(\.\d+)? move')
    def write_move(self, message):
        x, y, z, command = message.split()
        cls = self.__class__
        cls.x_pos = float(x)
        cls.y_pos = float(y)
        cls.z_pos = float(z)

    @message(r'[+-]?\d+(\.\d+)? [+-]?\d+(\.\d+)? [+-]?\d+(\.\d+)? rmove')
    def write_rmove(self, message):
        x, y, z, command = message.split()
        cls = self.__class__
        cls.x_pos += float(x)
        cls.y_pos += float(y)
        cls.z_pos += float(z)

    @message(r'\d joystick')
    def write_joystick(self, message):
        cls = self.__class__
        cls.joystick = bool(int(message.split()[0]))

    @message(r'getjoystick')
    def query_getjoystick(self, message):
        cls = self.__class__
        return f'{cls.joystick:d}'

    @message(r'-1 getunit')
    def query_getunit_all(self, message):
        cls = self.__class__
        return f'{cls.x_unit} {cls.y_unit} {cls.z_unit} 1'

    @message(r'1 getunit')
    def query_getunit_x(self, message):
        cls = self.__class__
        return f'{cls.x_unit}'

    @message(r'2 getunit')
    def query_getunit_y(self, message):
        cls = self.__class__
        return f'{cls.y_unit}'

    @message(r'3 getunit')
    def query_getunit_z(self, message):
        cls = self.__class__
        return f'{cls.z_unit}'

    @message(r'\d 1 setunit')
    def write_setunit_x(self, message):
        cls = self.__class__
        cls.x_unit = int(message.split()[0])

    @message(r'\d 2 setunit')
    def write_setunit_y(self, message):
        cls = self.__class__
        cls.y_unit = int(message.split()[0])

    @message(r'\d 3 setunit')
    def write_setunit_z(self, message):
        cls = self.__class__
        cls.z_unit = int(message.split()[0])


if __name__ == "__main__":
    run(Venus1Handler)
