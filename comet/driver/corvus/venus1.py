from typing import Tuple

from comet.driver import lock, Driver

__all__ = ['Venus1']

class Axis(Driver):

    @property
    def _axis(self):
        return self.kwargs.get('axis')

    @property
    def pitch(self) -> float:
        """Returns axis pitch.

        >>> instr.x.pitch
        2.0
        """
        return float(self.resource.query(f'{self._axis} getpitch'))

    @pitch.setter
    def pitch(self, value: float):
        """Set axis pitch.

        >>> instr.x.pitch = 2.0
        """
        self.resource.write(f'{value:.6f} {self._axis} setpitch')

    @property
    def unit(self):
        """Returns axis unit.

        >>> instr.x.unit
        2
        """
        return int(self.resource.query(f'{self._axis} getunit'))

    @property
    def umotmin(self) -> Tuple[int]:
        """Returns minimum motor voltage in [mV].

        >>> instr.x.umotmin
        1850
        """
        return int(self.resource.query(f'{self._axis} getumotmin'))

    @umotmin.setter
    def umotmin(self, value: int):
        """Set minimum motor voltage in [mV].

        >>> instr.x.umotmin = 1850
        """
        self.resource.write(f'{value:d} {self._axis} setumotmin')

    @property
    def umotgrad(self) -> int:
        """Returns motor phase current/torque.

        >>> instr.x.umotgrad
        55
        """
        return int(self.resource.query(f'{self._axis} getumotgrad'))

    @umotgrad.setter
    def umotgrad(self, value: int):
        """Set motor phase current/torque.

        >>> instr.x.umotgrad = 55
        """
        self.resource.write(f'{value:d} {self._axis} setumotgrad')

    @property
    def polepairs(self) -> int:
        """Returns step motor pole pairs.

        >>> instr.x.polepairs
        50
        """
        return int(self.resource.query(f'{self._axis} getpolepairs'))

    @polepairs.setter
    def polepairs(self, value: int):
        """Set step motor pole pairs.

        >>> instr.x.polepairs = 50
        """
        assert value == 50 or value == 100
        self.resource.write(f'{value:d} {self._axis} setpolepairs')

    @property
    def enabled(self) -> int:
        """Returns axis state.

        >>> instr.x.enabled
        1
        """
        return int(self.resource.query(f'{self._axis} getaxis'))

    @enabled.setter
    def enabled(self, value: int):
        """Set axis state.

        >>> instr.x.enabled = 1
        """
        assert 0 <= value <= 4
        self.resource.write(f'{value:d} {self._axis} setaxis')

    @property
    def phaseares(self) -> int:
        """Returns phase A resolution.

        >>> instr.x.phaseares
        16
        """
        return int(self.resource.query(f'{self._axis} getphaseares'))

    @phaseares.setter
    def phaseares(self, value: int):
        """Set phase A resolution.

        >>> instr.x.polepairs = 16
        """
        assert 2<= value <= 16
        self.resource.write(f'{value:d} {self._axis} setphaseares')

    @property
    def motiondir(self) -> int:
        """Returns motor rotation direction.

        >>> instr.x.motiondir
        0
        """
        return int(self.resource.query(f'{self._axis} getmotiondir'))

    @motiondir.setter
    def motiondir(self, value: int):
        """Set motor rotation direction.

        >>> instr.x.motiondir = 0
        """
        assert 0<= value <= 1
        self.resource.write(f'{value:d} {self._axis} setmotiondir')

    # TODO ncalvel

    # TODO nrmvel

    def speed(self, value):
        """Move axis using speed mode.

        >>> instr.x.speed(-0.1)
        """
        self.resource.write(f'{value:.6f} {self._axis} speed')

    def test(self, value: float):
        """Executes axis test routine.

        >>> instr.x.test(10.0)
        """
        self.resource.write(f'{value:.6f} {self._axis} test')

    @property
    def caldone(self) -> int:
        """Returns axis status of previous calibration or rangemeasure command.

        >>> instr.x.caldone
        1
        """
        return int(self.resource.query(f'{self._axis} getcaldone'))

    @property
    def sw(self) -> Tuple[int, int]:
        """Returns tuple containing axis limit switch modes for calibration and
        rangemeasure (0: closing, 1: opening, 2: ignore).

        >>> instr.x.sw
        (0, 0)
        """
        values = self.resource.query(f'{self._axis} getsw').split()
        return tuple(map(int, values))

    # TODO sw

    # TODO swst

    @property
    def calswdist(self) -> float:
        """Returns axis limit switch distance.

        >>> instr.calswdist
        0.0
        """
        return float(self.resource.query(f'{self._axis} getcalswdist'))

    @calswdist.setter
    def calswdist(self, value: float):
        """Set axis limit switch distance.

        >>> instr.calswdist = 0.0
        """
        self.resource.write(f'{value:.6f} {self._axis} setcalswdist')

    def ncal(self):
        """Calibrate axis.

        >>> instr.x.ncal()
        """
        self.resource.write(f'{self._axis} ncal')

    def nrm(self):
        """Rangemove axis.

        >>> instr.x.nrm()
        """
        self.resource.write(f'{self._axis} nrm')

    @property
    def nlimit(self) -> Tuple[float, float]:
        """Returns axis soft limits (lower, upper).

        >>> instr.x.nlimit
        (0.0, 12.0)
        """
        return tuple(map(float, self.resource.query(f'{self._axis} getnlimit').split()))

    # TODO org()

    # TODO org

    # TODO orgsw

    # TODO orgswst

    # TODO infunc

    @property
    def mp(self) -> int:
        """Returns state of axis motors (0: currentless, 1: under current).

        >>> instr.x.mp
        1
        """
        return int(self.resource.query(f'{self._axis} getmp'))

    @mp.setter
    def mp(self, value: int):
        """Set state of axis motors (0: currentless, 1: under current).

        >>> instr.x.mp = 1
        """
        assert 0<= value <= 1
        self.resource.write(f'{value:d} {self._axis} getmp')

    # TODO pdisplay

    # TODO njoyspeed

    # TODO joyassign

    # TODO wheelres

    # TODO wheelratio

    # TODO wheelbratio

