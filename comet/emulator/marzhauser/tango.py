"""TANGO emulator."""

from comet.emulator import Emulator, message, run

__all__ = ['TANGOEmulator']

class TANGOEmulator(Emulator):
    """TANGO emulator."""

    version_string = 'TANGO-MINI3-EMULATOR, Version 1.00, Mar 11 2022, 13:51:01'

    def __init__(self):
        super().__init__()
        self.position = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.velocity = {"x": 10.0, "y": 10.0, "z": 10.0}

    # Controller informations

    @message(r'\??version')
    def get_version(self):
        return type(self).version_string

    # Positioning

    @message(r'\?pos')
    def get_pos(self):
        x = self.position.get("x")
        y = self.position.get("y")
        z = self.position.get("z")
        return f"{x:.3f} {y:.3f} {z:.3f}"

    @message(r'\?pos (x|y|z)')
    def get_pos_xyz(self, axis):
        value = self.position.get(axis)
        return f"{value:.3f}"

    @message(r'^moa (x|y|z) (\w+)$')
    def set_move_absolute_xyz(self, axis, value):
        self.position[axis] = float(value)
        return "@@@-."

    @message(r'\?vel')
    def get_vel(self):
        x = self.velocity.get("x")
        y = self.velocity.get("y")
        z = self.velocity.get("z")
        return f"{x:.3f} {y:.3f} {z:.3f}"

    @message(r'\?vel (x|y|z)')
    def get_vel_xyz(self, axis):
        value = self.velocity.get(axis)
        return f"{value:.3f}"

    @message(r'!vel (x|y|z) (\w+)')
    def set_vel_xyz(self, axis, value):
        self.velocity[axis]= float(value)
        return "@@@-."

    # System configuration

    @message(r'save')
    def action_save(self):
        ...

    @message(r'restore')
    def action_restore(self):
        ...

    @message(r'reset')
    def action_reset(self):
        ...



if __name__ == '__main__':
    run(TANGOEmulator())
