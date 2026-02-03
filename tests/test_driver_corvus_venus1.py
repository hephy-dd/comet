import pytest

from comet.driver.corvus import Venus1


@pytest.fixture
def driver(resource):
    return Venus1(resource)


def test_driver(driver):
    assert driver.X_AXIS == 1
    assert driver.Y_AXIS == 2
    assert driver.Z_AXIS == 3


def test_identification(driver, resource):
    resource.buffer = ["Corvus 1 462 1 380", "1.42", "19091234"]
    assert driver.identification == "Corvus 1.42 19091234"
    assert resource.buffer == ["identify", "version", "getserialno"]


def test_pitch(driver, resource):
    resource.buffer = ["2", "2", "2", "1"]
    assert driver.pitch == (2.0, 2.0, 2.0, 1.0)
    assert resource.buffer == ["-1 getpitch"]


def test_dim(driver, resource):
    for value in 1, 2, 3:
        resource.buffer = [format(value)]
        assert driver.dim == value
        assert resource.buffer == ["getdim"]

        resource.buffer = []
        driver.dim = value
        assert resource.buffer == [f"{value:d} setdim"]


def test_unit(driver, resource):
    resource.buffer = ["2 1 1 1"]
    assert driver.unit == (2, 1, 1, 1)
    assert resource.buffer == ["-1 getunit"]


def test_umotmin(driver, resource):
    resource.buffer = ["1850", "1851", "1852"]
    assert driver.umotmin == (1850, 1851, 1852)
    assert resource.buffer == ["-1 getumotmin"]


def test_umotgrad(driver, resource):
    resource.buffer = ["55", "56", "57"]
    assert driver.umotgrad == (55, 56, 57)
    assert resource.buffer == ["-1 getumotgrad"]


def test_polepairs(driver, resource):
    resource.buffer = ["50", "51", "52"]
    assert driver.polepairs == (50, 51, 52)
    assert resource.buffer == ["-1 getpolepairs"]


def test_axes(driver, resource):
    resource.buffer = ["1 1 0"]
    assert driver.axes == (1, 1, 0)
    assert resource.buffer == ["-1 getaxis"]


def test_powerup(driver, resource):
    for value in 0, 1, False, True:
        resource.buffer = [f"{value:d}"]
        assert driver.powerup == int(value)
        assert resource.buffer == ["getpowerup"]

        resource.buffer = []
        driver.powerup = value
        assert resource.buffer == [f"{value:d} setpowerup"]


def test_phaseares(driver, resource):
    resource.buffer = ["16", "17", "18"]
    assert driver.phaseares == (16, 17, 18)
    assert resource.buffer == ["-1 getphaseares"]


def test_mode(driver, resource):
    for value in 0, 1, False, True:
        resource.buffer = ["foo"]
        driver.mode = value
        assert resource.buffer == [f"{value:d} mode", "identify"]


def test_ipadr(driver, resource):
    resource.buffer = ["192.168.1.2"]
    assert driver.ipadr == "192.168.1.2"
    assert resource.buffer == ["getipadr"]


def test_vel(driver, resource):
    for value in 0., 60., 90.:
        resource.buffer = [f"{value:.6f}"]
        assert driver.vel == value
        assert resource.buffer == ["getvel"]

        resource.buffer = []
        driver.vel = value
        assert resource.buffer == [f"{value:.6f} setvel"]


def test_accel(driver, resource):
    for value in 0., 120., 200.:
        resource.buffer = [f"{value:.6f}"]
        assert driver.accel == value
        assert resource.buffer == ["getaccel"]

        resource.buffer = []
        driver.accel = value
        assert resource.buffer == [f"{value:.6f} setaccel"]


def test_accelfunc(driver, resource):
    for value in 0, 1:
        resource.buffer = [f"{value:d}"]
        assert driver.accelfunc == value
        assert resource.buffer == ["getaccelfunc"]

        resource.buffer = []
        driver.accelfunc = value
        assert resource.buffer == [f"{value:d} setaccelfunc"]