class System(Driver):

    def save(self):
        """Save paramerters.

        >>> instr.system.save()
        """
        self.resource.write('save')

    def restore(self):
        """Restore saved parameters.

        >>> instr.system.restore()
        """
        self.resource.write('restore')

    def fpara(self):
        """Restores factory defaults.

        >>> instr.system.fpara()
        """
        self.resource.write('getfpara')

    def clear(self):
        """Clears content of parameter stack.

        >>> instr.system.clear()
        """
        self.resource.write('clear')

    def reset(self):
        """Reboot the instrument. Sockets are closed.

        >>> instr.system.reset()
        """
        self.resource.write('reset')

    def beep(self, value: int):
        """Beep.

        Note: Corvus TT only.

        >>> instr.beep(1000) # beep 1 sec
        """
        assert 1<= value <= 10000
        self.resource.write(f'{value:d} beep')

    @property
    def version(self) -> str:
        """Returns firmware version.

        >>> instr.system.version
        '1.42'
        """
        return self.resource.query('version').strip()

    @property
    def macadr(self) -> str:
        """Returns MAC address.

        Note: Corvus TT only.

        >>> instr.system.macadr
        '00:50:C2:10:91:91'
        """
        return self.resource.query('getmacadr').strip()

    @property
    def identify(self) -> str:
        """Returns Corvus TT identification.

        Note: Corvus TT only

        >>> instr.system.identify
        'Corvus 1 462 1 380'
        """
        return self.resource.query('identify')

    @property
    def options(self) -> int:
        """Returns available instrument options.

        >>> instr.system.options
        8
        """
        return int(self.resource.query('getoptions'))

