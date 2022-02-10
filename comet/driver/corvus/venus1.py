from typing import Tuple

from comet.driver import Driver

__all__ = ['Venus1']

class Axis(Driver):

    def __init__(self, resource, index):
        super().__init__(resource)
        self._index = index

    @property
    def pitch(self) -> float:
        """Returns axis pitch.

        >>> instr.x.pitch
        2.0
        """
        return float(self.resource.query(f'{self._index} getpitch'))

    @pitch.setter
    def pitch(self, value: float) -> None:
        """Set axis pitch.

        >>> instr.x.pitch = 2.0
        """
        self.resource.write(f'{value:.6f} {self._index} setpitch')

    @property
    def unit(self) -> int:
        """Returns axis unit.
        0: Microstep
        1: μm
        2: mm
        3: cm
        4: m
        5: inch
        6: mil (1/1000 inch)

        >>> instr.x.unit
        2
        """
        return int(self.resource.query(f'{self._index} getunit'))

    @unit.setter
    def unit(self, value: int) -> None:
        """Set axis unit.
        0: Microstep
        1: μm
        2: mm
        3: cm
        4: m
        5: inch
        6: mil (1/1000 inch)

        >>> instr.x.unit = 2
        """
        self.resource.write(f'{value:d} {self._index} setunit')

    @property
    def umotmin(self) -> int:
        """Returns minimum motor voltage in [mV].

        >>> instr.x.umotmin
        1850
        """
        return int(self.resource.query(f'{self._index} getumotmin'))

    @umotmin.setter
    def umotmin(self, value: int) -> None:
        """Set minimum motor voltage in [mV].

        >>> instr.x.umotmin = 1850
        """
        self.resource.write(f'{value:d} {self._index} setumotmin')

    @property
    def umotgrad(self) -> int:
        """Returns motor phase current/torque.

        >>> instr.x.umotgrad
        55
        """
        return int(self.resource.query(f'{self._index} getumotgrad'))

    @umotgrad.setter
    def umotgrad(self, value: int) -> None:
        """Set motor phase current/torque.

        >>> instr.x.umotgrad = 55
        """
        self.resource.write(f'{value:d} {self._index} setumotgrad')

    @property
    def polepairs(self) -> int:
        """Returns step motor pole pairs.

        >>> instr.x.polepairs
        50
        """
        return int(self.resource.query(f'{self._index} getpolepairs'))

    @polepairs.setter
    def polepairs(self, value: int) -> None:
        """Set step motor pole pairs.

        >>> instr.x.polepairs = 50
        """
        assert value == 50 or value == 100
        self.resource.write(f'{value:d} {self._index} setpolepairs')

    @property
    def enabled(self) -> int:
        """Returns axis state.

        >>> instr.x.enabled
        1
        """
        return int(self.resource.query(f'{self._index} getaxis'))

    @enabled.setter
    def enabled(self, value: int) -> None:
        """Set axis state.

        >>> instr.x.enabled = 1
        """
        assert 0 <= value <= 4
        self.resource.write(f'{value:d} {self._index} setaxis')

    @property
    def phaseares(self) -> int:
        """Returns phase A resolution.

        >>> instr.x.phaseares
        16
        """
        return int(self.resource.query(f'{self._index} getphaseares'))

    @phaseares.setter
    def phaseares(self, value: int) -> None:
        """Set phase A resolution.

        >>> instr.x.polepairs = 16
        """
        assert 2 <= value <= 16
        self.resource.write(f'{value:d} {self._index} setphaseares')

    @property
    def motiondir(self) -> int:
        """Returns motor rotation direction.

        >>> instr.x.motiondir
        0
        """
        return int(self.resource.query(f'{self._index} getmotiondir'))

    @motiondir.setter
    def motiondir(self, value: int) -> None:
        """Set motor rotation direction.

        >>> instr.x.motiondir = 0
        """
        assert 0 <= value <= 1
        self.resource.write(f'{value:d} {self._index} setmotiondir')

    # TODO ncalvel

    # TODO nrmvel

    def speed(self, value: float) -> None:
        """Move axis using speed mode.

        >>> instr.x.speed(-0.1)
        """
        self.resource.write(f'{value:.6f} {self._index} speed')

    def test(self, value: float) -> None:
        """Executes axis test routine.

        >>> instr.x.test(10.0)
        """
        self.resource.write(f'{value:.6f} {self._index} test')

    @property
    def caldone(self) -> int:
        """Returns axis status of previous calibration or rangemeasure command.

        >>> instr.x.caldone
        1
        """
        return int(self.resource.query(f'{self._index} getcaldone'))

    @property
    def sw(self) -> Tuple[int, int]:
        """Returns tuple containing axis limit switch modes for calibration and
        rangemeasure (0: closing, 1: opening, 2: ignore).

        >>> instr.x.sw
        (0, 0)
        """
        values = self.resource.query(f'{self._index} getsw').split()
        return int(values[0]), int(values[1])

    # TODO sw

    # TODO swst

    @property
    def calswdist(self) -> float:
        """Returns axis limit switch distance.

        >>> instr.calswdist
        0.0
        """
        return float(self.resource.query(f'{self._index} getcalswdist'))

    @calswdist.setter
    def calswdist(self, value: float) -> None:
        """Set axis limit switch distance.

        >>> instr.calswdist = 0.0
        """
        self.resource.write(f'{value:.6f} {self._index} setcalswdist')

    def ncal(self) -> None:
        """Calibrate axis.

        >>> instr.x.ncal()
        """
        self.resource.write(f'{self._index} ncal')

    def nrm(self) -> None:
        """Rangemove axis.

        >>> instr.x.nrm()
        """
        self.resource.write(f'{self._index} nrm')

    @property
    def nlimit(self) -> Tuple[float, float]:
        """Returns axis soft limits (lower, upper).

        >>> instr.x.nlimit
        (0.0, 12.0)
        """
        return tuple(map(float, self.resource.query(f'{self._index} getnlimit').split()))

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
        return int(self.resource.query(f'{self._index} getmp'))

    @mp.setter
    def mp(self, value: int) -> None:
        """Set state of axis motors (0: currentless, 1: under current).

        >>> instr.x.mp = 1
        """
        assert 0 <= value <= 1
        self.resource.write(f'{value:d} {self._index} setmp')

    # TODO pdisplay

    # TODO njoyspeed

    # TODO joyassign

    @property
    def joyspeed(self) -> float:
        """Returns maximum joystick speed for axis in mm/s.

        >>> instr.x.joyspeed
        20.0
        """
        return float(self.resource.query(f'{self._index} getnjoyspeed'))

    @joyspeed.setter
    def joyspeed(self, value: float) -> None:
        """Set maximum joystick speed for axis in mm/s.

        >>> instr.x.joyspeed = 20.0
        """
        self.resource.write(f'{value:.6f} {self._index} setnjoyspeed')

    # TODO wheelres

    # TODO wheelratio

    # TODO wheelbratio