def test_manaccel(driver, resource):
    for value in 0., 100., 2400.:
        resource.buffer = [f"{value:.6f}"]
        assert driver.manaccel == value
        assert resource.buffer == ["getmanaccel"]

        resource.buffer = []
        driver.manaccel = value
        assert resource.buffer == [f"{value:.6f} setmanaccel"]


def test_move(driver, resource):
    x, y, z = 2.01, 4.02, 0.03
    resource.buffer = []
    driver.move(x, y, z)
    assert resource.buffer == [f"{x:.6f} {y:.6f} {z:.6f} move"]

    resource.buffer = []
    driver.m(x, y, z)
    assert resource.buffer == [f"{x:.6f} {y:.6f} {z:.6f} move"]


def test_rmove(driver, resource):
    x, y, z = 2.01, 4.02, 0.03
    resource.buffer = []
    driver.rmove(x, y, z)
    assert resource.buffer == [f"{x:.6f} {y:.6f} {z:.6f} rmove"]

    resource.buffer = []
    driver.r(x, y, z)
    assert resource.buffer == [f"{x:.6f} {y:.6f} {z:.6f} rmove"]


def test_stopspeed(driver, resource):
    resource.buffer = []
    driver.stopspeed()
    assert resource.buffer == ["stopspeed"]


def test_randmove(driver, resource):
    resource.buffer = []
    driver.randmove()
    assert resource.buffer == ["randmove"]


def test_calibrate(driver, resource):
    resource.buffer = []
    driver.calibrate()
    assert resource.buffer == ["calibrate"]

    resource.buffer = []
    driver.cal()
    assert resource.buffer == ["calibrate"]


def test_rangemeasure(driver, resource):
    resource.buffer = []
    driver.rangemeasure()
    assert resource.buffer == ["rangemeasure"]

    resource.buffer = []
    driver.rm()
    assert resource.buffer == ["rangemeasure"]


def test_sw(driver, resource):
    resource.buffer = ["0 0 1 0 2 2"]
    assert driver.sw == (0, 0, 1, 0, 2, 2)
    assert resource.buffer == ["-1 getsw"]


def test_limit(driver, resource):
    resource.buffer = ["0.0 16383.0", "0.0 16383.0", "-16383.0 16383.0"]
    assert driver.limit == ((0.0, 16383.0), (0.0, 16383.0), (-16383.0, 16383.0))
    assert resource.buffer == ["getlimit"]

    resource.buffer = []
    driver.limit = (1, 2), (3, 4), (5, 6)
    assert resource.buffer == ["1.000000 3.000000 5.000000 2.000000 4.000000 6.000000 setlimit"]


def test_abort(driver, resource):
    resource.buffer = []
    driver.abort()
    assert resource.buffer == ["abort"]


def test_mp(driver, resource):
    resource.buffer = ["0 1 1"]
    assert driver.mp == (0, 1, 1)
    assert resource.buffer == ["-1 getmp"]


def test_pos(driver, resource):
    resource.buffer = ["1.000000 19.000000 0.000000"]
    assert driver.pos == (1.0, 19.0, 0.0)
    assert resource.buffer == ["pos"]

    resource.buffer = []
    driver.pos = 1, 2, 3.005
    assert resource.buffer == ["1.000000 2.000000 3.005000 setpos"]


def test_pdisplay(driver, resource):
    resource.buffer = ["10 5", "10 6", "10 7"]
    assert driver.pdisplay == ((10, 5), (10, 6), (10, 7))
    assert resource.buffer == ["-1 getpdisplay"]


def test_align(driver, resource):
    resource.buffer = []
    driver.align(1, 2, 10, 11, axis=1)
    assert resource.buffer == ["1 2 10 11 1 align"]


def test_reset_ico(driver, resource):
    resource.buffer = []
    driver.reset_ico()
    assert resource.buffer == ["ico"]


def test_ico(driver, resource):
    resource.buffer = ["2"]
    assert driver.ico == 2
    assert resource.buffer == ["getico"]


