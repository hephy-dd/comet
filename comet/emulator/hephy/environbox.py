from comet.emulator import Emulator
from comet.emulator import message, run


class EnvironBoxEmulator(Emulator):

    IDENTITY = 'EnvironBox, v1.0 (Emulator)'
    SUCCESS = 'OK'
    PC_DATA_SIZE = 39
    SENSOR_ADRESSES = [40, 41, 42, 43, 44, 45]

    def __init__(self):
        super().__init__()
        self.sensor_address = 40
        self.discharge = 'OFF'

        self.laser_sensor = False
        self.box_light = False
        self.microscope_control = False
        self.microscope_light = False
        self.microscope_camera = False
        self.probecard_light = False
        self.probecard_camera = False
        self.discharge_time = 1000

        self.box_temperature = 24.0
        self.box_humidity = 40.0
        self.box_lux = 0.001
        self.door_open = False
        self.laser_enabled = False

        self.test_led = False
        self.pt100_1_enabled = True
        self.pt100_1 = 22.5
        self.pt100_2_enabled = True
        self.pt100_2 = float('nan')
        self.pid_control = False
        self.pid_control_mode = 'HUM'
        self.setpoints = {'HUM': 30, 'DEW': 30}
        self.pid_kp = 0.25
        self.pid_ki = 0.01
        self.pid_kd = 1.23
        self.pid_kp2 = 22.4
        self.pid_ki2 = 1.25
        self.pid_kd2 = 3.56
        self.pid_min = 10
        self.pid_max = 560
        self.pid_sample_time = 100
        self.pid_drop_mode = 'M'
        self.pid_threshold = 0
        self.parameter_set = 1
        self.parameter_threshold = 25.5
        self.dac = 25

        # self.env_ii_pcb = False
        # self.factory_default = False
        # self.clear_log = False

    def power_relay_states(self):
        power_relay_states = 0
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
        pc_data = [0] * self.PC_DATA_SIZE
        pc_data[1] = self.box_humidity
        pc_data[2] = self.box_temperature
        pc_data[4] = int(self.pid_control)
        pc_data[23] = self.power_relay_states()
        pc_data[24] = int(self.box_light)
        pc_data[25] = int(self.door_open)
        pc_data[32] = self.box_lux
        pc_data[33] = self.pt100_1
        pc_data[34] = self.pt100_2
        return pc_data

    @message(r'\*IDN\?')
    def get_idn(self):
        return self.IDENTITY

    # @message(r'\*RST')
    # def set_idn(self):
    #     return self.SUCCESS

    @message(r'SET:NEW_ADDR (\d+)')
    def set_new_addr(self, address):
        value = int(address)
        if value not in self.SENSOR_ADRESSES:
            return 'Err14'
        self.sensor_address = value
        return self.SUCCESS

    @message(r'SET:TEST_LED (ON|OFF)')
    def set_test_led(self, value):
        self.test_led = value == 'ON'
        return self.SUCCESS

    @message(r'GET:TEST_LED \?')
    def get_test_led(self):
        return {True: '1', False: '0'}[self.test_led]

    @message(r'SET:DISCHARGE (AUTO|ON|OFF)')
    def set_discharge(self, state):
        self.discharge = state
        return self.SUCCESS

    @message(r'SET:DISCHARGE_TIME (\d+)')
    def set_discharge_time(self, seconds):
        seconds = int(seconds)
        if 0 <= seconds <= 9999:
             self.discharge_time = seconds
             return self.SUCCESS
        return 'Err44'

    @message(r'GET:DISCHARGE_TIME \?')
    def get_discharge_time(self):
        return format(self.discharge_time)

    @message(r'SET:PT100_1 (ON|OFF)')
    def set_pt100_1(self, value):
        self.pt100_1_enabled = value == 'ON'
        return self.SUCCESS

    @message(r'GET:PT100_1 \?')
    def get_pt100_1(self):
        return format(self.pt100_1, '.1f')

    @message(r'SET:PT100_2 (ON|OFF)')
    def set_pt100_2(self, value):
        self.pt100_2_enabled = value == 'ON'
        return self.SUCCESS

    @message(r'GET:PT100_2 \?')
    def get_pt100_2(self):
        return format(self.pt100_2, '.1f')

    @message(r'SET:CTRL (ON|OFF)')
    def set_ctrl(self, value):
        self.pid_control = value == 'ON'
        return self.SUCCESS

    @message(r'GET:CTRL \?')
    def get_ctrl(self):
        return '1' if self.pid_control else '0'

    @message(r'SET:CTRL_MODE (HUM|DEW)')
    def set_ctrl_mode(self, mode):
        self.pid_control_mode = mode
        return self.SUCCESS

    @message(r'SET:SETPOINT (\d+)')
    def set_setpoint(self, setpoint):
        setpoint = float(setpoint)
        if self.pid_control_mode == 'HUM':
            self.setpoints['HUM'] = setpoint
        elif self.pid_control_mode == 'DEW':
            self.setpoints['DEW'] = setpoint
        return self.SUCCESS

    @message(r'GET:SETPOINT \?')
    def get_setpoint(self):
        if self.pid_control_mode == 'HUM':
            return format(self.setpoints['HUM'], '.2f')
        elif self.pid_control_mode == 'DEW':
            return format(self.setpoints['HUM'], '.2f')
        return '0'

    @message(r'SET:PID_KP (.+)')
    def set_pid_kp(self, value):
        try:
            value = float(value)
        except Exception:
            return 'Err31'
        self.pid_kp = value
        return self.SUCCESS

    @message(r'GET:PID_KP \?')
    def get_pid_kp(self):
        return format(self.pid_kp, '.2f')

    @message(r'SET:PID_KI (.+)')
    def set_pid_ki(self, value):
        try:
            value = float(value)
        except Exception:
            return 'Err32'
        self.pid_ki = value
        return self.SUCCESS

    @message(r'GET:PID_KI \?')
    def get_pid_ki(self):
        return format(self.pid_ki, '.2f')

    @message(r'SET:PID_KD (.+)')
    def set_pid_kd(self, value):
        try:
            value = float(value)
        except Exception:
            return 'Err33'
        self.pid_kd = value
        return self.SUCCESS

    @message(r'GET:PID_KD \?')
    def get_pid_kd(self):
        return format(self.pid_kd, '.2f')

    @message(r'SET:PID_KP2 (.+)')
    def set_pid_kp2(self, value):
        try:
            value = float(value)
        except Exception:
            return 'Err34'
        self.pid_kp2 = value
        return self.SUCCESS

    @message(r'GET:PID_KP2 \?')
    def get_pid_kp2(self):
        return format(self.pid_kp2, '.2f')

    @message(r'SET:PID_KI2 (.+)')
    def set_pid_ki2(self, value):
        try:
            value = float(value)
        except Exception:
            return 'Err35'
        self.pid_ki2 = value
        return self.SUCCESS

    @message(r'GET:PID_KI2 \?')
    def get_pid_ki2(self):
        return format(self.pid_ki2, '.2f')

    @message(r'SET:PID_KD2 (.+)')
    def set_pid_kd2(self, value):
        try:
            value = float(value)
        except Exception:
            return 'Err36'
        self.pid_kd2 = value
        return self.SUCCESS

    @message(r'GET:PID_KD2 (.+)')
    def get_pid_kd2(self):
        return format(self.pid_kd2, '.2f')

    @message(r'SET:PID_MIN (\d+)')
    def set_pid_min(self, value):
        self.pid_min = int(value)
        return self.SUCCESS

    @message(r'GET:PID_MIN \?')
    def get_pid_min(self):
        return format(self.pid_min, 'd')

    @message(r'SET:PID_MAX (\d+)')
    def set_pid_max(self, value):
        self.pid_max = int(value)
        return self.SUCCESS

    @message(r'GET:PID_MAX \?')
    def get_pid_max(self):
        return format(self.pid_max, 'd')

    @message(r'SET:PID_SAMPLE_TIME (\d+)')
    def set_pid_sample_time(self, value):
        self.pid_sample_time = int(value)
        return self.SUCCESS

    @message(r'GET:PID_SAMPLE_TIME \?')
    def get_pid_sample_time(self):
        return format(self.pid_sample_time, 'd')

    @message(r'SET:PID_PROP_MODE (M|E)')
    def set_pid_drop_mode(self, mode):
        self.pid_drop_mode = mode
        return self.SUCCESS

    @message(r'GET:PID_PROP_MODE \?')
    def get_pid_drop_mode(self):
        return self.pid_drop_mode

    @message(r'SET:PID_THRESHOLD (\d+)')
    def set_pid_threshold(self, value):
        self.pid_threshold = int(value)
        return self.SUCCESS

    @message(r'GET:PID_THRESHOLD \?')
    def get_pid_threshold(self):
        return format(self.pid_threshold, 'd')

    @message(r'SET:PARAMETER_SET (1|2)')
    def set_parameter_set(self, value):
        self.parameter_set = int(value)
        return self.SUCCESS

    @message(r'GET:PARAMETER_SET \?')
    def get_parameter_set(self):
        return format(self.parameter_set, 'd')

    @message(r'SET:PARA_THRESHOLD (.+)')
    def set_parameter_threshold(self, value):
        try:
            value = float(value)
        except Exception:
            return 'Err38'
        self.parameter_threshold = int(value)
        return self.SUCCESS

    @message(r'SET:DAC (\d+)')
    def set_dac(self, value):
        self.dac = int(value)
        return self.SUCCESS

    @message(r'SET:MICROSCOPE_CTRL (ON|OFF)')
    def set_microscope_control(self, value):
        self.microscope_control = value == 'ON'
        return self.SUCCESS

    @message(r'GET:MICROSCOPE_CTRL \?')
    def get_microscope_control(self):
        return format(int(self.microscope_control))

    @message(r'SET:MICROSCOPE_LIGHT (ON|OFF)')
    def set_microscope_light(self, value):
        self.microscope_light = value == 'ON'
        return self.SUCCESS

    @message(r'GET:MICROSCOPE_LIGHT \?')
    def get_microscope_light(self):
        return format(int(self.microscope_light))

    @message(r'SET:MICROSCOPE_CAM (ON|OFF)')
    def set_microscope_camera(self, value):
        self.microscope_camera = value == 'ON'
        return self.SUCCESS

    @message(r'GET:MICROSCOPE_CAM \?')
    def get_microscope_camera(self):
        return format(int(self.microscope_camera))

    @message(r'SET:PROBCARD_LIGHT (ON|OFF)')
    def set_probecard_light(self, value):
        self.probecard_light = value == 'ON'
        return self.SUCCESS

    @message(r'GET:PROBCARD_LIGHT \?')
    def get_probecard_light(self):
        return format(int(self.probecard_light))

    @message(r'SET:PROBCARD_CAM (ON|OFF)')
    def set_probecard_camera(self, value):
        self.probecard_camera = value == 'ON'
        return self.SUCCESS

    @message(r'GET:PROBCARD_CAM \?')
    def get_probecard_camera(self):
        return format(int(self.probecard_camera))

    @message(r'SET:LASER_SENSOR (ON|OFF)')
    def set_laser_sensor(self, value):
        self.laser_sensor = value == 'ON'
        return self.SUCCESS

    @message(r'SET:BOX_LIGHT (ON|OFF)')
    def set_box_light(self, value):
        self.box_light = value == 'ON'
        return self.SUCCESS

    @message(r'GET:LIGHT \?')
    def get_box_light(self):
        return format(self.box_light, 'd')

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

    # @message(r'GET:CHIP_ADDR \d')
    # def get_chip_addr(self):
    #     return self.SUCCESS

    # @message(r'GET:DATA \d')
    # def get_data(self):
    #     return self.SUCCESS

    # @message(r'GET:DATA_BOX \?')
    # def get_data_box(self):
    #     return 'TODO'

    # @message(r'GET:CHIP_NBR \?')
    # def get_chip_nbr(self):
    #     return 'TODO'

    @message(r'GET:TEMP \?')
    def get_temp(self):
        return format(self.box_temperature, '.1f')

    @message(r'GET:HUM \?')
    def get_hum(self):
        return format(self.box_humidity, '.1f')

    @message(r'GET:LUX \?')
    def get_lux(self):
        return format(self.box_lux, '.0f')

    @message(r'GET:VALVE_ON \?')
    def get_valve_on(self):
        return '0'

    @message(r'GET:DOOR \?')
    def get_door(self):
        return format(int(self.door_open))

    @message(r'GET:LASER \?')
    def get_laser(self):
        return format(int(self.laser_enabled))

    @message(r'GET:PC_DATA \?')
    def get_pc_data(self):
        return ','.join(map(format, self.create_pc_data()))

    @message(r'GET:RELAY_STATUS \?')
    def get_relay_status(self):
        return format(self.power_relay_states())

    @message(r'GET:ENV \?')
    def get_env(self):
        values = [
            format(self.box_temperature, '.1f'),
            format(self.box_humidity, '.1f'),
            format(self.box_light, 'd'),
            format(self.pt100_1, '.1f')
        ]
        return ','.join(values)

    @message(r'GET:VERSION \?')
    def get_version(self):
        return 'V2.0'

    @message(r'.*')
    def unknown_message(self):
        return 'Err999'


if __name__ == "__main__":
    run(EnvironBoxEmulator())