class System(Driver):

    def save(self) -> None:
        """Save paramerters.

        >>> instr.system.save()
        """
        self.resource.write('save')

    def restore(self) -> None:
        """Restore saved parameters.

        >>> instr.system.restore()
        """
        self.resource.write('restore')

    def fpara(self) -> None:
        """Restores factory defaults.

        >>> instr.system.fpara()
        """
        self.resource.write('getfpara')

    def clear(self) -> None:
        """Clears content of parameter stack.

        >>> instr.system.clear()
        """
        self.resource.write('clear')

    def reset(self) -> None:
        """Reboot the instrument. Sockets are closed.

        >>> instr.system.reset()
        """
        self.resource.write('reset')

    def beep(self, value: int) -> None:
        """Beep.

        Note: Corvus TT only.

        >>> instr.beep(1000) # beep 1 sec
        """
        assert 1 <= value <= 10000
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
        """Returns Corvus TT identification in the following format:
        <Model> <HW-Rev> <SW-Rev> <Board-SW> <DIP-Sw>

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

    @property
    def serialno(self) -> str:
        """Returns instrument serial in the following format:
        <YY><HW><SERIAL>

        >>> isntr.system.serialno
        '19091234'
        """
        return self.resource.query('getserialno')

class Venus1(Driver):
    """Venus-1 driver for Corvus TT/eco controllers."""

    X_AXIS = 1
    Y_AXIS = 2
    Z_AXIS = 3

    HOST_MODE = 0
    TERMINAL_MODE = 1

    def __init__(self, resource, **kwargs) -> None:
        super().__init__(resource, **kwargs)
        self.x: Axis = Axis(self.resource, self.X_AXIS)
        self.y: Axis = Axis(self.resource, self.Y_AXIS)
        self.z: Axis = Axis(self.resource, self.Z_AXIS)
        self.system: System = System(self.resource)

    @property
    def identification(self) -> str:
        """Returns instrument identification consisting of model, version and
        serial number.

        >>> instr.identification
        'Corvus 2.62 19091073'
        """
        model = self.system.identify.split()[0]
        version = self.system.version
        serialno = self.system.serialno
        return f'{model} {version} {serialno}'

    @property
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
    def unit(self) -> Tuple[int]:
        """Returns tuple containing units.
        0: Microstep
        1: μm
        2: mm
        3: cm
        4: m
        5: inch
        6: mil (1/1000 inch)

        >>> instr.unit
        (2, 1, 1, 1)
        """
        values = self.resource.query('-1 getunit').split()
        return tuple(map(int, values))

    @property
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
    def axes(self) -> Tuple[int, ...]:
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
    def powerup(self, value: int) -> None:
        """Set power up commands.

        >>> instr.powerup = 0
        """
        assert (0 <= value <= 7) or (15 <= value <= 16)
        self.resource.write(f'{value:d} setpowerup')

    @property
    def phaseares(self) -> Tuple[int, int, int]:
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

    def mode(self, value: int) -> None:
        """Set command mode.

        0: HOST_MODE
        1: TERMINAL_MODE

        >>> instr.mode = instr.HOST_MODE
        """
        assert value in (self.HOST_MODE, self.TERMINAL_MODE)
        self.resource.write(f'{value:d} mode')
        # Workaround: clear clogged control characters from internal
        # buffer by reading querying instrument identity.
        self.resource.query('identify')

    mode = property(None, mode)

    @property
    def ipadr(self) -> str:
        """Returns instrument IP address.

        >>> instr.ipadr
        '192.168.1.2'
        """
        return self.resource.query('getipadr')

    # @ipadr.setter
    # def ipadr(self, value: str) -> None:
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
    def vel(self, value: float) -> None:
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
    def accel(self, value: float) -> None:
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

    def move(self, x: float, y: float, z: float) -> None:
        """Moves axes to absolute coordinates.

        >>> instr.move(2, 4, 0)
        """
        self.resource.write(f'{x:.6f} {y:.6f} {z:.6f} move')

    m = move

    def rmove(self, x: float, y: float, z: float) -> None:
        """Moves axes relative to current coordinates.

        >>> instr.rmove(1, 1, 0)
        """
        self.resource.write(f'{x:.6f} {y:.6f} {z:.6f} rmove')

    r = rmove

    def stopspeed(self) -> None:
        """Abort speed mode for all axes.

        >>> instr.stopspeed()
        """
        self.resource.write('stopspeed')

    def randmove(self) -> None:
        """Moves axes to random coordinates using random accelarations and
        velocities.

        >>> instr.randmove()
        """
        self.resource.write('randmove')

    def calibrate(self) -> None:
        """Calibrates axes by moving to limit switches.

        >>> instr.calibrate()
        """
        self.resource.write('calibrate')

    cal = calibrate

    def rangemeasure(self) -> None:
        """Moves axes to limit switches.

        >>> instr.rangemeasure()
        """
        self.resource.write('rangemeasure')

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
    def limit(self) -> Tuple[Tuple[float, ...], ...]:
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
    def limit(self, values: Tuple[Tuple[float, float], ...]) -> None:
        """Set soft limits (lower, upper) for all axes.

        >>> instr.limit = ((0, 12), (0, 25), (-10, 30))
        """
        # NOTE: from the documentation, page 124
        # [-A1] [-A2] [-A3] [A1+] [A2+] [A3+] setlimit
        limits = [
            values[0][0],
            values[1][0],
            values[2][0],
            values[0][1],
            values[1][1],
            values[2][1],
        ]
        limits = ' '.join([format(limit, '.6f') for limit in limits])
        self.resource.write(f'{limits} setlimit')

    # TODO orgsw

    # TODO orgswst

    def abort(self) -> None:
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
        values = self.resource.query('-1 getmp').split()
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
    def pos(self, values: Tuple[float, float, float]) -> None:
        """Set coordinate origin relative to current position.

        >>> instr.pos = 0, 0, 0
        """
        x, y, z = values
        self.resource.write(f'{x:.6f} {y:.6f} {z:.6f} setpos')

    @property
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
    def align(self, x, y, org_x, org_y, axis) -> None:
        """Align orthogonal coordinate system.

        >>> instr.align(0, 0, 10, 10, axis=1)
        """
        self.resource.write(f'{x} {y} {org_x} {org_y} {axis} align')

    def reset_ico(self) -> None:
        """Reset rotated coordinate system.

        >>> instr.reset_ico()
        """
        self.resource.write('ico')

    @property
    def ico(self) -> int:
        """Get rotated coordinate system.

        >>> instr.ico
        1
        """
        return int(self.resource.query('getico'))

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

    # TODO out

    # TODO aout

    # TODO in

    # TODO joysticktype

    @property
    def joystick(self) -> bool:
        """Returns True if joystick is enabled.

        >>> instr.joystick
        True
        """
        return bool(int(self.resource.query('getjoystick')))

    @joystick.setter
    def joystick(self, value: bool) -> None:
        """Set True to enable joystick.

        >>> instr.joystick = True
        """
        self.resource.write(f'{value:d} joystick')

    @property
    def joyspeed(self) -> float:
        """Returns maximum joystick speed in mm/s.

        >>> instr.joyspeed
        20.0
        """
        return float(self.resource.query('getjoyspeed'))

    @joyspeed.setter
    def joyspeed(self, value: float) -> None:
        """Set maximum joystick speed in mm/s.

        >>> instr.joyspeed = 20.0
        """
        self.resource.write(f'{value:.6f} setjoyspeed')

    @property
    def joybspeed(self) -> float:
        """Returns special joystick button speed in mm/s.

        >>> instr.joybspeed
        0.01
        """
        return float(self.resource.query('getjoybspeed'))

    @joybspeed.setter
    def joybspeed(self, value: float) -> None:
        """Set special joystick button speed in mm/s.

        >>> instr.joybspeed = 0.01
        """
        self.resource.write(f'{value:.6f} setjoybspeed')

    # TODO wheel