def test_status(driver, resource):
    resource.buffer = ["2"]
    assert driver.status == 2
    assert resource.buffer == ["status"]


def test_error(driver, resource):
    resource.buffer = ["1004"]
    assert driver.error == 1004
    assert resource.buffer == ["geterror"]


def test_merror(driver, resource):
    resource.buffer = ["0"]
    assert driver.merror == 0
    assert resource.buffer == ["getmerror"]


def test_gsp(driver, resource):
    resource.buffer = ["2"]
    assert driver.gsp == 2
    assert resource.buffer == ["gsp"]


def test_ticks(driver, resource):
    resource.buffer = ["22016079"]
    assert driver.ticks == 22016079
    assert resource.buffer == ["getticks"]


def test_joystick(driver, resource):
    for value in 0, 1, False, True:
        resource.buffer = [f"{value:d}"]
        assert driver.joystick == bool(value)
        assert resource.buffer == ["getjoystick"]

        resource.buffer = []
        driver.joystick = value
        assert resource.buffer == [f"{value:d} joystick"]


def test_joyspeed(driver, resource):
    resource.buffer = ["20.000001"]
    assert driver.joyspeed == 20.000001
    assert resource.buffer == ["getjoyspeed"]

    resource.buffer = []
    driver.joyspeed = 20.000001
    assert resource.buffer == ["20.000001 setjoyspeed"]


def test_joybspeed(driver, resource):
    resource.buffer = ["0.123456"]
    assert driver.joybspeed == .123456
    assert resource.buffer == ["getjoybspeed"]

    resource.buffer = []
    driver.joybspeed = .123456
    assert resource.buffer == ["0.123456 setjoybspeed"]


def test_axis_pitch(driver, resource):
    resource.buffer = ["0.1", "0.2", "0.3"]
    assert driver.x.pitch == .1
    assert driver.y.pitch == .2
    assert driver.z.pitch == .3
    assert resource.buffer == ["1 getpitch", "2 getpitch", "3 getpitch"]

    resource.buffer = []
    driver.x.pitch = .3
    driver.y.pitch = .2
    driver.z.pitch = .1
    assert resource.buffer == ["0.300000 1 setpitch", "0.200000 2 setpitch", "0.100000 3 setpitch"]


def test_axis_unit(driver, resource):
    for value in 0, 1, 2, 3, 4, 5, 6:
        resource.buffer = [format(value), format(value), format(value)]
        assert driver.x.unit == value
        assert driver.y.unit == value
        assert driver.z.unit == value
        assert resource.buffer == ["1 getunit", "2 getunit", "3 getunit"]

        resource.buffer = []
        driver.x.unit = value
        driver.y.unit = value
        driver.z.unit = value
        assert resource.buffer == [f"{value:d} 1 setunit", f"{value:d} 2 setunit", f"{value:d} 3 setunit"]


def test_axis_umotmin(driver, resource):
    for value in 0, 1850:
        resource.buffer = [format(value), format(value), format(value)]
        assert driver.x.umotmin == value
        assert driver.y.umotmin == value
        assert driver.z.umotmin == value
        assert resource.buffer == ["1 getumotmin", "2 getumotmin", "3 getumotmin"]

        resource.buffer = []
        driver.x.umotmin = value
        driver.y.umotmin = value
        driver.z.umotmin = value
        assert resource.buffer == [f"{value:d} 1 setumotmin", f"{value:d} 2 setumotmin", f"{value:d} 3 setumotmin"]


def test_axis_umotgrad(driver, resource):
    for value in 0, 55:
        resource.buffer = [format(value), format(value), format(value)]
        assert driver.x.umotgrad == value
        assert driver.y.umotgrad == value
        assert driver.z.umotgrad == value
        assert resource.buffer == ["1 getumotgrad", "2 getumotgrad", "3 getumotgrad"]

        resource.buffer = []
        driver.x.umotgrad = value
        driver.y.umotgrad = value
        driver.z.umotgrad = value
        assert resource.buffer == [f"{value:d} 1 setumotgrad", f"{value:d} 2 setumotgrad", f"{value:d} 3 setumotgrad"]


