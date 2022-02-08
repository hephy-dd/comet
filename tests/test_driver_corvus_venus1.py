import unittest

from comet.driver.corvus import Venus1

from .test_driver import BaseDriverTest

class Venus1Test(BaseDriverTest):

    driver_cls = Venus1

    def test_driver(self):
        self.assertEqual(self.driver.X_AXIS, 1)
        self.assertEqual(self.driver.Y_AXIS, 2)
        self.assertEqual(self.driver.Z_AXIS, 3)

    def test_identification(self):
        self.resource.buffer = ['Corvus 1 462 1 380', '1.42', '19091234']
        self.assertEqual(self.driver.identification, 'Corvus 1.42 19091234')
        self.assertEqual(self.resource.buffer, ['identify', 'version', 'getserialno'])

    def test_pitch(self):
        self.resource.buffer = ['2', '2', '2', '1']
        self.assertEqual(self.driver.pitch, (2.0, 2.0, 2.0, 1.0))
        self.assertEqual(self.resource.buffer, ['-1 getpitch'])

    def test_dim(self):
        for value in 1, 2, 3:
            self.resource.buffer = [format(value)]
            self.assertEqual(self.driver.dim, value)
            self.assertEqual(self.resource.buffer, ['getdim'])

            self.resource.buffer = []
            self.driver.dim = value
            self.assertEqual(self.resource.buffer, [f'{value:d} setdim'])

    def test_unit(self):
        self.resource.buffer = ['2 1 1 1']
        self.assertEqual(self.driver.unit, (2, 1, 1, 1))
        self.assertEqual(self.resource.buffer, ['-1 getunit'])

    def test_umotmin(self):
        self.resource.buffer = ['1850', '1851', '1852']
        self.assertEqual(self.driver.umotmin, (1850, 1851, 1852))
        self.assertEqual(self.resource.buffer, ['-1 getumotmin'])

    def test_umotgrad(self):
        self.resource.buffer = ['55', '56', '57']
        self.assertEqual(self.driver.umotgrad, (55, 56, 57))
        self.assertEqual(self.resource.buffer, ['-1 getumotgrad'])

    def test_axes(self):
        self.resource.buffer = ['50', '51', '52']
        self.assertEqual(self.driver.axes, (50, 51, 52))
        self.assertEqual(self.resource.buffer, ['-1 getpolepairs'])

    def test_axes(self):
        self.resource.buffer = ['1 1 0']
        self.assertEqual(self.driver.axes, (1, 1, 0))
        self.assertEqual(self.resource.buffer, ['-1 getaxis'])

    def test_axes(self):
        for value in 0, 1, False, True:
            self.resource.buffer = [f'{value:d}']
            self.assertEqual(self.driver.powerup, int(value))
            self.assertEqual(self.resource.buffer, ['getpowerup'])

            self.resource.buffer = []
            self.driver.powerup = value
            self.assertEqual(self.resource.buffer, [f'{value:d} setpowerup'])

    def test_phaseares(self):
        self.resource.buffer = ['16', '17', '18']
        self.assertEqual(self.driver.phaseares, (16, 17, 18))
        self.assertEqual(self.resource.buffer, ['-1 getphaseares'])

    def test_mode(self):
        for value in 0, 1, False, True:
            self.resource.buffer = ['foo']
            self.driver.mode = value
            self.assertEqual(self.resource.buffer, [f'{value:d} mode', 'identify'])

    def test_ipadr(self):
        self.resource.buffer = ['192.168.1.2']
        self.assertEqual(self.driver.ipadr, '192.168.1.2')
        self.assertEqual(self.resource.buffer, ['getipadr'])

    def test_vel(self):
        for value in 0., 60., 90.:
            self.resource.buffer = [f'{value:.6f}']
            self.assertEqual(self.driver.vel, value)
            self.assertEqual(self.resource.buffer, ['getvel'])

            self.resource.buffer = []
            self.driver.vel = value
            self.assertEqual(self.resource.buffer, [f'{value:.6f} setvel'])

    def test_accel(self):
        for value in 0., 120., 200.:
            self.resource.buffer = [f'{value:.6f}']
            self.assertEqual(self.driver.accel, value)
            self.assertEqual(self.resource.buffer, ['getaccel'])

            self.resource.buffer = []
            self.driver.accel = value
            self.assertEqual(self.resource.buffer, [f'{value:.6f} setaccel'])

    def test_accelfunc(self):
        for value in 0, 1:
            self.resource.buffer = [f'{value:d}']
            self.assertEqual(self.driver.accelfunc, value)
            self.assertEqual(self.resource.buffer, ['getaccelfunc'])

            self.resource.buffer = []
            self.driver.accelfunc = value
            self.assertEqual(self.resource.buffer, [f'{value:d} setaccelfunc'])

    def test_manaccel(self):
        for value in 0., 100., 2400.:
            self.resource.buffer = [f'{value:.6f}']
            self.assertEqual(self.driver.manaccel, value)
            self.assertEqual(self.resource.buffer, ['getmanaccel'])

            self.resource.buffer = []
            self.driver.manaccel = value
            self.assertEqual(self.resource.buffer, [f'{value:.6f} setmanaccel'])

    def test_move(self):
        x, y, z = 2.01, 4.02, 0.03
        self.resource.buffer = []
        self.driver.move(x, y, z)
        self.assertEqual(self.resource.buffer, [f'{x:.6f} {y:.6f} {z:.6f} move'])

        self.resource.buffer = []
        self.driver.m(x, y, z)
        self.assertEqual(self.resource.buffer, [f'{x:.6f} {y:.6f} {z:.6f} move'])

    def test_rmove(self):
        x, y, z = 2.01, 4.02, 0.03
        self.resource.buffer = []
        self.driver.rmove(x, y, z)
        self.assertEqual(self.resource.buffer, [f'{x:.6f} {y:.6f} {z:.6f} rmove'])

        self.resource.buffer = []
        self.driver.r(x, y, z)
        self.assertEqual(self.resource.buffer, [f'{x:.6f} {y:.6f} {z:.6f} rmove'])

    def test_stopspeed(self):
        self.resource.buffer = []
        self.driver.stopspeed()
        self.assertEqual(self.resource.buffer, [f'stopspeed'])

    def test_randmove(self):
        self.resource.buffer = []
        self.driver.randmove()
        self.assertEqual(self.resource.buffer, [f'randmove'])

    def test_calibrate(self):
        self.resource.buffer = []
        self.driver.calibrate()
        self.assertEqual(self.resource.buffer, [f'calibrate'])

        self.resource.buffer = []
        self.driver.cal()
        self.assertEqual(self.resource.buffer, [f'calibrate'])

    def test_rangemeasure(self):
        self.resource.buffer = []
        self.driver.rangemeasure()
        self.assertEqual(self.resource.buffer, [f'rangemeasure'])

        self.resource.buffer = []
        self.driver.rm()
        self.assertEqual(self.resource.buffer, [f'rangemeasure'])

    def test_sw(self):
        self.resource.buffer = ['0 0 1 0 2 2']
        self.assertEqual(self.driver.sw, (0, 0, 1, 0, 2, 2))
        self.assertEqual(self.resource.buffer, ['-1 getsw'])

    def test_limit(self):
        self.resource.buffer = ['0.0 16383.0', '0.0 16383.0', '-16383.0 16383.0']
        self.assertEqual(self.driver.limit, ((0.0, 16383.0), (0.0, 16383.0), (-16383.0, 16383.0)))
        self.assertEqual(self.resource.buffer, ['getlimit'])

        self.resource.buffer = []
        self.driver.limit = (1, 2), (3, 4), (5, 6)
        self.assertEqual(self.resource.buffer, ['1.000000 3.000000 5.000000 2.000000 4.000000 6.000000 setlimit'])

    def test_abort(self):
        self.resource.buffer = []
        self.driver.abort()
        self.assertEqual(self.resource.buffer, ['abort'])

    def test_mp(self):
        self.resource.buffer = ['0 1 1']
        self.assertEqual(self.driver.mp, (0, 1, 1))
        self.assertEqual(self.resource.buffer, ['-1 getmp'])

    def test_pos(self):
        self.resource.buffer = ['1.000000 19.000000 0.000000']
        self.assertEqual(self.driver.pos, (1.0, 19.0, 0.0))
        self.assertEqual(self.resource.buffer, ['pos'])

        self.resource.buffer = []
        self.driver.pos = 1, 2, 3.005
        self.assertEqual(self.resource.buffer, ['1.000000 2.000000 3.005000 setpos'])

    def test_pdisplay(self):
        self.resource.buffer = ['10 5', '10 6', '10 7']
        self.assertEqual(self.driver.pdisplay, ((10, 5), (10, 6), (10, 7)))
        self.assertEqual(self.resource.buffer, ['-1 getpdisplay'])

    def test_align(self):
        self.resource.buffer = []
        self.driver.align(1, 2, 10, 11, axis=1)
        self.assertEqual(self.resource.buffer, ['1 2 10 11 1 align'])

    def test_reset_ico(self):
        self.resource.buffer = []
        self.driver.reset_ico()
        self.assertEqual(self.resource.buffer, ['ico'])

    def test_ico(self):
        self.resource.buffer = ['2']
        self.assertEqual(self.driver.ico, 2)
        self.assertEqual(self.resource.buffer, ['getico'])

    def test_status(self):
        self.resource.buffer = ['2']
        self.assertEqual(self.driver.status, 2)
        self.assertEqual(self.resource.buffer, ['status'])

    def test_error(self):
        self.resource.buffer = ['1004']
        self.assertEqual(self.driver.error, 1004)
        self.assertEqual(self.resource.buffer, ['geterror'])

    def test_merror(self):
        self.resource.buffer = ['0']
        self.assertEqual(self.driver.merror, 0)
        self.assertEqual(self.resource.buffer, ['getmerror'])

    def test_gsp(self):
        self.resource.buffer = ['2']
        self.assertEqual(self.driver.gsp, 2)
        self.assertEqual(self.resource.buffer, ['gsp'])

    def test_ticks(self):
        self.resource.buffer = ['22016079']
        self.assertEqual(self.driver.ticks, 22016079)
        self.assertEqual(self.resource.buffer, ['getticks'])

    def test_joystick(self):
        for value in 0, 1, False, True:
            self.resource.buffer = [f'{value:d}']
            self.assertEqual(self.driver.joystick, bool(value))
            self.assertEqual(self.resource.buffer, ['getjoystick'])

            self.resource.buffer = []
            self.driver.joystick = value
            self.assertEqual(self.resource.buffer, [f'{value:d} joystick'])

    def test_joyspeed(self):
        self.resource.buffer = ['20.000001']
        self.assertEqual(self.driver.joyspeed, 20.000001)
        self.assertEqual(self.resource.buffer, ['getjoyspeed'])

        self.resource.buffer = []
        self.driver.joyspeed = 20.000001
        self.assertEqual(self.resource.buffer, [f'20.000001 setjoyspeed'])

    def test_joybspeed(self):
        self.resource.buffer = ['0.123456']
        self.assertEqual(self.driver.joybspeed, .123456)
        self.assertEqual(self.resource.buffer, ['getjoybspeed'])

        self.resource.buffer = []
        self.driver.joybspeed = .123456
        self.assertEqual(self.resource.buffer, [f'0.123456 setjoybspeed'])

    def test_axis_pitch(self):
        self.resource.buffer = ['0.1', '0.2', '0.3']
        self.assertEqual(self.driver.x.pitch, .1)
        self.assertEqual(self.driver.y.pitch, .2)
        self.assertEqual(self.driver.z.pitch, .3)
        self.assertEqual(self.resource.buffer, ['1 getpitch', '2 getpitch', '3 getpitch'])

        self.resource.buffer = []
        self.driver.x.pitch = .3
        self.driver.y.pitch = .2
        self.driver.z.pitch = .1
        self.assertEqual(self.resource.buffer, ['0.300000 1 setpitch', '0.200000 2 setpitch', '0.100000 3 setpitch'])

    def test_axis_unit(self):
        for value in 0, 1, 2, 3, 4, 5, 6:
            self.resource.buffer = [format(value), format(value), format(value)]
            self.assertEqual(self.driver.x.unit, value)
            self.assertEqual(self.driver.y.unit, value)
            self.assertEqual(self.driver.z.unit, value)
            self.assertEqual(self.resource.buffer, ['1 getunit', '2 getunit', '3 getunit'])

            self.resource.buffer = []
            self.driver.x.unit = value
            self.driver.y.unit = value
            self.driver.z.unit = value
            self.assertEqual(self.resource.buffer, [f'{value:d} 1 setunit', f'{value:d} 2 setunit', f'{value:d} 3 setunit'])

    def test_axis_umotmin(self):
        for value in 0, 1850:
            self.resource.buffer = [format(value), format(value), format(value)]
            self.assertEqual(self.driver.x.umotmin, value)
            self.assertEqual(self.driver.y.umotmin, value)
            self.assertEqual(self.driver.z.umotmin, value)
            self.assertEqual(self.resource.buffer, ['1 getumotmin', '2 getumotmin', '3 getumotmin'])

            self.resource.buffer = []
            self.driver.x.umotmin = value
            self.driver.y.umotmin = value
            self.driver.z.umotmin = value
            self.assertEqual(self.resource.buffer, [f'{value:d} 1 setumotmin', f'{value:d} 2 setumotmin', f'{value:d} 3 setumotmin'])

    def test_axis_umotgrad(self):
        for value in 0, 55:
            self.resource.buffer = [format(value), format(value), format(value)]
            self.assertEqual(self.driver.x.umotgrad, value)
            self.assertEqual(self.driver.y.umotgrad, value)
            self.assertEqual(self.driver.z.umotgrad, value)
            self.assertEqual(self.resource.buffer, ['1 getumotgrad', '2 getumotgrad', '3 getumotgrad'])

            self.resource.buffer = []
            self.driver.x.umotgrad = value
            self.driver.y.umotgrad = value
            self.driver.z.umotgrad = value
            self.assertEqual(self.resource.buffer, [f'{value:d} 1 setumotgrad', f'{value:d} 2 setumotgrad', f'{value:d} 3 setumotgrad'])

    def test_axis_polepairs(self):
        for value in 50, 100:
            self.resource.buffer = [format(value), format(value), format(value)]
            self.assertEqual(self.driver.x.polepairs, value)
            self.assertEqual(self.driver.y.polepairs, value)
            self.assertEqual(self.driver.z.polepairs, value)
            self.assertEqual(self.resource.buffer, ['1 getpolepairs', '2 getpolepairs', '3 getpolepairs'])

            self.resource.buffer = []
            self.driver.x.polepairs = value
            self.driver.y.polepairs = value
            self.driver.z.polepairs = value
            self.assertEqual(self.resource.buffer, [f'{value:d} 1 setpolepairs', f'{value:d} 2 setpolepairs', f'{value:d} 3 setpolepairs'])

    def test_axis_enabled(self):
        for value in 0, 1, 2, 3, 4:
            self.resource.buffer = [format(value), format(value), format(value)]
            self.assertEqual(self.driver.x.enabled, value)
            self.assertEqual(self.driver.y.enabled, value)
            self.assertEqual(self.driver.z.enabled, value)
            self.assertEqual(self.resource.buffer, ['1 getaxis', '2 getaxis', '3 getaxis'])

            self.resource.buffer = []
            self.driver.x.enabled = value
            self.driver.y.enabled = value
            self.driver.z.enabled = value
            self.assertEqual(self.resource.buffer, [f'{value:d} 1 setaxis', f'{value:d} 2 setaxis', f'{value:d} 3 setaxis'])

    def test_axis_phaseares(self):
        for value in 2, 16:
            self.resource.buffer = [format(value), format(value), format(value)]
            self.assertEqual(self.driver.x.phaseares, value)
            self.assertEqual(self.driver.y.phaseares, value)
            self.assertEqual(self.driver.z.phaseares, value)
            self.assertEqual(self.resource.buffer, ['1 getphaseares', '2 getphaseares', '3 getphaseares'])

            self.resource.buffer = []
            self.driver.x.phaseares = value
            self.driver.y.phaseares = value
            self.driver.z.phaseares = value
            self.assertEqual(self.resource.buffer, [f'{value:d} 1 setphaseares', f'{value:d} 2 setphaseares', f'{value:d} 3 setphaseares'])

    def test_axis_motiondir(self):
        for value in 0, 1:
            self.resource.buffer = [format(value), format(value), format(value)]
            self.assertEqual(self.driver.x.motiondir, value)
            self.assertEqual(self.driver.y.motiondir, value)
            self.assertEqual(self.driver.z.motiondir, value)
            self.assertEqual(self.resource.buffer, ['1 getmotiondir', '2 getmotiondir', '3 getmotiondir'])

            self.resource.buffer = []
            self.driver.x.motiondir = value
            self.driver.y.motiondir = value
            self.driver.z.motiondir = value
            self.assertEqual(self.resource.buffer, [f'{value:d} 1 setmotiondir', f'{value:d} 2 setmotiondir', f'{value:d} 3 setmotiondir'])

    def test_axis_speed(self):
        self.resource.buffer = []
        self.driver.x.speed(-0.1)
        self.driver.y.speed(-0.2)
        self.driver.z.speed(-0.3)
        self.assertEqual(self.resource.buffer, [f'{-.1:.6f} 1 speed', f'{-.2:.6f} 2 speed', f'{-.3:.6f} 3 speed'])

    def test_axis_test(self):
        self.resource.buffer = []
        self.driver.x.test(10)
        self.driver.y.test(11)
        self.driver.z.test(12)
        self.assertEqual(self.resource.buffer, [f'{10:.6f} 1 test', f'{11:.6f} 2 test', f'{12:.6f} 3 test'])

    def test_axis_caldone(self):
        self.resource.buffer = ['1', '0', '1']
        self.assertEqual(self.driver.x.caldone, 1)
        self.assertEqual(self.driver.y.caldone, 0)
        self.assertEqual(self.driver.z.caldone, 1)
        self.assertEqual(self.resource.buffer, ['1 getcaldone', '2 getcaldone', '3 getcaldone'])

    def test_axis_sw(self):
        self.resource.buffer = ['1 2', '2 1', '1 0']
        self.assertEqual(self.driver.x.sw, (1, 2))
        self.assertEqual(self.driver.y.sw, (2, 1))
        self.assertEqual(self.driver.z.sw, (1, 0))
        self.assertEqual(self.resource.buffer, ['1 getsw', '2 getsw', '3 getsw'])

    def test_calswdist(self):
        for value in 0., 1.:
            self.resource.buffer = [f'{value:.6f}', f'{value:.6f}', f'{value:.6f}']
            self.assertEqual(self.driver.x.calswdist, value)
            self.assertEqual(self.driver.y.calswdist, value)
            self.assertEqual(self.driver.z.calswdist, value)
            self.assertEqual(self.resource.buffer, ['1 getcalswdist', '2 getcalswdist', '3 getcalswdist'])

            self.resource.buffer = []
            self.driver.x.calswdist = value
            self.driver.y.calswdist = value
            self.driver.z.calswdist = value
            self.assertEqual(self.resource.buffer, [f'{value:.6f} 1 setcalswdist', f'{value:.6f} 2 setcalswdist', f'{value:.6f} 3 setcalswdist'])

    def test_ncal(self):
        self.resource.buffer = []
        self.driver.x.ncal()
        self.driver.y.ncal()
        self.driver.z.ncal()
        self.assertEqual(self.resource.buffer, ['1 ncal', '2 ncal', '3 ncal'])

    def test_nrm(self):
        self.resource.buffer = []
        self.driver.x.nrm()
        self.driver.y.nrm()
        self.driver.z.nrm()
        self.assertEqual(self.resource.buffer, ['1 nrm', '2 nrm', '3 nrm'])

    def test_nlimit(self):
        self.resource.buffer = ['0 1', '2 3', '4 5']
        self.assertEqual(self.driver.x.nlimit, (0., 1.))
        self.assertEqual(self.driver.y.nlimit, (2., 3.))
        self.assertEqual(self.driver.z.nlimit, (4., 5.))
        self.assertEqual(self.resource.buffer, ['1 getnlimit', '2 getnlimit', '3 getnlimit'])

    def test_axis_mp(self):
        for value in 0, 1:
            self.resource.buffer = [format(value), format(value), format(value)]
            self.assertEqual(self.driver.x.mp, value)
            self.assertEqual(self.driver.y.mp, value)
            self.assertEqual(self.driver.z.mp, value)
            self.assertEqual(self.resource.buffer, ['1 getmp', '2 getmp', '3 getmp'])

            self.resource.buffer = []
            self.driver.x.mp = value
            self.driver.y.mp = value
            self.driver.z.mp = value
            self.assertEqual(self.resource.buffer, [f'{value:d} 1 setmp', f'{value:d} 2 setmp', f'{value:d} 3 setmp'])

    def test_axis_joyspeed(self):
        value = 20.0
        self.resource.buffer = [format(value), format(value), format(value)]
        self.assertEqual(self.driver.x.joyspeed, value)
        self.assertEqual(self.driver.y.joyspeed, value)
        self.assertEqual(self.driver.z.joyspeed, value)
        self.assertEqual(self.resource.buffer, ['1 getnjoyspeed', '2 getnjoyspeed', '3 getnjoyspeed'])

        self.resource.buffer = []
        self.driver.x.joyspeed = value
        self.driver.y.joyspeed = value
        self.driver.z.joyspeed = value
        self.assertEqual(self.resource.buffer, [f'{value:.6f} 1 setnjoyspeed', f'{value:.6f} 2 setnjoyspeed', f'{value:.6f} 3 setnjoyspeed'])

    def test_system(self):
        self.resource.buffer = []
        self.driver.system.save()
        self.assertEqual(self.resource.buffer, ['save'])

        self.resource.buffer = []
        self.driver.system.restore()
        self.assertEqual(self.resource.buffer, ['restore'])

        self.resource.buffer = []
        self.driver.system.fpara()
        self.assertEqual(self.resource.buffer, ['getfpara'])

        self.resource.buffer = []
        self.driver.system.clear()
        self.assertEqual(self.resource.buffer, ['clear'])

        self.resource.buffer = []
        self.driver.system.reset()
        self.assertEqual(self.resource.buffer, ['reset'])

        self.resource.buffer = []
        self.driver.system.beep(1001)
        self.assertEqual(self.resource.buffer, ['1001 beep'])

        self.resource.buffer = ['1.42']
        self.assertEqual(self.driver.system.version, '1.42')
        self.assertEqual(self.resource.buffer, ['version'])

        self.resource.buffer = ['00:50:C2:10:91:91']
        self.assertEqual(self.driver.system.macadr, '00:50:C2:10:91:91')
        self.assertEqual(self.resource.buffer, ['getmacadr'])

        self.resource.buffer = ['Corvus 1 462 1 380']
        self.assertEqual(self.driver.system.identify, 'Corvus 1 462 1 380')
        self.assertEqual(self.resource.buffer, ['identify'])

        self.resource.buffer = ['8']
        self.assertEqual(self.driver.system.options, 8)
        self.assertEqual(self.resource.buffer, ['getoptions'])

        self.resource.buffer = ['19091234']
        self.assertEqual(self.driver.system.serialno, '19091234')
        self.assertEqual(self.resource.buffer, ['getserialno'])