class Venus1(Driver):
    """Venus-1 driver for Corvus TT/eco controllers."""

    x = Axis(axis=1)
    y = Axis(axis=2)
    z = Axis(axis=3)

    system = System()

    @property
    def identification(self) -> str:
        """Returns instrument identification.

        >>> instr.identification
        'Corvus 1 462 1 380'
        """
        return self.system.identify

    @property
    @lock
    def pitch(self) -> Tuple[float]:
        """Returns tuple containing pitches.

        >>> instr.pitch
        (2.0, 2.0, 2.0, 1.0)
        """
        self.resource.write('-1 getpitch')
        values = []
        values.append(self.resource.read())
        values.append(self.resource.read())
        values.append(self.resource.read())
        values.append(self.resource.read())
        return tuple(map(float, values))

    @property
    def dim(self) -> int:
        """Return number of active dimensions.

        >>> instr.dim
        3
        """
        return int(self.resource.query('getdim'))

    @dim.setter
    def dim(self, value: int):
        """Set number of active dimensions.

        >>> instr.dim = 3
        """
        assert 1 <= value <= 3
        self.resource.write(f'{value:d} setdim')

    @property
    def unit(self):
        """Returns tuple containing units.

        >>> instr.unit
        (2.0, 2.0, 2.0, 2.0)
        """
        values = self.resource.query('-1 getunit').split()
        return tuple(map(float, values))

    @property
    @lock
    def umotmin(self) -> Tuple[int]:
        """Returns tuple containing minimum motor voltages in [mV].

        >>> instr.umotmin
        (1850, 1850, 1850)
        """
        self.resource.write('-1 getumotmin')
        values = []
        values.append(self.resource.read())
        values.append(self.resource.read())
        values.append(self.resource.read())
        return tuple(map(int, values))

    @property
    @lock
    def umotgrad(self) -> Tuple[int]:
        """Returns tuple containing motor phase current/torque.

        >>> instr.umotgrad
        (55, 55, 55)
        """
        self.resource.write('-1 getumotgrad')
        values = []
        values.append(self.resource.read())
        values.append(self.resource.read())
        values.append(self.resource.read())
        return tuple(map(int, values))

    @property
    @lock
    def polepairs(self) -> Tuple[int]:
        """Returns tuple containing step motor pole pairs.

        >>> instr.polepairs
        (50, 50, 50)
        """
        self.resource.write('-1 getpolepairs')
        values = []
        values.append(self.resource.read())
        values.append(self.resource.read())
        values.append(self.resource.read())
        return tuple(map(int, values))

    @property
    def axes(self):
        """Returns axes states.

        >>> instr.axes
        (1, 1, 0)
        """
        values = self.resource.query('-1 getaxis').split()
        return tuple(map(int, values))

    @property
    def powerup(self) -> int:
        """Returns power up commands.

        >>> instr.powerup
        0
        """
        return int(self.resource.query('getpowerup'))

    @powerup.setter
    def powerup(self, value: int):
        """Set power up commands.

        >>> instr.powerup = 0
        """
        assert (0<= value <= 7) or (15<= value <= 16)
        self.resource.write(f'{value:d} setpowerup')

    @property
    @lock
    def phaseares(self) -> Tuple[int, int ,int]:
        """Returns tuple containing phase A resolution.

        >>> instr.phaseares
        (16, 16, 16)
        """
        self.resource.write('-1 getphaseares')
        values = []
        values.append(self.resource.read())
        values.append(self.resource.read())
        values.append(self.resource.read())
        return tuple(map(int, values))

    def __mode(self, value: int):
        """Set command mode, 0 for host mode, 1 for terminal mode.

        >>> instr.mode = 0
        """
        assert 0<= value <= 1
        self.resource.write(f'{value:d} mode')
    mode = property(None, __mode)

    @property
    def ipadr(self) -> str:
        """Returns instrument IP address.

        >>> instr.ipadr
        '192.168.1.2'
        """
        return self.resource.query('getipadr')

    # @ipadr.setter
    # def ipadr(self, value: str):
    #     """Set instrument IP address.
    #
    #     >>> instr.ipadr = '192.168.1.2'
    #     """
    #     aaa, bbb, ccc, ddd = list(map(int, value.split('.')))
    #     self.resource.write(f'{aaa} {bbb} {ccc} {ddd} setipadr')

    @property
    def vel(self) -> float:
        """Returns velocity.

        >>> instr.vel
        90.0
        """
        return float(self.resource.query('getvel'))

    @vel.setter
    def vel(self, value: float):
        """Set velocity.

        >>> instr.vel = 90.0
        """
        self.resource.write(f'{value:.6f} setvel')

    @property
    def accel(self) -> float:
        """Returns acceleration.

        >>> instr.accel
        200.0
        """
        return float(self.resource.query('getaccel'))

    @accel.setter
    def accel(self, value: float):
        """Set acceleration.

        >>> instr.accel = 200.0
        """
        self.resource.write(f'{value:.6f} setaccel')

    @property
    def accelfunc(self) -> int:
        """Returns acceleration function.

        >>> instr.accelfunc
        0
        """
        return int(self.resource.query('getaccelfunc'))

    @accelfunc.setter
    def accelfunc(self, value: int):
        """Set acceleration function.

        >>> instr.accelfunc = 0
        """
        assert 0 <= value <= 1
        self.resource.write(f'{value:d} setaccelfunc')

    @property
    def manaccel(self) -> float:
        """Returns acceleration for manual mode.

        >>> instr.manaccel
        50.0
        """
        return float(self.resource.query('getmanaccel'))

    @manaccel.setter
    def manaccel(self, value: float):
        """Set acceleration function.

        >>> instr.accelfunc = 0
        """
        assert 0. <= value <= 2400.
        self.resource.write(f'{value:.6f} setmanaccel')

    # TODO calvel

    # TODO rmvel

    # TODO refvel

    def move(self, x: float, y: float, z: float):
        """Moves axes to absolute coordinates.

        >>> instr.move(2, 4, 0)
        """
        return self.resource.query(f'{x:.6f} {y:.6f} {z:.6f} move')

    m = move

    def rmove(self, x: float, y: float, z: float):
        """Moves axes relative to current coordinates.

        >>> instr.rmove(1, 1, 0)
        """
        return self.resource.query(f'{x:.6f} {y:.6f} {z:.6f} rmove')

    r = rmove

    def stopspeed(self):
        """Abort speed mode for all axes.

        >>> instr.stopspeed()
        """
        self.resource.write('stopspeed')

    def randmove(self):
        """Moves axes to random coordinates using random accelarations and
        velocities.

        >>> instr.randmove()
        """
        self.resource.write('randmove')

    def calibrate(self):
        """Calibrates axes by moving to limit switches.

        >>> instr.calibrate()
        """
        self.resource.write('calibrate')

    cal = calibrate

    def rangemeasure(self):
        """Moves axes to limit switches.

        >>> instr.rangemeasure()
        """

    rm = rangemeasure

    @property
    def sw(self) -> Tuple[int, int, int, int, int, int]:
        """Returns tuple containing limit switch modes for calibration and
        rangemeasure (0: closing, 1: opening, 2: ignore).

        >>> instr.sw
        (0, 0, 1, 0, 2, 2)
        """
        values = self.resource.query('-1 getsw').split()
        return tuple(map(int, values))

    @property
    @lock
    def limit(self) -> Tuple[Tuple[float, float]]:
        """Returns tuple containing soft limits (lower, upper) for all axes.

        >>> instr.limit
        ((0.0, 16383.0), (0.0, 16383.0), (-16383.0, 16383.0))
        """
        self.resource.write('getlimit')
        values = []
        values.append(tuple(map(float, self.resource.read().split())))
        values.append(tuple(map(float, self.resource.read().split())))
        values.append(tuple(map(float, self.resource.read().split())))
        return tuple(values)

    @limit.setter
    def limit(self, values: Tuple[Tuple[float, float]]):
        """Set soft limits (lower, upper) for all axes.

        >>> instr.limit = ((0, 12), (0, 25), (-10, 30))
        """
        # NOTE: from the documentation, page 124
        # [-A1] [-A2] [-A3] [A1+] [A2+] [A3+] setlimit
        limits = [
            value[0][0],
            value[1][0],
            value[2][0],
            value[0][1],
            value[1][1],
            value[2][1],
        ]
        limits = " ".join([format(limit, '.6f') for limit in limits])
        self.resource.write(f'{limits} setlimit')

    # TODO orgsw

    # TODO orgswst

    def abort(self):
        """Aborts currently executed command.

        >>> instr.abort()
        """
        self.resource.write('abort')

    @property
    def mp(self) -> Tuple[int]:
        """Returns states of axes motors (0: currentless, 1: under current).

        >>> instr.mp
        (0, 1, 1)
        """
        values = self.resource.query('-1 getmp')
        return tuple(map(int, values))

    @property
    def pos(self) -> Tuple[float, float, float]:
        """Returns tuple containing axes position.

        >>> instr.pos
        (1.0, 19.0, 0.0)
        """
        values = self.resource.query('pos').split()
        return tuple(map(float, values))

    @pos.setter
    def pos(self, values: Tuple[float, float, float]):
        """Set coordinate origin relative to current position.

        >>> instr.pos = 0, 0, 0
        """
        x, y, z = values
        self.resource.write(f'{x:.6f} {y:.6f} {z:.6f} setpos')

    @property
    @lock
    def pdisplay(self) -> Tuple[Tuple[int, int]]:
        """Returns format of position display for host and terminal mode.

        >>> instr.pdisplay
        ((10, 5), (10, 5), (10, 5))
        """
        self.resource.write('-1 getpdisplay')
        values = []
        values.append(tuple(map(int, self.resource.read().split())))
        values.append(tuple(map(int, self.resource.read().split())))
        values.append(tuple(map(int, self.resource.read().split())))
        return tuple(values)

    # TODO ugly
    def align(self, x, y, org_x, org_y, axis):
        """Align orthogonal coordinate system.

        >>> instr.align(0, 0, 10, 10, axis=1)
        """
        self.resource.write(f'{x} {y} {org_x} {org_y} align')

    def ico(self):
        """Reset rotated coordinate system.

        >>> instr.ico()
        """
        self.resource.write('ico')

    # TODO (get)ico

    # TODO decode register
    @property
    def status(self) -> int:
        """Returns instrument status.

        >>> instr.status
        2
        """
        return int(self.resource.query('status'))

    @property
    def error(self) -> int:
        """Returns error code.

        >>> instr.error
        1001
        """
        return int(self.resource.query('geterror'))

    @property
    def merror(self) -> int:
        """Returns machine error code.

        >>> instr.merror
        0
        """
        return int(self.resource.query('getmerror'))

    @property
    def gsp(self) -> int:
        """Returns number of elements on parameter stack.

        >>> instr.gsp
        2
        """
        return int(self.resource.query('gsp'))

    @property
    def ticks(self) -> int:
        """Return processor cycles counter (250us).

        >>> instr.ticks
        22016079
        """
        return int(self.resource.query('getticks'))

    # TODO ...

    # TODO joysticktype

    @property
    def joystick(self) -> bool:
        """Returns True if joystick is enabled.

        >>> instr.joystick
        True
        """
        return bool(int(self.resource.query('getjoystick')))

    @joystick.setter
    def joystick(self, value: bool):
        """Set True to enable joystick.

        >>> instr.joystick = True
        """
        self.resource.write(f'{value:d} joystick')

    # TODO joyspeed

    # TODO joybspeed

    # TODO wheel