def test_axis_polepairs(driver, resource):
    for value in 50, 100:
        resource.buffer = [format(value), format(value), format(value)]
        assert driver.x.polepairs == value
        assert driver.y.polepairs == value
        assert driver.z.polepairs == value
        assert resource.buffer == ["1 getpolepairs", "2 getpolepairs", "3 getpolepairs"]

        resource.buffer = []
        driver.x.polepairs = value
        driver.y.polepairs = value
        driver.z.polepairs = value
        assert resource.buffer == [f"{value:d} 1 setpolepairs", f"{value:d} 2 setpolepairs", f"{value:d} 3 setpolepairs"]


def test_axis_enabled(driver, resource):
    for value in 0, 1, 2, 3, 4:
        resource.buffer = [format(value), format(value), format(value)]
        assert driver.x.enabled == value
        assert driver.y.enabled == value
        assert driver.z.enabled == value
        assert resource.buffer == ["1 getaxis", "2 getaxis", "3 getaxis"]

        resource.buffer = []
        driver.x.enabled = value
        driver.y.enabled = value
        driver.z.enabled = value
        assert resource.buffer == [f"{value:d} 1 setaxis", f"{value:d} 2 setaxis", f"{value:d} 3 setaxis"]


def test_axis_phaseares(driver, resource):
    for value in 2, 16:
        resource.buffer = [format(value), format(value), format(value)]
        assert driver.x.phaseares == value
        assert driver.y.phaseares == value
        assert driver.z.phaseares == value
        assert resource.buffer == ["1 getphaseares", "2 getphaseares", "3 getphaseares"]

        resource.buffer = []
        driver.x.phaseares = value
        driver.y.phaseares = value
        driver.z.phaseares = value
        assert resource.buffer == [f"{value:d} 1 setphaseares", f"{value:d} 2 setphaseares", f"{value:d} 3 setphaseares"]


def test_axis_motiondir(driver, resource):
    for value in 0, 1:
        resource.buffer = [format(value), format(value), format(value)]
        assert driver.x.motiondir == value
        assert driver.y.motiondir == value
        assert driver.z.motiondir == value
        assert resource.buffer == ["1 getmotiondir", "2 getmotiondir", "3 getmotiondir"]

        resource.buffer = []
        driver.x.motiondir = value
        driver.y.motiondir = value
        driver.z.motiondir = value
        assert resource.buffer == [f"{value:d} 1 setmotiondir", f"{value:d} 2 setmotiondir", f"{value:d} 3 setmotiondir"]


def test_axis_speed(driver, resource):
    resource.buffer = []
    driver.x.speed(-0.1)
    driver.y.speed(-0.2)
    driver.z.speed(-0.3)
    assert resource.buffer == [f"{-.1:.6f} 1 speed", f"{-.2:.6f} 2 speed", f"{-.3:.6f} 3 speed"]


def test_axis_test(driver, resource):
    resource.buffer = []
    driver.x.test(10)
    driver.y.test(11)
    driver.z.test(12)
    assert resource.buffer == [f"{10:.6f} 1 test", f"{11:.6f} 2 test", f"{12:.6f} 3 test"]


def test_axis_caldone(driver, resource):
    resource.buffer = ["1", "0", "1"]
    assert driver.x.caldone == 1
    assert driver.y.caldone == 0
    assert driver.z.caldone == 1
    assert resource.buffer == ["1 getcaldone", "2 getcaldone", "3 getcaldone"]


def test_axis_sw(driver, resource):
    resource.buffer = ["1 2", "2 1", "1 0"]
    assert driver.x.sw == (1, 2)
    assert driver.y.sw == (2, 1)
    assert driver.z.sw == (1, 0)
    assert resource.buffer == ["1 getsw", "2 getsw", "3 getsw"]


