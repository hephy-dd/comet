import random

from comet.emulator import Emulator
from comet.emulator import message, run
from comet.utils import t_dew


def format_error(code: int) -> str:
    return f"Err{abs(code):d}"


class EnvironBoxEmulator(Emulator):

    IDENTITY = "EnvironBox, v1.0 (Emulator)"
    SUCCESS = "OK"
    PC_DATA_SIZE = 39
    SENSOR_ADRESSES = [40, 41, 42, 43, 44, 45]

    def __init__(self):
        super().__init__()
        self.sensor_address: int = 40
        self.discharge: str = "OFF"
        self.sensor_count: int = 2

        self.laser_sensor: bool = False
        self.box_light: bool = False
        self.microscope_control: bool = False
        self.microscope_light: bool = False
        self.microscope_camera: bool = False
        self.probecard_light: bool = False
        self.probecard_camera: bool = False
        self.discharge_time: bool = 1000

        self.door_open: bool = False
        self.laser_enabled: bool = False
        self.safety_alert: bool = False

        self.test_led: bool = False
        self.pt100_1_enabled: bool = True
        self.pt100_2_enabled: bool = False
        self.pid_control: bool = False
        self.pid_control_mode = "HUM"
        self.pid_setpoints = {"HUM": 30., "DEW": 30.}
        self.pid_kp: float = 0.25
        self.pid_ki: float = 0.01
        self.pid_kd: float = 1.23
        self.pid_kp2: float = 22.4
        self.pid_ki2: float = 1.25
        self.pid_kd2: float = 3.56
        self.pid_min: int = 10
        self.pid_max: int = 560
        self.pid_sample_time: int = 100
        self.pid_drop_mode: str = "M"
        self.pid_threshold: int = 0
        self.parameter_set: int = 1
        self.parameter_threshold: float = 25.5
        self.dac: int = 25

        # self.env_ii_pcb = False
        # self.factory_default = False
        # self.clear_log = False

    @property
    def box_temperature(self) -> float:
        minimum = float(self.options.get("box_temperature.min", 24.0))
        maximum = float(self.options.get("box_temperature.max", 24.5))
        return round(random.uniform(minimum, maximum), 1)

    @property
    def box_humidity(self) -> float:
        minimum = float(self.options.get("box_humidity.min", 40.0))
        maximum = float(self.options.get("box_humidity.max", 40.5))
        return round(random.uniform(minimum, maximum), 1)

    @property
    def box_dewpoint(self) -> float:
        return round(t_dew(self.box_temperature, self.box_humidity), 2)

    @property
    def pid_setpoint(self) -> float:
        return self.pid_setpoints[self.pid_control_mode]

    @pid_setpoint.setter
    def pid_setpoint(self, value: float) -> None:
        self.pid_setpoints[self.pid_control_mode] = value

    @property
    def pt100_1(self) -> float:
        if self.pt100_1_enabled:
            minimum = float(self.options.get("pt100_1.min", 21.0))
            maximum = float(self.options.get("pt100_1.max", 21.5))
            return round(random.uniform(minimum, maximum), 1)
        return float("nan")

    @property
    def pt100_2(self) -> float:
        if self.pt100_2_enabled:
            minimum = float(self.options.get("pt100_2.min", 22.0))
            maximum = float(self.options.get("pt100_2.max", 22.5))
            return round(random.uniform(minimum, maximum), 1)
        return float("nan")

    @property
    def box_lux(self) -> float:
        lux: float = 0.0
        if self.box_light:
            lux += random.uniform(0.40, 0.42)
        if self.probecard_light:
            lux += random.uniform(0.1, 0.12)
        if self.microscope_light:
            lux += random.uniform(0.2, 0.22)
        return lux

    def power_relay_states(self) -> int:
        power_relay_states: int = 0
        if self.microscope_control:
            power_relay_states |= 1 << 0
        if self.box_light:
            power_relay_states |= 1 << 1
        if self.probecard_light:
            power_relay_states |= 1 << 2
        if self.laser_sensor:
            power_relay_states |= 1 << 3
        if self.probecard_camera:
            power_relay_states |= 1 << 4
        if self.microscope_camera:
            power_relay_states |= 1 << 5
        if self.microscope_light:
            power_relay_states |= 1 << 6
        return power_relay_states

    def create_pc_data(self):
        pc_data = ["0"] * type(self).PC_DATA_SIZE
        pc_data[0] = format(self.sensor_count, "d")
        pc_data[1] = format(self.box_humidity, ".1F")
        pc_data[2] = format(self.box_temperature, ".1F")
        pc_data[3] = format(self.box_dewpoint, ".2F")
        pc_data[4] = format(self.pid_control, "d")
        pc_data[5] = format(self.pid_setpoint, ".1F")
        pc_data[6] = format(0, ".1F")
        pc_data[7] = format(0, ".2F")
        pc_data[8] = format(self.pid_kp, ".6F")
        pc_data[9] = format(self.pid_ki, ".6F")
        pc_data[10] = format(self.pid_kd, ".6F")
        pc_data[11] = format(0, ".2F")
        pc_data[12] = format(0, ".2F")
        pc_data[13] = "1"  # format(self.pid_control_mode)  # TODO
        pc_data[14] = format(self.pid_kp2, ".6F")
        pc_data[15] = format(self.pid_ki2, ".6F")
        pc_data[16] = format(self.pid_kd2, ".6F")
        pc_data[17] = "1"
        pc_data[18] = format(0, ".2F")
        pc_data[20] = format(0, ".2F")
        pc_data[21] = format(0, ".2F")
        pc_data[23] = format(self.power_relay_states(), "d")
        pc_data[24] = format(self.box_light, "d")
        pc_data[25] = format(self.door_open, "d")
        pc_data[26] = format(self.safety_alert, "d")
        pc_data[30] = format(self.test_led, "d")
        pc_data[31] = format(self.discharge_time, "d")
        pc_data[32] = format(self.box_lux, ".1F")
        pc_data[33] = format(self.pt100_1, ".2F")
        pc_data[34] = format(self.pt100_2, ".2F")
        pc_data[36] = format(self.pid_sample_time, "d")
        pc_data[36] = "1"  # format(self.pid_drop_mode)  # TODO
        pc_data[37] = format(self.pt100_1_enabled, "d")
        pc_data[38] = format(self.pt100_2_enabled, "d")
        return pc_data

    @message(r"\*IDN\?")
    def get_idn(self):
        return type(self).IDENTITY

    # @message(r"\*RST")
    # def set_reset(self):
    #     return self.SUCCESS

    # @message(r"\*CLS")
    # def set_clear(self):
    #     return self.SUCCESS

    @message(r"SET:NEW_ADDR (\d+)")
    def set_new_addr(self, address):
        value = int(address)
        if value not in type(self).SENSOR_ADRESSES:
            return format_error(14)
        self.sensor_address = value
        return self.SUCCESS

    @message(r"SET:TEST_LED (ON|OFF)")
    def set_test_led(self, value) -> str:
        self.test_led = value == "ON"
        return self.SUCCESS

    @message(r"GET:TEST_LED \?")
    def get_test_led(self) -> str:
        return {True: "1", False: "0"}[self.test_led]

    @message(r"SET:DISCHARGE (AUTO|ON|OFF)")
    def set_discharge(self, state):
        self.discharge = state
        return self.SUCCESS

    @message(r"SET:DISCHARGE_TIME (\d+)")
    def set_discharge_time(self, seconds):
        seconds = int(seconds)
        if 0 <= seconds <= 9999:
            self.discharge_time = seconds
            return self.SUCCESS
        return format_error(44)

    @message(r"GET:DISCHARGE_TIME \?")
    def get_discharge_time(self):
        return format(self.discharge_time)

    @message(r"SET:PT100_1 (ON|OFF)")
    def set_pt100_1(self, value):
        self.pt100_1_enabled = value == "ON"
        return self.SUCCESS

    @message(r"GET:PT100_1 \?")
    def get_pt100_1(self):
        return format(self.pt100_1, ".2F")

    @message(r"SET:PT100_2 (ON|OFF)")
    def set_pt100_2(self, value):
        self.pt100_2_enabled = value == "ON"
        return self.SUCCESS

    @message(r"GET:PT100_2 \?")
    def get_pt100_2(self):
        return format(self.pt100_2, ".2F")

    @message(r"SET:CTRL (ON|OFF)")
    def set_ctrl(self, value):
        self.pid_control = value == "ON"
        return self.SUCCESS

    @message(r"GET:CTRL \?")
    def get_ctrl(self):
        return "1" if self.pid_control else "0"

    @message(r"SET:CTRL_MODE (HUM|DEW)")
    def set_ctrl_mode(self, mode):
        self.pid_control_mode = mode
        return self.SUCCESS

    @message(r"SET:SETPOINT (.+)")
    def set_setpoint(self, setpoint):
        try:
            self.pid_setpoint = float(setpoint)
        except Exception:
            return format_error(30)
        return self.SUCCESS

    @message(r"GET:SETPOINT \?")
    def get_setpoint(self):
        return format(self.pid_setpoint, ".2F")

    @message(r"SET:PID_KP (.+)")
    def set_pid_kp(self, value):
        try:
            self.pid_kp = float(value)
        except Exception:
            return format_error(31)
        return self.SUCCESS

    @message(r"GET:PID_KP \?")
    def get_pid_kp(self):
        return format(self.pid_kp, ".2F")

    @message(r"SET:PID_KI (.+)")
    def set_pid_ki(self, value):
        try:
            self.pid_ki = float(value)
        except Exception:
            return format_error(32)
        return self.SUCCESS

    @message(r"GET:PID_KI \?")
    def get_pid_ki(self):
        return format(self.pid_ki, ".2F")

    @message(r"SET:PID_KD (.+)")
    def set_pid_kd(self, value):
        try:
            self.pid_kd = float(value)
        except Exception:
            return format_error(33)
        return self.SUCCESS

    @message(r"GET:PID_KD \?")
    def get_pid_kd(self):
        return format(self.pid_kd, ".2F")

    @message(r"SET:PID_KP2 (.+)")
    def set_pid_kp2(self, value):
        try:
            self.pid_kp2 = float(value)
        except Exception:
            return format_error(34)
        return self.SUCCESS

    @message(r"GET:PID_KP2 \?")
    def get_pid_kp2(self):
        return format(self.pid_kp2, ".2F")

    @message(r"SET:PID_KI2 (.+)")
    def set_pid_ki2(self, value):
        try:
            self.pid_ki2 = float(value)
        except Exception:
            return format_error(35)
        return self.SUCCESS

    @message(r"GET:PID_KI2 \?")
    def get_pid_ki2(self):
        return format(self.pid_ki2, ".2F")

    @message(r"SET:PID_KD2 (.+)")
    def set_pid_kd2(self, value):
        try:
            self.pid_kd2 = float(value)
        except Exception:
            return format_error(36)
        return self.SUCCESS

    @message(r"GET:PID_KD2 (.+)")
    def get_pid_kd2(self):
        return format(self.pid_kd2, ".2F")

    @message(r"SET:PID_MIN (\d+)")
    def set_pid_min(self, value):
        self.pid_min = int(value)
        return self.SUCCESS

    @message(r"GET:PID_MIN \?")
    def get_pid_min(self):
        return format(self.pid_min, "d")

    @message(r"SET:PID_MAX (\d+)")
    def set_pid_max(self, value):
        self.pid_max = int(value)
        return self.SUCCESS

    @message(r"GET:PID_MAX \?")
    def get_pid_max(self):
        return format(self.pid_max, "d")

    @message(r"SET:PID_SAMPLE_TIME (\d+)")
    def set_pid_sample_time(self, value):
        self.pid_sample_time = int(value)
        return self.SUCCESS

    @message(r"GET:PID_SAMPLE_TIME \?")
    def get_pid_sample_time(self):
        return format(self.pid_sample_time, "d")

    @message(r"SET:PID_PROP_MODE (M|E)")
    def set_pid_drop_mode(self, mode):
        self.pid_drop_mode = mode
        return self.SUCCESS

    @message(r"GET:PID_PROP_MODE \?")
    def get_pid_drop_mode(self):
        return "1"  # self.pid_drop_mode  # TODO

    @message(r"SET:PID_THRESHOLD (\d+)")
    def set_pid_threshold(self, value):
        self.pid_threshold = int(value)
        return self.SUCCESS

    @message(r"GET:PID_THRESHOLD \?")
    def get_pid_threshold(self):
        return format(self.pid_threshold, "d")

    @message(r"SET:PARAMETER_SET (1|2)")
    def set_parameter_set(self, value):
        self.parameter_set = int(value)
        return self.SUCCESS

    @message(r"GET:PARAMETER_SET \?")
    def get_parameter_set(self):
        return format(self.parameter_set, "d")

    @message(r"SET:PARA_THRESHOLD (.+)")
    def set_parameter_threshold(self, value):
        try:
            self.parameter_threshold = float(value)
        except Exception:
            return format_error(38)
        return self.SUCCESS

    @message(r"SET:DAC (\d+)")
    def set_dac(self, value):
        self.dac = int(value)
        return self.SUCCESS

    @message(r"SET:MICROSCOPE_CTRL (ON|OFF)")
    def set_microscope_control(self, value):
        self.microscope_control = value == "ON"
        return self.SUCCESS

    @message(r"GET:MICROSCOPE_CTRL \?")
    def get_microscope_control(self):
        return format(int(self.microscope_control))

    @message(r"SET:MICROSCOPE_LIGHT (ON|OFF)")
    def set_microscope_light(self, value):
        self.microscope_light = value == "ON"
        return self.SUCCESS

    @message(r"GET:MICROSCOPE_LIGHT \?")
    def get_microscope_light(self):
        return format(int(self.microscope_light))

    @message(r"SET:MICROSCOPE_CAM (ON|OFF)")
    def set_microscope_camera(self, value):
        self.microscope_camera = value == "ON"
        return self.SUCCESS

    @message(r"GET:MICROSCOPE_CAM \?")
    def get_microscope_camera(self):
        return format(int(self.microscope_camera))

    @message(r"SET:PROBCARD_LIGHT (ON|OFF)")
    def set_probecard_light(self, value):
        self.probecard_light = value == "ON"
        return self.SUCCESS

    @message(r"GET:PROBCARD_LIGHT \?")
    def get_probecard_light(self):
        return format(int(self.probecard_light))

    @message(r"SET:PROBCARD_CAM (ON|OFF)")
    def set_probecard_camera(self, value):
        self.probecard_camera = value == "ON"
        return self.SUCCESS

    @message(r"GET:PROBCARD_CAM \?")
    def get_probecard_camera(self):
        return format(int(self.probecard_camera))

    @message(r"SET:LASER_SENSOR (ON|OFF)")
    def set_laser_sensor(self, value):
        self.laser_sensor = value == "ON"
        return self.SUCCESS

    @message(r"SET:BOX_LIGHT (ON|OFF)")
    def set_box_light(self, value):
        self.box_light = value == "ON"
        return self.SUCCESS

    @message(r"GET:LIGHT \?")
    def get_box_light(self):
        return format(self.box_light, "d")

    # @message(r'SET:ENV_II_PCB (YES|NO)')
    # def set_env_ii_pcb(self, value):
    #     self.env_ii_pcb = value == 'YES'
    #     return self.SUCCESS

    # @message(r'SET:FACTORY_DEFAULT (YES|NO)')
    # def set_factory_default(self, value):
    #     self.factory_default = value == 'YES'
    #     return self.SUCCESS

    # @message(r'SET:CLEAR_LOG (YES|NO)')
    # def set_clear_log(self, value):
    #     self.clear_log = value == 'YES'
    #     return self.SUCCESS

    # @message(r'SET:CLOCK \d\d:\d\d:\d\d_\d\d\.\d\d\.\d\d\d\d')
    # def set_clock(self):
    #     return self.SUCCESS

    @message(r'GET:CHIP_ADDR (1|2)')
    def get_chip_addr(self):
        return format(self.sensor_address, "d")

    # @message(r'GET:DATA \d')
    # def get_data(self):
    #     return self.SUCCESS

    # @message(r'GET:DATA_BOX \?')
    # def get_data_box(self):
    #     return 'TODO'

    @message(r'GET:CHIP_NBR \?')
    def get_chip_nbr(self):
        return format(self.sensor_count, "d")

    @message(r"GET:TEMP \?")
    def get_temp(self):
        return format(self.box_temperature, ".1F")

    @message(r"GET:HUM \?")
    def get_hum(self):
        return format(self.box_humidity, ".1F")

    @message(r"GET:LUX \?")
    def get_lux(self):
        return format(self.box_lux, ".1F")

    @message(r"GET:VALVE_ON \?")
    def get_valve_on(self):
        return "0"

    @message(r"GET:DOOR \?")
    def get_door(self):
        return format(int(self.door_open))

    @message(r"GET:LASER \?")
    def get_laser(self):
        return format(int(self.laser_enabled))

    @message(r"GET:PC_DATA \?")
    def get_pc_data(self):
        return ",".join(map(format, self.create_pc_data()))

    @message(r"GET:RELAY_STATUS \?")
    def get_relay_status(self):
        return format(self.power_relay_states())

    @message(r"GET:ENV \?")
    def get_env(self):
        values = [
            format(self.box_temperature, ".1F"),
            format(self.box_humidity, ".1F"),
            format(self.box_light, "d"),
            format(self.pt100_1, ".1F"),
        ]
        return ",".join(values)

    @message(r"GET:VERSION \?")
    def get_version(self):
        return "V2.0"

    @message(r".*")
    def unknown_message(self):
        return format_error(999)


if __name__ == "__main__":
    run(EnvironBoxEmulator())