def test_calswdist(driver, resource):
    for value in 0., 1.:
        resource.buffer = [f"{value:.6f}", f"{value:.6f}", f"{value:.6f}"]
        assert driver.x.calswdist == value
        assert driver.y.calswdist == value
        assert driver.z.calswdist == value
        assert resource.buffer == ["1 getcalswdist", "2 getcalswdist", "3 getcalswdist"]

        resource.buffer = []
        driver.x.calswdist = value
        driver.y.calswdist = value
        driver.z.calswdist = value
        assert resource.buffer == [f"{value:.6f} 1 setcalswdist", f"{value:.6f} 2 setcalswdist", f"{value:.6f} 3 setcalswdist"]


def test_ncal(driver, resource):
    resource.buffer = []
    driver.x.ncal()
    driver.y.ncal()
    driver.z.ncal()
    assert resource.buffer == ["1 ncal", "2 ncal", "3 ncal"]


def test_nrm(driver, resource):
    resource.buffer = []
    driver.x.nrm()
    driver.y.nrm()
    driver.z.nrm()
    assert resource.buffer == ["1 nrm", "2 nrm", "3 nrm"]


def test_nlimit(driver, resource):
    resource.buffer = ["0 1", "2 3", "4 5"]
    assert driver.x.nlimit == (0., 1.)
    assert driver.y.nlimit == (2., 3.)
    assert driver.z.nlimit == (4., 5.)
    assert resource.buffer == ["1 getnlimit", "2 getnlimit", "3 getnlimit"]


def test_axis_mp(driver, resource):
    for value in 0, 1:
        resource.buffer = [format(value), format(value), format(value)]
        assert driver.x.mp == value
        assert driver.y.mp == value
        assert driver.z.mp == value
        assert resource.buffer == ["1 getmp", "2 getmp", "3 getmp"]

        resource.buffer = []
        driver.x.mp = value
        driver.y.mp = value
        driver.z.mp = value
        assert resource.buffer == [f"{value:d} 1 setmp", f"{value:d} 2 setmp", f"{value:d} 3 setmp"]


def test_axis_joyspeed(driver, resource):
    value = 20.0
    resource.buffer = [format(value), format(value), format(value)]
    assert driver.x.joyspeed == value
    assert driver.y.joyspeed == value
    assert driver.z.joyspeed == value
    assert resource.buffer == ["1 getnjoyspeed", "2 getnjoyspeed", "3 getnjoyspeed"]

    resource.buffer = []
    driver.x.joyspeed = value
    driver.y.joyspeed = value
    driver.z.joyspeed = value
    assert resource.buffer == [f"{value:.6f} 1 setnjoyspeed", f"{value:.6f} 2 setnjoyspeed", f"{value:.6f} 3 setnjoyspeed"]


def test_system(driver, resource):
    resource.buffer = []
    driver.system.save()
    assert resource.buffer == ["save"]

    resource.buffer = []
    driver.system.restore()
    assert resource.buffer == ["restore"]

    resource.buffer = []
    driver.system.fpara()
    assert resource.buffer == ["getfpara"]

    resource.buffer = []
    driver.system.clear()
    assert resource.buffer == ["clear"]

    resource.buffer = []
    driver.system.reset()
    assert resource.buffer == ["reset"]

    resource.buffer = []
    driver.system.beep(1001)
    assert resource.buffer == ["1001 beep"]

    resource.buffer = ["1.42"]
    assert driver.system.version == "1.42"
    assert resource.buffer == ["version"]

    resource.buffer = ["00:50:C2:10:91:91"]
    assert driver.system.macadr == "00:50:C2:10:91:91"
    assert resource.buffer == ["getmacadr"]

    resource.buffer = ["Corvus 1 462 1 380"]
    assert driver.system.identify == "Corvus 1 462 1 380"
    assert resource.buffer == ["identify"]

    resource.buffer = ["8"]
    assert driver.system.options == 8
    assert resource.buffer == ["getoptions"]

    resource.buffer = ["19091234"]
    assert driver.system.serialno == "19091234"
    assert resource.buffer == ["getserialno"]
